let lanIP ;
let socket ;
let title,description,start,back,game,tiks,score,currenttime=0,scoreboard;


const loadpageElements=function(){
	title=document.querySelector(".js-title");
	description=document.querySelector(".js-description");
	start=document.querySelector(".js-start");
	back=document.querySelector(".js-back");
	game=document.querySelector(".js-game");
	tiks=document.querySelectorAll(".js-tik");
	score=document.querySelector(".js-score");
	scoreboard=document.querySelector(".js-scoreboard");
	addlisteners();

}
const loadscoreboard = function(scorelist){
	let tempstring="",number=1,sortedlist;
	
	
	scorelist.sort(getsortorder("score"));
	sortedlist=scorelist.reverse()
	console.log(scorelist);
	
	sortedlist.forEach(scoreitem => {
		if(number==1){
			tempstring+=`<div class="c-scoreboard__item u-score__1">
		<div class="c-scoreboard__place">${number}</div>
		<div class="c-scoreboard__name">${scoreitem.name}</div>
		<div class="c-scoreboard__score">${scoreitem.score}</div>
	</div>`;
		}else{
			if (number==2) {
				tempstring+=`<div class="c-scoreboard__item u-score__2">
		<div class="c-scoreboard__place">${number}</div>
		<div class="c-scoreboard__name">${scoreitem.name}</div>
		<div class="c-scoreboard__score">${scoreitem.score}</div>
	</div>`;
			}else{
				if (number==3) {
					tempstring+=`<div class="c-scoreboard__item u-score__3">
		<div class="c-scoreboard__place">${number}</div>
		<div class="c-scoreboard__name">${scoreitem.name}</div>
		<div class="c-scoreboard__score">${scoreitem.score}</div>
	</div>`;
				}else tempstring+=`<div class="c-scoreboard__item">
				<div class="c-scoreboard__place">${number}</div>
				<div class="c-scoreboard__name">${scoreitem.name}</div>
				<div class="c-scoreboard__score">${scoreitem.score}</div>
			</div>`;
			}
		}
		
	number+=1;
	});
	
	scoreboard.innerHTML=tempstring;
}
const addlisteners= function(){
	
	if(back){
		back.addEventListener("click",function(){window.history.back();});
	}
	if(game){
		startgame();
		socket= io(`http://${lanIP}`);
		io= `${window.location.hostname}:5000`;
		listenToSocket();
	}
	if(tiks[0]){
		console.log(tiks)
	}
	if(score){
		starttimer();
	}
	if(scoreboard){
		testscoreboard();
	}
}
const sendmessage=function(game){
	var gametitle,gamedescription,gameid,current;
	current=data[game-1];
	gametitle=current.game;
	gamedescription=current.info.description;
	gameid=current.info.gameid;
	if(title){
		title.innerHTML=gametitle;
	}
	if(description){
		description.innerHTML=gamedescription;
	}
	if(start){
		start.addEventListener("click",function(){
			socket.emit("F2B_start",{"gameid":gameid});
			console.log("start game",gameid);
			console.log(window.location);
			console.log(window.location.host)
			window.location.href=`/frontend/game.html?game=${gameid}`;
			
		});
	}
}
const starttimer=function(){
	
	window.setInterval(UpdateTime,100);
}
const UpdateTime=function(){
	currenttime+=100;
	//console.log(currenttime);
	score.innerHTML=currenttime/1000;
	
}
const startgame=function(){
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const gametype=urlParams.get("game");
	console.log(gametype);
	sendmessage(gametype);
}
const getsortorder=function(prop){
	return function(a, b) {    
        if (a[prop] > b[prop]) {    
            return 1;    
        } else if (a[prop] < b[prop]) {    
            return -1;    
        }    
        return 0;    
    }
}
const testscoreboard=function(){
	let scorelist=[{"name":"marijn","score":200},{"name":"marijn","score":300},{"name":"marijn","score":100},{"name":"marijn","score":700},{"name":"marijn","score":600},{"name":"marijn","score":200}]
	loadscoreboard(scorelist)
}
const listenToSocket = function () {
	socket.on("connected", function () {
	  console.log("verbonden met socket webserver");
	});
	socket.on("B2F_end",function(){
		console.log("game is done")
		window.location.href=`/frontend/endgame.html?game=${gameid}`;
		//get score true message
		document.querySelector(".js-score-end").innerHTML="message.score";
	});
	socket.on("B2F_scoreboard",(scorelist)=>loadscoreboard(scorelist));

  };
document.addEventListener('DOMContentLoaded', function() {
	// 1 We will query the API with longitude and latitude.
	loadpageElements();
	console.info("dom loaded");
	
	
	
});