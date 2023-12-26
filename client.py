#! /usr/bin/env python
import paho.mqtt.client as mqtt
import os
import uuid
from test import MyApp
from threading import Thread


qos = 0
topic = "game"
add_score_msg = "score"

# ROLES
DEFEND = "defend"
TERROR = "terror"

class User():
    def __init__(self, role, url, port):
        self.value = uuid.uuid4()
        self.role = role
        self.score = 0
        self.url = url
        self.port = port

    @property
    def uid(self): return self.value

    def initiate(self):
        self.score = 0

defend_user_env = os.getenv("DEFEND", "hi:!234").split(":")
attack_user_env = os.getenv("ATTACK", "hi:1234").split(":")

### TODO: url
defend_user = User(role=DEFEND, url=defend_user_env[0], port=defend_user_env[1])
attack_user = User(role=TERROR, url=attack_user_env[0], port=attack_user_env[1])

USER_DATA = {}
USER_DATA[defend_user.uid] = defend_user
USER_DATA[attack_user.uid] = attack_user

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global topic
    print("Connected with result code "+str(rc))
    client.subscribe(topic, qos=qos)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic != topic:
        return
    
    decoded_msg = msg.payload.decode("utf-8")
    if decoded_msg == add_score_msg:
        client_id = client.client_id
        user = USER_DATA[client_id]
        user.score += 1
        if app.win(user.role):
            defend_user.initiate()
            attack_user.initiate()

def make_client(client_uid, client_url, port):
    client = mqtt.Client(client_id=client_uid)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(client_url, port, 60)
    return client
    # return client


app = MyApp(False)

# class client():
#     def update():
#         print(app.win(DEFEND))

client1 = make_client(defend_user.uid, defend_user.url, defend_user.port)
client2 = make_client(attack_user.uid, attack_user.url, attack_user.port)

def connect(client):
    # client1.loop_start()
    # client2.loop_start()
    client.loop_forever()
    # client.update()

client_thread1 = Thread(target=connect, kwargs={"client": client1})
client_thread2 = Thread(target=connect, kwargs={"client": client2})
client_thread1.start()
client_thread2.start()

app.MainLoop()