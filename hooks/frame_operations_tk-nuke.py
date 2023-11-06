# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import nuke
import os

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class FrameOperation(HookBaseClass):
    """
    Hook called to perform a frame operation with the
    current scene
    """

    def get_frame_range(self, **kwargs):
        """
        get_frame_range will return a tuple of (in_frame, out_frame)

        :returns: Returns the frame range in the form (in_frame, out_frame)
        :rtype: tuple[int, int]
        """
        current_in = int(nuke.root()["first_frame"].value())
        current_out = int(nuke.root()["last_frame"].value())
        current_fps = int(nuke.root()['fps'].value())
        return (current_in, current_out, current_fps)

    def set_frame_range(self, in_frame=None, out_frame=None, framerate=None, res=None, **kwargs):
        """
        set_frame_range will set the frame range using `in_frame` and `out_frame`

        :param int in_frame: in_frame for the current context
            (e.g. the current shot, current asset etc)

        :param int out_frame: out_frame for the current context
            (e.g. the current shot, current asset etc)

        """

        # unlock
        # locked = nuke.root()["lock_range"].value()
        # if locked:
        nuke.root()["lock_range"].setValue(False)

        # set values
        if in_frame != None or out_frame != None:
            nuke.root()["first_frame"].setValue(in_frame)
            nuke.root()["last_frame"].setValue(out_frame)
            
        if framerate != None:  
            nuke.root()['fps'].setValue(framerate)
            
        width, height = res
        if width != None and height != None:
            width, height = res
            current_width = nuke.root()["format"].value().width()
            current_height = nuke.root()["format"].value().height()
            
            if width != current_width or height != current_height:
                file = os.path.abspath(__file__)
                name = str(file).split(os.sep)[3]
                
                fmt = None
                for f in nuke.formats():
                    if f.width() == width and f.height() == height:
                        fmt = f.name()
                        
                    if fmt == None:
                        nuke.addFormat(
                            '{0} {1} {2}'.format(int(width), int(height), name)
                        )
                        fmt = name
                    print('\n', fmt, '\n')
                    nuke.root()['format'].setValue(fmt)

        # and lock again
        # if locked:
        nuke.root()["lock_range"].setValue(True)
