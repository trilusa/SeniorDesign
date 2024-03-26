#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FFT Test
# Author: adrian
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import audio
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import fft_test_epy_block_0 as epy_block_0  # embedded python block
import numpy as np



from gnuradio import qtgui

class fft_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FFT Test", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FFT Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fft_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 96000
        self.ts = ts = 1/samp_rate
        self.N = N = 2**10
        self.t = t = np.linspace(-N*ts/2,N*ts/2,N,endpoint=False)
        self.f0 = f0 = 1000
        self.x = x = np.sinc(f0*t)
        self.N_delay = N_delay = 0
        self.x_w = x_w = x*window.blackmanharris(N)
        self.t_delay = t_delay = N_delay*ts
        self.fs = fs = samp_rate
        self.dec = dec = 100
        self.N_frames = N_frames = 7
        self.N_delay_tof = N_delay_tof = 0
        self.N_FFT = N_FFT = 512

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            N_FFT,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1.set_y_axis(0, N)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            N_FFT,
            0,
            ts,
            "Time",
            "",
            "Input Signal",
            2, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-1, 1)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("s")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ["x(t)", '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            10, #size
            samp_rate/N_FFT/dec, #samp_rate
            "Sample delay", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-50, 50)

        self.qtgui_time_sink_x_0.set_y_label('Sample', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.fft_vxx_0_0_0 = fft.fft_vcc(N_FFT, False, np.ones(N_FFT), True, 1)
        self.fft_vxx_0_0 = fft.fft_vfc(N_FFT, True, np.ones(N_FFT), False, 1)
        self.fft_vxx_0 = fft.fft_vfc(N_FFT, True, np.ones(N_FFT), False, 1)
        self._f0_range = Range(0, fs/2, 1, 1000, 200)
        self._f0_win = RangeWidget(self._f0_range, self.set_f0, "'f0'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._f0_win)
        self.epy_block_0 = epy_block_0.blk(N=N_FFT)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, N_FFT)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_float*1, N_FFT)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, N_FFT)
        self.blocks_multiply_const_xx_1 = blocks.multiply_const_ff(1/dec, 1)
        self.blocks_multiply_const_xx_0_1 = blocks.multiply_const_cc(N_FFT**-1, N_FFT)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(N_FFT)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, N_FFT)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(dec, 1)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(N_FFT)
        self.audio_source_0 = audio.source(samp_rate, '', False)
        self._N_delay_tof_range = Range(-N*N_frames, N*N_frames, 1, 0, 200)
        self._N_delay_tof_win = RangeWidget(self._N_delay_tof_range, self.set_N_delay_tof, "'N_delay_tof'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._N_delay_tof_win)
        self._N_delay_range = Range(-N*N_frames, N*N_frames, 1, 0, 200)
        self._N_delay_win = RangeWidget(self._N_delay_range, self.set_N_delay, "'N_delay'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._N_delay_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.audio_source_0, 1), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.qtgui_vector_sink_f_0_1, 1))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_xx_1, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_multiply_const_xx_0_1, 0))
        self.connect((self.blocks_multiply_const_xx_0_1, 0), (self.fft_vxx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_0_0, 0), (self.blocks_complex_to_real_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fft_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fs(self.samp_rate)
        self.set_ts(1/self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/self.N_FFT/self.dec)

    def get_ts(self):
        return self.ts

    def set_ts(self, ts):
        self.ts = ts
        self.set_t(np.linspace(-self.N*self.ts/2,self.N*self.ts/2,self.N,endpoint=False))
        self.set_t_delay(self.N_delay*self.ts)
        self.qtgui_vector_sink_f_0.set_x_axis(0, self.ts)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.set_t(np.linspace(-self.N*self.ts/2,self.N*self.ts/2,self.N,endpoint=False))
        self.set_x_w(self.x*window.blackmanharris(self.N))
        self.epy_block_0.N = self.N_FFT
        self.qtgui_vector_sink_f_0_1.set_y_axis(0, self.N)

    def get_t(self):
        return self.t

    def set_t(self, t):
        self.t = t
        self.set_x(np.sinc(self.f0*self.t))

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.set_x(np.sinc(self.f0*self.t))

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x
        self.set_x_w(self.x*window.blackmanharris(self.N))

    def get_N_delay(self):
        return self.N_delay

    def set_N_delay(self, N_delay):
        self.N_delay = N_delay
        self.set_t_delay(self.N_delay*self.ts)

    def get_x_w(self):
        return self.x_w

    def set_x_w(self, x_w):
        self.x_w = x_w

    def get_t_delay(self):
        return self.t_delay

    def set_t_delay(self, t_delay):
        self.t_delay = t_delay

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.blocks_multiply_const_xx_1.set_k(1/self.dec)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/self.N_FFT/self.dec)

    def get_N_frames(self):
        return self.N_frames

    def set_N_frames(self, N_frames):
        self.N_frames = N_frames

    def get_N_delay_tof(self):
        return self.N_delay_tof

    def set_N_delay_tof(self, N_delay_tof):
        self.N_delay_tof = N_delay_tof

    def get_N_FFT(self):
        return self.N_FFT

    def set_N_FFT(self, N_FFT):
        self.N_FFT = N_FFT
        self.blocks_keep_one_in_n_0.set_n(self.N_FFT)
        self.blocks_multiply_const_xx_0_1.set_k(self.N_FFT**-1)
        self.epy_block_0.N = self.N_FFT
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/self.N_FFT/self.dec)




def main(top_block_cls=fft_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
