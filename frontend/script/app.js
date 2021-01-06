let lanIP ;
let socket ;

const sendmessage=function(game){
	var data=`[
		{
			"game":"Speedrun",
			"info":{
				"description":"Deze game bestaat uit een vast parcour van een aantal oplichtende Tik’s. Hoe sneller je dit parcour  doet hoe hoger je score.",
				"gameid":1
				}
		},
		{
			"game":"Simon says",
			"info":{
				"description":"Je begint met 1 Tik die een kleur toont die je moet aantikken, per keer dat je het juist hebt komt er een extra Tik bij. Dit blijft zicht herhalen tot je een fout maakt. Scoreboard houdt bij hoeveel Tik's je hebt kunnen onthouden.",
				"gameid":2
				}
		},
		{
			"game":"Tik tak boem",
			"info":{
				"description":"Tik's veranderen van groen naar rood, en flikkeren/piepen. Hoe sneller ze flikkeren/piepen hoe sneller ze van groen naar rood veranderen.  Bij het tikken van de Tik wordt deze terug gereset. De score hangt af van hoelang je het kan volhouden voor er eentje 'ontploft'.",
				"gameid":3
				}
		},
		{
			"game":"Color hunt",
			"info":{
				"description":"Iedere Tik zal een verschillende kleur krijgen als je deze aantikt krijg je een score die bij die kleur past. De kleuren zullen na een bepaalde tijd veranderen dus wees snel. De bedoeling is om zoveel mogelijk punten te krijgen in een bepaalde tijd",
				"gameid":4
				}
		},
		{
			"game":"Color team",
			"info":{
				"description":"spel voor 1 tot 3 spelers. Elke speler heeft een kleur, bij de start van de ronde licht er van elk kleur 1 Tik op. Bij het tikken van deze Tik licht er een nieuwe op, op een andere locatie. De speler met het meeste  aantal aangeraakte Tik’s wint.",
				"gameid":5
				}
		},
		{
			"game":"Simon says versus",
			"info":{
				"description":"spel voor 2 + spelers. Speler 1 begint & mag 1 Tik aantikken, dan moet speler 2 deze Tik aanraken & de 2de kiezen. Speler 3 moet de eerste 2 aantikken en kiest de derde enz. De speler die een fout maakt valt af.",
				"gameid":6
				}
		}
	]`;
	//socket.emit("F2B_info", {gametype: game});
	//of controle en toevoegen van info hier
	var dataset=JSON.parse(data);
	console.log(dataset);
	var gametitle,gamedescription,gameid;
	switch (game) {
		case "speedrun":
			gametitle=dataset[0].game;
			gamedescription=dataset[0].info.description;
			gameid=dataset[0].info.gameid;
			break;
		case "simonsays":
			gametitle=dataset[1].game;
			gamedescription=dataset[1].info.description;
			gameid=dataset[1].info.gameid;
			break;
		case "tiktakboem":
			gametitle=dataset[2].game;
			gamedescription=dataset[2].info.description;
			gameid=dataset[2].info.gameid;
			break;
		case "colorhunt":
			gametitle=dataset[3].game;
			gamedescription=dataset[3].info.description;
			gameid=dataset[3].info.gameid;
			break;
		case "simonversus":
			gametitle=dataset[4].game;
			gamedescription=dataset[4].info.description;
			gameid=dataset[4].info.gameid;
			break;
		case "colorteam":
			gametitle=dataset[5].game;
			gamedescription=dataset[5].info.description;
			gameid=dataset[5].info.gameid;
			break;
		default:
			break;
	};
	document.querySelector(".js-title").innerHTML=gametitle;
	document.querySelector(".js-description").innerHTML=gamedescription;
	document.querySelector(".js-start").addEventListener("click",function(){
		socket.emit("F2B_start",{"gameid":gameid});
		//handleData(`http://${lanIP}/api/v1/start`, callbackShowToken, callbackShowErrorNoLogin, "POST", body);
		console.log("start game",gameid);
	});
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
  
	
  };
document.addEventListener('DOMContentLoaded', function() {
	// 1 We will query the API with longitude and latitude.
	
	console.info("dom loaded");
	document.querySelector(".js-back").addEventListener("click",function(){window.history.back();});
	if(document.querySelector(".js-game")){
		startgame();
		
		
	}
	if(document.querySelector(".js-game")){
		lanIP=`${window.location.hostname}:5000`;
		socket= io(`http://${lanIP}`);
		listenToSocket();
	}
	
	
});