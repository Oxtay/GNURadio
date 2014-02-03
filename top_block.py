#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Fri Oct 25 17:52:57 2013
##################################################

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.qtgui import qtgui
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import numpy
import sip
import sys

class top_block(gr.top_block, Qt.QWidget):

	def __init__(self):
		gr.top_block.__init__(self, "Top Block")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("Top Block")
		self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
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


		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000

		##################################################
		# Blocks
		##################################################
		self.random_source_x_0 = gr.vector_source_s(map(int, numpy.random.randint(0, 2, 1000)), True)
		self.qtgui_sink_x_0 = qtgui.sink_c(
			1024, #fftsize
			firdes.WIN_BLACKMAN_hARRIS, #wintype
			0, #fc
			samp_rate, #bw
			"QT GUI Plot", #name
			True, #plotfreq
			True, #plotwaterfall
			True, #plottime
			True, #plotconst
		)
		self.qtgui_sink_x_0.set_update_time(1.0 / 10)
		self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
		self.top_layout.addWidget(self._qtgui_sink_x_0_win)
		self.digital_ofdm_mod_0 = grc_blks2.packet_mod_f(digital.ofdm_mod(
				options=grc_blks2.options(
					modulation="qpsk",
					fft_length=512,
					occupied_tones=300,
					cp_length=128,
					pad_for_usrp=True,
					log=None,
					verbose=None,
				),
			),
			payload_length=0,
		)
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)

		##################################################
		# Connections
		##################################################
		self.connect((self.random_source_x_0, 0), (self.blocks_short_to_float_0, 0))
		self.connect((self.blocks_short_to_float_0, 0), (self.digital_ofdm_mod_0, 0))
		self.connect((self.digital_ofdm_mod_0, 0), (self.blocks_throttle_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0, 0))


	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)
		self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	qapp = Qt.QApplication(sys.argv)
	tb = top_block()
	tb.start()
	tb.show()
	qapp.exec_()
	tb.stop()

