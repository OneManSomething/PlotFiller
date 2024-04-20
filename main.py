from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
# from PIL import Image
# from grid import FPGrid
from math import floor
import json
from CTkToolTip import CTkToolTip

# # Minimum Viable Product:
# TODO: Add floor plans
# TODO: Delete floor plans
# TODONE: Edit floor plans

# ### After MVP uncomment 229-237 & 332-341 &  247-248 & 285-286 ###
# ### And reimport FPGrid ###

# # Extra Features:
# TODO: Add custom plot options
# TODONE: Hide rectangle plot options
# TODO: Beautify output, objectify the floor plans, ?add images?
# TODO: ***Implement math for grid system geometry collision checking***   <GET IT OVER WITH PUSSY
# TODO: Export results                          *not necessary
# TODONE: Implement output frame
# TODONE: Check plot validity for basic rectangular plots
# TODONE: Add input for setback distance / per city

TEXT_COLOR = "white"
BUTTON_COLOR = "#5BB68B"
APP_BG_COLOR = "#344049"
FRAME_BG_COLOR = "#557084"


class PlotWindow(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.CORNER_RAD = parent.CORNER_RAD
        self.X_PAD = parent.X_PAD
        self.Y_PAD = parent.Y_PAD
        self.configure(height=300, width=200, fg_color=FRAME_BG_COLOR)
        self.grid(column=0, row=0, pady=self.Y_PAD, padx=self.X_PAD, sticky=tk.NSEW)


class FloorPlanWindow(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.edit_floor_plan_modules = None
        self.floor_plan_name = None
        self.parent = parent
        self.CORNER_RAD = parent.CORNER_RAD
        self.X_PAD = parent.X_PAD
        self.Y_PAD = parent.Y_PAD
        self.configure(height=300, width=200, fg_color=FRAME_BG_COLOR)
        self.grid(column=0, row=0, pady=self.Y_PAD, padx=self.X_PAD, sticky=tk.NSEW)

        with open("FloorPlans.json", "r+") as f:  # Open the json file containing floor plan data and city settings
            self.data = json.load(f)

        floor_plans = self.data["FloorPlans"]
        i = 1
        j = 1
        self.foo_list = []
        for plan in floor_plans:
            i += 1
            j += 1
            foo = (ctk.CTkButton(master=self, corner_radius=self.CORNER_RAD,
                                 width=50, height=20, text=plan,
                                 text_color=TEXT_COLOR), plan)
            foo[0].grid(column=(j % 2), row=floor(i/2), padx=self.X_PAD, pady=self.Y_PAD)
            foo[0].configure(command=lambda c=foo: self.edit_floor_plan(floor_plan=c))
            self.foo_list.append(foo)

    def edit_floor_plan(self, floor_plan):
        self.floor_plan_name = floor_plan[1]
        floor_plan_width = self.data["FloorPlans"][self.floor_plan_name][0]
        floor_plan_length = self.data["FloorPlans"][self.floor_plan_name][1]
        self.edit_floor_plan_modules = []
        for foo in self.foo_list:
            foo[0].grid_remove()
        width_entry = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=50, height=20)
        width_entry.grid(column=1, row=1, pady=self.Y_PAD, padx=self.X_PAD)
        width_entry_text = ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD,
                                        width=50, height=20, text="Width",
                                        text_color=TEXT_COLOR)
        width_entry_text.grid(column=0, row=1, pady=self.Y_PAD, padx=self.X_PAD)
        width_entry.insert(0, floor_plan_width)
        length_entry = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=50, height=20)
        length_entry.grid(column=1, row=2, pady=self.Y_PAD, padx=self.X_PAD)
        length_entry_text = ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD,
                                         width=50, height=20, text="length",
                                         text_color=TEXT_COLOR)
        length_entry_text.grid(column=0, row=2, pady=self.Y_PAD, padx=self.X_PAD)
        length_entry.insert(0, floor_plan_length)
        save_changes = ctk.CTkButton(master=self, corner_radius=self.CORNER_RAD,
                                     width=50, height=20, text="Save Changes",
                                     text_color=TEXT_COLOR, command=self.save_changes)
        save_changes.grid(column=0, row=3, pady=self.Y_PAD, padx=self.X_PAD)
        cancel_changes = ctk.CTkButton(master=self, corner_radius=self.CORNER_RAD,
                                       width=50, height=20, text="Cancel",
                                       text_color=TEXT_COLOR, command=self.cancel_changes)
        cancel_changes.grid(column=1, row=3, pady=self.Y_PAD, padx=self.X_PAD)
        self.edit_floor_plan_modules.append((cancel_changes, save_changes, length_entry,
                                             length_entry_text, width_entry_text, width_entry))

    def save_changes(self):
        new_length = int(self.edit_floor_plan_modules[0][2].get())
        new_width = int(self.edit_floor_plan_modules[0][5].get())

        with open("FloorPlans.json", "r+") as f:  # Open floor plan data/city settings .json
            self.data = json.load(f)

        self.data["FloorPlans"][self.floor_plan_name] = [new_width, new_length]

        with open("FloorPlans.json", "w+") as f:  # Open floor plan data/city settings .json
            json.dump(self.data, fp=f)

        for thing in self.edit_floor_plan_modules[0]:
            thing.destroy()
        for foo in self.foo_list:
            foo[0].grid()
            
    def cancel_changes(self):
        for thing in self.edit_floor_plan_modules[0]:
            thing.destroy()
        for foo in self.foo_list:
            foo[0].grid()


