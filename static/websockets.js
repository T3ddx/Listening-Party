//websocket js
var loc = window.location;
var wsStart = 'ws://';
if(loc.protocol == 'https:'){
    wsStart = 'wss://';
}
var endpoint = wsStart + loc.host + loc.pathname;
var socket = new WebSocket(endpoint);

socket.onmessage = function(e){
    console.log("message", e);
    socket.send("{{ party_name }}");
};
socket.onopen = function(e){
    console.log("open", e);
};
socket.onerror = function(e){
    console.log("error", e);
};
socket.onclose = function(e){
    socket.send("closing");
    console.log("disconnect", e);
};