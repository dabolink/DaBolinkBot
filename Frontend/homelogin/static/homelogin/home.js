function toggleBot(event, username){
    if(event.target.className == "btn btn-lg btn-danger"){
    	var xmlhttp = new XMLHttpRequest();
        var backend_server_ip = document.getElementById("backend_server_ip").innerHTML
        alert(backend_server_ip)
    	xmlhttp.open("GET", backend_server_ip + "/dabolinkbot/api/v1.0/bot/start/"+username);
    	xmlhttp.send();
        event.target.className = "btn btn-lg btn-success";
        event.target.innerHTML = "Online";

    }else{
    	var xmlhttp = new XMLHttpRequest();
    	xmlhttp.open("GET", "http://localhost:5000/dabolinkbot/api/v1.0/bot/end/"+username);
    	xmlhttp.send();
        event.target.className = "btn btn-lg btn-danger";
        event.target.innerHTML = "Offline";
    }
}