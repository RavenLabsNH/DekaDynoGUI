"""
old_dyno.py

Copyright © 2022 Raven Labs
Manchester, New Hampshire
www.ravenlabsnh.com

"""
import time

import dearpygui.dearpygui as dpg
import multiprocessing as mp
from math import sin, sqrt
import pyaudio
import wave
import numpy as np

dpg.create_context()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096  # RATE / number of updates per second
TOP_FREQ = 20000

normalized = np.blackman(CHUNK)
soundDevice = pyaudio.PyAudio()
stream = soundDevice.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

def sound_plot(time_fft_q, data_fft_q):
    while(True):
        data = stream.read(CHUNK, exception_on_overflow=False)
        waveData = wave.struct.unpack("%dh"%(CHUNK), data)
        npArrayData = np.array(waveData)
        indata = npArrayData * normalized

        data_fft_q.put(np.abs(np.fft.rfft(indata)))
        time_fft_q.put(np.fft.rfftfreq(CHUNK, 1.0 / RATE))


    # time_fft_q.put(pickle.dumps(np.abs(np.fft.rfft(indata))))
    # data_fft_q.put(pickle.dumps(np.fft.rfftfreq(CHUNK, 1.0 / RATE)))

def update_plot_data(plot_data, amplitude_data, frequency_data, rpm_data, time_data, time_fft_q, data_fft_q, amplitude_queue, frequency_queue, rpm_queue):
    """
    Updates the acoustic plot with the number randomly generated by a separate python process
    :param plot_data: the array of values we are using to as a data source for the acoustic plot
    :param q: The queue the other python process is adding random numbers to
    :return:
    """
    if data_fft_q.qsize() > 0:
        fftData = data_fft_q.get()
        fftTime = time_fft_q.get()
        dpg.set_value('fft_series', [fftTime, fftData])

    if rpm_queue.qsize() > 0:
        if len(rpm_data) > 100:
            rpm_data.pop(0)
        rpm = rpm_queue.get()
        rpm_data.append(rpm)
        dpg.set_value('rpm_series', [time_data, rpm_data])

    if frequency_queue.qsize() > 0:
        if len(frequency_data) > 100:
            frequency_data.pop(0)
        frequency = frequency_queue.get()
        frequency_data.append(frequency)
        dpg.set_value('frequency_series', [time_data, frequency_data])

    if amplitude_queue.qsize() > 0:
        if len(amplitude_data) > 100:
            amplitude_data.pop(0)
        amplitude = amplitude_queue.get()
        amplitude_data.append(amplitude)
        dpg.set_value('amplitude_series', [time_data, amplitude_data])


def generate_data(rmp_queue, frequency_queue, amplitude_queue):
    for i in range(0, 70000):
        rmp_queue.put(sqrt(i)*300)


        if i < 3000:
            frequency_queue.put(i)
        elif i%3 == 0:
             frequency_queue.put(3006)
        else:
            frequency_queue.put(3000)

        if i < 5001:
            amplitude_queue.put(i*3.2)
        # elif i%3 == 0:
        #     amplitude_queue.put(5001)
        else:
            amplitude_queue.put(5000*3.2)

        time.sleep(0.01)


def kill_processes(sender, app_data, p):
    p[0].terminate()
    p[1].terminate()


def change_view(sender, app_data, user_data):
    """
    Change the main view of the application
    :return:
    """
    dpg.configure_item("help_page", show=False)
    dpg.configure_item("home_page", show=False)
    dpg.configure_item("rpm_page", show=False)
    dpg.configure_item("sound_page", show=False)
    dpg.configure_item(user_data, show=True)

