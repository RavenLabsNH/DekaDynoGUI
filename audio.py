import pyaudio
import wave
import multiprocessing as mp
import numpy as np

class Recorder(mp.Process):
    def __init__(self, time_fft_q, data_fft_q, file_name, mode, flag,
                 rate=44100, frames_per_buffer=4096):
        self.file_name = file_name
        self.mode = mode
        self.channels = 1
        self.rate = rate
        self.time_fft_q = time_fft_q
        self.data_fft_q = data_fft_q
        self.flag = flag
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.file_name, self.mode)
        self.normalized = np.blackman(frames_per_buffer)

        self._stream = None

    def record(self):
        # Use a stream with no callback function in blocking mode

        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer)

        while bool(self.flag.value):
            in_data = self._stream.read(self.frames_per_buffer, exception_on_overflow=False)
            waveData = wave.struct.unpack("%dh" % self.frames_per_buffer, in_data)
            npArrayData = np.array(waveData)
            indata = npArrayData * self.normalized

            self.data_fft_q.put(np.abs(np.fft.rfft(indata)))
            self.time_fft_q.put(np.fft.rfftfreq(self.frames_per_buffer, 1.0 / self.rate))

            self.wavefile.writeframes(in_data)

        #cleanup
        self._stream.stop_stream()
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, file_name, mode='wb'):
        wavefile = wave.open(file_name, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile