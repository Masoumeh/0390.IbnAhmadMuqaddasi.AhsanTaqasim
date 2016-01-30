var system = require('system');
var page = require('webpage').create();

page.open(system.args[1], function()
{
    setTimeout(function(){
      console.log(page.content);
      phantom.exit();},3000); 
});
