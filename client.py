#! /usr/bin/env python
import paho.mqtt.client as mqtt
import os
import uuid
from test import MyApp
from threading import Thread


qos = 0
topic = "game"
add_score_msg = "score"

game_ending_topic = "end"
game_ending_msg = "end"

# ROLES
DEFEND = "defend"
TERROR = "terror"

class User():
    def __init__(self, role, url, port):
        self.uid = uuid.uuid4()
        self.role = role
        self.score = 0
        self.url = url
        self.port = port
        self.client = self.make_client()

    def make_client(self):
        client = mqtt.Client(client_id=self.uid)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(self.url, self.port, 60)

        return client
    
    def connect(self):
        self.client.loop_forever()

    def threading(self):
        self.thread = Thread(target=self.connect)
        self.thread.start()

    def initiate(self):
        self.client.publish(game_ending_topic, game_ending_msg, qos)
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
            # When Game is over
            defend_user.initiate()
            attack_user.initiate()

app = MyApp(False)

defend_user.threading()
attack_user.threading()

# class client():
#     def update():
#         print(app.win(DEFEND))

# client1 = make_client(defend_user.uid, defend_user.url, defend_user.port)
# client2 = make_client(attack_user.uid, attack_user.url, attack_user.port)

# defend_user.client = client1
# attack_user.client = client2

app.MainLoop()