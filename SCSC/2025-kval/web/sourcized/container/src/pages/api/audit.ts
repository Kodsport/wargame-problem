import type { NextApiRequest, NextApiResponse } from 'next';
import puppeteer from 'puppeteer-core';
import PQueue from 'p-queue';

const { FLAG, BASE_URL, PUPPETEER_EXECUTABLE_PATH } = process.env;
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== 'POST')
        return res.status(405).json({ error: 'Method not allowed' });

    const { postId } = req.body;
    if (typeof postId !== 'string' || !/^[A-Za-z0-9-_=]+$/.test(postId))
        return res.status(400).json({ error: 'Invalid post ID' });

    try {
        await queue.add(() => auditPost(postId));
        res.status(200).json({ message: 'Visited links successfully' });
    } catch (error) {
        console.error('Puppeteer error:', error);
        res.status(500).json({ error: 'Failed to process the request' });
    }
}

const queue = new PQueue({ concurrency: 3 });
async function auditPost(postId: string) {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: PUPPETEER_EXECUTABLE_PATH,
        args: [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--js-flags=--noexpose_wasm,--jitless",
        ],
    });

    const page = await browser.newPage();
    await page.goto(`${BASE_URL}/post/${postId}`, { waitUntil: 'domcontentloaded' });

    // Set FLAG in localStorage
    await page.evaluate((flag) => {
        localStorage.setItem('FLAG', flag);
    }, FLAG!);

    // Note: This will only visit the first 5 links
    const links = await page.evaluate(() =>
        Array.from(document.querySelectorAll('a')).map(a => a.href).slice(0, 5)
    );

    await Promise.all(
        links.map(async (link) => {
            const newPage = await browser.newPage();
            await newPage.goto(link, { waitUntil: 'domcontentloaded' });
            await new Promise(res => setTimeout(res, 1500));
            await newPage.close();
        })
    );

    await browser.close();
}