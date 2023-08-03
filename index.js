const express = require("express");
const db = require("./routes/db-config");
const app = express();
const cookies = require("cookie-parser");
const PORT = process.env.PORT || 3000;
app.use("/js", express.static(__dirname + "/public/js"));
app.use("/css", express.static(__dirname + "/public/css"));
app.set("view engine", "ejs");
app.set("views", "./views");
app.use(cookies());
app.use(express.json());
db.connect((err) => {
  if(err) throw err;
  console.log("database connected")
});
app.use("/", require("./routes/pages"));
app.use("/api", require("./controllers/auth"));
app.listen(PORT);