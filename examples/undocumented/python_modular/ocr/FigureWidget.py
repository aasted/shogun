# File   : $HeadURL$
# Version: $Id$

import gtk
import numpy as np

import common as com
from QuadrWidget import QuadrWidget

class FigureWidget(QuadrWidget):
    THICKNESS_FRAC = 0.03

    def __init__(self):
        QuadrWidget.__init__(self)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)

        self.drag = False
        self.coords = []

        self.connect("expose_event", FigureWidget.on_redraw)
        self.connect("button-press-event", FigureWidget.on_press)
        self.connect("button-release-event", FigureWidget.on_release)
        self.connect("motion-notify-event", FigureWidget.on_motion)
        self.connect("realize", FigureWidget.on_realize)

    def on_realize(self):
        self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))

    def on_press(self, event):
        if event.button == com.BUTTON_RIGHT:
            self.clear_coords()
            self.drag = False

        if event.button != com.BUTTON_LEFT:
            return False

        self.drag = True
        self.coords.insert(0, [])

        # Two times to add a zero-length line
        self.on_motion(event)
        self.on_motion(event)

        return False

    def on_release(self, event):
        if event.button != com.BUTTON_LEFT:
            return False

        self.drag = False
        return False

    def on_motion(self, event):
        if not self.drag:
            return False

        width = self.window.get_size()[0]
        height = self.window.get_size()[1]
        x = event.x/width if event.x < width else com.NEAR_ONE_NEG
        y = event.y/height if event.y < height else com.NEAR_ONE_NEG
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y

        self.coords[0].append((x, y))

        self.update()

        return False

    def on_redraw(self, event):
        gc = self.style.fg_gc[self.state]
        w = self.window
        width = w.get_size()[0]
        height = w.get_size()[1]

        # Backup graphic context
        self.default_fg = gc.foreground
        self.line_width = gc.line_width
        self.line_style = gc.line_style
        self.cap_style = gc.cap_style
        self.join_style = gc.join_style

        # Background
        gc.set_rgb_fg_color(com.COLOR_WHITE)
        w.draw_rectangle(gc, True, 0, 0, width-1, height-1)
        gc.set_rgb_fg_color(com.COLOR_BLACK)
        w.draw_rectangle(gc, False, 0, 0, width-1, height-1)

        # Data
        gc.set_line_attributes(int(height*self.THICKNESS_FRAC),
                               gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND,
                               gtk.gdk.JOIN_ROUND)
        for poly in self.coords:
            w.draw_lines(gc, map(
                    lambda coord:
                        (int(coord[0]*width), int(coord[1]*height)),
                    poly))

        # Recovering graphic context
        gc.line_width = self.line_width
        gc.line_style = self.line_style
        gc.cap_style = self.cap_style
        gc.join_style = self.join_style
        gc.foreground = self.default_fg

        return False

    def get_coords(self):
        result = []

        for poly in self.coords:
            result.extend(poly)
        result = np.array(result)

        if result.shape[0] == 0:
            return result

        result = result.transpose()

        result[0] -= min(result[0])
        result[1] -= min(result[1])
        result /= result.max() + com.NEAR_ZERO_POS
        result[0] += (1 - max(result[0]))/2
        result[1] += (1 - max(result[1]))/2

        result = result.transpose()
        return result

    def clear_coords(self):
        self.coords = []
        self.update()