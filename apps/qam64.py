#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Qam64
# Generated: Thu Feb 20 20:59:28 2014
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import qam
import wx

class qam64(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Qam64")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5056941 * 2
        self.rrc_taps = rrc_taps = 20
        self.gain = gain = 0
        self.center_freq = center_freq = 441000000

        ##################################################
        # Blocks
        ##################################################
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="TX gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=25,
        	num_steps=25,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.qam_trellis_enc_bb_0 = qam.trellis_enc_bb()
        self.qam_transport_framing_bb_0 = qam.transport_framing_bb()
        self.qam_reed_solomon_enc_bb_0 = qam.reed_solomon_enc_bb()
        self.qam_randomizer_bb_0 = qam.randomizer_bb()
        self.qam_interleaver_bb_0 = qam.interleaver_bb(128,4)
        self.qam_frame_sync_enc_bb_0 = qam.frame_sync_enc_bb(6)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=0,buffers=128,buflen=32768" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(gain, 0)
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(-4, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(6000000, 0)
          
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(2, (firdes.root_raised_cosine(0.14, samp_rate, samp_rate/2, 0.18, rrc_taps)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(([complex(1,1), complex(1,-1), complex(1,-3), complex(-3,-1), complex(-3,1), complex(1,3), complex(-3,-3), complex(-3,3), complex(-1,1), complex(-1,-1), complex(3,1), complex(-1,3), complex(-1,-3), complex(3,-1), complex(3,-3), complex(3,3), complex(5,1), complex(1,-5), complex(1,-7), complex(-7,-1), complex(-3,5), complex(5,3), complex(-7,-3), complex(-3,7), complex(-1,5), complex(-5,-1), complex(7,1), complex(-1,7), complex(-5,-3), complex(3,-5), complex(3,-7), complex(7,3), complex(1,5), complex(5,-1), complex(5,-3), complex(-3,-5), complex(-7,1), complex(1,7), complex(-3,-7), complex(-7,3), complex(-5,1), complex(-1,-5), complex(3,5), complex(-5,3), complex(-1,-7), complex(7,-1), complex(7,-3), complex(3,7), complex(5,5), complex(5,-5), complex(5,-7), complex(-7,-5), complex(-7,5), complex(5,7), complex(-7,-7), complex(-7,7), complex(-5,5), complex(-5,-5), complex(7,5), complex(-5,7), complex(-5,-7), complex(7,-5), complex(7,-7), complex(7,7)]), 1)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(7, gr.GR_MSB_FIRST)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/home/argilo/git/gr-qam/in.fifo", False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.qam_reed_solomon_enc_bb_0, 0), (self.qam_interleaver_bb_0, 0))
        self.connect((self.qam_trellis_enc_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.qam_transport_framing_bb_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.qam_reed_solomon_enc_bb_0, 0))
        self.connect((self.qam_transport_framing_bb_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.qam_interleaver_bb_0, 0), (self.qam_randomizer_bb_0, 0))
        self.connect((self.qam_randomizer_bb_0, 0), (self.qam_frame_sync_enc_bb_0, 0))
        self.connect((self.qam_frame_sync_enc_bb_0, 0), (self.qam_trellis_enc_bb_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.interp_fir_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.14, self.samp_rate, self.samp_rate/2, 0.18, self.rrc_taps)))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.interp_fir_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.14, self.samp_rate, self.samp_rate/2, 0.18, self.rrc_taps)))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_sink_0.set_gain(self.gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = qam64()
    tb.Start(True)
    tb.Wait()

