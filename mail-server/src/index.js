require("./models/User");
require("./models/Public_Key");
require("./models/Mail");
const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const authRoutes = require("./routes/authRoutes");
const keyRoutes = require("./routes/keyRoutes");
const mailRoutes = require("./routes/mailRoutes");
const requireAuth = require("./middlewares/requireAuth");
const https = require("https");
const fs = require('fs');


const app = express();


app.use(bodyParser.json());
app.use(authRoutes);
app.use(keyRoutes);
app.use(mailRoutes);

const mongoUri = "mongodb+srv://chatAppAdmin:Fy7L5mhj%23JaH.cH@cluster0.4cv2qzz.mongodb.net/?retryWrites=true&w=majority";
if (!mongoUri) {
  throw new Error(
    `MongoURI was not supplied.  Make sure you watch the video on setting up Mongo DB!`
  );
}

mongoose.set("strictQuery", true);
// resolves future deprecation issue with Mongoose v7

mongoose.connect(mongoUri);
mongoose.connection.on("connected", () => {
  console.log("Connected to mongo instance");
});
mongoose.connection.on("error", (err) => {
  console.error("Error connecting to mongo", err);
});

app.get("/", requireAuth, (req, res) => {
  res.send(`Your email: ${req.user.email}`);
});

const SSLoptions = {
  key: fs.readFileSync("/home/pehlivanoglu/Desktop/mail_enc/mail-server/src/server.key"),
  cert: fs.readFileSync('/home/pehlivanoglu/Desktop/mail_enc/mail-server/src/server.cert')
};

https.createServer(SSLoptions, app).listen(443, () => {
  console.log('HTTPS server running on port 443');
});

// app.listen(3000, () => {
//   console.log("Listening on port 3000");
// });