class CitySettings(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.CORNER_RAD = parent.CORNER_RAD
        self.X_PAD = parent.X_PAD
        self.Y_PAD = parent.Y_PAD
        self.configure(height=300, width=200, fg_color=FRAME_BG_COLOR)
        self.grid(column=0, row=0, pady=self.Y_PAD, padx=self.X_PAD, sticky=tk.NSEW)

        with open("FloorPlans.json", "r+") as f:  # Open the json file containing floor plan data and city settings
            self.data = json.load(f)

        self.cities = list(self.data["Cities"].keys())
        self.default_city = tk.StringVar()
        self.city_selection = ctk.CTkComboBox(master=self, values=self.cities, command=self.update_entries)
        self.city_selection.grid(columnspan=2, column=0, row=0, pady=self.Y_PAD, padx=self.X_PAD)
        self.current_city = self.city_selection.get()
        self.city_side_setback_entry = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=50, height=20)
        self.city_side_setback_entry.grid(column=1, row=1, pady=self.Y_PAD, padx=self.X_PAD)
        self.city_side_setback_entry_text = (ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD,
                                                          width=50, height=20, text="Front Setback",
                                                          text_color=TEXT_COLOR)
                                             .grid(column=0, row=1, pady=self.Y_PAD, padx=self.X_PAD))
        self.city_front_setback_entry = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=50, height=20)
        self.city_front_setback_entry.grid(column=1, row=2, pady=self.Y_PAD, padx=self.X_PAD)
        self.city_front_setback_entry_text = (ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD,
                                                           width=50, height=20, text="Side Setback",
                                                           text_color=TEXT_COLOR)
                                              .grid(column=0, row=2, pady=self.Y_PAD, padx=self.X_PAD))
        self.city_rear_setback_entry = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=50, height=20)
        self.city_rear_setback_entry.grid(column=1, row=3, pady=self.Y_PAD, padx=self.X_PAD)
        self.city_rear_setback_entry_text = (ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD,
                                                          width=50, height=20, text="Rear Setback",
                                                          text_color=TEXT_COLOR)
                                             .grid(column=0, row=3, pady=self.Y_PAD, padx=self.X_PAD))
        self.city_flanking_side_setback_entry = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD,
                                                             width=50, height=20)
        self.city_flanking_side_setback_entry.grid(column=1, row=4, pady=self.Y_PAD, padx=self.X_PAD)
        self.city_flanking_side_setback_entry_text = (ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD,
                                                                   text_color=TEXT_COLOR,
                                                                   width=50, height=20, text="Flanking Side Setback")
                                                      .grid(column=0, row=4, pady=self.Y_PAD, padx=self.X_PAD))

        self.save_city_settings = ctk.CTkButton(master=self, corner_radius=self.CORNER_RAD, width=100, height=30,
                                                text="Save Setback Settings", command=self.save_city_settings)
        self.save_city_settings.grid(columnspan=2, column=0, row=5, pady=self.Y_PAD, padx=self.X_PAD)
        CTkToolTip(self.save_city_settings, message="No Fields are to be left empty", follow=True)
        self.update_entries()

    def update_entries(self, *args):
        self.current_city = self.city_selection.get()
        self.city_side_setback_entry.delete(first_index=0, last_index=tk.END)
        self.city_side_setback_entry.insert(0, self.data["Cities"][self.current_city][0])
        self.city_front_setback_entry.delete(first_index=0, last_index=tk.END)
        self.city_front_setback_entry.insert(0, self.data["Cities"][self.current_city][1])
        self.city_rear_setback_entry.delete(first_index=0, last_index=tk.END)
        self.city_rear_setback_entry.insert(0, self.data["Cities"][self.current_city][2])
        self.city_flanking_side_setback_entry.delete(first_index=0, last_index=tk.END)
        self.city_flanking_side_setback_entry.insert(0, self.data["Cities"][self.current_city][3])

    def add_city(self):
        new_city = self.city_selection.get()
        print(new_city.isprintable())
        if new_city.isprintable():
            with open("FloorPlans.json", "r+") as f:  # Open the json file containing floor plan data and city settings
                data = json.load(f)

            data["Cities"][new_city] = [self.city_side_setback_entry.get(),  # Get entry data/add new city to json data
                                        self.city_front_setback_entry.get(),
                                        self.city_rear_setback_entry.get(),
                                        self.city_flanking_side_setback_entry.get()]

            with open("FloorPlans.json", "w+") as f:  # Store new JSON data
                json.dump(data, fp=f)
        else:
            tk.messagebox.showinfo(message="Please do not include any non-printable characters when adding a city name")

    def save_city_settings(self):

        with open("FloorPlans.json", "r+") as f:  # Open the json file containing floor plan data and city settings
            data = json.load(f)

        try:  # Check for empty fields
            ssb = self.city_side_setback_entry.get()
            fsb = self.city_front_setback_entry.get()
            rsb = self.city_rear_setback_entry.get()
            fssb = self.city_flanking_side_setback_entry.get()
            sb = [fsb, ssb, rsb, fssb]
            for v in sb:
                if len(v) <= 0 or not v.isdigit():
                    raise Exception("Invalid Field")
        except Exception as e:
            tk.messagebox.showwarning(title="Invalid Entry",
                                      message=f"{e}\nPlease enter a number into each field before saving.")
        else:
            self.current_city = self.city_selection.get()
            data["Cities"][self.current_city] = [ssb, fsb, rsb, fssb]
            with open("FloorPlans.json", "w+") as f:  # Save new data to json file
                json.dump(data, f)


class OutputFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.CORNER_RAD = parent.CORNER_RAD
        self.X_PAD = parent.X_PAD
        self.Y_PAD = parent.Y_PAD
        self.TEXTCOLOR = TEXT_COLOR
        self.BUTTON_COLOR = BUTTON_COLOR
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(fg_color=FRAME_BG_COLOR, corner_radius=self.CORNER_RAD)
        self.grid(column=0, row=0, sticky=tk.NSEW, padx=parent.X_PAD, pady=parent.Y_PAD)
        self.output_msg_box = ctk.CTkTextbox(master=self, width=100, height=200, corner_radius=self.CORNER_RAD,
                                             fg_color=FRAME_BG_COLOR, wrap="word", text_color=TEXT_COLOR,
                                             font=("Arial CE", 20))
        self.output_msg_box.grid(column=0, row=0, sticky=tk.NSEW, padx=self.X_PAD)

    def output_set(self, output: (str, list)):
        """Displays 'output' to output textbox"""
        self.output_msg_box.delete(0.0, tk.END)
        self.output_msg_box.insert(0.0, output)


class CustomPlotSpecFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.CORNER_RAD = parent.CORNER_RAD
        self.X_PAD = parent.X_PAD
        self.Y_PAD = parent.Y_PAD
        self.TEXTCOLOR = TEXT_COLOR
        self.BUTTON_COLOR = BUTTON_COLOR
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(fg_color=FRAME_BG_COLOR, corner_radius=self.CORNER_RAD)
        self.grid(column=0, row=0, sticky=tk.NSEW, padx=parent.X_PAD, pady=parent.Y_PAD)


