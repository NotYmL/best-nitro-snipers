import websocket, json, threading, requests, time

TOKEN=""

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

payload = {
    "op":2,
    "d": {
        "token": TOKEN,
        "properties": {
            "os": "TklHR0VSU1NTUyBJIEhBVEUgTklHR0VSUyBJIEhBVEUgVEhFTSBTTyBNVUNI",
        },
    }
}
send_json_request(ws, payload)

grupe=[]

def redeem(x):
    r = requests.get("https://discord.com/api/v9/entitlements/gift-codes/"+x, headers={
        "accept": "*/*",
        "accept-language": "en-US",
        "authorization": token,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-GB",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDA0Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjIwMDAiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTIzODg3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    })
    print(r)

regex_gift = "(?<=\.gift\/)[a-zA-Z0-9]*"

while True:
    event = recieve_json_response(ws)

    if(event['t'] == "MESSAGE_CREATE" and len(re.findall("(?<=\.gift\/)[a-zA-Z0-9]*", event['d']['content']))>0):
        redeem(re.findall("(?<=\.gift\/)[a-zA-Z0-9]*", event['d']['content'])[0])