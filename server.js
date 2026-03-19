
const express = require('express');
const WebSocket = require('ws');

const app = express();
const port = process.env.PORT || 5000;  // Railway自动提供PORT

const server = app.listen(port, () => {
  console.log(`服务器已启动在端口 ${port}`);
});

// 创建 WebSocket Server
const wss = new WebSocket.Server({ server });

let clients = [];

wss.on('connection', (ws) => {
  console.log('本地服务器连接');
  clients.push(ws);

  ws.on('close', () => {
    console.log('本地服务器断开');
    clients = clients.filter(client => client !== ws);
  });
});

app.use(express.json());

app.get('/api/send_all', (req, res) => {
  const query = req.query;
  console.log('收到第三方 GET 请求:', query);

  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(query));
    }
  });

  res.json({ status: 'ok', message: 'GET 指令已推送到本地服务器' });
});

