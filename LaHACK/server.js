var path = require('path')
var express = require('express'),
    app = express(),
    port = 80,
    bodyParser = require('body-parser');
 
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var routes = require('./api/routes/routes');
routes(app);

console.log('RESTful API server started on: ' + port);

app.use('/web' ,express.static(path.join(__dirname, 'static')));

app.use(function(req, res) {
    res.status(404).send({url: req.originalUrl + ' not found'})
});

app.listen(port);