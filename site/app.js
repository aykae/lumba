var serv;
var bleDevice;

async function onConnect() {
    //let service
    console.log("Requesting Access to Lumba Sign")

    let uartUuid =  "6E400001-B5A3-F393-E0A9-E50E24DCCA9E".toLowerCase();
    let txdUuid =  "6E400002-B5A3-F393-E0A9-E50E24DCCA9E".toLowerCase();
    let rxdUuid =  "6E400003-B5A3-F393-E0A9-E50E24DCCA9E".toLowerCase();
    //navigator.bluetooth.requestDevice({filters: [{services: [uartUuid]}]})
    navigator.bluetooth.requestDevice({
        filters: [{namePrefix: "CIRCUIT"}],
        optionalServices: [0x02, 0x03, uartUuid, txdUuid, rxdUuid],
        })
        .then(device => {
            console.log("in device");
            bleDevice = device;
            return device.gatt.connect();
        })
        .then(server => {
            console.log("in server");
            let ps = server.getPrimaryService(uartUuid);
            console.log(ps);
            return server.getPrimaryServices();
            //return server.getPrimaryService(uartUuid);
        })
        .then(service => {
            console.log("in service");
            serv = service;
            console.log(service);
        })
}

async function onUpdate() {
    console.log("Update Attempted");
    console.log("Service: " + serv);

    let com = document.getElementById("command").value;
    console.log("Command: " + com);
}

async function onDisconnect() {
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

/* TESTING AREA */

function onConnectToBluetoothDevicesButtonClick() {
  console.log('Getting existing permitted Bluetooth devices...');
  navigator.bluetooth.getDevices()
  .then(devices => {
    console.log('> Got ' + devices.length + ' Bluetooth devices.');
    // These devices may not be powered on or in range, so scan for
    // advertisement packets from them before connecting.
    for (const device of devices) {
      connectToBluetoothDevice(device);
    }
  })
  .catch(error => {
    console.log('Argh! ' + error);
  });
}

function connectToBluetoothDevice(device) {
  const abortController = new AbortController();

  device.addEventListener('advertisementreceived', (event) => {
    console.log('> Received advertisement from "' + device.name + '"...');
    // Stop watching advertisements to conserve battery life.
    abortController.abort();

    console.log('Connecting to GATT Server from "' + device.name + '"...');
    let server = device.gatt.connect()
    .then(() => {
      console.log('> Bluetooth device "' +  device.name + ' connected.');
      console.log(server.getPrimaryServices())
    })
    .catch(error => {
      console.log('Argh! ' + error);
    });
  }, { once: true });

  console.log('Watching advertisements from "' + device.name + '"...');
  device.watchAdvertisements({ signal: abortController.signal })
  .catch(error => {
    console.log('Argh! ' + error);
  });
}

function onRequestBluetoothDeviceButtonClick() {
  console.log('Requesting any Bluetooth device...');
  navigator.bluetooth.requestDevice({
 // filters: [...] <- Prefer filters to save energy & show relevant devices.
    acceptAllDevices: true
  })
  .then(device => {
    console.log('> Requested ' + device.name);
  })
  .catch(error => {
    console.log('Argh! ' + error);
  });
}