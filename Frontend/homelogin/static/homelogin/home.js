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

        $("#adminBtn").attr("class","btn btn-primary btn-md active");
        $("#userBtn").attr("class","btn btn-primary btn-md")
    }else {
        $(".adminCommands").hide();
        $(".userCommands").show();

        $("#adminBtn").attr("class","btn btn-primary btn-md");
        $("#userBtn").attr("class","btn btn-primary btn-md active");
    }
}