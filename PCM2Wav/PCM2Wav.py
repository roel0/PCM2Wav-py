'''
    File name: PCM2Wav.py
    Author: Roel Postelmans
    Date created: 2017
'''
# Avoid integer division in python 2
from __future__ import division, print_function
import struct
import wave
from .PCM.PCM import PCM
from .PCM.logic import saleae as _saleae
from .PCM.logic import sigrok as _sigrok

class PCM2Wav(object):
    '''
        PCM data to Wav converter
    '''
    saleae = _saleae
    sigrok = _sigrok
    analyzers = saleae, sigrok
    sample_freq = 48000
    sample_width = 2
    channels = 2
    chunk_size = 256

    __formats = {1 : 'c', 2 : 'h'}
    __sample_rates = 16000, 32000, 44100, 48000, 96000, 128000

    def __init__(self, PCM_parser, csv_file, dst):
        """
            PCM2Wav initialiser
        """
        self.data = PCM_parser(csv_file)
        self._generate(dst)

    def _generate(self, dst):
        """
            The actual conversion
        """
        generating = True
        wav_file = wave.open(dst, 'wb')
        wav_file.setnchannels(self.channels)
        wav_file.setsampwidth(self.sample_width)
        sample_rate = self.data.determine_sample_rate()
        wav_file.setframerate(min(self.__sample_rates, key=lambda x: abs(x-sample_rate)))
        while generating:
            try:
                channels = [self.data.pop_data()[1] for DISCARD in range(0, self.chunk_size)]
            except EOFError:
                generating = False
                self.data.close()
            frame = self._calc_frame(channels)
            wav_file.writeframes(frame)
        wav_file.close()

    def _chr(self, arg):
        if self.sample_width == 1:
            return chr(arg)
        return arg

    def _sample_2_bin(self, sample):
        return struct.pack(self.__formats[self.sample_width], self._chr(int(sample)))

    def _calc_frame(self, channels_data):
        return b"".join(self._sample_2_bin(sample) for sample in channels_data)