if __name__ == '__main__':
    data = []

    amplitude_data = []
    frequency_data = []
    rpm_data = []
    time_data = []

    for i in range(0, 100):
        time_data.append(i)

    # Add a font registry
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        title_font = dpg.add_font("fonts/Sans.TTF", 86)
        home_font = dpg.add_font("fonts/Sans.TTF", 41)
        chart_font = dpg.add_font("fonts/Sans.TTF", 22)

    # Add images by creating textures
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
        dpg.add_static_texture(width, height, data2, tag="matplotlib")

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 6, category=dpg.mvThemeCat_Plots)

    with dpg.theme() as rpm_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (233, 92, 32), category=dpg.mvThemeCat_Plots)
    with dpg.theme() as frequency_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 103, 71), category=dpg.mvThemeCat_Plots)
    with dpg.theme() as amplitude_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (79, 44, 29), category=dpg.mvThemeCat_Plots)


    dpg.bind_theme(global_theme)

    # Main Window
    with dpg.window(tag="Dyno", width=900, height=1080):
        # dpg.bind_font(home_font)
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
                    dpg.add_spacer(height=4)
                    dpg.add_image_button("speed_icon", callback=change_view, user_data="rpm_page")
                    dpg.add_spacer(height=4)
                    dpg.add_image_button("sound_icon", callback=change_view, user_data="sound_page")
                    dpg.add_spacer(height=4)
                    dpg.add_image_button("help_icon", callback=change_view, user_data="help_page")
                    dpg.add_spacer(height=2)

                # Main Body
                # Home Page
                with dpg.child_window(width=1480, autosize_y=True, show=True, tag="home_page", border=False):
                    dpg.bind_item_font("home_page", home_font)
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

                    #dpg.add_image("matplotlib", pos=[-100, -150])
                    # with dpg.plot(label="Output", height=400, width=-1):
                    #     dpg.add_plot_legend()
                    #
                    #     # create x axis
                    #     dpg.add_plot_axis(dpg.mvXAxis, label="time", tag="time_axis", no_tick_labels=True)
                    #
                    #     # create y axis 1
                    #     dpg.add_plot_axis(dpg.mvYAxis, label="RPM", tag="rpm_axis")
                    #
                    #     dpg.add_line_series(time_data, rpm_data, label="RPM", parent=dpg.last_item(), tag="rpm_series")
                    #     dpg.set_axis_limits("rpm_axis", 0, 8000)
                    #
                    #     # create y axis 2
                    #     dpg.add_plot_axis(dpg.mvYAxis, label="Frequency", tag="frequency_axis")
                    #     dpg.add_line_series(time_data, frequency_data, label="Frequency", parent=dpg.last_item(), tag="frequency_series")
                    #     dpg.set_axis_limits("frequency_axis", 0, 5000)
                    #
                    #     # create y axis 3
                    #     dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="amplitude_axis")
                    #     dpg.add_line_series(time_data, amplitude_data, label="Amplitude", parent=dpg.last_item(), tag="amplitude_series")
                    #     dpg.set_axis_limits("amplitude_axis", 0, 7000)

                    with dpg.plot(label="RPM", height=200, width=-1, tag="rpm_plot"):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, show=False, no_tick_labels=True)

                        dpg.add_plot_axis(dpg.mvYAxis, label="RPM", tag="rpm_axis")
                        dpg.add_line_series(time_data, rpm_data, label="RPM", parent=dpg.last_item(), tag="rpm_series")
                        dpg.set_axis_limits("rpm_axis", 2000, 12000)

                    with dpg.plot(label="Frequency", height=200, width=-1, tag="frequency_plot"):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, show=False, no_tick_labels=True)

                        dpg.add_plot_axis(dpg.mvYAxis, label="Frequency", tag="frequency_axis")
                        dpg.add_line_series(time_data, frequency_data, label="Frequency", parent=dpg.last_item(), tag="frequency_series")
                        dpg.set_axis_limits("frequency_axis", 0, 5000)

                    with dpg.plot(label="Amplitude", height=200, width=-1, tag="amplitude_plot"):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, show=False, no_tick_labels=True)

                        dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="amplitude_axis")
                        dpg.add_line_series(time_data, amplitude_data, label="Amplitude", parent=dpg.last_item(), tag="amplitude_series")
                        dpg.set_axis_limits("amplitude_axis", 0, 7000)
                    dpg.bind_item_theme("rpm_plot", rpm_theme)
                    dpg.bind_item_theme("frequency_plot", frequency_theme)
                    dpg.bind_item_theme("amplitude_plot", amplitude_theme)
                # Sound Page
                with dpg.child_window(width=1480, autosize_y=True, show=False, tag="sound_page", border=False):
                    #dpg.add_simple_plot(min_scale=-1.0, max_scale=1.0, height=350, width=1000, tag="plot")
                    with dpg.plot(label="Frequency Spectrum", height=800, width=-1, tag="fft_plot"):
                        #dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="Hertz", tag="hertz_axis", log_scale=False)
                        dpg.add_plot_axis(dpg.mvYAxis, label="dB", tag="db_axis", log_scale=False)
                        dpg.add_line_series([], [], label="FFT", parent=dpg.last_item(), tag="fft_series")

                # Help Page
                with dpg.child_window(width=1480, autosize_y=True, show=False, tag="help_page", border=False):
                    dpg.add_image("raven-logo1", pos=[200, 100])



    # Start a new python process to generate random numbers
    mp.set_start_method('spawn')
    time_fft_q = mp.Queue()
    data_fft_q = mp.Queue()
    sound_process = mp.Process(target=sound_plot, args=(time_fft_q, data_fft_q,))

    rpm_queue = mp.Queue()
    frequency_queue = mp.Queue()
    amplitude_queue = mp.Queue()

    data_process = mp.Process(target=generate_data, args=(rpm_queue, frequency_queue, amplitude_queue,))

    sound_process.start()
    data_process.start()

    dpg.create_viewport(title='Deka Dyno', width=1800, height=975)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_primary_window("Dyno", True)
    dpg.set_exit_callback(kill_processes, user_data=[sound_process, data_process])

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        update_plot_data(data, amplitude_data, frequency_data, rpm_data, time_data, time_fft_q, data_fft_q, amplitude_queue, frequency_queue, rpm_queue)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    sound_process.join()
    data_process.join()
