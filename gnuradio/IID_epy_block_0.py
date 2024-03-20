import numpy as np
from gnuradio import gr

class avg_two_floats(gr.sync_block):  # Define the block as a subclass of gr.sync_block
    def __init__(self):
        gr.sync_block.__init__(self,
            name="IID",   # Block name
            in_sig=[np.float32, np.float32],  # Define two float input ports
            out_sig=[np.float32])    # Define one float output port

    def work(self, input_items, output_items):
        # input_items[0] and input_items[1] are the two input streams
        # output_items[0] is the output stream

        # Calculate the sample-wise average of the two input streams
        output_items[0][:] = (input_items[0] - input_items[1]) 
        return len(output_items[0])  # Return the number of output samples

