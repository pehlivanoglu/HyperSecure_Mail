const express = require('express');
const mongoose = require('mongoose');
const requireAuth = require('../middlewares/requireAuth');

const Mail = mongoose.model('Mail');

const router = express.Router();

router.use(requireAuth);

router.post('/sendMail', async (req, res) => {
  const sender = req.user.email;
  const {receiver, subject, body, sym_key} = req.body;
  if (!sender || !body || !receiver) {
    return res
      .status(422)
      .send({ error: 'Sender, receiver or body must not be empty!' });
  }

  try {
    const new_mail = new Mail({ sender , receiver, subject, body, sym_key:sym_key});
    await new_mail.save();
    res.send("Mail has been succesfully sent!");
  } catch (err) {
    res.status(422).send({ error: err.message });
  }
  
});

router.get('/getMails', async (req, res) => {
  const email_address = req.user.email;

  try{
    const mails = await Mail.find({ receiver: email_address });
    res.send(mails);
  }catch (err){
    res.status(422).send({ error: err.message });
  }
  
});

router.get('/getSentMails', async (req, res) => {
  const email_address = req.user.email;

  try{
    const mails = await Mail.find({ sender: email_address });
    res.send(mails);
  }catch (err){
    res.status(422).send({ error: err.message });
  }
  
});

module.exports = router;