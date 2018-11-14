# -*- coding:UTF-8 -*-
from MainProcessor import GameStart, CommonUtil, TaskThread, GameHandle, ConstantUtil
from pynput.keyboard import Key, Listener
import win32gui as Window
from queue import Queue
from PIL import Image
import threading
import WeChat
import itchat
import os

def populate(q):
    evt = threading.Event()
    q.put(("Sub1Game", evt))
    evt.wait()


def onKeyPress(key):
    if key == Key.esc:
        # 处理强制终止
        os.system("TASKKILL /F /IM python.exe")


def main():
    q = Queue()
    #初期化登陆方式
    GameHandle.setLoginType("no")
    # 读取配置文件
    className, windowName = GameHandle.getClassName(True)
    #游戏启动确认，未启动的情况下启动游戏s
    gameHWD = Window.FindWindow(className, windowName)
    if not gameHWD:
        #脚本启动
        startThread = threading.Thread(target=GameStart.start, name="GameStart", args=(True, q))
        startThread.start()
        taskThread = threading.Thread(target=TaskThread.init, name="GameMainHandle", args=(q,))
        taskThread.start()
        q.join()
    else:
        CommonUtil.initGlobalVar()
        CommonUtil.clearScreen(True, False)
        if CommonUtil.isLoginOver(True):
            #大号已经启动结束
            hwd = GameHandle.getHWD(False)
            if not hwd:
                # 第二个窗口启动
                # 判断多重启动按钮是否可用
                CommonUtil.capture(True)
                if Image.open("%s\\temp.jpg" % os.getcwd()).size[0] < 1060:
                    CommonUtil.leftClick(1034, 19, True)
                # 多重启动开始
                CommonUtil.leftClick(1057, 286, True)

                #游戏启动程序
                startThread = threading.Thread(target=GameStart.start, name="GameStart", args=(False, q))
                startThread.start()
                #游戏操作程序
                taskThread = threading.Thread(target=TaskThread.init, name="GameMainHandle", args=(q,))
                taskThread.start()
                q.join()
            else:
                #小号启动结束的话，通知处理线程
                startThread = threading.Thread(target=populate, name="GameStart", args=(q,))
                startThread.start()
                taskThread = threading.Thread(target=TaskThread.init, name="GameMainHandle", args=(q,))
                taskThread.start()
                q.join()


def startThread():
    #threading.Thread(name="itchat", target=ConstantUtil.getWeChat().run).start()
    #threading.Thread(name="RabbitMQ", target=WeChat.listenMSG).start()
    threading.Thread(name="GameThread", target=main).start()

    #键盘事件追加
    with Listener(
        on_press=onKeyPress,
        on_release=None
    ) as listener:
        listener.join()


if __name__ == "__main__":
    #os.system("TASKKILL /PID %d" % GameHandle.getHWD(False))
    #微信登陆
    #ConstantUtil.setWeChat(itchat)
    #ConstantUtil.getWeChat().auto_login(hotReload=True, enableCmdQR=1, loginCallback=startThread)
    startThread()
