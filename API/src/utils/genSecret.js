// run "node genSecret" to generate a 256-bit secret
const crypto = require('crypto');
const secret = crypto.randomBytes(32).toString('hex');
console.log(secret);
