console.log('Core Exiles Tools Client');

function getElementByXpath(path, node) {
  return document.evaluate(path, node, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function post(endpoint, content) {
    fetch('http://localhost:4321' + endpoint, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(content),
        // mode: 'no-cors'
    })
   .then(response => response.json())
   .then(response => console.log(JSON.stringify(response)))
}

function createButton(displayText, onclick) {
    var result = document.createElement('button');
    result.className = 'ce-tools';
    result.innerHTML = displayText;
    result.onclick = onclick;
    result.style = 'background-color:black;color:white;width:150px;height:40px;padding:1px;';
    return result
}

function createTextField(placeholder, id) {
    var result = document.createElement('input');
    result.type = 'text';
    result.id = id;
    result.placeholder = placeholder;
    result.style = 'background-color:black;color:white;width:150px;height:40px;padding:1px;';
    return result
}


var inputs = [
    createButton('Login', function() { post('/login') }),
    createButton('Travel', function() { post('/map/travel', {
        current: {
            system: document.getElementById('travel-current-system').value || undefined,
            planet: document.getElementById('travel-current-planet').value || undefined,
            port: document.getElementById('travel-current-port').value || undefined,
            building: document.getElementById('travel-current-building').value || undefined
        },
        destination: {
            system: document.getElementById('travel-destination-system').value || undefined,
            planet: document.getElementById('travel-destination-planet').value || undefined,
            port: document.getElementById('travel-destination-port').value || undefined,
            building: document.getElementById('travel-destination-building').value || undefined
        }
    }) }),
    createTextField('Current System', 'travel-current-system'),
    createTextField('Current Planet', 'travel-current-planet'),
    createTextField('Current Port', 'travel-current-port'),
    createTextField('Current Building', 'travel-current-building'),
    createTextField('Destination System', 'travel-destination-system'),
    createTextField('Destination Planet', 'travel-destination-planet'),
    createTextField('Destination Port', 'travel-destination-port'),
    createTextField('Destination Building', 'travel-destination-building'),
    // createButton('Travel Raw', function() { post('/map/travel', JSON.parse(document.getElementById('travel-info').value)) }),
    // createTextField('Travel Info', 'travel-info'),
]

var main_div = getElementByXpath('/html/body', document);
inputs = inputs.reverse();
for (var i in inputs) {
    main_div.insertBefore(inputs[i], main_div.childNodes[0]);
}
