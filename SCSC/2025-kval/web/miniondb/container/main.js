const express = require("express");
const crypto = require("crypto");
const assert = require("node:assert");
const path = require("path");
const expressLayouts = require("express-ejs-layouts");
const { Sequelize, DataTypes, Op } = require("sequelize");

const SECRET_MINION_PASSWORD = crypto.randomBytes(16).toString("hex");
const FLAG = process.env.FLAG || "SNHT{fake_flag}";
assert(FLAG.slice(4).toLowerCase() === FLAG.slice(4));

const app = express();
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.set("layout", "layout");
app.use(expressLayouts);
app.use(express.static(path.join(__dirname, "public")));

const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: "db.db",
  logging: false,
  operatorsAliases: Object.fromEntries(
    Object.entries(Op).map(([k, v]) => [` ${k} `, v])
  ),
});

const Minion = sequelize.define("Minion", {
  name: {
    type: DataTypes.STRING,
    primaryKey: true,
  },
  description: {
    type: DataTypes.STRING,
  },
  age: {
    type: DataTypes.INTEGER,
  },
  secret: {
    type: DataTypes.STRING,
  },
  not_feeling_well: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  },
});

async function initDB() {
  await sequelize.sync({ force: true });
  const minions = [
    {
      name: "Bob",
      description: "A tiny ball of chaos with a love for teddy bears.",
      age: 6,
      secret: "I once ate an entire banana cake... without sharing!",
    },
    {
      name: "Kevin",
      description:
        "The self-proclaimed leader who takes himself very seriously.",
      age: 10,
      secret:
        "I accidentally hacked into Gru's top-secret computer where i found " +
        FLAG,
    },
    {
      name: "Stuart",
      description: "A laid-back rockstar wannabe with a love for his ukulele.",
      age: 8,
      secret:
        "I once tried to play the ukulele with my feet... it did not end well.",
      not_feeling_well: true,
    },
    {
      name: "Dave",
      description:
        "A tech-savvy minion who once tried to invent a banana-powered rocket.",
      age: 9,
      secret:
        "I may or may not have turned Gru's lab into a giant slip-and-slide.",
    },
    {
      name: "Jerry",
      description:
        "A hyperactive prankster who never misses a chance to cause mayhem.",
      age: 7,
      secret:
        "I replaced all the coffee in the lab with banana smoothies. No one noticed.",
      not_feeling_well: true,
    },
  ];

  for (const minion of minions) {
    await Minion.create(minion);
  }
}
initDB();

app.get("/", async (req, res) => {
  try {
    const minions = await Minion.findAll({
      attributes: ["name", "description", "age"],
    });
    res.render("index", { minions });
  } catch {
    res.status(500).send("Error fetching minions");
  }
});

app.get("/minion/:name", async (req, res) => {
  try {
    const minion = await Minion.findOne({
      where: {
        name: req.params.name,
      },
      attributes: ["name", "description", "age"],
    });

    if (!minion) {
      return res.status(404).send("Minion not found");
    }

    res.render("minion", { minion });
  } catch {
    res.status(500).send("Error fetching minion");
  }
});

app.get("/api/minion/health", async (req, res) => {
  let minion = {};
  try {
    minion = (await Minion.findOne(req.query)) || {};
  } catch {
    console.error("Error fetching minion");
  }

  if (minion.not_feeling_well) {
    return res.json({
      message: "Minion is not feeling well :(",
    });
  }

  res.json({
    message: "Minion is in good health!",
  });
});

app.get("/api/minion/secret", async (req, res) => {
  if (req.query.password !== SECRET_MINION_PASSWORD) {
    return res.json({
      message: "Incorrect minion password, access denied!",
    });
  }

  let minion = {};

  try {
    minion = await Minion.findOne({
      where: {
        name: req.query.name,
      },
      attributes: ["name", "secret"],
    });
  } catch {
    return res.status(500).send("Error fetching minion");
  }

  res.json({ message: `${minion.name}'s secret is: ${minion.secret}` });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
