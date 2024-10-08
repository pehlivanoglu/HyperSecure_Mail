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

// This is not a real URI, I just used it for testing purposes
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
  key: fs.readFileSync("path/to/your/server.key"),
  cert: fs.readFileSync('path/to/your/server.cert')
};

https.createServer(SSLoptions, app).listen(443, () => {
  console.log('HTTPS server running on port 443');
});
