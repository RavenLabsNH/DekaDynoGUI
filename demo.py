"""
demo.py

Copyright © 2022 Raven Labs
Manchester, New Hampshire
www.ravenlabsnh.com

"""

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()
dpg.create_viewport(title='Demo', width=900, height=900)

demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()