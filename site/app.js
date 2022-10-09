var serv;
var bleDevice;

function onConnect() {
    //let service
    console.log("Requesting Access to Lumba Sign")

    let uartUuid =  "6E400001-B5A3-F393-E0A9-E50E24DCCA9E".toLowerCase();
    let txdUuid =  "6E400002-B5A3-F393-E0A9-E50E24DCCA9E".toLowerCase();
    let rxdUuid =  "6E400003-B5A3-F393-E0A9-E50E24DCCA9E".toLowerCase();
    //navigator.bluetooth.requestDevice({filters: [{services: [uartUuid]}]})
    navigator.bluetooth.requestDevice({
        filters: [{
            services: [0x02, 0x03, uartUuid, txdUuid, rxdUuid],
        }]})
        .then(device => {
            bleDevice = device;
            return device.gatt.connect();
        })
        .then(server => {
            let ps = server.getPrimaryServices();
            console.log(ps);
            return server.getPrimaryServices();
            //return server.getPrimaryService(uartUuid);
        })
        .then(service => {
            serv = service;
            console.log(service);
        })
}

function onUpdate() {
    console.log("Update Attempted");
    console.log("Service: " + serv);

    let com = document.getElementById("command").value;
    console.log("Command: " + com);
}

function onDisconnect() {
  if (!bleDevice) {
    return;
  }
  console.log('Disconnecting from Bluetooth Device...');
  if (bleDevice.gatt.connected) {
    bleDevice.gatt.disconnect();
  } else {
    console.log('> Bluetooth Device is already disconnected');
  }
}