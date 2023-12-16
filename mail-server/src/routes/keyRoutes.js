const express = require('express');
const mongoose = require('mongoose');
const requireAuth = require('../middlewares/requireAuth');

const Public_Key = mongoose.model('Public_Key');
const User = mongoose.model('User');

const router = express.Router();

router.use(requireAuth);

router.get('/key', async (req, res) => {
  const email = req.rawHeaders[13];

  if (!email) {
    return res
      .status(422)
      .send({ error: 'You must provide an email!' });
  }

  try{
    const public_key = await Public_Key.find({ email: email });
    res.send(public_key);
  }catch (err){
    res.status(422).send({ error: err.message });
  }
  
});

router.post('/key', async (req, res) => {
  const email = req.user.email;
  const public_key = req.rawHeaders[13];

  const ifUnique = await User.find({ email: email });
  
  if (!public_key) {
    return res
      .status(422)
      .send({ error: 'You must provide a public key!' });
  }

  if(ifUnique!=undefined){
    return res
      .status(422)
      .send({ error: 'User already has a public key!' });
  }

  try {
    const ret_public_key = new Public_Key({ email:email , value:public_key });
    await ret_public_key.save();
    res.send("Public key created");
  } catch (err) {
    res.status(422).send({ error: err.message });
  }
  
});

module.exports = router;