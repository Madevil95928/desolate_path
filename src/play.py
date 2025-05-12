#!/usr/bin/env python
# coding=utf-8

import time
import sys
import contextlib
from pathlib import Path
from typing import Optional, Tuple, Union
import keyboard
import mss
import numpy as np
import pyautogui
import cv2
from loguru import logger
logger.configure(handlers=[{'sink': sys.stderr, "level": "INFO"}])


class DesolatePath:
    def __init__(self):
        self.dir_images = Path(__file__).parent.joinpath("../data/images").resolve()
        self.img_fight = cv2.imread(self.dir_images.joinpath("fight.jpg").__str__(), 0)
        self.img_ignore = cv2.imread(self.dir_images.joinpath("ignore.jpg").__str__(), 0)
        self.img_enter = cv2.imread(self.dir_images.joinpath("enter.jpg").__str__(), 0)
        self.img_escape = cv2.imread(self.dir_images.joinpath("escape.jpg").__str__(), 0)
        self.img_treasure = cv2.imread(self.dir_images.joinpath("treasure.jpg").__str__(), 0)
        self.img_roger = cv2.imread(self.dir_images.joinpath("roger.jpg").__str__(), 0)
        self.img_deal = cv2.imread(self.dir_images.joinpath("deal.jpg").__str__(), 0)
        self.img_ruin = cv2.imread(self.dir_images.joinpath("ruin.jpg").__str__(), 0)
        self.img_boss = cv2.imread(self.dir_images.joinpath("boss.jpg").__str__(), 0)
        self.img_upgrade = cv2.imread(self.dir_images.joinpath("upgrade.jpg").__str__(), 0)
        self.img_abandon = cv2.imread(self.dir_images.joinpath("abandon.jpg").__str__(), 0)
        self.img_bless = cv2.imread(self.dir_images.joinpath("bless.jpg").__str__(), 0)
        # self.img_meet = cv2.imread(self.dir_images.joinpath("meet.jpg").__str__(), 0)
        self.img_scroll = cv2.imread(self.dir_images.joinpath("scroll.jpg").__str__(), 0)
        self.dimensions = dict(
            left=1952,
            top=155,
            width=600,
            height=1400,
        )
        self.threshold: float = .95
        self.mss_obj = mss.mss()
        self.img: Optional[cv2.typing.MatLike] = None

    @property
    def screenshot(self):
        return np.array(self.mss_obj.grab(self.dimensions))

    @staticmethod
    def wait_but_monitor_q(timeout: Union[int, float]):
        time_end = time.time() + timeout
        while time.time() < time_end:
            if keyboard.is_pressed("q"):
                return True
        else:
            return False

    @staticmethod
    @contextlib.contextmanager
    def start_info():
        print("脚本运行后，连续多次键入 \"q\" 退出自动化")
        pos = pyautogui.position()
        yield
        pyautogui.moveTo(pos[0], pos[1])

    def get_click_pos(self, loc: np.ndarray, offset_x: int = 10, offset_y: int = 10):
        # logger.warning(f'{loc[1]}')
        # logger.warning(f'{loc[0]}')
        left = self.dimensions["left"] + loc[1][0]
        top = self.dimensions["top"] + loc[0][0]
        return left + offset_x, top + offset_y

    def get_loc(self, child_img: cv2.typing.MatLike):
        # if not self.img:
        res = cv2.matchTemplate(self.img, child_img, cv2.TM_CCOEFF_NORMED)
        return np.where(res >= self.threshold)

    @staticmethod
    def move_and_click(x, y, interval: Union[int, float] = .1):
        pyautogui.moveTo(x, y)
        time.sleep(interval)
        pyautogui.click()

    def fight(self) -> bool:
        """迎战"""
        logger.debug("检测迎战")
        loc = self.get_loc(self.img_fight)
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[迎战]")
            return True
        return False

    def is_boss(self) -> bool:
        """是否BOSS关"""
        logger.debug("是否BOSS关")
        loc = self.get_loc(self.img_boss)
        if len(loc[0]) > 0:
            logger.success("检测到[BOSS关]")
            return True
        return False

    def escape(self) -> bool:
        """逃跑"""
        logger.debug("逃跑")
        loc = self.get_loc(self.img_escape)
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[逃跑]")
            return True
        return False

    def enter(self) -> bool:
        """进入"""
        logger.debug("进入")
        loc = self.get_loc(self.img_enter)
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[进入]")
            return True
        return False

    def ignore(self) -> bool:
        """无视"""
        logger.debug("无视")
        loc = self.get_loc(self.img_ignore)
        # logger.warning(f'{loc=}')
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[无视]")
            return True
        return False

    def roger(self) -> bool:
        """知道了"""
        logger.debug("知道了")
        self.scroll()
        loc = self.get_loc(self.img_roger)
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[知道了]")
            return True
        return False

    def treasure(self) -> bool:
        """打开乾坤袋"""
        logger.debug("打开乾坤袋")
        loc = self.get_loc(self.img_treasure)
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[打开乾坤袋]")
            return True
        return False

    def is_upgrade(self) -> bool:
        """是否升级"""
        logger.debug("是否升级")
        loc = self.get_loc(self.img_upgrade)
        if len(loc[0]) > 0:
            logger.success("检测到[升级]")
            logger.critical("请手动选择升级属性")
            return True
        return False

    def is_bless(self) -> bool:
        """是否眷天"""
        logger.debug("是否眷天")
        loc = self.get_loc(self.img_bless)
        if len(loc[0]) > 0:
            logger.success("检测到[眷天]")
            return True
        return False

    def deal(self) -> bool:
        """成交"""
        logger.debug("成交")
        loc = self.get_loc(self.img_deal)
        if len(loc[0]) > 0:
            x, y = self.get_click_pos(loc)
            self.move_and_click(x, y)
            logger.success("已点击[成交]")
            return True
        return False

    def scroll(self):
        logger.debug("滚动条")
        loc = self.get_loc(self.img_scroll)
        if len(loc[0]) > 0:
            logger.success("检测到[滚动条]")
            x, y = self.get_click_pos(loc, offset_x=3, offset_y=3)
            pyautogui.mouseDown(button="left", x=x, y=y)
            time.sleep(0.1)
            pyautogui.moveTo(x, y + self.dimensions['height'])
            pyautogui.mouseUp(button="left")
            # self.move_and_click(x, y)
            # pyautogui.scroll(self.dimensions['height'])

    def test(self) -> bool:
        with self.start_info():
            for _ in range(100):
                if self.wait_but_monitor_q(0.2):
                    return True

                pyautogui.moveTo(self.dimensions["left"], self.dimensions["top"] + 50)
                time.sleep(0.1)
                self.img = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)

                print(self.ignore())
                return False
        return False

    def always_fight(self, is_boss: bool = False) -> bool:
        with self.start_info():
            while True:
                if self.wait_but_monitor_q(0.2):
                    return True

                pyautogui.moveTo(self.dimensions["left"] + 50, self.dimensions["top"] + 50)
                time.sleep(0.1)
                self.img = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)

                if self.is_upgrade():
                    return False

                if not is_boss and self.is_boss():
                    self.ignore()
                    continue
                elif is_boss and self.is_boss():
                    self.enter()
                    continue

                if self.is_bless():
                    self.deal()
                    continue

                if any((
                    self.fight(),
                    self.treasure(),
                    self.roger(),
                    # self.enter(),
                    self.ignore()
                )):
                    continue
                # if self.fight() or self.treasure() or self.roger() or self.ignore():
                #     continue
        return False


if __name__ == '__main__':
    dp = DesolatePath()
    logger.info(dp)
    # dp.test()
    dp.always_fight(is_boss=True)
    # dp.always_fight(is_boss=False)
