#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Qam64 B200
# Generated: Mon Apr  7 21:38:57 2014
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import qam
import time

class qam64_b200(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Qam64 B200")

        ##################################################
        # Variables
        ##################################################
        self.interpolation = interpolation = 2
        self.samp_rate = samp_rate = 5056941 * interpolation
        self.rrc_taps = rrc_taps = 50
        self.gain = gain = 83
        self.center_freq = center_freq = 441000000

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	device_addr="recv_frame_size=65536,num_recv_frames=128,send_frame_size=65536,num_send_frames=128,master_clock_rate=" + str(samp_rate*4),
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.qam_trellis_enc_bb_0 = qam.trellis_enc_bb()
        self.qam_transport_framing_enc_bb_0 = qam.transport_framing_enc_bb()
        self.qam_reed_solomon_enc_bb_0 = qam.reed_solomon_enc_bb()
        self.qam_randomizer_bb_0 = qam.randomizer_bb()
        self.qam_interleaver_bb_0 = qam.interleaver_bb(128,4)
        self.qam_frame_sync_enc_bb_0 = qam.frame_sync_enc_bb(6)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(interpolation, (firdes.root_raised_cosine(0.14, samp_rate, samp_rate/interpolation, 0.18, rrc_taps)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(([complex(1,1), complex(1,-1), complex(1,-3), complex(-3,-1), complex(-3,1), complex(1,3), complex(-3,-3), complex(-3,3), complex(-1,1), complex(-1,-1), complex(3,1), complex(-1,3), complex(-1,-3), complex(3,-1), complex(3,-3), complex(3,3), complex(5,1), complex(1,-5), complex(1,-7), complex(-7,-1), complex(-3,5), complex(5,3), complex(-7,-3), complex(-3,7), complex(-1,5), complex(-5,-1), complex(7,1), complex(-1,7), complex(-5,-3), complex(3,-5), complex(3,-7), complex(7,3), complex(1,5), complex(5,-1), complex(5,-3), complex(-3,-5), complex(-7,1), complex(1,7), complex(-3,-7), complex(-7,3), complex(-5,1), complex(-1,-5), complex(3,5), complex(-5,3), complex(-1,-7), complex(7,-1), complex(7,-3), complex(3,7), complex(5,5), complex(5,-5), complex(5,-7), complex(-7,-5), complex(-7,5), complex(5,7), complex(-7,-7), complex(-7,7), complex(-5,5), complex(-5,-5), complex(7,5), complex(-5,7), complex(-5,-7), complex(7,-5), complex(7,-7), complex(7,7)]), 1)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(7, gr.GR_MSB_FIRST)
        self.blks2_tcp_source_0 = grc_blks2.tcp_source(
        	itemsize=gr.sizeof_char*1,
        	addr="127.0.0.1",
        	port=5555,
        	server=True,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.qam_reed_solomon_enc_bb_0, 0), (self.qam_interleaver_bb_0, 0))
        self.connect((self.qam_trellis_enc_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.qam_interleaver_bb_0, 0), (self.qam_randomizer_bb_0, 0))
        self.connect((self.qam_randomizer_bb_0, 0), (self.qam_frame_sync_enc_bb_0, 0))
        self.connect((self.qam_frame_sync_enc_bb_0, 0), (self.qam_trellis_enc_bb_0, 0))
        self.connect((self.qam_transport_framing_enc_bb_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.qam_reed_solomon_enc_bb_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blks2_tcp_source_0, 0), (self.qam_transport_framing_enc_bb_0, 0))


# QT sink close method reimplementation

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.set_samp_rate(5056941 * self.interpolation)
        self.interp_fir_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.14, self.samp_rate, self.samp_rate/self.interpolation, 0.18, self.rrc_taps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.interp_fir_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.14, self.samp_rate, self.samp_rate/self.interpolation, 0.18, self.rrc_taps)))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.interp_fir_filter_xxx_0.set_taps((firdes.root_raised_cosine(0.14, self.samp_rate, self.samp_rate/self.interpolation, 0.18, self.rrc_taps)))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = qam64_b200()
    tb.start()
    raw_input('Press Enter to quit: ')
    tb.stop()
    tb.wait()

