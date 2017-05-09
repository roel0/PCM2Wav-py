PCM2Wav-py
=============

This library implements a converter for PCM data to Wav audio format,
obtained with logic analyzers.

For example I2S signals obtained with the Saleae logic analyzer.


Current supported formats
-------------------------

* I2S signals obtained and exported with the Saleae logic analyzer.
* I2S signals obtained with Sigrok (Software that supports multiple hardware devices)

Installation
------------

    (sudo) pip install PCM2Wav


Usage
-----

    python
    from PCM2Wav import *
    output = PCM2Wav(PCM2Wav.saleae.I2S, "i2s.csv", "example.wav")
