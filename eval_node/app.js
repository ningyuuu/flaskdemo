const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const fs = require('fs');
const request = require('request');
const port = 8081;

const testEndpoint = (endpoint, file, correctAns) => {
  var formData = {
    file: fs.createReadStream(__dirname + '/pics/' + file)
  };
  return new Promise((res, rej) => {
    request.post({url: endpoint, formData: formData}, cb = (err, _, body) => {
      if (err) {
        console.error('upload failed:', err);
        res({
          file,
          body,
          correctAns,
          result: 'ERROR'
        });
      }

      res({
        file,
        body,
        correctAns,
        result: body == correctAns
      });

    })
  });
}

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.post('/endpoint', (req, res) => {
  const queries = [
    testEndpoint(req.body.endpoint, '0.png', 0),
    testEndpoint(req.body.endpoint, '4.png', 4),
    testEndpoint(req.body.endpoint, '5.png', 5),
    testEndpoint(req.body.endpoint, '0_resize.png', 0),
    testEndpoint(req.body.endpoint, '4_rgb.png', 4),
    testEndpoint(req.body.endpoint, '0_jpeg.jpg', 0),
    testEndpoint(req.body.endpoint, '6_handwriting.png', 6),
    testEndpoint(req.body.endpoint, '4_handwriting.png', 4),
    testEndpoint(req.body.endpoint, '31337.png', 31337)
  ];
  Promise.all(queries)
    .then((vals) => {
      res.send(vals)
    })
    .catch((err) => {
      res.send('Error from nodejs: ' + err)
    })
});

app.listen(port, (err) => {
  if (err) {
    return console.log('Error:', err);
  }
});