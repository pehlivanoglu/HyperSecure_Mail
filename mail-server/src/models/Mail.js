const mongoose = require('mongoose');

const  mailSchema = new mongoose.Schema({
  sender: {
    type: String,
  },
  receiver: {
    type: String,
  },
  subject: {
    type: String,
    default: ""
  },
  body: {
    type: String,
    default: ""
  },
  sending_time: {
    type: Date,
    default: Date.now 
  }
});

mongoose.model('Mail', mailSchema);