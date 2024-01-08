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
    default: () => {
      const now = new Date();
      return new Date(now.getTime() + 3 * 60 * 60 * 1000); // Adding 3 hours
    }
  },
  sym_key: {
    type: String,
    default: "" 
  }
  
});

mongoose.model('Mail', mailSchema);
