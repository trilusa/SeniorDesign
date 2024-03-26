"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Takes a vector and returns the index of the maximum value"""

    def __init__(self, N=512):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Max idx',   # will show up in GRC
            in_sig=[(np.float32,N)],
            out_sig=[(np.float32,N)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.N = N

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = (np.ones(self.N)*np.argmax(np.fft.fftshift(input_items[0])))-self.N/2
        return len(output_items[0])
