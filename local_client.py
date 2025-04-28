import websocket
import threading
import requests
import json

def on_message(ws, message):
    print("收到云端指令：", message)
    try:
        data = json.loads(message)
        # 发送请求到本地127.0.0.1服务器
        resp = requests.post('http://127.0.0.1:5000/api/send_all', json=data)
        print("本地服务器返回：", resp.status_code, resp.text)
    except Exception as e:
        print("处理指令时出错：", e)

def on_error(ws, error):
    print("连接出错：", error)

def on_close(ws, close_status_code, close_msg):
    print("连接关闭，尝试重连...")
    # 简单自动重连
    threading.Timer(5, connect).start()

def on_open(ws):
    print("成功连接到云端服务器")

def connect():
    ws = websocket.WebSocketApp(
        "wss://你的云端服务器/ws",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()

if __name__ == "__main__":
    connect()
