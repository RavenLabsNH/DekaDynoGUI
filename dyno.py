import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    title_font = dpg.add_font("fonts/Sans.TTF", 86)
    home_font = dpg.add_font("fonts/Sans.TTF", 41)
    chart_font = dpg.add_font("fonts/Sans.TTF", 22)

with dpg.window(tag="Dyno", width=2560, height=1440):
    with dpg.group(horizontal=True, indent=150):
        dpg.add_combo(["Accostic", "Breakin"], tag="combo")
        dpg.add_input_text(hint="Enter the work order number", tag="work_order")

    # with dpg.group(horizontal=True):
    #     with dpg.child_window(height=40, width=150):
    #         dpg.add_text("140")
    #     with dpg.child_window(height=40, width=150):
    #         dpg.add_text("140")
    #     with dpg.child_window(height=40, width=150):
    #         dpg.add_text("140")

    with dpg.table(header_row=False):
        dpg.add_table_column(init_width_or_weight=3)
        dpg.add_table_column(init_width_or_weight=1)
        dpg.add_table_column(init_width_or_weight=3)
        dpg.add_table_column(init_width_or_weight=1)
        dpg.add_table_column(init_width_or_weight=3)
        dpg.add_table_column(init_width_or_weight=1)
        dpg.add_table_column(init_width_or_weight=3)
        with dpg.table_row():
            dpg.add_text("")
            with dpg.child_window(width=50, height=50):
                dpg.add_text("140")
            dpg.add_text("")
            dpg.add_text("140")
            dpg.add_text("")
            dpg.add_text("140")
            dpg.add_text("")


if __name__ == '__main__':
    dpg.create_viewport(title='Deka Dyno', width=2560, height=1440, x_pos=0, y_pos=0)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_primary_window("Dyno", True)

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()