class PlotSpecFrame(ctk.CTkFrame):
    """The area of the application in which you specify the plot dimensions and attributes"""

    def __init__(self, parent, output_frame: OutputFrame, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.CORNER_RAD = parent.CORNER_RAD
        self.X_PAD = parent.X_PAD
        self.Y_PAD = parent.Y_PAD
        self.TEXTCOLOR = TEXT_COLOR
        self.BUTTON_COLOR = BUTTON_COLOR
        self.parent = parent
        self.output_frame = output_frame
        self.configure(fg_color=FRAME_BG_COLOR)
        self.grid(column=0, row=0, sticky=tk.NSEW, padx=parent.X_PAD, pady=parent.Y_PAD)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        with open("FloorPlans.json", "r+") as f:  # Open the json file containing floor plan data and city settings
            self.data = json.load(f)

        # Width entry
        self.pwe_text = ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD, width=60, text="Plot width (Feet): ",
                                     text_color=self.TEXTCOLOR)
        self.pwe_text.grid(column=0, row=1, sticky=tk.E)
        self.plot_width = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=60, placeholder_text="0")
        self.plot_width.grid(column=1, row=1, sticky=tk.W)

        # Length entry
        self.ple_text = ctk.CTkLabel(master=self, corner_radius=self.CORNER_RAD, width=60, pady=self.Y_PAD,
                                     text="Plot length (Feet): ", text_color=self.TEXTCOLOR)
        self.ple_text.grid(column=0, row=2, sticky=tk.E)
        self.plot_length = ctk.CTkEntry(master=self, corner_radius=self.CORNER_RAD, width=60, placeholder_text="0")
        self.plot_length.grid(column=1, row=2, sticky=tk.W)

        # City Selection
        self.cities = list(self.data["Cities"].keys())
        self.default_city = tk.StringVar()
        self.default_city.set("Select a city...")
        self.city_selection = ctk.CTkComboBox(self, values=self.cities)
        self.city_selection.grid(columnspan=2, column=0, row=3)

        # Plot type selection
        #
        # self.radio_state = ctk.IntVar(value=1)
        # self.plot_type_R_radio = ctk.CTkRadioButton(master=self, text="Rectangle", text_color=TEXT_COLOR,
        #                                             variable=self.radio_state, value=1, command=parent.sel)
        # self.plot_type_R_radio.grid(column=0, row=0)
        #
        # self.plot_type_C_radio = ctk.CTkRadioButton(master=self, text="Custom", text_color=TEXT_COLOR,
        #                                             variable=self.radio_state, value=2, command=parent.sel)
        # self.plot_type_C_radio.grid(column=1, row=0)

        # Check valid floor plans Button
        self.check_fp = ctk.CTkButton(self, width=200, text="Check Valid Floor Plans", command=self.calc_floor_plans,
                                      text_color=self.TEXTCOLOR, fg_color=self.BUTTON_COLOR)
        self.check_fp.grid(column=0, columnspan=4, row=4, pady=self.Y_PAD)

    def calc_floor_plans(self):
        """The method which takes the plot specifications and returns a list of valid floor plans"""
        valid_fp: list = []
        # # plot_type = self.radio_state.get()
        # if plot_type == 1:
        try:
            width: int = int(self.plot_width.get())
            length: int = int(self.plot_length.get())

        except Exception as e:
            print(f"Error: {e}\n Likely no values were put into width/length entry.")

        else:
            city = self.city_selection.get()

            with open("FloorPlans.json", "r+") as f:
                data = json.load(f)

            try:

                side_setback = int(data["Cities"][city][0])
                front_setback = int(data["Cities"][city][1])
                rear_setback = int(data["Cities"][city][2])
                flanking_side_setback = int(data["Cities"][city][3])

            except Exception as e:
                print(f"Error: {e} not found in json file, using default values.")
                side_setback = 10
                front_setback = 25
                rear_setback = 25
                flanking_side_setback = 15

            max_width = width - (side_setback * 2)
            max_length = length - rear_setback - front_setback

            for i in data["FloorPlans"]:
                if int(data["FloorPlans"][i][0]) < max_width and int(data["FloorPlans"][i][1]) < max_length:
                    valid_fp.append(f"{i} {data['FloorPlans'][i][0]}x{data['FloorPlans'][i][1]}\n")

            # Send the valid floor plans to the output frame
            self.output_frame.output_set(output=valid_fp)
            # elif plot_type == 2:
            #     print("Maybe something fits in there IDK I didn't write the code for this yet")


