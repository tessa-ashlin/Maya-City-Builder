#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Tessa Ashlin (tea230000)

:synopsis:
    This module stacks random objects ontop of each other.

:description:
    The module receives three transform nodes from the user, then verifies if they
    are valid. If they are, it uses the objects' bounding box information to get
    the bottom and top center of the different objects so they can be placed ontop
    of each other. Then, it stacks them. The x and z bounding box information is
    averaged so that it's exactly in the center.

:applications:
    Maya

:see_also:
    N/A
"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports

import maya.cmds as cmds

# Imports That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def stack_objs(first_node=None, second_node=None, third_node=None):
    """
    A function which stacks random objects ontop of each other

    :param first_node: The translational node of the first object
    :type: str

    :param second_node:The translational node of the second object
    :type: str

    :param third_node: The translational node of the third object
    :type: str

    :return: The function returns True if the arguments are valid, and None if not
    :type: bool
    """

    # Create variables to store the bottom and top coordinates of objects being stacked
    bottom_center_coords = None
    top_center_coords = None

    # Verify that the arguments given by the user are valid. If they are not, inform
    # the user with a warning message
    if not verify_args(first_node,second_node,third_node):
        cmds.warning( "Invalid arguments" )
        return None

    # Get the top center of the first node and the bottom center of the second node,
    # then stack the two objects
    top_center_coords = get_center_point(first_node, None, True)
    bottom_center_coords = get_center_point(second_node, True, None)
    add_to_stack(second_node, bottom_center_coords, top_center_coords)

    # Get the top center of the second node and the bottom center of the third node,
    # then stack the two objects
    top_center_coords = get_center_point(second_node,None,True)
    bottom_center_coords = get_center_point(third_node,True,None)
    add_to_stack(third_node, bottom_center_coords, top_center_coords)

    # The stack is complete
    return True


def add_to_stack(trans_node=None, bottom_center=None, placement=None):
    """
    A function which adds objects to a stack of other objects based on the xyz values
    given

    :param trans_node: The translational node of the object
    :type: str

    :param bottom_center: The bottom center of the object to move in xyz values
    :type: list

    :param placement: The point in space to place the object in xyz values
    :type: str
    """

    #Move the object horizontally to the center of the other object. Then,
    # move it up the amount in y that it needs to stack on top of the first object
    cmds.move(placement[0],placement[2], trans_node, moveXZ = True, absolute=True)
    cmds.move(0,placement[1] - bottom_center[1],0, trans_node, relative=True)


def get_center_point (trans_node=None, bottom_center=None, top_center=None):
    """
    A function which gets either the top or bottom center of the object depending
    on what the user specifies

    :param trans_node: The name of the translational node to recieve coordinates for
    :type: str

    :param bottom_center: Tells the function to find the bottom center of the object
    :type: bool

    :param top_center: Tells the function to find the top center of the object
    :type: bool

    :return: The bottom or top center coordinates
    :type: list
    """

    #Get the bounding box for the object as a list and assign it to a variable
    bounding_box = cmds.xform(trans_node, query=True, boundingBox=True)
    #Get the average x and z coordinates for the bounding box
    average_x = (bounding_box[0] + bounding_box[3])/2
    average_z = (bounding_box[2] + bounding_box[5])/2
    height = (bounding_box[4] - bounding_box[1])

    # If the user wants the top center, return only those values as a list. Otherwise,
    # return the bottom center values as a list
    if top_center:
        return [average_x, bounding_box[4], average_z]
    elif bottom_center:
        return [average_x,bounding_box[1],average_z]

def verify_args(first=None, second=None, third=None):
    """
    A function which tests if the variables sent in all have values

    :param first: The first variable
    :type: str

    :param second: The second variable
    :type: str

    :param third: The third variable
    :type: str

    :return: Returns True if the variables have a value, None if not
    :type: bool
    """

    # If any of the variables don't have a value, return None
    if not first:
        return None
    if not second:
        return None
    if not third:
        return None

    #The variables all have values, return True
    return True

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

