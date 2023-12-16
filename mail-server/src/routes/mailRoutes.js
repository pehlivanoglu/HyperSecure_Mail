const express = require('express');
const mongoose = require('mongoose');
const requireAuth = require('../middlewares/requireAuth');

const Mail = mongoose.model('Mail');

const router = express.Router();

router.use(requireAuth);

router.get('/getMails', async (req, res) => {
  const email_address = req.user.email;

  try{
    const mails = await Mail.find({ sender: email_address });
    res.send(mails);
  }catch (err){
    res.status(422).send({ error: err.message });
  }
  
});

module.exports = router;