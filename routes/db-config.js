const sql = require("mysql");
const dotenv = require("dotenv").config();
const db = sql.createConnection({
  host:process.env.DATABASE_HOST,
  user:process.env.DATABASE_USER,
  password:process.env.DATABASE_PASSWORD,
  port:4306,
  database:process.env.DATABASE
})

module.exports = db;