import json
import tkinter as tk
from tkinter import messagebox
import math


# TODONE: draw line from point to point
# TODONE: Add point at edge
# TODONE: ADD point to point snapping for polygon closure
# TODONE: Add option to save the polygon
# TODONE: save polygon data
# TODO: Implement finer measurement for polygon edges  *Done but lacking inch precision
# Idea for fine measurement: Right click to open close up grid for inch measurement or something

# TODONE: Add length readout for polygon edge
# TODO: Add ability to edit point location
# TODO: Add option to set a curve for points/edges  ***fuck this

def midpoint(x1, x2, y1, y2):
    """Returns middle point between point 1 and point 2"""
    return ((x1 + x2) / 2), ((y1 + y2) / 2)


def distance_point_to_point(point1, point2):
    """Returns the distance from point 1 to point 2"""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class FPGrid:
    def __init__(self, parent, height: int, width: int, columns: int, rows: int, fine_voxel: int):
        self.callback_y = 1
        self.callback_x = 1
        self.cur_text = None
        self.FINE_VOXEL = fine_voxel
        self.ROWS = rows * self.FINE_VOXEL
        self.COLS = columns * self.FINE_VOXEL
        self.CANVAS_HEIGHT = height
        self.CANVAS_WIDTH = width
        self.point = 1
        self.cursor_line = 1
        self.poly_points = []
        self.visual_points = []
        self.poly_lines = []
        self.col_width = self.CANVAS_WIDTH / self.COLS
        self.row_height = self.CANVAS_HEIGHT / self.ROWS

        # Create a grid of coordinates
        self.tiles = [[[c, r] for c in range(self.COLS)] for r in range(self.ROWS)]
        self.c = tk.Canvas(parent, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                           borderwidth=0, background='white')

        # Draw the grid on the canvas
        for y in range(int(self.ROWS / self.FINE_VOXEL) + 1):
            line_row = int(self.ROWS / self.FINE_VOXEL)
            self.c.create_line(0, int(y * (self.CANVAS_HEIGHT / line_row)) - ((self.CANVAS_HEIGHT / self.ROWS) / 2),
                               self.CANVAS_WIDTH,
                               int(y * (self.CANVAS_HEIGHT / line_row)) - ((self.CANVAS_HEIGHT / self.ROWS) / 2))
        for x in range(int(self.COLS / self.FINE_VOXEL) + 1):
            line_cols = int(self.COLS / self.FINE_VOXEL)
            self.c.create_line(int(x * (self.CANVAS_WIDTH / line_cols)) - ((self.CANVAS_WIDTH / self.COLS) / 2), 0,
                               int(x * (self.CANVAS_WIDTH / line_cols)) - ((self.CANVAS_WIDTH / self.COLS) / 2),
                               self.CANVAS_HEIGHT)
        self.c.grid(column=0, row=1)
        self.c.bind("<Button-1>", self.callback)
        self.c.bind("<Motion>", self.update_grid)

    def save_plot(self):
        with open("PlotData.json", "r+") as f:  # Open the json file containing floor plan data and city settings
            data = json.load(f)

        new_plot_index = len(data["CustomPlots"])
        data["CustomPlots"][new_plot_index] = self.poly_points

        with open("PlotData.json", "w+") as f:  # Store new JSON data
            json.dump(data, fp=f)

        self.clear_grid()

    def clear_grid(self):
        print("points = ", self.poly_points, "\nlines = ", self.poly_lines)

        for point in self.visual_points:
            self.c.delete(point)
        self.poly_points.clear()

        for line in self.poly_lines:
            self.c.delete(line[0])
            self.c.delete(line[1])
        self.poly_lines.clear()

        print("points = ", self.poly_points, "\nlines = ", self.poly_lines)
        self.c.delete(self.cur_text)
        self.c.delete(self.point)
        self.c.delete(self.cursor_line)
        self.c.delete()

    def add_grid_point(self, x: int, y: int):  # really???
        self.poly_points.append((x, y))

    def callback(self, event):

        # Logic for point creation
        point_is_clicked = event.x != self.callback_x and event.y != self.callback_y
        if point_is_clicked:
            col = int(self.callback_x / self.col_width)
            row = int(self.callback_y / self.row_height)
            do_pass = False
            for p in self.poly_points:  # checks if the end of polygon is connected to the start
                if (col, row) == p and self.poly_points.index(p) != 0:
                    do_pass = True                                    # GET RID OF THIS SHIT.  !FUCK!
                    tk.messagebox.showwarning(title="Open Plot Edge",
                                              message="Each point on the plot must be connected")
            if do_pass:
                pass
            else:
                yon_box1 = tk.messagebox.askyesno(title="Save Plot",
                                                  message="Would you like to save these plot dimensions?")
                if yon_box1:
                    self.save_plot()
                    return

        elif len(self.poly_points) <= 1:
            col = int(event.x / self.col_width)
            row = int(event.y / self.row_height)
            self.add_grid_point(col, row)

        else:
            do_pass = False
            col = int(event.x / self.col_width)
            row = int(event.y / self.row_height)
            for p in self.poly_points:
                if (col, row) == p:
                    do_pass = True
            if not do_pass:
                self.add_grid_point(col, row)

        # Create line from point to point
        for i in range(len(self.poly_points) - 1):
            p1x = self.poly_points[i][0] * self.row_height + (self.row_height / 2)
            p1y = self.poly_points[i][1] * self.col_width + (self.col_width / 2)
            p2x = self.poly_points[i + 1][0] * self.row_height + (self.row_height / 2)
            p2y = self.poly_points[i + 1][1] * self.col_width + (self.col_width / 2)
            text_pos = midpoint(p1x, p2x, p1y, p2y)
            length = round(distance_point_to_point((p1x, p1y), (p2x, p2y)) / self.row_height, 2)
            self.visual_points.append(self.c.create_oval(p1x-5, p1y-5, p1x+5, p1y+5, fill="blue"))  # This should be stored with self.poly_points, but I was lazy
            # Format distance output to feet/inches
            if length > 99.99:
                feet = str(length)[0:3]
                inch = int(str(length)[4:]) % 12
            elif length > 9.99:
                feet = str(length)[0:2]
                inch = int(str(length)[3:]) % 12
            else:
                feet = str(length)[0:1]
                inch = int(str(length)[2:]) % 12
            line = (self.c.create_line(p1x, p1y, p2x, p2y, fill="blue"),
                    self.c.create_text(text_pos, text=f"{feet} ft. {inch} in.")
                    )
            print("New line being added to 'poly_lines' is: ", line)
            self.poly_lines.append(line)

        # Create last visual point
        px = self.poly_points[-1][0] * self.row_height + (self.row_height / 2)
        py = self.poly_points[-1][1] * self.col_width + (self.col_width / 2)
        self.visual_points.append(self.c.create_oval(px - 5, py - 5, px + 5, py + 5, fill="blue"))

    def update_grid(self, event):

        # Bounds check for grid snap
        if event.x > self.CANVAS_WIDTH - 1:
            event.x = self.CANVAS_WIDTH - 1
        elif event.x < 1:
            event.x = 1
        if event.y > self.CANVAS_HEIGHT - 1:
            event.y = self.CANVAS_HEIGHT - 1
        elif event.y < self.row_height / 2:
            event.y = self.row_height / 2

        # Grid snapping for polygon point
        self.callback_x = event.x
        self.callback_y = event.y
        closest_x_point = int(event.x / self.col_width) * self.col_width - (self.col_width / 2) + self.col_width
        closest_y_point = int(event.y / self.row_height) * self.row_height - (self.row_height / 2) + self.row_height

        # Check poly points to snap to
        for i in self.poly_points[:-1]:
            snap_dist = 10
            if (event.x / self.col_width + snap_dist > i[0] > event.x / self.col_width - snap_dist
                    and event.y / self.col_width + snap_dist > i[1] > event.y / self.col_width - snap_dist):
                closest_x_point = i[0] * self.col_width - (self.col_width / 2) + self.col_width
                closest_y_point = i[1] * self.row_height - (self.row_height / 2) + self.row_height
                # Set callback x and y for new point creation
                self.callback_x = closest_x_point
                self.callback_y = closest_y_point
        self.c.delete(self.point)
        self.point = self.c.create_oval(closest_x_point - 3, closest_y_point - 3, closest_x_point + 3,
                                        closest_y_point + 3, fill="red")

        if not self.poly_points:
            pass
        else:
            self.c.delete(self.cursor_line)
            self.c.delete(self.cur_text)
            # Draw line to cursor and live length readout
            last_point = self.poly_points[-1]
            self.cursor_line = self.c.create_line(last_point[0] * self.row_height + (self.row_height / 2),
                                                  last_point[1] * self.col_width + (self.col_width / 2),
                                                  closest_x_point, closest_y_point, fill="red")

            p1x = self.poly_points[-1][0] * self.row_height + (self.row_height / 2)
            p1y = self.poly_points[-1][1] * self.col_width + (self.col_width / 2)
            length = float(round(distance_point_to_point((p1x, p1y), (closest_x_point, closest_y_point))
                           / self.row_height, 2))
            # Format distance output to feet/inches
            if length > 99.99:
                feet = str(length)[0:3]
                inch = int(str(length)[4:]) % 12
            elif length > 9.99:
                feet = str(length)[0:2]
                inch = int(str(length)[3:]) % 12
            else:
                feet = str(length)[0:1]
                inch = int(str(length)[2:]) % 12

            self.cur_text = self.c.create_text(event.x + 30, event.y - 15, text=f"{feet} ft. {inch} in.")


if __name__ == "__main__":
    # Create the window
    root = tk.Tk()
    FPGrid(root, 500, 500, 16, 16, 10)
    root.mainloop()
