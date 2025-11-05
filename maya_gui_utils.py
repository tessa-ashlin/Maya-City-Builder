#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Tessa Ashlin (tea230000)

:synopsis:
    This module prevents GUI from disappearing behind the Maya window.

:description:
    This module grabs a pointer to the Maya window and ensures the GUI created will not
    disappear off of the screen if the user clicks somewhere else in Maya.

:applications:
    Maya

:see_also:
    N/A
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports

from PySide2 import QtGui, QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def get_maya_window():
    """
    This function gets a pointer to the main Maya window.

    :return: A pointer to the Main Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

