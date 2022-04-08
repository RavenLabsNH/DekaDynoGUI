"""
original_dyno.py

Copyright © 2022 Raven Labs
Manchester, New Hampshire
www.ravenlabsnh.com

"""

import dearpygui.dearpygui as dpg
import multiprocessing as mp
from math import sin
import random

dpg.create_context()


def update_plot_data(plot_data, q):
    """
    Updates the acoustic plot with the number randomly generated by a separate python process
    :param plot_data: the array of values we are using to as a data source for the acoustic plot
    :param q: The queue the other python process is adding random numbers to
    :return:
    """
    if q.qsize() > 0:
        if len(plot_data) > 100:
            plot_data.pop(0)
        t = q.get()
        plot_data.append(sin(t / 30))
        dpg.set_value("plot", plot_data)


def generate_random_number(q):
    """
    Running as a separate python process, randomly generate numbers and add it queue
    :param q: The queue to add the random numbers to that other python processes can access.
    :return:
    """
    while (True):
        q.put(random.randint(1, 100))


def change_view(sender, app_data, user_data):
    """
    Change the main view of the application
    :param sender: sender event args
    :param app_data: app data event args
    :param user_data: page to switch to
    :return:
    """
    dpg.configure_item("help_page", show=False)
    dpg.configure_item("home_page", show=False)
    dpg.configure_item("rpm_page", show=False)
    dpg.configure_item("sound_page", show=False)
    dpg.configure_item(user_data, show=True)

if __name__ == '__main__':
    data = []

    # Add a font registry
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        title_font = dpg.add_font("fonts/Sans.TTF", 86)
        primary_font = dpg.add_font("fonts/Sans.TTF", 41)

    # Add images by creating textures
    with dpg.texture_registry():
        width, height, channels, data2 = dpg.load_image("content/home.png")
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
        dpg.add_static_texture(width, height, data2, tag="matplotlib")

    # Main Window
    with dpg.window(tag="Dyno", width=900, height=1080):
        dpg.bind_font(primary_font)
        with dpg.child_window(autosize_x=True, autosize_y=True, border=False):
            # Header
            with dpg.group(horizontal=True, indent=150):
                title = dpg.add_text("Dyno Cluster Tester")
                dpg.bind_item_font(title, title_font)
            dpg.add_separator()

            # Body
            with dpg.group(horizontal=True):
                # Left menu bar
                with dpg.child_window(width=120, autosize_y=True, border=True):
                    dpg.add_spacer(height=2)
                    dpg.add_image_button("home_icon", callback=change_view, user_data="home_page")
                    dpg.add_spacer(height=2)
                    dpg.add_spacer(height=2)
                    dpg.add_image_button("speed_icon", callback=change_view, user_data="rpm_page")
                    dpg.add_spacer(height=2)
                    dpg.add_spacer(height=2)
                    dpg.add_image_button("sound_icon", callback=change_view, user_data="sound_page")
                    dpg.add_spacer(height=2)
                    dpg.add_spacer(height=2)
                    dpg.add_image_button("help_icon", callback=change_view, user_data="help_page")
                    dpg.add_spacer(height=2)

                # Main Body
                # Home Page
                with dpg.child_window(width=1480, autosize_y=True, show=True, tag="home_page", border=False):
                    with dpg.group(horizontal=True, horizontal_spacing=10, pos=[100, 50]):
                        dpg.add_text("Enter Serial Number")
                        dpg.add_input_text(width=400)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Start Acoustics Test", width=400, height=70, pos=[50, 150],
                                       callback=change_view, user_data="sound_page")
                        dpg.add_button(label="Start Break In Cycle", width=400, height=70, pos=[500, 150],
                                       callback=change_view, user_data="rpm_page")
                # RPM Page
                with dpg.child_window(width=1480, autosize_y=True, show=False, tag="rpm_page", border=False):
                    dpg.add_image("matplotlib", pos=[-100, -150])
                # Sound Page
                with dpg.child_window(width=1480, autosize_y=True, show=False, tag="sound_page", border=False):
                    dpg.add_simple_plot(min_scale=-1.0, max_scale=1.0, height=350, width=1000, tag="plot")
                # Help Page
                with dpg.child_window(width=1480, autosize_y=True, show=False, tag="help_page", border=False):
                    dpg.add_image("raven-logo1", pos=[200, 100])

    # Start a new python process to generate random numbers
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=generate_random_number, args=(q,))
    p.start()

    dpg.create_viewport(title='Deka Dyno', width=1500, height=975)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_primary_window("Dyno", True)

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        update_plot_data(data, q)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()