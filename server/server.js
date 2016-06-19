var http = require("http");
var fs = require('fs');
var port = 3000;
var serverUrl = "127.0.0.1";
var counter = 0;

var server = http.createServer(function(req, res) {
  counter++;
  console.log("Request: " + req.url + " (" + counter + ")");
  if(req.url == "/") {
    fs.readFile("matchToCornu.html", function(err, text){
      res.setHeader("Content-Type", "text/html");
      res.end(text);
    });
    return;
  }
  //
  if(req.url == "/SttlReg_CoordsCSV_fuzzyWuzzy.csv") {
    fs.readFile('SttlReg_CoordsCSV_fuzzyWuzzy.csv', 'utf8', function (err, data) {
      res.setHeader("Content-Type", "text");
      res.write(data);
      res.end();
    })
  }
});

var io = require('socket.io')(server);
io.on('connection', function(socket){
  socket.on('writeDataToFile', function(message){
    fs.appendFile(message.file, message.data+"\n", function(err) {
      if(err) {
        return console.log(err);
      }
      console.log("The file was saved!");
    });
  });
});
server.listen(port, serverUrl);
console.log("Starting web server at " + serverUrl + ":" + port);
