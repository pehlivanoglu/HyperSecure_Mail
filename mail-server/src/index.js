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
const Mail = mongoose.model('Mail');

const { SMTPServer } = require('smtp-server');
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

app.listen(3000, () => {
  console.log("Listening on port 3000");
});


const server = new SMTPServer({
  secure: true,
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert'),
  onData(stream, session, callback) {
      simpleParser(stream, {}, (err, parsed) => {
          if (err) {
              console.error(err);
              return callback(err);
          }
          const emailData = new Mail({
              sender: parsed.from.text,
              receiver: parsed.to.text,
              subject: parsed.subject,
              body: parsed.text
          });

          emailData.save(err => {
              if (err) {
                  console.error('Error saving email:', err);
                  return callback(err);
              }
              console.log('Email saved successfully');
              callback();
          });
      });
  },
});

server.listen(465);