import websocket
import json
import pandas as pd

df = pd.DataFrame(columns=['t', 'c', 'h', 'l', 'o'])
sub = False
count = 0


def on_open(ws):
    print("[BERHASIL] terhubung ke websocket")
    ws.send('{"sub":"btcidr.kline.1m", "id":"1"}')


def on_message(ws, message):
    global sub, count, df
    msg = json.loads(message)
    if sub:
        print('[HIGH]', msg["tick"]['h'])
        print('[LOW]', msg["tick"]['l'])
        print('[OPEN]', msg["tick"]['o'])
        print('[CLOSE]', msg["tick"]['c'])
        row = pd.Series(
            {'t': msg["tick"]['t'], 'c': msg["tick"]['c'], 'h': msg["tick"]['h'], 'l': msg["tick"]['l'], 'o': msg["tick"]['o']})
        df = df.append(row, ignore_index=True)
        print("=======================")

    else:
        sub = True
        if msg['status'] == "ok":
            print("[BERHASIL] subscribe k-line")
        else:
            print("[GAGAL] subscribe k-line")


def on_close(ws):
    ws.send('{"unsub":"btcidr.kline.1m", "id":"1"}')
    print("closed connection")


socket = "wss://kline.indodax.com/ws/"

ws = websocket.WebSocketApp(socket, on_open=on_open,
                            on_message=on_message, on_close=on_close)
ws.run_forever()
