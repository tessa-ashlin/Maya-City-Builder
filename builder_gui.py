#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Tessa Ashlin (tea230000)

:synopsis:
    A module which allows users to stack as many random objects as they want.

:description:
    This module creates a GUI to build stacks of random objects. The user can choose what
    objects to stack by pressing buttons in the GUI, and the objects they select will be
    held and displayed in line edits. The user can press a button to stack objects and
    also determine how many objects to stack. If there are no arguments in the line
    edits when they try to stack things, it will display a warning message to them and
    inform them of what they need to do to fix the error.

:applications:
    Maya

:see_also:
    N/A
"""
from multiprocessing.reduction import duplicate

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports

from PySide2 import QtGui, QtWidgets
import maya.cmds as cmds
import random

# Imports That You Wrote

from td_maya_tools.guis.maya_gui_utils import get_maya_window
from td_maya_tools.stacker import stack_objs, verify_args


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#


class BuilderGUI(QtWidgets.QDialog):
    """
    This is a GUI class which allows users to stack random objects ontop of eachother.
    They can choose the amount of stacks to make and which objects will be included
    in the random lists. It will warn them if it does not get sufficient arguments.
    """
    def __init__(self):
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())

        # Line edits that hold the objects the user selected for the base, middle, and top
        self.top_obj_le = None
        self.mid_obj_le = None
        self.base_obj_le = None

        # Line edit to store the number of stacks the user wants
        self.number_of_stacks = None

    def init_gui(self):
        """
        This method shows the GUI to the user, setting up all of the buttons and
        line edits.
        """

        # Declare a layout.
        main_vbox = QtWidgets.QGridLayout(self)

        # Add four buttons and three corresponding line edits
        top_obj_btn = QtWidgets.QPushButton('Top Objects')
        mid_obj_btn = QtWidgets.QPushButton('Middle Objects')
        base_obj_btn = QtWidgets.QPushButton('Base Objects')
        #Set the button's object name so they can be found in the set_selection method
        top_obj_btn.setObjectName('top_obj_btn')
        mid_obj_btn.setObjectName('mid_obj_btn')
        base_obj_btn.setObjectName('base_obj_btn')
        stack_obj_btn = QtWidgets.QPushButton('Make Stacks')
        self.top_obj_le = QtWidgets.QLineEdit('')
        self.mid_obj_le = QtWidgets.QLineEdit('')
        self.base_obj_le = QtWidgets.QLineEdit('')
        #Make a label and line edit to determine how many stacks to make
        stacks_number_label = QtWidgets.QLabel('Number of stacks:')
        self.number_of_stacks = QtWidgets.QLineEdit('')


        #Add functionality to the buttons. When pressed, they should update the line
        #edit with the transform nodes of whatever the user selected
        top_obj_btn.clicked.connect(self.set_selection)
        mid_obj_btn.clicked.connect(self.set_selection)
        base_obj_btn.clicked.connect(self.set_selection)
        #The stack objects button should duplicate random objects from the
        # top, middle, and base objects and stack them
        stack_obj_btn.clicked.connect(self.make_all_stacks)

        #Add a cancel button which will close the GUI if pressed
        cancel_btn = QtWidgets.QPushButton('Cancel')
        cancel_btn.clicked.connect(self.close)

        # Add the widgets to the layout.
        main_vbox.addWidget(top_obj_btn, 0, 0)
        main_vbox.addWidget(mid_obj_btn, 1, 0)
        main_vbox.addWidget(base_obj_btn, 2, 0)
        main_vbox.addWidget(self.top_obj_le, 0, 1)
        main_vbox.addWidget(self.mid_obj_le, 1, 1)
        main_vbox.addWidget(self.base_obj_le, 2, 1)
        main_vbox.addWidget(stacks_number_label, 3,0)
        main_vbox.addWidget(self.number_of_stacks, 3,1)
        main_vbox.addWidget(stack_obj_btn, 4,0)
        main_vbox.addWidget(cancel_btn, 4, 1)

        # Add the basics of the GUI.
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Builder GUI')
        #img_icon = QtGui.QIcon('C:/Users/teash/code/cat.png')
        #self.setWindowIcon(img_icon) Code for adding an icon image if I want to later
        self.show()

    def set_selection(self):
        """
        This method grabs whatever the user selected and shows it in the button's
        corresponding line edit

        :return: True, if operation completes with no error. If error, return None.
        :type: bool
        """
        # Get the user's selection as a list. If the user selects nothing, return None
        sel = cmds.ls(selection=True)
        if not sel:
            return None

        # Define the string that will be shown to the user in the line edit
        le_str = ""
        for trans_node in sel:
            le_str = le_str + f"{trans_node}, "

        # Remove the space and comma from the end of the new string
        le_str = le_str[:-2]

        # Make a string for the name of the sender (the button which was pressed)
        btn_str = self.sender().objectName()

        # Check which button was pressed, then put the transform nodes into the
        # proper line edit
        if btn_str.startswith('top'):
            self.top_obj_le.setText(le_str)
            return True
        elif btn_str.startswith('mid'):
            self.mid_obj_le.setText(le_str)
            return True
        elif btn_str.startswith('base'):
            self.base_obj_le.setText(le_str)
            return True
        else:
            return None

    def make_all_stacks(self):
        """
        Method that makes a stack of random objects from what information is in the
        GUI's line edits. It only works if the line edits have text in them

        :return: Returns True if no errors occur. If errors, it returns None
        :type: bool
        """

        # Check the arguments before proceeding
        if not self.verify_args():
            return None

        # Initialize variables for the max and current stacks, and the stack name
        max_stacks = int(self.number_of_stacks.text())
        curr_stack = 0
        stack_name = ""

        # Make a list out of the top, middle, and base line edit strings
        base_list = self.base_obj_le.text().split(", ")
        mid_list = self.mid_obj_le.text().split(", ")
        top_list = self.top_obj_le.text().split(", ")

        #Initialize variables to store the current random base, middle, and top objects
        base_obj = None
        mid_obj = None
        top_obj = None

        # Loop through the number of stacks the user wants
        while curr_stack < max_stacks:
            curr_stack += 1
            # Grab a random object from the base list, middle list, and top list
            base_obj = random.choice(base_list)
            mid_obj = random.choice(mid_list)
            top_obj = random.choice(top_list)

            # Duplicate the objects and store them
            base_obj = cmds.duplicate(base_obj)
            mid_obj = cmds.duplicate(mid_obj)
            top_obj = cmds.duplicate(top_obj)

            # Duplicate and stack the random objects, then group them at the origin
            cmds.move(0, 0, 0, base_obj, absolute = True)
            stack_objs(base_obj, mid_obj,top_obj)
            stack_name = "stack" + str(curr_stack).zfill(3)
            cmds.group(base_obj, mid_obj, top_obj, name = stack_name)

        return True

    def verify_args(self):
        """
        A method which verifies the arguments in each of the line edits before the user
        can stack objects

        :return: Returns True if everything is correct, None if not
        :type: bool
        """

        # Initialize a warning message to display to the user if their arguments are not
        # correct

        # Add to a warning message based on the user's errors
        warning_message = ""
        if not self.top_obj_le.text():
            warning_message += "-Select top objects\n"
        if not self.mid_obj_le.text():
            warning_message += "-Select middle objects\n"
        if not self.base_obj_le.text():
            warning_message += "-Select base objects\n"
        if not self.number_of_stacks.text():
            warning_message += "-Declare a number of stacks to make"

        # If no errors have occurred, return True. Otherwise, warn the user and return
        # nothing
        if warning_message == "":
            return True
        else:
            self.warn_user("Insufficient Arguments", warning_message)
            return None


    def warn_user(self, title, message):
        """
        A method which warns the user and will not let them continue until they accept
        the warning

        :param title: The title of the message box to be displayed
        :type: str
        :param message: An explanation of why the warning was issued
        :type: str
        """

        # Make the message box, including a title and message, then show it to the user
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

