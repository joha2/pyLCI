"""test for class DialogBox"""

import unittest
import logging
import dialog
import os

#set up logging
LOG_FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class DummyOutputDevice():
    """fake output device, just dumps stuff to logger"""
    def __init__(self):
        self.cols = 80
        logger.debug("DummyOutputDevice constructor called")
    def setCursor(self, arg1, arg2):
        """mock set cursor routine"""
        logger.debug("setCursor called.  arg1=%d, arg2=%d", arg1, arg2)
    def display_data(self, message, displayed_label):
        """mock display_data routine"""
        logger.debug("display_data called, message='%s'", message)
        logger.debug("display_data called, displayed_label='%s'", displayed_label)

class TestDialogBox(unittest.TestCase):
    """tests dialog box class"""
    def test_constructor(self):
        """tests constructor"""
        logger.debug("entering DialogBox test_constructor")
        logger.debug("os.getcwd()=%s", os.getcwd())
        default_options = "ync"
        output_device = DummyOutputDevice()
        dialog_box = dialog.DialogBox(default_options, None, output_device)
        self.assertIsNotNone(dialog_box)
