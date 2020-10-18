console.log("Core Exiles Tools (".concat(ip.toString()).concat(")"));

function getElementByXpath(path, node) {
  return document.evaluate(path, node, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function sendMessage(msg) {
    console.log(ip.concat(" : ").concat(msg));
    var socket = new WebSocket("ws://127.0.0.1:8765");
    socket.onopen = function(e) {
        socket.send(msg);
    }
    socket.onclose = function(e) {}
}

var buttons = [];

var buttonLogin = document.createElement("button");
buttonLogin.innerHTML = "Login";
buttonLogin.onclick = function() {sendMessage("--- login()")};
buttons.push(buttonLogin);

var buttonGetHaulMission = document.createElement("button");
buttonGetHaulMission.innerHTML = "Get Haul Mission";
buttonGetHaulMission.onclick = function() {sendMessage("--- get_haul_mission()")};
buttons.push(buttonGetHaulMission);

var buttonHaul = document.createElement("button");
buttonHaul.innerHTML = "Haul";
buttonHaul.onclick = function() {sendMessage("--- haul()")};
buttons.push(buttonHaul);

var buttonQuit = document.createElement("button");
buttonQuit.innerHTML = "Quit";
buttonQuit.onclick = function() {sendMessage("--- driver.quit(); __import__(\"os\")._exit(0)")};
buttons.push(buttonQuit)

var main_div = getElementByXpath("/html/body", document);
buttons = buttons.reverse();
for (var i in buttons) {
    buttons[i].style = "background-color:black;color:white;width:150px;height:40px;";
    main_div.insertBefore(buttons[i], main_div.childNodes[0]);
}

console.log("--------");
