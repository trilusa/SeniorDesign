#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ITD
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
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import ITD_epy_block_0 as epy_block_0  # embedded python block
import numpy as np



from gnuradio import qtgui

class ITD(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "ITD", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("ITD")
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

        self.settings = Qt.QSettings("GNU Radio", "ITD")

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
        self.fc = fc = 4000
        self.FFT_L = FFT_L = 1024
        self.imp_N = imp_N = FFT_L//4
        self.imp_L = imp_L = 10
        self.ft = ft = fc/8
        self.f = f = 500
        self.dec = dec = 100
        self.FFAGC_L = FFAGC_L = int(samp_rate/64)
        self.A = A = .1

        ##################################################
        # Blocks
        ##################################################
        self._f_range = Range(100, 5000, 10, 500, 200)
        self._f_win = RangeWidget(self._f_range, self.set_f, "f", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._f_win)
        self._A_range = Range(0, 10, .01, .1, 200)
        self._A_win = RangeWidget(self._A_range, self.set_A, "'A'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._A_win)
        self.qtgui_vector_sink_f_0_1 = qtgui.vector_sink_f(
            FFT_L,
            0,
            1,
            "x-Axis",
            "y-Axis",
            "Cross Correlation",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1.set_y_axis(-.01, 1)
        self.qtgui_vector_sink_f_0_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1.set_ref_level(0)

        labels = ['correlation', 'Im', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["red", "blue", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            10, #size
            samp_rate/FFT_L/dec, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(0, FFT_L)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            FFT_L*10, #size
            samp_rate, #samp_rate
            "", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['L_re', 'R_re', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['black', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
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
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                fc,
                ft,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                fc,
                ft,
                window.WIN_HAMMING,
                6.76))
        self.fft_vxx_0_0_0 = fft.fft_vcc(FFT_L, False, window.blackmanharris(FFT_L), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(FFT_L, True, window.blackmanharris(FFT_L), False, 1)
        self.fft_vxx_0 = fft.fft_vcc(FFT_L, True, window.blackmanharris(FFT_L), False, 1)
        self.epy_block_0 = epy_block_0.blk(N=FFT_L)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, FFT_L)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT_L)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT_L)
        self.blocks_phase_shift_0 = blocks.phase_shift(45, False)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*FFT_L)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(FFT_L)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((FFT_L**-1)*np.array([1] * int(FFT_L/2) + [0] *int( FFT_L/2)))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(dec, FFT_L)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_magphase_0_1 = blocks.complex_to_magphase(FFT_L)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_source_0 = audio.source(samp_rate, '', False)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, f, A, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.audio_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.audio_source_0, 1), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_magphase_0_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_magphase_0_1, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_phase_shift_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.qtgui_vector_sink_f_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.fft_vxx_0_0_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.fft_vxx_0_0_0, 0), (self.blocks_complex_to_magphase_0_1, 0))
        self.connect((self.fft_vxx_0_0_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ITD")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_FFAGC_L(int(self.samp_rate/64))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.fc, self.ft, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.fc, self.ft, window.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/self.FFT_L/self.dec)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_ft(self.fc/8)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.fc, self.ft, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.fc, self.ft, window.WIN_HAMMING, 6.76))

    def get_FFT_L(self):
        return self.FFT_L

    def set_FFT_L(self, FFT_L):
        self.FFT_L = FFT_L
        self.set_imp_N(self.FFT_L//4)
        self.blocks_multiply_const_vxx_0.set_k((self.FFT_L**-1)*np.array([1] * int(self.FFT_L/2) + [0] *int( self.FFT_L/2)))
        self.epy_block_0.N = self.FFT_L
        self.qtgui_time_sink_x_1.set_y_axis(0, self.FFT_L)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/self.FFT_L/self.dec)

    def get_imp_N(self):
        return self.imp_N

    def set_imp_N(self, imp_N):
        self.imp_N = imp_N

    def get_imp_L(self):
        return self.imp_L

    def set_imp_L(self, imp_L):
        self.imp_L = imp_L

    def get_ft(self):
        return self.ft

    def set_ft(self, ft):
        self.ft = ft
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.fc, self.ft, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.fc, self.ft, window.WIN_HAMMING, 6.76))

    def get_f(self):
        return self.f

    def set_f(self, f):
        self.f = f
        self.analog_sig_source_x_0.set_frequency(self.f)

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/self.FFT_L/self.dec)

    def get_FFAGC_L(self):
        return self.FFAGC_L

    def set_FFAGC_L(self, FFAGC_L):
        self.FFAGC_L = FFAGC_L

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A
        self.analog_sig_source_x_0.set_amplitude(self.A)




def main(top_block_cls=ITD, options=None):

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
