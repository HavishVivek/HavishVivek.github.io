const sql = require("mysql");
const dotenv = require("dotenv").config();
const db = sql.createConnection({
  host:process.env.DATABASE_HOST,
  user:process.env.DATABASE_USER,
  password:process.env.DATABASE_PASSWORD,
  secretOrKey:process.env.JWT_KEY,
  port:4308,
  database:process.env.DATABASE
})

module.exports = db;