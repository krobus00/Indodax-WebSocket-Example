const WebSocketClient = require('websocket').client

var client = new WebSocketClient()
const pair = 'btcidr'
const interval = '15m'

client.on('connectFailed', (error) => {
    console.log('Connect Error: ' + error.toString());
})

client.on('connect', (connection) => {
    console.log('[BERHASIL] terhubung ke websocket');
    connection.send(`{"sub":"${pair}.kline.${interval}", "id":"1717"}`)
    connection.on('error', (error) => {
        console.log("Connection Error: " + error.toString());
    })
    connection.on('close', () => {
        console.log('echo-protocol Connection Closed');
    })
    connection.on('message', (message) => {
        let res = JSON.parse(message.utf8Data)
        if ('subbed' in res) {
            console.log(`[BERHASIL] terhubung ke ${res.subbed}`)
        } else {
            console.log("================")
            let data = res.tick
            console.log(`[TIME] ${data.t}`)
            console.log(`[CLOSE] ${data.c}`)
            console.log(`[HIGH] ${data.h}`)
            console.log(`[LOW] ${data.l}`)
            console.log(`[OPEN] ${data.o}`)
        }
    })

    function sendPing() {
        if (connection.connected) {
            connection.send('{}')
            setTimeout(sendPing, 1000)
        }
    }
    sendPing()
})

client.connect('wss://kline.indodax.com/ws/')