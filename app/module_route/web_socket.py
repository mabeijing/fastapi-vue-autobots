# @Time 2022/11/4 17:16
# Author: beijingm

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import aioredis
from fastapi.responses import HTMLResponse

redis = aioredis.from_url("redis://localhost/10", password="root123")

# html在页面上做显示的用途
html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>websocket</title>
    </head>
    <body>
    <h1>User1 Chat</h1>
    <form action="" οnsubmit="sendMessage(event)">
        <input type="text" id="messageText" autocomplete="off"/>
        <button>Send</button>
    </form>
    <ul id='messages'>
    </ul>

    <script>
        var ws = new WebSocket("ws://127.0.0.1:8000/test/");

        ws.onmessage = function(event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        };
        function sendMessage(event) {
            var input = document.getElementById("messageText")
            ws.send(input.value)
            input.value = ''
            event.preventDefault()
        }
    </script>

    </body>
    </html>

"""
# 注册子路由
socket = APIRouter()


# 定义聊天类
class ConnectionManager:
    ## 初始化定义记录全部的链接
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.sessions = dict()

    ##
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    ## 关闭链接时的动作
    async def on_close(self, websocket: WebSocket, close_code: int):
        await websocket.close(close_code)
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        await ws.send_text(message)

    ## 点对点的操作
    @staticmethod
    async def send_user_message(message: str, ws: WebSocket):
        await ws.send_text(message)

    ## 广播信息的操作
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    ## 解析关键词
    async def filter_message(self, message: str):
        json_object = None
        try:
            json_object = json.loads(message)
            # if 'event' not in json_object:
            #     json_object = None
        except ValueError as e:
            print('yichang')

        print('json_object', json_object)
        return json_object

    # {"event":"join"}
    ## 收到对应的消息之后解析消息并确定需要干什么事情
    async def on_message(self, message: str, ws: WebSocket):
        print('on_message', message)
        msg = await self.filter_message(message)
        # print('msg', msg['event'])
        if msg:
            # 接收pong ping
            if msg['event'] == 'pong':
                await self.send_personal_message('ping', ws)
            elif msg['event'] == 'ping':
                await self.send_personal_message('pong', ws)
            # 进入房间
            elif msg['event'] == 'join':
                # await self.on_join(msg)
                await self.send_personal_message('success', ws)

            # 退出房间的情况 会触发异常
            elif msg['event'] == 'close':
                await self.send_personal_message('再见', ws)
                await self.on_close(ws, 1008)

        else:
            await self.send_personal_message('wrong message format', ws)

    # ## 获取房间的一些信息
    # async def get_room_info(self, room_id, db):
    #     room = db.query(Room).filter(Room.id == room_id).first()
    #     return room

    ## 使用逻辑将新进的用户加到对应的房间中
    async def register_user(self, room_id, user_id, ws: WebSocket):
        await self.set_userid(user_id, ws)
        await self.set_roomid(room_id, ws)

        # 验证是否存储进去
        roomid = await self.get_roomid(ws)
        print('-------------------------', roomid)

        # register session
        if self.sessions.get(room_id, None) is None:
            self.sessions[room_id] = []
        self.sessions[room_id].append(ws)

        print('self.sessions', self.sessions)

    # async def test(self):
    #     async with redis.client() as conn:
    #         val = await conn.get('session2userid:{}'.format(self))
    #         room_id = await conn.get('session2roomid:{}'.format(self))
    #     return val, room_id

    ## 将用户移出房间
    async def deregister_user(self, ws: WebSocket):
        # del session -> user_id
        user_id = await self.get_userid(ws)
        await self.del_userid()

        # del session -> race_id
        room_id = await self.get_roomid(ws)
        await self.del_roomid()
        room_id = int(room_id)

        # 登陆过的才有user_id
        if user_id:
            # deregister session
            self.sessions[room_id].remove(ws)
            # 从业层面将用户移除
            # await self.leave_room(room_id, user_id)
        # 查看是否删除
        print('session', self.sessions)

    # user离开room的时候
    async def leave_room(self, room_id, user_id):
        pass

    # 将信息发送给房间中的人
    async def send_msg_room(self, msg, ws1: WebSocket):
        print('session', self.sessions)

        # TODO 不能使用函数取需要自定义取参数

        # user_id = self.get_userid(ws1)
        # room_id = self.get_roomid(ws1)
        async with redis.client() as conn:
            user_id = await conn.get('session2userid:{}'.format(ws1))
            room_id = await conn.get('session2roomid:{}'.format(ws1))

        print('----------user=------------', user_id)
        print('----------room=------------', room_id)

        # get room_id
        # room_id = await self.get_roomid()
        room_id = int(room_id)
        for ws in self.sessions[room_id]:
            if ws != ws1:
                # 进来时取ws的姓名和房间号
                async with redis.client() as conn:
                    user_id = await conn.get('session2userid:{}'.format(ws1))
                    room_id = await conn.get('session2roomid:{}'.format(ws1))

                print('send msg user[{}] room_id [{}]'.format(user_id, room_id))
                await ws.send_text(msg)

    # 存入sessin到redis
    async def set_sessions(self, ws: WebSocket):
        async with redis.client() as conn:
            await conn.hset('sessions', json.dumps([ws]))

    # 将userid存储起来
    async def set_userid(self, user_id, ws: WebSocket):
        async with redis.client() as conn:
            await conn.set('session2userid:{}'.format(ws), user_id)
            val = await conn.get('session2userid:{}'.format(ws))
        return val

    # 将roomid 存储起来
    async def set_roomid(self, room_id, ws: WebSocket):
        async with redis.client() as conn:
            await conn.set('session2roomid:{}'.format(ws), room_id)
            val = await conn.get('session2roomid:{}'.format(ws))
        return val

    # 获取用户id
    async def get_userid(self, ws: WebSocket):
        print('-------------ws-------------', ws)
        async with redis.client() as conn:
            user_id = await conn.get('session2userid:{}'.format(ws))

        return user_id

    # 获取房间id
    async def get_roomid(self, ws: WebSocket):
        async with redis.client() as conn:
            room_id = await conn.get('session2roomid:{}'.format(ws))

        return room_id

    # 删除用户
    async def del_userid(self):
        async with redis.client() as conn:
            await conn.delete('session2userid:{}'.format(self))

    # 删除房间
    async def del_roomid(self):
        async with redis.client() as conn:
            await conn.delete('session2roomid:{}'.format(self))


manager = ConnectionManager()


@socket.get("/ws/")
async def index():
    return HTMLResponse(html)


@socket.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):
    await manager.connect(websocket)
    await manager.broadcast(f"用户{user}进入聊天室")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)
            await manager.broadcast(f"用户:{user} 说: {data}")



    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户-{user}-离开")


@socket.websocket("/ws/{room_id}/{user_id}")
async def join_room(websocket: WebSocket, room_id: int, user_id: str):
    # 判定当前进入房间的user 是不是已经在链接中存在了
    await manager.connect(websocket)
    await manager.register_user(room_id, user_id, websocket)
    await manager.send_msg_room(f"用户-{user_id}-进入", websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)
            # 解析用户是发送的消息是否是正常的
            # await manager.on_message(data, websocket)
            # 将信息发送给房间中的人
            await manager.send_msg_room(f"{user_id}说了: {data}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.deregister_user(websocket)
        await manager.send_msg_room(f"用户-{user_id}-离开", websocket)


@socket.websocket("/test/")
async def websocket_test(websocket: WebSocket):
    # todo 进来时查看是不是携带token，如果没有携带直接断开
    # 将用户加入到websocket链接中
    await manager.connect(websocket)
    # 第一个人进入存储1 依次类推

    # await redis_set_msg(websocket, '1234')

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)
            # 解析用户是发送的消息是否是正常的
            await manager.on_message(data, websocket)


    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.deregister_user(websocket)
        await manager.broadcast(f"用户-test-离开")
