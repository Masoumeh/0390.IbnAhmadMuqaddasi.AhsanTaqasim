/**
 * Created by rostam on 04.02.17.
 */
var socket = io();
function writeDataToFile(d, f) {
    var str = { data: d, file:f};
    socket.emit('writeDataToFile', str);
}
function writeJsonToFile(d,f) {
    var str = { data: d, file:f};
    socket.emit('writeJsonToFile',str);
}
function appendDataToFile(d, f) {
    var str = { data: d, file:f};
    socket.emit('appendDataToFile', str);
}
function readProcessedData(func) {
    socket.emit('readProcessedData',"hi");
    socket.on('readProcessedData', function(msg){
        func(msg);
    });
}
function saveData(data, fileName) {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    var json = JSON.stringify(data),
        blob = new Blob([json], {type: "octet/stream"}),
        url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(url);

};
