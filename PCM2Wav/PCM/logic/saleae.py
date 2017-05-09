'''
    File name: PCM.py
    Author: Roel Postelmans
    Date created: 2017
'''
from ..PCM import PCM

class I2S(PCM):
    '''
        I2S data parser for the saleae logic analyzer
    '''
    TIME_LOC = 0
    VALUE_LOC = -1
    CHANNEL_LOC = -2
    FIRST_D = 1

    def __init__(self, csv_file, delimiter=','):
        '''
            Saleae I2S export parser initiator
        '''
        super(I2S, self).__init__(csv_file, self.FIRST_D)
        self.delimiter = delimiter
        self.start_time = float(self.extract_value(self.start_time, self.TIME_LOC))
        self.end_time = float(self.extract_value(self.end_time, self.TIME_LOC))

    def extract_value(self, line, key):
        '''
            Extract a value from a string by a given position
        '''
        line = line.split(self.delimiter)
        line = line[key].rstrip()
        return line

    def determine_sample_rate(self):
        '''
            Calculate the sample rate based on the
            timestamps
        '''
        super(I2S, self).determine_sample_rate()
        # 2 samples per period
        self.sample_rate /= 2
        super(I2S, self).reset()
        return int(self.sample_rate)

    def pop_data(self):
        '''
            Extract the values from one line of data
        '''
        super(I2S, self).pop_data()
        # Skip header
        if self.sample_count <= self.FIRST_D:
            return self.pop_data()

        value = self.extract_value(self.line, self.VALUE_LOC)
        channel = self.extract_value(self.line, self.CHANNEL_LOC)
        return channel, value

    def close(self):
        '''
            Close the export file
        '''
        self.sample_count -= self.FIRST_D #header
        super(I2S, self).close()
