#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Meteor Bb Analyser
# Generated: Wed Aug 17 22:40:17 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import math


class meteor_bb_analyser(gr.top_block):

    def __init__(self, bw=250, fftsize=512, infile="/dev/null", outfile="/dev/null", reflvl=-53, srate=2500):
        gr.top_block.__init__(self, "Meteor Bb Analyser")

        ##################################################
        # Parameters
        ##################################################
        self.bw = bw
        self.fftsize = fftsize
        self.infile = infile
        self.outfile = outfile
        self.reflvl = reflvl
        self.srate = srate

        ##################################################
        # Blocks
        ##################################################
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(0.75, fftsize)
        self.low_pass_filter_0 = filter.fir_filter_ccf(srate/bw, firdes.low_pass(
        	1, srate, bw/2, bw/4, firdes.WIN_HAMMING, 6.76))
        self.fft_vxx_0 = fft.fft_vcc(fftsize, True, (window.blackmanharris(fftsize)), False, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, int(20e3),True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsize)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(20, fftsize, -10*(math.log10(fftsize)))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, infile, True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*fftsize, outfile, False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(fftsize)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_nlog10_ff_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_nlog10_ff_0, 0), (self.single_pole_iir_filter_xx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_file_sink_0, 0))    

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.srate, self.bw/2, self.bw/4, firdes.WIN_HAMMING, 6.76))

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize

    def get_infile(self):
        return self.infile

    def set_infile(self, infile):
        self.infile = infile
        self.blocks_file_source_0.open(self.infile, True)

    def get_outfile(self):
        return self.outfile

    def set_outfile(self, outfile):
        self.outfile = outfile
        self.blocks_file_sink_0.open(self.outfile)

    def get_reflvl(self):
        return self.reflvl

    def set_reflvl(self, reflvl):
        self.reflvl = reflvl

    def get_srate(self):
        return self.srate

    def set_srate(self, srate):
        self.srate = srate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.srate, self.bw/2, self.bw/4, firdes.WIN_HAMMING, 6.76))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--bw", dest="bw", type="intx", default=250,
        help="Set Bandwidth [default=%default]")
    parser.add_option(
        "", "--fftsize", dest="fftsize", type="intx", default=512,
        help="Set FFT Size [default=%default]")
    parser.add_option(
        "", "--infile", dest="infile", type="string", default="/dev/null",
        help="Set Input File [default=%default]")
    parser.add_option(
        "", "--outfile", dest="outfile", type="string", default="/dev/null",
        help="Set Output file [default=%default]")
    parser.add_option(
        "", "--reflvl", dest="reflvl", type="eng_float", default=eng_notation.num_to_str(-53),
        help="Set Reference Level [default=%default]")
    parser.add_option(
        "", "--srate", dest="srate", type="intx", default=2500,
        help="Set Sample Rate [default=%default]")
    return parser


def main(top_block_cls=meteor_bb_analyser, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(bw=options.bw, fftsize=options.fftsize, infile=options.infile, outfile=options.outfile, reflvl=options.reflvl, srate=options.srate)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
