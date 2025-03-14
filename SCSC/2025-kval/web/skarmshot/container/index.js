const express = require("express");
const puppeteer = require("puppeteer");
const Queue = require("./queue");
const app = express();
const port = 3000;
const config = require("./config");
const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");

// Rate limits the number of concurrent screenshots, we dont want to explode the server
// Please test your solution locally before attacking the remote :)
const screenshotQueue = new Queue(3, 30);

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.get("/shot", async (req, res) => {
  try {
    if (!req.query.url) {
      res.status(400).send("URL parameter is required");
      return;
    }

    const screenshot = await screenshotQueue.add(async () => {
      let browser = null;
      try {
        browser = await puppeteer.launch({
          headless: "new",
          args: [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--js-flags=--noexpose_wasm,--jitless",
          ],
        });

        // Make sure the URL query parameter is a string
        if (typeof req.query.url !== "string") {
          throw new Error("URL parameter is malformed");
        }

        const url = new URL(req.query.url);

        // Prevent loading local files
        if (url.protocol === "file:") {
          throw new Error("Bad protocol");
        }

        const isAdmin = req.query.admin === config.admin_token;

        // Prevent loading external URLs for admin users
        if (isAdmin && url.hostname && url.hostname !== "127.0.0.1") {
          throw new Error("Only local URLs are allowed for admin users");
        }

        const page = await browser.newPage();

        // NO JAVASCRIPT FOR NON-ADMIN USERS!!!
        let block = false;
        page.setJavaScriptEnabled(isAdmin);
        page.on("response", async (response) => {
          const body = await response.buffer().catch(() => {});
          if (isAdmin || !body || block) {
            return;
          }
          block = true;
          const contentType = response.headers()["content-type"];
          if (contentType && contentType.includes("text/html")) {
            try {
              const window = new JSDOM("").window;
              const purify = createDOMPurify(window);
              const clean = purify.sanitize(await response.text());
              await page.setContent(clean);
            } catch (error) {
              console.error(error);
            }
          }
        });

        await page.goto(url, {
          timeout: 10000,
          waitUntil: ["load", "domcontentloaded", "networkidle0"],
        });

        const screenshot = await page.screenshot();
        return screenshot;
      } finally {
        if (browser) {
          await browser.close().catch(console.error);
        }
      }
    }, 30000);

    res.send(screenshot);
  } catch (err) {
    res.status(500).send(err.message || "An error occurred");
  }
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
