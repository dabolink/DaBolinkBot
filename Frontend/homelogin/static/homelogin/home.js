function toggleBot(event, username, backend_server_ip){
    if(event.target.className == "btn btn-lg btn-danger"){
    	var xmlhttp = new XMLHttpRequest();
    	xmlhttp.open("GET", backend_server_ip + "/dabolinkbot/api/v1.0/bot/start/"+username);
    	xmlhttp.send();
        event.target.className = "btn btn-lg btn-success";
        event.target.innerHTML = "Online";

    }else{
    	var xmlhttp = new XMLHttpRequest();
    	xmlhttp.open("GET", backend_server_ip + "/dabolinkbot/api/v1.0/bot/end/"+username);
    	xmlhttp.send();
        event.target.className = "btn btn-lg btn-danger";
        event.target.innerHTML = "Offline";
    }
}

function toggleCommand(admin){
    if(admin) {
        $(".adminCommands").show();
        $(".userCommands").hide();

    }else {
        $(".adminCommands").hide();
        $(".userCommands").show();
    }
}

function saveUserData(username, backend_server_ip){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", backend_server_ip + "/dabolinkbot/api/v1.0/channel/settings/"+username);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.setRequestHeader("Access-Control-Allow-Origin", "http://localhost:8000")
    xmlhttp.send(JSON.stringify({
        "channel": username,
        "freq_viewer_time": 0
    }));
    alert(xmlhttp.status)
}