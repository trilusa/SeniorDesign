"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Zeros out the second hald of the input vector"""

    def __init__(self, N=1024):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Zero Second Half',   # will show up in GRC
            in_sig=[(np.float32,N)],
            out_sig=[(np.float32,N)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.N = N

    def work(self, input_items, output_items):
        """zero out half"""
        tmp=input_items[0]
        tmp[:len(tmp)//2] = 0.0
        output_items[0][:] = input_items[0]
        return len(output_items[0])
