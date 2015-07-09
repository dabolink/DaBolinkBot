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