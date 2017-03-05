#!/usr/bin/env python
import sys
import os
from subprocess import call
from time import sleep
import argparse
#Welcome to pyLCI innards
#Here, things are about i and o, which are input and output
#And we output things for debugging, so o goes first.
from output import output

main_config_path = "/boot/pylci_config.json"
backup_config_path = "./config.json"

#Debugging helper snippet
import threading
import traceback
import signal
import sys
def dumpthreads(*args):
    print("")
    print("SIGUSR received, dumping threads")
    print("")
    for th in threading.enumerate():
        print(th)
        traceback.print_stack(sys._current_frames()[th.ident])
        print("")
signal.signal(signal.SIGUSR1, dumpthreads)

#Locating pyLCI config - if config at main_config_path exists, use that
#If not, use the backup path
#Simple and hacky, we're not even checking the validity for now (TODO)

if os.path.exists(main_config_path): config_path = main_config_path
else: config_path = backup_config_path

#Getting pyLCI config, it will be passed to input and output initializers
from helpers import read_config

try:
    config = read_config(config_path)
except Exception as e:
    print(repr(e))
    print("------------------------------")    
    print("Couldn't read config, exiting!")
    sys.exit(1)


#These lines are here so that welcome message stays on the screen a little longer:
output.init(config["output"])
o = output.screen
from ui import Printer, Menu


try: #If there's an internal error, we show it on display and exit
    from apps.manager import AppManager
    #Now we init the input subsystem
    from input import input
    input.init(config["input"])
    i = input.listener
except:
    Printer(["Oops. :(", "y u make mistake"], None, o, 0) #Yeah, that's about all the debug data. 
    raise

def splash_screen():
    try:
        from splash import splash
        splash(i, o)
    except ImportError:
        pass

def exception_wrapper(callback):
    """This is a wrapper for all applications and menus. It catches exceptions and stops the system the right way when something bad happens, be that a Ctrl+c or an exception in one of the applications."""
    try:
        callback()
    except KeyboardInterrupt:
        Printer(["Does Ctrl+C", "hurt scripts?"], None, o, 0)
        i.atexit()
        sys.exit(1)
    except Exception as e:
        print(e)
        #raise
        Printer(["A wild exception", "appears!"], None, o, 0)
        i.atexit()
        sys.exit(1)
    else:
        Printer("Exiting pyLCI", None, o, 0)
        i.atexit()
        sys.exit(0)

def launch(name=None):
    """Function that launches pyLCI, either in full mode or single-app mode (if ``name`` kwarg is passed)."""
    app_man = AppManager("apps", Menu, Printer, i, o)
    if name != None:
        name = name.rstrip('/') #If using autocompletion from main folder, it might append a / at the name end, which isn't acceptable for load_app
        try:
            app = app_man.load_app(name)
        except:
            i.atexit()
            raise
        exception_wrapper(app.callback)
    else:
        splash_screen()
        app_menu = app_man.load_all_apps()
        exception_wrapper(app_menu.activate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyLCI runner")
    parser.add_argument('-a', '--app', action="store", help="Launch pyLCI with a single app loaded (useful for testing)", default=None)
    args = parser.parse_args()
    launch(name=args.app)
