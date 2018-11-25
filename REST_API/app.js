var express = require("express");
var bodyParser = require("body-parser");
var routes = require("./routes/routes.js");
var app = express();



app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

routes(app);


var server = app.listen(3000 ,function(){
    var host = server.address().address;
    var port = server.address().port;
    console.log("app listening on http://%s:%s", host, port);
});