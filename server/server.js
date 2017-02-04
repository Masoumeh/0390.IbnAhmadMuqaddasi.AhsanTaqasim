var http = require("http");
var fs = require('fs');
var port = 8008;
var serverUrl = "0.0.0.0";
var counter = 0;
var server = http.createServer(function (request, response) {
  console.log(request.url);
  fs.readFile('./' + request.url, function(err, data) {
    if (!err) {
      var dotoffset = request.url.lastIndexOf('.');
      var mimetype = dotoffset == -1
          ? 'text/plain'
          : {
        '.html' : 'text/html',
        '.ico' : 'image/x-icon',
        '.jpg' : 'image/jpeg',
        '.png' : 'image/png',
        '.gif' : 'image/gif',
        '.css' : 'text/css',
        '.js' : 'text/javascript',
	'.geojson' : 'application/json',
	'.json' : 'application/json',
	'.csv' : 'text/csv'
      }[ request.url.substr(dotoffset) ];
      response.setHeader('Content-type' , mimetype);
      response.end(data);
      console.log( request.url, mimetype );
    } else {
      console.log ('file not found: ' + request.url);
      response.writeHead(404, "Not Found");
      response.end();
    }
  });
});

var io = require('socket.io')(server);
io.on('connection', function(socket){
  socket.on('writeDataToFile', function(message){
    fs.writeFile(message.file, message.data, function(err) {
      if(err) {
        return console.log(err);
      }
      console.log("The file was saved!");
    });
  });
  socket.on('writeJsonToFile', function(message){
    fs.writeFile(message.file, JSON.stringify(message.data), function(err) {
      if(err) {
        return console.log(err);
      }
      console.log("The file was saved!");
    });
  });

  socket.on('appendDataToFile', function(message){
    fs.appendFile(message.file, message.data, function(err) {
      if(err) {
        return console.log(err);
      }
      console.log("Changes saved!");
    });
  });

  socket.on('readProcessedData', function(msg){
    fs.readFile('processed.txt', 'utf8', function (err, data) {
      socket.emit('readProcessedData',data);
    })
  });
});
server.listen(port, serverUrl);
console.log("Starting web server at " + serverUrl + ":" + port);
