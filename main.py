"""
main.py

Copyright © 2022 Raven Labs
Manchester, New Hampshire
www.ravenlabsnh.com

"""

import dearpygui.dearpygui as dpg
import multiprocessing as mp
from math import sin, cos
import random

import matplot as mpl

dpg.create_context()


def update_plot_data(plot_data, q):
    if q.qsize() > 1:
        if len(plot_data) > 100:
            plot_data.pop(0)
        t = q.get()
        plot_data.append(sin(t / 30))
        #dpg.set_value("plot2", plot_data)
        #dpg.set_value("plot1", plot_data)

def generate_random_number(q):
    while(True):
        #print("generate")
        q.put(random.randint(1,100))

def change_view_home():
    dpg.configure_item("home_page", show=True)
    dpg.configure_item("test_page", show=False)
    dpg.configure_item("sound_page", show=False)
    dpg.configure_item("help_page", show=False)

def change_view_test():
    dpg.configure_item("test_page", show=True)
    dpg.configure_item("home_page", show=False)
    dpg.configure_item("sound_page", show=False)
    dpg.configure_item("help_page", show=False)

def change_view_sound():
    dpg.configure_item("sound_page", show=True)
    dpg.configure_item("home_page", show=False)
    dpg.configure_item("test_page", show=False)
    dpg.configure_item("help_page", show=False)

def change_view_help():
    dpg.configure_item("help_page", show=True)
    dpg.configure_item("home_page", show=False)
    dpg.configure_item("test_page", show=False)
    dpg.configure_item("sound_page", show=False)


if __name__ == '__main__':
    data = []

    mpl.generate()


    # add a font registry
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        title_font = dpg.add_font("fonts/Sans.TTF", 57)
        second_font = dpg.add_font("fonts/Sans.TTF", 27)


    with dpg.texture_registry():
        width, height, channels, data2 = dpg.load_image("content/Home.png")
        dpg.add_static_texture(width, height, data2, tag="home_icon")
        width, height, channels, data2 = dpg.load_image("content/settings.png")
        dpg.add_static_texture(width, height, data2, tag="settings_icon")
        width, height, channels, data2 = dpg.load_image("content/speed.png")
        dpg.add_static_texture(width, height, data2, tag="speed_icon")
        width, height, channels, data2 = dpg.load_image("content/help.png")
        dpg.add_static_texture(width, height, data2, tag="help_icon")
        width, height, channels, data2 = dpg.load_image("content/sonometer.png")
        dpg.add_static_texture(width, height, data2, tag="sound_icon")
        width, height, channels, data2 = dpg.load_image("content/RavenLabs/Raven_Labs_Logo-White-4.png")
        dpg.add_static_texture(width, height, data2, tag="raven-logo1")
        width, height, channels, data2 = dpg.load_image("content/matplotlib.png")
        dpg.add_static_texture(width, height, data2, tag="chart")
    sindatax = []
    sindatay = []
    cosdatay = []
    for i in range(100):
        sindatax.append(i / 100)
        sindatay.append(0.5 + 0.5 * sin(50 * i / 100))
        cosdatay.append(0.5 + 0.75 * cos(50 * i / 100))


    with dpg.window(tag="Dyno", width=900, height=1080):

        dpg.bind_font(second_font)
        with dpg.child_window(autosize_x=True, autosize_y=True, border=False):
            with dpg.child_window(autosize_x=True, height=900):
                with dpg.group(horizontal=True, indent=150):
                    title = dpg.add_text("Dyno Cluster Tester")
                    dpg.bind_item_font(title, title_font)
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=120, autosize_y=True, border=True):
                        dpg.add_spacer(height=2)
                        dpg.add_image_button("home_icon", callback=change_view_home)
                        dpg.add_spacer(height=2)
                        #dpg.add_separator()
                        dpg.add_spacer(height=2)
                        dpg.add_image_button("speed_icon", callback=change_view_test)
                        dpg.add_spacer(height=2)
                        #dpg.add_separator()
                        dpg.add_spacer(height=2)
                        dpg.add_image_button("sound_icon", callback=change_view_sound)
                        dpg.add_spacer(height=2)
                        #dpg.add_separator()
                        dpg.add_spacer(height=2)
                        dpg.add_image_button("help_icon", callback=change_view_help)
                        dpg.add_spacer(height=2)
                    with dpg.child_window(width=1480, autosize_y=True, show=True, tag="home_page", border=False):
                        with dpg.group(horizontal=True, horizontal_spacing=10, pos=[100,50]):
                            dpg.add_text("Enter Serial Number   ")
                            dpg.add_input_text(width=400)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Start Acoustics Test", width=400, height=70, pos=[50,150], callback=change_view_sound)
                            dpg.add_button(label="Start Break In Cycle", width=400, height=70, pos=[500,150], callback=change_view_test)
                    with dpg.child_window(width=1480, autosize_y=True, show=False, tag="test_page", border=False):
                        with dpg.plot(label="Cluster RPM Output", height=600, width=1300):
                            dpg.add_plot_axis(dpg.mvXAxis, label="x")

                            with dpg.plot_axis(dpg.mvYAxis, label="y"):
                                # series belong to a y axis
                                dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)")
                    with dpg.child_window(width=1480, autosize_y=True, show=False, tag="sound_page", border=False):
                        #dpg.add_simple_plot(min_scale=-1.0, max_scale=1.0, height=350, width=1000, tag="plot2")
                        dpg.add_image("chart", pos=[-100,-150])
                    with dpg.child_window(width=1480, autosize_y=True, show=False, tag="help_page", border=False):
                        dpg.add_image("raven-logo1", pos=[200,100])


    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=generate_random_number, args=(q,))
    p.start()

    dpg.create_viewport(title='Deka Dyno', width=1500, height=975)
    dpg.setup_dearpygui()
    dpg.set_global_font_scale(1.5)
    dpg.show_viewport()

    dpg.set_primary_window("Dyno", True)

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        update_plot_data(data, q)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

