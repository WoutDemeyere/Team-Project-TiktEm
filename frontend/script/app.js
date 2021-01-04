const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
const sendmessage=function(game){
	socket.emit("F2B_info", {gametype: game});
	//of controle en toevoegen van info hier
}
const startgame=function(){
	const queryString = window.location.search;
	//console.log(queryString);
	const urlParams = new URLSearchParams(queryString);
	const gametype=urlParams.get("game");
	console.log(gametype);
	//send message to start game
	sendmessage(gametype);
}
const listenToSocket = function () {
	socket.on("connected", function () {
	  console.log("verbonden met socket webserver");
	});
  
	//in stap 2
	socket.on("B2F_game_detail", function (json) {
	  //gets game data
	  // fils description 
	  document.querySelector(".js-title").innerHTML=json["title"];
	  document.querySelector(".js-description").innerHTML=json["info"];
	});
  };
document.addEventListener('DOMContentLoaded', function() {
	// 1 We will query the API with longitude and latitude.
	
	console.info("dom loaded");
	if(document.querySelector(".js-game")){
		startgame();
		document.querySelector(".js-start").addEventListener("click",function(){
			socket.emit("F2B_start");
			console.log("start game");
		});
	}
	
});