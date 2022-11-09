var audio;
var source_playing;

function playAudio(source){
    if(audio == null){
        source_playing = source;
        audio = new Audio(source);
        audio.play();
    }  else if(source_playing != source){
        audio.pause();
        source_playing = source;
        audio = new Audio(source);
        audio.play();
    } else if(!audio.paused){
        audio.pause();
    } else if(audio.paused){
        audio.play();
    }
}

function friendButton(){
    var friend_div = $("#friends_list");
    var party_div = $("#party_list");

    if(party_div.css("display") == "block"){
        party_div.css("display", "none")
    }

    if(friend_div.css("display") == "none"){
        friend_div.css("display", "block");
    } else {
        friend_div.css("display", "none");
    }
}

function partyButton(){
    var party_div = $("#party_list");
    var friend_div = $("#friends_list");

    if(friend_div.css("display") == "block"){
        friend_div.css("display", "none")
    }
    
    if(party_div.css("display") == "none"){
        party_div.css("display", "block");
    } else {
        party_div.css("display", "none");
    }
}

function createParty(){
    var input = $("#party_name");
    if(input.val() != ""){
        var res = input.val().replace(" ", "-");
        window.location.pathname = 'p/' + res;
    }
}

document.getElementById("party_list").addEventListener("keypress", function(e) {
    if(e.key == "Enter"){
        createParty();
    }
});