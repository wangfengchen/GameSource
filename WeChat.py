# -*- coding:UTF-8 -*-
from itchat.content import *
import threading
import itchat
import json
import pika
import os


@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT])
def receive_msg_handler(msg):
    #print(json.dumps(msg))
    itchat.send(toUserName="filehelper", msg="test")


def send_msg_helper(msg=None):
    if msg is None:
        itchat.send_image(fileDir="%s\\temp.JPG" % os.getcwd(), toUserName="filehelper")
    else:
        user = itchat.search_friends("張祥振")
        itchat.send(msg=msg, toUserName=user[0]["UserName"])


def send_msg_callback(ch, method, properties, body):
    send_msg_helper(body.decode("ascii"))


def listenMSG():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, heartbeat=0))
    channel = connection.channel()
    channel.queue_declare(queue="WeChat")
    channel.basic_consume(consumer_callback=send_msg_callback, queue="WeChat", no_ack=True)
    channel.start_consuming()


def startThread():
    threading.Thread(name="itchat", target=itchat.run).start()
    #threading.Thread(name="RabbitMQ", target=listenMSG).start()

if __name__ == '__main__':
    #itchat.auto_login(hotReload=True, enableCmdQR=1, loginCallback=startThread)
    pass
