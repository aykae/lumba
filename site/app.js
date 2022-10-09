function onButtonClick() {
    console.log("button clicked");
}

function onButtonClick() {
    //let service

    navigator.bluetooth.requestDevice({filters: [{services: []}]})
        .then(device => {
            return device.gatt.connect()
        })
        .then(server => {
            return server.getPrimaryService(serviceUuid);
        })

}