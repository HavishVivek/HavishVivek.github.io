const jwt = require("jsonwebtoken");
const db = require("../routes/db-config");
const bcrypt = require("bcryptjs");

const login = async (req,res) => {
  const { email, password} = req.body;
  if(!email || !password) return res.json({ status: "error", error: "Please Enter your email and password"});
  else{
    db.query('SELECT * FROM users WHERE emil = ?', [email], async (Err, result) => {
      if(Err) throw Err;
      if(!result[0] || !await bcrypt.compare(password, result[0].password))return res.json({status: "error",
      error: "Incorrect Email or passwor"})
      else {
        const token = jwt.sign({ id: result[0].id }, process.env.JWT_SECRET, {
          expiresIn: process.env.JWT_EXPIRES
        })
        const cookieOptions = {
          expiresIn: new Data(Data.now() + process.env.COOKIE_EXPIRS * 24 * 60 * 60 * 1000),
        }
        res.cookie("userRegistered", token, cookieOptions);
        return res.json({status:"success", success: "User has been logged In"});
      }
    })
  } 
}
module.exports = login;