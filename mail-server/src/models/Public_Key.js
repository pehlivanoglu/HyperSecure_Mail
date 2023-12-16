const mongoose = require('mongoose');

const keySchema = new mongoose.Schema({
  email: {
    type: String,
  },
  value: {
    type: String,
    default: ''
  },
});

mongoose.model('Public_Key', keySchema);