class MainApplication(tk.Tk):
    """The main application class, all primary windows and widgets should initialize through this class"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Main window setup
        self.floor_plan_window = None
        self.plot_list_window = None
        self.customplot = None
        self.city_conf_window = None
        self.CORNER_RAD = 5
        self.X_PAD = 5
        self.Y_PAD = 5
        self.configure(width=400, height=500, padx=1, pady=1, bg=APP_BG_COLOR)
        self.minsize(width=275, height=500)
        self.title("Plot-Filler")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)

        # Initialize plot spec and output frames
        self.output_frame = OutputFrame(parent=self, width=300, height=200, corner_radius=self.CORNER_RAD)
        self.output_frame.grid(columnspan=2, column=0, row=1, sticky=tk.NSEW)
        self.plot_spec_frame = PlotSpecFrame(parent=self, output_frame=self.output_frame, width=300,
                                             height=200, corner_radius=self.CORNER_RAD)
        self.plot_spec_frame.grid(column=0, row=0, sticky=tk.NSEW)

        # Top menu bar
        self.mainMenu = tk.Menu(master=self)
        self.mainMenu.add_command(label="City Settings", command=lambda: self.menu_controller(1))
        self.mainMenu.add_command(label="Plots", command=lambda: self.menu_controller(2))
        self.mainMenu.add_command(label="Floor Plans", command=lambda: self.menu_controller(3))
        self.mainMenu.add_command(label="Exit", command=self.destroy)
        self.config(menu=self.mainMenu)

    def sel(self):
        """Runs when the radio button for plot type is pressed"""
        state = self.plot_spec_frame.radio_state.get()
        if state == 1:                                  # Set UI to the rectangle plot input
            self.plot_spec_frame.plot_width.grid()
            self.plot_spec_frame.pwe_text.grid()
            self.plot_spec_frame.plot_length.grid()
            self.plot_spec_frame.ple_text.grid()
            self.plot_spec_frame.city_selection.grid()
            self.plot_spec_frame.check_fp.grid()
            self.customplot.c.grid_remove()
        # if state == 2:                                  # Set UI to the custom plot input
        #     self.customplot = FPGrid(parent=self, height=500, width=500, columns=15, rows=15, fine_voxel=10)
        #     self.customplot.c.grid(column=0, row=1, sticky=tk.NSEW)
        #     self.plot_spec_frame.plot_width.grid_remove()
        #     self.plot_spec_frame.pwe_text.grid_remove()
        #     self.plot_spec_frame.plot_length.grid_remove()
        #     self.plot_spec_frame.ple_text.grid_remove()
        #     self.plot_spec_frame.city_selection.grid_remove()
        #     self.plot_spec_frame.check_fp.grid_remove()
        #     self.plot_spec_frame.configure(height=10)
        else:
            self.plot_spec_frame.radio_state.set(value=1)

    def menu_controller(self, menu: int):
        def grid_main_app_frame():
            self.rowconfigure(1, weight=2)
            self.output_frame.grid(column=0, row=1, sticky=tk.NSEW, padx=self.X_PAD,
                                   pady=self.Y_PAD)
            self.plot_spec_frame.grid(column=0, row=0, sticky=tk.NSEW, padx=self.X_PAD,
                                      pady=self.Y_PAD)
        match menu:
            case 1:
                if (self.plot_spec_frame.winfo_ismapped(), self.output_frame.winfo_ismapped()) != (1, 1):
                    self.city_conf_window.grid_remove()
                    grid_main_app_frame()

                else:
                    self.plot_spec_frame.grid_remove()
                    self.output_frame.grid_remove()
                    self.rowconfigure(1, weight=0)
                    try:
                        self.city_conf_window.grid()
                    except AttributeError:
                        self.city_conf_window = CitySettings(self)
            case 2:
                if (self.plot_spec_frame.winfo_ismapped(), self.output_frame.winfo_ismapped()) != (1, 1):
                    self.plot_list_window.grid_remove()
                    grid_main_app_frame()
                else:
                    self.plot_spec_frame.grid_remove()
                    self.output_frame.grid_remove()
                    self.rowconfigure(1, weight=0)
                    try:
                        self.plot_list_window.grid()
                    except AttributeError:
                        self.plot_list_window = PlotWindow(self)
            case 3:
                if (self.plot_spec_frame.winfo_ismapped(), self.output_frame.winfo_ismapped()) != (1, 1):
                    self.floor_plan_window.grid_remove()
                    grid_main_app_frame()

                else:
                    self.plot_spec_frame.grid_remove()
                    self.output_frame.grid_remove()
                    self.rowconfigure(1, weight=0)
                    try:
                        self.floor_plan_window.grid()
                    except AttributeError:
                        self.floor_plan_window = FloorPlanWindow(self)
            case _:
                pass


if __name__ == "__main__":
    root = MainApplication()
    root.update()
    root.mainloop()
