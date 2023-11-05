import os
import time
import logging
from pystyle import Colorate, Colors, Col, Add

primaryColor = Colors.StaticMIX((Col.black, Col.purple, Col.purple, Col.white))
secondaryColor = Colors.StaticMIX((Col.black, Col.white, Col.purple, Col.white))
terciaryColor = Colors.StaticMIX((Col.black, Col.black, Col.white, Col.white))
timeColor = Colors.StaticMIX((Col.gray, Col.purple, Col.gray, Col.purple, Col.white))
dataColor = Colors.StaticMIX((Col.gray, Col.purple, Col.purple, Col.black, Col.white))
red = Colors.StaticMIX((Col.red, Col.red, Col.white, Col.white))
green = Colors.StaticMIX((Col.green, Col.green, Col.white, Col.white))
blue = Colors.StaticMIX((Col.blue, Col.blue, Col.white, Col.white))
yellow = Colors.StaticMIX((Col.yellow, Col.yellow, Col.white, Col.white))
orange = Colors.StaticMIX((Col.orange, Col.orange, Col.white, Col.white))
reset = Colors.reset

def get_time():
    return time.strftime("%H:%M:%S")

class Log:
    def __init__(self, typeL, execPart, message):
        self.type = typeL
        self.logging = None
        self.message = message
        self.execPart = execPart
        
        if self.logging:
            if self.type == "error":
                self.logging.error(f"[{execPart}] PopHook | {self.message}")
            elif self.type == "info":
                self.logging.info(f"[{execPart}] PopHook | {self.message}")
            elif self.type == "warning":
                self.logging.warning(f"[{execPart}] PopHook | {self.message}")
            elif self.type == "debug":
                self.logging.debug(f"[{execPart}] PopHook | {self.message}")
            elif self.type == "session":
                self.logging.info(f"------------------------------------ New PopHook Session | [{get_time()}] ------------------------------------")
            else:
                self.logging.critical(f"[{execPart}] PopHook | {self.message}")
        else:
            Printcol(self.type, self.execPart, self.message)
            
    def set_logger(self, logger):
        self.logging = logger
            
class Printcol:
    def __init__(self, typeL, execPart, message):
        self.type = typeL
        self.message = message
        self.execPart = execPart
        
        if self.type == "error":
            print(f"{terciaryColor}[{red}-{terciaryColor}]{primaryColor} {execPart} {terciaryColor}|{secondaryColor} {self.message} {terciaryColor}- [{timeColor}{get_time()}{terciaryColor}]{reset}")
        elif self.type == "info":
            print(f"{terciaryColor}[{green}+{terciaryColor}]{primaryColor} {execPart} {terciaryColor}|{secondaryColor} {self.message} {terciaryColor}- [{timeColor}{get_time()}{terciaryColor}]{reset}")
        elif self.type == "warning":
            print(f"{terciaryColor}[{yellow}!{terciaryColor}]{primaryColor} {execPart} {terciaryColor}|{secondaryColor} {self.message} {terciaryColor}- [{timeColor}{get_time()}{terciaryColor}]{reset}")
        elif self.type == "debug":
            print(f"{terciaryColor}[{blue}*{terciaryColor}]{primaryColor} {execPart} {terciaryColor}|{secondaryColor} {self.message} {terciaryColor}- [{timeColor}{get_time()}{terciaryColor}]{reset}")
        elif self.type == "session":
            self.size = os.get_terminal_size()
            self.size = self.size.columns
            self.size = (self.size - 33)/2
            dashes = "─" * int(self.size)
            print(f"\n{terciaryColor}{dashes} {primaryColor}New PopHook Session {terciaryColor}| [{timeColor}{get_time()}{terciaryColor}] {dashes}{reset}\n")
        elif self.type == "notice":
            print(f"{terciaryColor}[{orange}@{terciaryColor}]{primaryColor} {execPart} {terciaryColor}|{secondaryColor} {self.message} {terciaryColor}- [{timeColor}{get_time()}{terciaryColor}]{reset}")
        else:
            raise Exception(f"Invalid log type: {self.type}")