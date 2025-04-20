

window.onload = function () {



let request_button = document.getElementById("request_button");
let response_div = document.getElementById("response_div");
let statusContainer = document.getElementById("server_status");

async function fetchServerStatus(){

    try {
        let res = await fetch ("http://localhost:8080/server_status"); //send get request using fetch and await for the response then store it in res variable
        let data = await res.json(); //from the res varibale extract the json and store it in data variable

        let statusContainer = document.getElementById("server_status");
        statusContainer.innerHTML = ""; //clear the previous status


         // Map server addresses to their names
         const serverNameMap = {
            "localhost:8001": "Server 1",
            "localhost:8002": "Server 2",
            "localhost:8003": "Server 3"
        };

        const statusEmojiMap = {
            "healthy": "✅",  
            "unhealthy": "❌"  
        };

        for (let server in data) { //Loops over each server key in the data object, the server will be "Server 1", "Server 2", etc.
            let status = data[server];
            let serverName = serverNameMap[server] || server; // Use the server name from the map, or fallback to the address if not found

            // Create a container for each server
            let serverDiv = document.createElement("div");
            serverDiv.style.display = "flex";
            serverDiv.style.alignItems = "center";
            serverDiv.style.marginBottom = "10px";

            // Create a span for the server name
            let serverNameSpan = document.createElement("span");
            serverNameSpan.innerText = serverName;
            serverNameSpan.style.marginRight = "10px";
            serverNameSpan.style.fontWeight = "bold";

            // Create a span for the status emoji
            let statusEmojiSpan = document.createElement("span");
            statusEmojiSpan.innerText = statusEmojiMap[status]; // Set the emoji based on the status

            // Append the server name and status image to the server div
            serverDiv.appendChild(serverNameSpan);
            serverDiv.append(statusEmojiSpan);

            // Append the server div to the status container
            statusContainer.appendChild(serverDiv);
        }
    }
    catch(err){
        console.log(err); //catch any error and log it to the console
    }

}

fetchServerStatus(); //call the fetchServerStatus function to get the server status

setInterval(fetchServerStatus, 5000); //call the fetchServerStatus function every 5 seconds to get the server status



request_button.addEventListener("click", async () => 
{   try {
    let res = await fetch("http://localhost:8080");        //send get request using fetch and await for the response then store it in res variable
    let data = await res.text();                           //from the res varibale extract the text and store it in data variable
    response_div.innerHTML =  data;
    }
    catch (err) {
        response_div.innerHTML = "Error: " + err + " causing issue"; //catch any error and display it in the response div
    }

});

}