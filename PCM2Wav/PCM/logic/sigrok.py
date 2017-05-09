'''
    File name: PCM.py
    Author: Roel Postelmans
    Date created: 2017
'''
from ..PCM import PCM

class I2S(PCM):
    '''
        I2S data parser for sigrok protocol decoders

        format example:
        ...
        Left channel: 00010000
        Right channel: 00260000
        Left channel: 00010000
        Right channel: 00270000
        ...

    '''
    VALUE_LOC = -1
    CHANNEL_LOC = 0
    FIRST_D = 0

    sample_rate = None
    line = None

    def __init__(self, csv_file, delimiter=' '):
        '''
            Sigrok I2S export parser initiator
        '''
        super(I2S, self).__init__(csv_file, self.FIRST_D)
        self.delimiter = delimiter

    def extract_value(self, line, key):
        '''
            Extract a value from a string by a given position
        '''
        line = line.split(self.delimiter)
        line = line[key].rstrip()
        return line

    def determine_sample_rate(self):
        '''
            Returns the sample_rate or raises an exception
            when it has not been set.
            (no timestamps in sigrok export)
        '''
        if self.sample_rate is None:
            raise ValueError("Sigrok export doesn't contain timestamps,"
                              "you have to set sigrok.sample_rate")
        super(I2S, self).reset()
        return self.sample_rate

    def pop_data(self):
        '''
            Extract the values from one line of data
        '''
        d_channel = {"Left" : 0, "Right": 1}
        if self.line is None:
            super(I2S, self).pop_data()
            value = self.extract_value(self.line, self.VALUE_LOC)[:4]
            channel = self.extract_value(self.line, self.CHANNEL_LOC)
        else:
            value = self.extract_value(self.line, self.VALUE_LOC)[4:]
            channel = self.extract_value(self.line, self.CHANNEL_LOC)
            self.line = None

        value = int(value, 16)
        # check sign bit
        if (value & 0x8000) == 0x8000:
            value = -((value ^ 0xffff) + 1)
        return d_channel[channel], value

    def close(self):
        '''
            Close the export file
        '''
        self.sample_count -= self.FIRST_D #header
        super(I2S, self).close()
