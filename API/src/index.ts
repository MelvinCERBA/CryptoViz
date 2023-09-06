import express from 'express';

const app = express();
const port = 8080;
const ip = "0.0.0.0";

app.get('/', (req, res) => {
  res.send('Hello, TypeScript with Express!');
});

app.listen(port, ip, () => {
  console.log(`API listening at http://${ip}:${port}`);
});
