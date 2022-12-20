var audio;
var source_playing;
var invalid_url_symbols = ["%", "'", "\"", "?", "|", "\\", "-", "!", "#", "$", "^", "&", "*", "(", ")", "<", ">", ".", ";", ":", "=", "{", "[", "]", "}", "`", "~"];
const party_form = document.getElementById("party_form");

if(party_form){
    party_form.addEventListener("submit", function(event){
        clearPartyErrors();

        party_name = $("#party_name").val();
        
        if(!checkURL(party_name)){
            event.preventDefault();
        }
    });
}

function go_home(){
    window.location = "../";
}

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
    
    clearPartyErrors();
    clearPartyInput();
    clearFriendErrors();
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

    clearPartyErrors();
    clearPartyInput();
    clearFriendErrors();
}

function createParty(){
    var input = $("#party_name");
    if(input.val() != "" && checkURL(input.val())){
        var res = input.val().replace(" ", "-");
        window.location.pathname = 'p/' + res;
    }
}

function checkURL(url){
    var valid = true;
    var party_sym_error = $("#party_sym_error");
    var party_len_error = $("#party_len_error")
    party_sym_error.html("Not a valid party name. Cannot include these symbols: ");
    party_len_error.html("Party name must not be over 50 characters.");
    

    for(let i=0;i<invalid_url_symbols.length;i++){
        if(url.includes(invalid_url_symbols[i])){
            valid = false;
            party_sym_error.html(party_sym_error.html() + invalid_url_symbols[i]);
            party_sym_error.css("display", "block"); 
        }
    }

    if(url.length > 50){
        valid = false;
        party_len_error.css("display", "block");
    }
    
    return valid;
}

function clearPartyErrors(){
    var party_sym_error_message = $("#party_sym_error");
    var party_len_error = $("#party_len_error");

    if(party_sym_error_message.css("display") == "block"){
        party_sym_error_message.css("display", "none")
    }

    if(party_len_error.css("display") == "block"){
        party_len_error.css("display", "none");
    }
}

function clearFriendErrors(){
    var user_does_not_exist = $("#user_does_not_exist");
    var already_friends = $("#already_friends");
    var already_sent = $("#already_sent");

    user_does_not_exist.css("display", "none");
    already_friends.css("display", "none");
    already_sent.css("display", "none");
}

function clearPartyInput(){
    var input = $("#party_name");
    if(input.val() != ""){
        input.val("");
    }
}

/*document.getElementById("party_list").addEventListener("keypress", function(e) {
    if(e.key == "Enter"){
        createParty();
    }
});*/