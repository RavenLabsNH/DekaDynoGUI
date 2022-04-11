import dearpygui.dearpygui as dpg
import multiprocessing as mp
from ctypes import c_bool
import time

from audio import Recorder

class DynoGUI():
    def __init__(self, config):
        self.config = config
        dpg.create_context()
        mp.set_start_method('spawn')
        self.time_fft_q = mp.Queue()
        self.data_fft_q = mp.Queue()
        self.flag = mp.Value(c_bool, False)
        self.profile_names = []
        self.test_sequence = []

        #To Be Deleted
        self.last_time = 0
        self.time_x_axis = []
        self.fake_rpm_data = []
        self.index = 0


    def create_page(self):
        for profile in self.config["profiles"]:
            self.profile_names.append(profile['name'])

        with dpg.font_registry():
            # first argument ids the path to the .ttf or .otf file
            font_regular_12 = dpg.add_font("fonts/Inter-Regular.ttf", 14)
            font_regular_14 = dpg.add_font("fonts/Inter-Regular.ttf", 18)
            font_regular_16 = dpg.add_font("fonts/Inter-Regular.ttf", 22)
            font_regular_18 = dpg.add_font("fonts/Inter-Regular.ttf", 32)
            font_regular_24 = dpg.add_font("fonts/Inter-Regular.ttf", 36)
            font_regular_40 = dpg.add_font("fonts/Inter-Regular.ttf", 44)

        with dpg.theme() as rpm_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (26, 30, 32), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (36, 40, 42), category=dpg.mvThemeCat_Core)

                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 8, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)

                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)

        with dpg.theme() as pause_button_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (76, 172, 234), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (76, 172, 234), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)

        with dpg.theme() as stop_button_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (249, 122, 94), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (249, 122, 94), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)

        with dpg.theme() as input_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 7, 9, category=dpg.mvThemeCat_Core)

        with dpg.window(tag="Dyno", width=1440, height=1024) as window:
            # Title
            dpg.add_text("Gearbox Dyno", pos=[40, 40])
            dpg.bind_item_font(dpg.last_item(), font_regular_24)

            # Input & Controls
            dpg.add_text("Profile", pos=[51, 96])
            dpg.bind_item_font(dpg.last_item(), font_regular_12)
            dpg.add_combo(self.profile_names, pos=[40, 116], width=429, default_value="Acoustic", tag="profile_combo")
            dpg.bind_item_font("profile_combo", font_regular_16)
            dpg.bind_item_theme(dpg.last_item(), input_theme)

            dpg.add_text("Work Order Number", pos=[516, 96])
            dpg.bind_item_font(dpg.last_item(), font_regular_12)
            dpg.add_input_text(hint="Enter the work order number", pos=[505, 116], width=430, height=40,
                               tag="work_order")
            dpg.bind_item_font("work_order", font_regular_16)
            dpg.bind_item_theme(dpg.last_item(), input_theme)

            dpg.add_button(label="Start", width=429, height=40, pos=[971, 116], show=True, tag="start_button",
                           callback=self.start_test)
            dpg.bind_item_font(dpg.last_item(), font_regular_14)
            # dpg.bind_item_theme(dpg.last_item(), pause_button_theme)

            dpg.add_button(label="Pause", width=202, height=40, pos=[971, 116], show=False, tag="pause_button",
                           callback=self.pause_test)
            dpg.bind_item_font(dpg.last_item(), font_regular_14)
            dpg.bind_item_theme(dpg.last_item(), pause_button_theme)

            dpg.add_button(label="Stop", width=202, height=40, pos=[1198, 116], show=False, tag="stop_button",
                           callback=self.stop_test)
            dpg.bind_item_font(dpg.last_item(), font_regular_14)
            dpg.bind_item_theme(dpg.last_item(), stop_button_theme)

            with dpg.child_window(height=136, width=429, pos=[40, 196]):
                dpg.add_text("RPM", pos=[170, 17])
                dpg.bind_item_font(dpg.last_item(), font_regular_16)
                dpg.add_text("140", pos=[161, 79])
                dpg.bind_item_font(dpg.last_item(), font_regular_40)

            with dpg.child_window(height=136, width=429, pos=[505, 196]):
                dpg.add_text("Motor Torque", pos=[132, 17])
                dpg.bind_item_font(dpg.last_item(), font_regular_16)
                dpg.add_text("123", pos=[161, 79])
                dpg.bind_item_font(dpg.last_item(), font_regular_40)

            with dpg.child_window(height=136, width=429, pos=[971, 196]):
                dpg.add_text("Holding Torque", pos=[129, 17])
                dpg.bind_item_font(dpg.last_item(), font_regular_16)
                dpg.add_text("162", pos=[161, 79])
                dpg.bind_item_font(dpg.last_item(), font_regular_40)

            with dpg.child_window(height=614, width=646, pos=[40, 370]):
                dpg.add_text("Noise Analysis", pos=[21, 39])
                dpg.bind_item_font(dpg.last_item(), font_regular_16)
                with dpg.plot(pos=[22, 79], height=510, width=598, tag="fft_plot"):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Hertz", log_scale=False)
                    dpg.add_plot_axis(dpg.mvYAxis, label="dB", log_scale=False)
                    dpg.add_line_series([0, 5000, 10000, 15000, 20000, 25000], [0, 10000, 20000, 30000, 40000],
                                        label="FFT",
                                        parent=dpg.last_item(), tag="fft_series")

            with dpg.child_window(height=614, width=680, pos=[720, 370]):
                dpg.add_text("Motor Profile", pos=[21, 39])
                dpg.bind_item_font(dpg.last_item(), font_regular_16)
                with dpg.plot(pos=[22, 79], height=510, width=632):
                    dpg.add_plot_legend()

                    # create x axis
                    dpg.add_plot_axis(dpg.mvXAxis, label="time", tag="time_axis", no_tick_labels=False)

                    # create y axis 1
                    dpg.add_plot_axis(dpg.mvYAxis, label="RPM", tag="rpm_axis")

                    dpg.add_line_series([], [], label="RPM", parent=dpg.last_item(), tag="rpm_series")
                    dpg.add_line_series([], [], parent="rpm_axis", tag="present_time")

                    # create y axis 2
                    dpg.add_plot_axis(dpg.mvYAxis, label="Torque (Nm)", tag="torque_axis")

                    dpg.add_line_series([], [], label="Load Torque", parent=dpg.last_item(), tag="load_torque_series")
                    dpg.add_line_series([], [], label="Motor Torque", parent="torque_axis", tag="motor_torque_series")


        dpg.create_viewport(title='Gearbox Dyno', width=1440, height=1064, x_pos=40, y_pos=40)
        dpg.bind_item_theme(window, rpm_theme)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        dpg.set_exit_callback(self.clean_up)

        dpg.set_primary_window("Dyno", True)

    def run(self):
        while dpg.is_dearpygui_running():
            self.update_plot_data()
            dpg.render_dearpygui_frame()

    def start_test(self):
        """
            starts the dynamometer test
        """
        self.populate_test()
        self.flag.value = True
        dpg.configure_item("start_button", show=False)
        dpg.configure_item("stop_button", show=True)
        dpg.configure_item("pause_button", show=True)
        work_order = dpg.get_value("work_order")
        file_name = "recordings/" + work_order + "_" + time.strftime("%m%d%Y-%H%M%S") + ".wav"

        audio_process = mp.Process(target=self.audio_proccesing, args=(file_name,))
        audio_process.start()

    def stop_test(self):
        """
            stops the dynamometer test
        """
        self.flag.value = False
        dpg.configure_item("start_button", show=True)
        dpg.configure_item("stop_button", show=False)
        dpg.configure_item("pause_button", show=False)

    def pause_test(self):
        """
           pauses the dynamometer test
       """
        dpg.configure_item("start_button", show=True)
        dpg.configure_item("stop_button", show=False)
        dpg.configure_item("pause_button", show=False)

    def populate_test(self):
        for profile in self.config["profiles"]:
            if profile["name"] == dpg.get_value("profile_combo"):
                for sequence in profile["sequence"]:
                    for step in sequence:
                        if step == "RPM":
                            rpm = sequence[step]
                        if step == "Dwell":
                            for x in range(sequence[step]):
                                self.test_sequence.append(rpm)
                self.time_x_axis = list(range(0, len(self.test_sequence)))
                dpg.set_value('rpm_series', [self.time_x_axis, self.test_sequence])
                dpg.set_axis_limits("rpm_axis", min(self.test_sequence) - 100, max(self.test_sequence) + 100)
                dpg.set_axis_limits("time_axis", 0, len(self.time_x_axis))

    def update_plot_data(self):
        """
            Updates the plots with new data generated from separate python processes
            :param time_fft_q: The queue for fft time x-axis data
            :param data_fft_q: The queue for fft data y-axis data
        """
        if self.data_fft_q.qsize() > 0:
            fft_data = self.data_fft_q.get()
            fft_time = self.time_fft_q.get()
            dpg.set_value('fft_series', [fft_time, fft_data])

        if self.flag.value == True:
            if int(time.time()) > self.last_time:
                print("Add")
                self.last_time = int(time.time())

                dpg.set_value('present_time',  [self.time_x_axis[0:self.index], self.test_sequence[0:self.index]])
                self.index = self.index + 1




    def audio_proccesing(self, file_name):
        """
           Separate python process for doing audio processing
           :param time_fft_q: The queue for fft time x-axis data
           :param data_fft_q: The queue for fft data y-axis data
           :param file_name: The name of the file to save the audio recordings to
           :param flag: multiprocessing flag to singal when recording should be active
       """
        recording_process = Recorder(self.time_fft_q, self.data_fft_q, file_name, 'wb', self.flag)
        recording_process.record()

    def clean_up(self):
        """
           cleans up the python processes before terminating
       """
        self.flag.value = False
