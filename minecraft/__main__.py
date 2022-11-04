# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import atexit
import sys
import traceback
from os import remove
from os.path import isfile, join

import pyglet

from minecraft.scene import GameWindow
from minecraft.scene.start import StartScene
from minecraft.utils.opengl import setup_opengl
from minecraft.utils.test import test
from minecraft.utils.utils import *


def start():
    """游戏从这里开始。

    创建窗口、进入场景、开始游戏。
    """
    try:
        setup_opengl()
        game = GameWindow(800, 600, resizable=True)
        game.add_scene("minecraft:start", StartScene)
        game.switch_scene("minecraft:start")
        pyglet.app.run()
    except SystemExit:
        pass
    except:
        # 这里负责处理不知道谁引发的异常，并将异常写入日志
        for line in traceback.format_exception(*sys.exc_info()):
            for s in line.split("\n")[:-1]:
                log_err(s)


if __name__ == "__main__":
    if isfile(join(search_mcpy(), "mcpy.lock")):
        # 检测程序是否重复启动
        log_info("Minecrft-in-python is running now!", where="c")
    else:
        open(join(search_mcpy(), "mcpy.lock"), "w+").close()
        # 注册退出处理器
        if "--no-save-log" not in sys.argv:
            atexit.register(on_exit)
        # 打印运行环境等基本信息
        test()
        # 开始游戏！
        start()
        if isfile(join(search_mcpy(), "mcpy.lock")):
            remove(join(search_mcpy(), "mcpy.lock"))
