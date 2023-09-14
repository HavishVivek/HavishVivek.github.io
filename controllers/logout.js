const logout = (req, res) => {
  res.clearCookie("userRegisted");
  res.redirect("/");
}
module.exports = logout;