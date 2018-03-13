#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: VHF Meteor Detection Receiver
# Author: Marcus Leech
# Description: Meteor detection using broadcast VHF
# Generated: Wed Aug 17 21:57:33 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import meteor_helper
import osmosdr
import threading
import time
import wx


class meteor_detector(grc_wxgui.top_block_gui):

    def __init__(self, agc=0, bw1=500, bw2=500, bw3=500, cfreq=216.980e6, devid='rtl=0', dgain1=1, dgain2=1, dgain3=1, f1=216.970e6, f2=216.980e6, f3=216.990e6, ftune=0, offs=25.0e3, ppm=0, rfgain=25, srate=1.0e6, trig=5.5):
        grc_wxgui.top_block_gui.__init__(self, title="VHF Meteor Detection Receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.agc = agc
        self.bw1 = bw1
        self.bw2 = bw2
        self.bw3 = bw3
        self.cfreq = cfreq
        self.devid = devid
        self.dgain1 = dgain1
        self.dgain2 = dgain2
        self.dgain3 = dgain3
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.ftune = ftune
        self.offs = offs
        self.ppm = ppm
        self.rfgain = rfgain
        self.srate = srate
        self.trig = trig

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(srate)
        self.chan_width = chan_width = 50e3
        self.chan_trigger_poll = chan_trigger_poll = 0
        self.xx = xx = False if agc == 0 else True
        self.trigs3 = trigs3 = meteor_helper.trig_state(3,chan_trigger_poll)
        self.trigs2 = trigs2 = meteor_helper.trig_state(2,chan_trigger_poll)
        self.trigs1 = trigs1 = meteor_helper.trig_state(1,chan_trigger_poll)
        self.thresh = thresh = trig
        self.record_3 = record_3 = False
        self.record_2 = record_2 = False
        self.record_1 = record_1 = False
        self.input_filter = input_filter = firdes.low_pass(1.0,samp_rate,samp_rate/2.2,samp_rate/3.0)
        self.freq3 = freq3 = f3
        self.freq2 = freq2 = f2
        self.freq1 = freq1 = f1
        self.dc_gain_3 = dc_gain_3 = dgain3
        self.dc_gain_2 = dc_gain_2 = dgain2
        self.dc_gain_1 = dc_gain_1 = dgain1
        self.chan_filter = chan_filter = firdes.low_pass(1.0,int(samp_rate),(chan_width/2.2),(chan_width/3),firdes.WIN_HAMMING,6.76)
        self.chan3_value = chan3_value = 0
        self.chan2_value = chan2_value = 0
        self.chan1_value = chan1_value = 0
        self.bb_files = bb_files = ["met-bb-fifo0", "met-bb-fifo1", "met-bb-fifo2"]
        self.Fc = Fc = cfreq
        self.variable_static_text_0_0_0 = variable_static_text_0_0_0 = freq3
        self.variable_static_text_0_0 = variable_static_text_0_0 = freq2
        self.variable_static_text_0 = variable_static_text_0 = freq1
        self.trig_state_3_0_0_0 = trig_state_3_0_0_0 = trigs3[3]
        self.trig_state_3_0_0 = trig_state_3_0_0 = trigs3[2]
        self.trig_state_3_0 = trig_state_3_0 = trigs3[1]
        self.trig_state_3 = trig_state_3 = trigs3[0]
        self.trig_state_2_0_0_0 = trig_state_2_0_0_0 = trigs2[3]
        self.trig_state_2_0_0 = trig_state_2_0_0 = trigs2[2]
        self.trig_state_2_0 = trig_state_2_0 = trigs2[1]
        self.trig_state_2 = trig_state_2 = trigs2[0]
        self.trig_state_1_0_0_0 = trig_state_1_0_0_0 = trigs1[3]
        self.trig_state_1_0_0 = trig_state_1_0_0 = trigs1[2]
        self.trig_state_1_0 = trig_state_1_0 = trigs1[1]
        self.trig_state_1 = trig_state_1 = trigs1[0]
        self.thread_start_stats = thread_start_stats = meteor_helper.start_threads(bb_files)
        self.rfg = rfg = rfgain
        self.post_det_rate = post_det_rate = meteor_helper.getHz()/2
        self.offset = offset = offs
        self.input_len = input_len = len(input_filter)
        self.iagc = iagc = xx
        self.fine = fine = ftune
        self.filt_len = filt_len = len(chan_filter)
        self.detector_rate = detector_rate = 5.0e3
        self.cur_time = cur_time = meteor_helper.current_time(chan_trigger_poll)
        self.chan_write_3 = chan_write_3 = meteor_helper.write_chan(3,chan3_value,freq3,thresh,record_3,dc_gain_3)
        self.chan_write_2 = chan_write_2 = meteor_helper.write_chan(2,chan2_value,freq2,thresh,record_2,dc_gain_2)
        self.chan_write_1 = chan_write_1 = meteor_helper.write_chan(1,chan1_value,freq1,thresh,record_1,dc_gain_1)
        self.bandwidth_3 = bandwidth_3 = bw3
        self.bandwidth_2 = bandwidth_2 = bw2
        self.bandwidth_1 = bandwidth_1 = bw1
        self.F3 = F3 = freq3-Fc
        self.F2 = F2 = freq2-Fc
        self.F1 = F1 = freq1-Fc

        ##################################################
        # Blocks
        ##################################################
        self.Main = self.Main = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Main Spectral")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Detectors")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Ch1 Detail")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Ch 2 Detail")
        self.Main.AddPage(grc_wxgui.Panel(self.Main), "Ch 3 Detail")
        self.Add(self.Main)
        _rfg_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rfg_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_rfg_sizer,
        	value=self.rfg,
        	callback=self.set_rfg,
        	label='RF Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rfg_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_rfg_sizer,
        	value=self.rfg,
        	callback=self.set_rfg,
        	minimum=0,
        	maximum=50,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_rfg_sizer, 1, 1, 1, 2)
        _offset_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_offset_sizer,
        	value=self.offset,
        	callback=self.set_offset,
        	label='LO Offset',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_offset_sizer,
        	value=self.offset,
        	callback=self.set_offset,
        	minimum=25e3,
        	maximum=250e3,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_offset_sizer, 0, 8, 1, 1)
        self._iagc_check_box = forms.check_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.iagc,
        	callback=self.set_iagc,
        	label='AGC',
        	true=1,
        	false=0,
        )
        self.Main.GetPage(0).GridAdd(self._iagc_check_box, 1, 0, 1, 1)
        _fine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._fine_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_fine_sizer,
        	value=self.fine,
        	callback=self.set_fine,
        	label='Fine Tuning',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._fine_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_fine_sizer,
        	value=self.fine,
        	callback=self.set_fine,
        	minimum=-15e3,
        	maximum=15e3,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_fine_sizer, 0, 6, 1, 1)
        self._dc_gain_3_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.dc_gain_3,
        	callback=self.set_dc_gain_3,
        	label='Detector Gain',
        	choices=[1,5,10,20,50],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(4).GridAdd(self._dc_gain_3_chooser, 1, 2, 1, 1)
        self._dc_gain_2_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.dc_gain_2,
        	callback=self.set_dc_gain_2,
        	label='Detector Gain',
        	choices=[1,5,10,20,50],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(3).GridAdd(self._dc_gain_2_chooser, 1, 2, 1, 1)
        self._dc_gain_1_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.dc_gain_1,
        	callback=self.set_dc_gain_1,
        	label='Detector Gain',
        	choices=[1,5,10,20,50],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(2).GridAdd(self._dc_gain_1_chooser, 1, 2, 1, 1)
        self.chan2_pwr = blocks.probe_signal_f()
        self.chan1_pwr = blocks.probe_signal_f()
        self._bandwidth_3_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.bandwidth_3,
        	callback=self.set_bandwidth_3,
        	label='Detector Bandwidth (Hz)',
        	choices=[500, 1000, 2000, 3000],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(4).GridAdd(self._bandwidth_3_chooser, 1, 1, 1, 1)
        self._bandwidth_2_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.bandwidth_2,
        	callback=self.set_bandwidth_2,
        	label='Detector Bandwidth (Hz)',
        	choices=[500, 1000, 2000, 3000],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(3).GridAdd(self._bandwidth_2_chooser, 1, 1, 1, 1)
        self._bandwidth_1_chooser = forms.radio_buttons(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.bandwidth_1,
        	callback=self.set_bandwidth_1,
        	label='Detector Bandwidth (Hz)',
        	choices=[500, 1000, 2000, 3000],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.Main.GetPage(2).GridAdd(self._bandwidth_1_chooser, 1, 1, 1, 1)
        self._Fc_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.Fc,
        	callback=self.set_Fc,
        	label='Fc',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._Fc_text_box, 0, 7, 1, 1)
        self.wxgui_waterfallsink2_0_0_0_0 = waterfallsink2.waterfall_sink_c(
        	self.Main.GetPage(4).GetWin(),
        	baseband_freq=0,
        	dynamic_range=10,
        	ref_level=-53,
        	ref_scale=2.0,
        	sample_rate=detector_rate/2,
        	fft_size=2048,
        	fft_rate=5,
        	average=True,
        	avg_alpha=0.5,
        	title='Ch 3 Spectrum Detail',
        	size=(700,525),
        )
        self.Main.GetPage(4).Add(self.wxgui_waterfallsink2_0_0_0_0.win)
        self.wxgui_waterfallsink2_0_0_0 = waterfallsink2.waterfall_sink_c(
        	self.Main.GetPage(3).GetWin(),
        	baseband_freq=0,
        	dynamic_range=10,
        	ref_level=-53,
        	ref_scale=2.0,
        	sample_rate=detector_rate/2,
        	fft_size=2048,
        	fft_rate=5,
        	average=True,
        	avg_alpha=0.5,
        	title='Ch 2 Spectrum Detail',
        	size=(700,525),
        )
        self.Main.GetPage(3).Add(self.wxgui_waterfallsink2_0_0_0.win)
        self.wxgui_waterfallsink2_0_0 = waterfallsink2.waterfall_sink_c(
        	self.Main.GetPage(2).GetWin(),
        	baseband_freq=0,
        	dynamic_range=10,
        	ref_level=-53,
        	ref_scale=2.0,
        	sample_rate=detector_rate/2,
        	fft_size=2048,
        	fft_rate=5,
        	average=True,
        	avg_alpha=0.5,
        	title='Ch 1 Spectrum Detail',
        	size=(700,525),
        )
        self.Main.GetPage(2).Add(self.wxgui_waterfallsink2_0_0.win)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.Main.GetPage(0).GetWin(),
        	baseband_freq=Fc,
        	dynamic_range=10,
        	ref_level=-40,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2048,
        	fft_rate=4,
        	average=True,
        	avg_alpha=0.5,
        	title='Spectrogram',
        	size=(700,425),
        )
        self.Main.GetPage(0).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.Main.GetPage(1).GetWin(),
        	title='Detected Power',
        	sample_rate=post_det_rate,
        	v_scale=5e-6,
        	v_offset=10e-6,
        	t_scale=450,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=3,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Relative Power',
        	size=(700,300),
        )
        self.Main.GetPage(1).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.Main.GetPage(0).GetWin(),
        	baseband_freq=Fc,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2048,
        	fft_rate=8,
        	average=True,
        	avg_alpha=0.1,
        	title='Instantaneous Spectrum',
        	peak_hold=False,
        	size=(700,150),
        )
        self.Main.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self._variable_static_text_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.variable_static_text_0_0_0,
        	callback=self.set_variable_static_text_0_0_0,
        	label='Ch 3 Freq',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(4).GridAdd(self._variable_static_text_0_0_0_static_text, 0, 0, 1, 1)
        self._variable_static_text_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.variable_static_text_0_0,
        	callback=self.set_variable_static_text_0_0,
        	label='Ch 2 Freq',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(3).GridAdd(self._variable_static_text_0_0_static_text, 0, 0, 1, 1)
        self._variable_static_text_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.variable_static_text_0,
        	callback=self.set_variable_static_text_0,
        	label='Ch 1 Freq',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(2).GridAdd(self._variable_static_text_0_static_text, 0, 0, 1, 1)
        self._trig_state_3_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.trig_state_3_0_0_0,
        	callback=self.set_trig_state_3_0_0_0,
        	label='Rate',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(4).GridAdd(self._trig_state_3_0_0_0_static_text, 1, 5, 1, 1)
        self._trig_state_3_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.trig_state_3_0_0,
        	callback=self.set_trig_state_3_0_0,
        	label='Count',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(4).GridAdd(self._trig_state_3_0_0_static_text, 1, 4, 1, 1)
        self._trig_state_3_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.trig_state_3_0,
        	callback=self.set_trig_state_3_0,
        	label='Filename',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(4).GridAdd(self._trig_state_3_0_static_text, 0, 5, 1, 1)
        self._trig_state_3_static_text = forms.static_text(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.trig_state_3,
        	callback=self.set_trig_state_3,
        	label='Trig state',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(4).GridAdd(self._trig_state_3_static_text, 0, 4, 1, 1)
        self._trig_state_2_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.trig_state_2_0_0_0,
        	callback=self.set_trig_state_2_0_0_0,
        	label='Rate',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(3).GridAdd(self._trig_state_2_0_0_0_static_text, 1, 5, 1, 1)
        self._trig_state_2_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.trig_state_2_0_0,
        	callback=self.set_trig_state_2_0_0,
        	label='Count',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(3).GridAdd(self._trig_state_2_0_0_static_text, 1, 4, 1, 1)
        self._trig_state_2_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.trig_state_2_0,
        	callback=self.set_trig_state_2_0,
        	label='Filename',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(3).GridAdd(self._trig_state_2_0_static_text, 0, 5, 1, 1)
        self._trig_state_2_static_text = forms.static_text(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.trig_state_2,
        	callback=self.set_trig_state_2,
        	label='Trig state',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(3).GridAdd(self._trig_state_2_static_text, 0, 4, 1, 1)
        self._trig_state_1_0_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.trig_state_1_0_0_0,
        	callback=self.set_trig_state_1_0_0_0,
        	label='Rate',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(2).GridAdd(self._trig_state_1_0_0_0_static_text, 1, 5, 1, 1)
        self._trig_state_1_0_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.trig_state_1_0_0,
        	callback=self.set_trig_state_1_0_0,
        	label='Count',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(2).GridAdd(self._trig_state_1_0_0_static_text, 1, 4, 1, 1)
        self._trig_state_1_0_static_text = forms.static_text(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.trig_state_1_0,
        	callback=self.set_trig_state_1_0,
        	label='Filename',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(2).GridAdd(self._trig_state_1_0_static_text, 0, 5, 1, 1)
        self._trig_state_1_static_text = forms.static_text(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.trig_state_1,
        	callback=self.set_trig_state_1,
        	label='Trig state',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(2).GridAdd(self._trig_state_1_static_text, 0, 4, 1, 1)
        _thresh_sizer = wx.BoxSizer(wx.VERTICAL)
        self._thresh_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_thresh_sizer,
        	value=self.thresh,
        	callback=self.set_thresh,
        	label='Trigger Threshold',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._thresh_slider = forms.slider(
        	parent=self.Main.GetPage(0).GetWin(),
        	sizer=_thresh_sizer,
        	value=self.thresh,
        	callback=self.set_thresh,
        	minimum=2,
        	maximum=20,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Main.GetPage(0).GridAdd(_thresh_sizer, 0, 5, 1, 1)
        self.single_pole_iir_filter_xx_0_0_0 = filter.single_pole_iir_filter_ff(1.0/(detector_rate/10), 1)
        self.single_pole_iir_filter_xx_0_0 = filter.single_pole_iir_filter_ff(1.0/(detector_rate/10), 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(1.0/(detector_rate/10), 1)
        self._record_3_check_box = forms.check_box(
        	parent=self.Main.GetPage(4).GetWin(),
        	value=self.record_3,
        	callback=self.set_record_3,
        	label='Record Baseband',
        	true=True,
        	false=False,
        )
        self.Main.GetPage(4).GridAdd(self._record_3_check_box, 1, 0, 1, 1)
        self._record_2_check_box = forms.check_box(
        	parent=self.Main.GetPage(3).GetWin(),
        	value=self.record_2,
        	callback=self.set_record_2,
        	label='Record Baseband',
        	true=True,
        	false=False,
        )
        self.Main.GetPage(3).GridAdd(self._record_2_check_box, 1, 0, 1, 1)
        self._record_1_check_box = forms.check_box(
        	parent=self.Main.GetPage(2).GetWin(),
        	value=self.record_1,
        	callback=self.set_record_1,
        	label='Record Baseband',
        	true=True,
        	false=False,
        )
        self.Main.GetPage(2).GridAdd(self._record_1_check_box, 1, 0, 1, 1)
        self.osmosdr_source_c_0 = osmosdr.source( args="numchan=" + str(1) + " " + devid )
        self.osmosdr_source_c_0.set_sample_rate(samp_rate)
        self.osmosdr_source_c_0.set_center_freq(Fc+(offset), 0)
        self.osmosdr_source_c_0.set_freq_corr(0, 0)
        self.osmosdr_source_c_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_c_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_c_0.set_gain_mode(iagc, 0)
        self.osmosdr_source_c_0.set_gain(25 if iagc else rfg, 0)
        self.osmosdr_source_c_0.set_if_gain(20, 0)
        self.osmosdr_source_c_0.set_bb_gain(20, 0)
        self.osmosdr_source_c_0.set_antenna('', 0)
        self.osmosdr_source_c_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_1_1 = filter.fir_filter_ccf(int(chan_width/(detector_rate*2)), firdes.low_pass(
        	5, chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0_1 = filter.fir_filter_ccf(int(chan_width/(detector_rate*2)), firdes.low_pass(
        	5, chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0_0_0 = filter.fir_filter_ccf(int(chan_width/(detector_rate*2)), firdes.low_pass(
        	5, chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0_0 = filter.fir_filter_ccf(int(chan_width/(detector_rate/2)), firdes.low_pass(
        	5, chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0 = filter.fir_filter_ccf(int(chan_width/(detector_rate/2)), firdes.low_pass(
        	5, chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1 = filter.fir_filter_ccf(int(chan_width/(detector_rate/2)), firdes.low_pass(
        	5, chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0 = filter.fir_filter_ccf(int(chan_width/detector_rate), firdes.low_pass(
        	1, chan_width, bandwidth_3/2, (bandwidth_3/2)/3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(int(chan_width/detector_rate), firdes.low_pass(
        	1, chan_width, bandwidth_2/2, (bandwidth_2/2)/3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(int(chan_width/detector_rate), firdes.low_pass(
        	1, chan_width, bandwidth_1/2, (bandwidth_1/2)/3, firdes.WIN_HAMMING, 6.76))
        self.keep_one_in_n_0_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(detector_rate/post_det_rate))
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(1, (input_filter), (offset)+((Fc/1.0e6 * ppm))+fine, samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0_0 = filter.freq_xlating_fir_filter_ccc(int(samp_rate/chan_width), (chan_filter), (-F3), samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(int(samp_rate/chan_width), (chan_filter), (-F2), samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(int(samp_rate/chan_width), (chan_filter), (-F1), samp_rate)
        self._freq3_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.freq3,
        	callback=self.set_freq3,
        	label='Ch 3',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._freq3_text_box, 0, 2, 1, 1)
        self._freq2_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.freq2,
        	callback=self.set_freq2,
        	label='Ch 2',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._freq2_text_box, 0, 1, 1, 1)
        self._freq1_text_box = forms.text_box(
        	parent=self.Main.GetPage(0).GetWin(),
        	value=self.freq1,
        	callback=self.set_freq1,
        	label='Ch 1',
        	converter=forms.float_converter(),
        )
        self.Main.GetPage(0).GridAdd(self._freq1_text_box, 0, 0, 1, 1)
        self._cur_time_static_text = forms.static_text(
        	parent=self.Main.GetPage(1).GetWin(),
        	value=self.cur_time,
        	callback=self.set_cur_time,
        	label='Current Time',
        	converter=forms.str_converter(),
        )
        self.Main.GetPage(1).GridAdd(self._cur_time_static_text, 0, 1, 1, 1)
        self.complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        
        def _chan_trigger_poll_probe():
            while True:
                val = self.chan1_pwr.level()
                try:
                    self.set_chan_trigger_poll(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (2))
        _chan_trigger_poll_thread = threading.Thread(target=_chan_trigger_poll_probe)
        _chan_trigger_poll_thread.daemon = True
        _chan_trigger_poll_thread.start()
            
        
        def _chan3_value_probe():
            while True:
                val = self.chan3_pwr.level()
                try:
                    self.set_chan3_value(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (meteor_helper.getHz()))
        _chan3_value_thread = threading.Thread(target=_chan3_value_probe)
        _chan3_value_thread.daemon = True
        _chan3_value_thread.start()
            
        self.chan3_pwr_0 = blocks.probe_signal_f()
        
        def _chan2_value_probe():
            while True:
                val = self.chan2_pwr.level()
                try:
                    self.set_chan2_value(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (meteor_helper.getHz()))
        _chan2_value_thread = threading.Thread(target=_chan2_value_probe)
        _chan2_value_thread.daemon = True
        _chan2_value_thread.start()
            
        
        def _chan1_value_probe():
            while True:
                val = self.chan1_pwr.level()
                try:
                    self.set_chan1_value(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (meteor_helper.getHz()))
        _chan1_value_thread = threading.Thread(target=_chan1_value_probe)
        _chan1_value_thread.daemon = True
        _chan1_value_thread.start()
            
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_vff((dc_gain_3*5, ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((dc_gain_2*5, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((dc_gain_1*5, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.285, ))
        self.blocks_keep_one_in_n_0_0_0_1 = blocks.keep_one_in_n(gr.sizeof_float*1, int(detector_rate/post_det_rate))
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(detector_rate/post_det_rate))
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, bb_files[2], False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, bb_files[1 ], False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, bb_files[0], False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_squared_0_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0_0_0, 0), (self.single_pole_iir_filter_xx_0_0_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0_0_1, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.freq_xlating_fir_filter_xxx_0_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.chan1_pwr, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.chan2_pwr, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.wxgui_scopesink2_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.chan3_pwr_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.wxgui_scopesink2_0, 2))    
        self.connect((self.complex_to_mag_squared_0_0, 0), (self.single_pole_iir_filter_xx_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_1_1, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.low_pass_filter_1_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.low_pass_filter_1_0_1, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.low_pass_filter_0_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.low_pass_filter_1_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_0, 0), (self.low_pass_filter_1_0_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.keep_one_in_n_0_0_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.complex_to_mag_squared_0_0, 0))    
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.wxgui_waterfallsink2_0_0, 0))    
        self.connect((self.low_pass_filter_1_0, 0), (self.wxgui_waterfallsink2_0_0_0, 0))    
        self.connect((self.low_pass_filter_1_0_0, 0), (self.wxgui_waterfallsink2_0_0_0_0, 0))    
        self.connect((self.low_pass_filter_1_0_0_0, 0), (self.blocks_file_sink_0_0_0, 0))    
        self.connect((self.low_pass_filter_1_0_1, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.low_pass_filter_1_1, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.osmosdr_source_c_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))    
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.keep_one_in_n_0_0_0_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0_0_0, 0), (self.blocks_keep_one_in_n_0_0_0_1, 0))    

    def get_agc(self):
        return self.agc

    def set_agc(self, agc):
        self.agc = agc
        self.set_xx(False if self.agc == 0 else True)

    def get_bw1(self):
        return self.bw1

    def set_bw1(self, bw1):
        self.bw1 = bw1
        self.set_bandwidth_1(self.bw1)

    def get_bw2(self):
        return self.bw2

    def set_bw2(self, bw2):
        self.bw2 = bw2
        self.set_bandwidth_2(self.bw2)

    def get_bw3(self):
        return self.bw3

    def set_bw3(self, bw3):
        self.bw3 = bw3
        self.set_bandwidth_3(self.bw3)

    def get_cfreq(self):
        return self.cfreq

    def set_cfreq(self, cfreq):
        self.cfreq = cfreq
        self.set_Fc(self.cfreq)

    def get_devid(self):
        return self.devid

    def set_devid(self, devid):
        self.devid = devid

    def get_dgain1(self):
        return self.dgain1

    def set_dgain1(self, dgain1):
        self.dgain1 = dgain1
        self.set_dc_gain_1(self.dgain1)

    def get_dgain2(self):
        return self.dgain2

    def set_dgain2(self, dgain2):
        self.dgain2 = dgain2
        self.set_dc_gain_2(self.dgain2)

    def get_dgain3(self):
        return self.dgain3

    def set_dgain3(self, dgain3):
        self.dgain3 = dgain3
        self.set_dc_gain_3(self.dgain3)

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1
        self.set_freq1(self.f1)

    def get_f2(self):
        return self.f2

    def set_f2(self, f2):
        self.f2 = f2
        self.set_freq2(self.f2)

    def get_f3(self):
        return self.f3

    def set_f3(self, f3):
        self.f3 = f3
        self.set_freq3(self.f3)

    def get_ftune(self):
        return self.ftune

    def set_ftune(self, ftune):
        self.ftune = ftune
        self.set_fine(self.ftune)

    def get_offs(self):
        return self.offs

    def set_offs(self, offs):
        self.offs = offs
        self.set_offset(self.offs)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.freq_xlating_fir_filter_xxx_1.set_center_freq((self.offset)+((self.Fc/1.0e6 * self.ppm))+self.fine)

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.set_rfg(self.rfgain)

    def get_srate(self):
        return self.srate

    def set_srate(self, srate):
        self.srate = srate
        self.set_samp_rate(int(self.srate))

    def get_trig(self):
        return self.trig

    def set_trig(self, trig):
        self.trig = trig
        self.set_thresh(self.trig)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_input_filter(firdes.low_pass(1.0,self.samp_rate,self.samp_rate/2.2,self.samp_rate/3.0))
        self.set_chan_filter(firdes.low_pass(1.0,int(self.samp_rate),(self.chan_width/2.2),(self.chan_width/3),firdes.WIN_HAMMING,6.76))
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_c_0.set_sample_rate(self.samp_rate)

    def get_chan_width(self):
        return self.chan_width

    def set_chan_width(self, chan_width):
        self.chan_width = chan_width
        self.set_chan_filter(firdes.low_pass(1.0,int(self.samp_rate),(self.chan_width/2.2),(self.chan_width/3),firdes.WIN_HAMMING,6.76))
        self.low_pass_filter_1_1.set_taps(firdes.low_pass(5, self.chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0_1.set_taps(firdes.low_pass(5, self.chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0_0_0.set_taps(firdes.low_pass(5, self.chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0_0.set_taps(firdes.low_pass(5, self.chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(5, self.chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(5, self.chan_width, 1200, 600, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.chan_width, self.bandwidth_3/2, (self.bandwidth_3/2)/3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.chan_width, self.bandwidth_2/2, (self.bandwidth_2/2)/3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.chan_width, self.bandwidth_1/2, (self.bandwidth_1/2)/3, firdes.WIN_HAMMING, 6.76))

    def get_chan_trigger_poll(self):
        return self.chan_trigger_poll

    def set_chan_trigger_poll(self, chan_trigger_poll):
        self.chan_trigger_poll = chan_trigger_poll
        self.set_trigs3(meteor_helper.trig_state(3,self.chan_trigger_poll))
        self.set_trigs2(meteor_helper.trig_state(2,self.chan_trigger_poll))
        self.set_trigs1(meteor_helper.trig_state(1,self.chan_trigger_poll))
        self.set_cur_time(meteor_helper.current_time(self.chan_trigger_poll))

    def get_xx(self):
        return self.xx

    def set_xx(self, xx):
        self.xx = xx
        self.set_iagc(self.xx)

    def get_trigs3(self):
        return self.trigs3

    def set_trigs3(self, trigs3):
        self.trigs3 = trigs3
        self.set_trig_state_3_0_0_0(self.trigs3[3])
        self.set_trig_state_3_0_0(self.trigs3[2])
        self.set_trig_state_3_0(self.trigs3[1])
        self.set_trig_state_3(self.trigs3[0])

    def get_trigs2(self):
        return self.trigs2

    def set_trigs2(self, trigs2):
        self.trigs2 = trigs2
        self.set_trig_state_2_0_0_0(self.trigs2[3])
        self.set_trig_state_2_0_0(self.trigs2[2])
        self.set_trig_state_2_0(self.trigs2[1])
        self.set_trig_state_2(self.trigs2[0])

    def get_trigs1(self):
        return self.trigs1

    def set_trigs1(self, trigs1):
        self.trigs1 = trigs1
        self.set_trig_state_1_0_0_0(self.trigs1[3])
        self.set_trig_state_1_0_0(self.trigs1[2])
        self.set_trig_state_1_0(self.trigs1[1])
        self.set_trig_state_1(self.trigs1[0])

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh
        self._thresh_slider.set_value(self.thresh)
        self._thresh_text_box.set_value(self.thresh)
        self.set_chan_write_3(meteor_helper.write_chan(3,self.chan3_value,self.freq3,self.thresh,self.record_3,self.dc_gain_3))
        self.set_chan_write_2(meteor_helper.write_chan(2,self.chan2_value,self.freq2,self.thresh,self.record_2,self.dc_gain_2))
        self.set_chan_write_1(meteor_helper.write_chan(1,self.chan1_value,self.freq1,self.thresh,self.record_1,self.dc_gain_1))

    def get_record_3(self):
        return self.record_3

    def set_record_3(self, record_3):
        self.record_3 = record_3
        self._record_3_check_box.set_value(self.record_3)
        self.set_chan_write_3(meteor_helper.write_chan(3,self.chan3_value,self.freq3,self.thresh,self.record_3,self.dc_gain_3))

    def get_record_2(self):
        return self.record_2

    def set_record_2(self, record_2):
        self.record_2 = record_2
        self._record_2_check_box.set_value(self.record_2)
        self.set_chan_write_2(meteor_helper.write_chan(2,self.chan2_value,self.freq2,self.thresh,self.record_2,self.dc_gain_2))

    def get_record_1(self):
        return self.record_1

    def set_record_1(self, record_1):
        self.record_1 = record_1
        self._record_1_check_box.set_value(self.record_1)
        self.set_chan_write_1(meteor_helper.write_chan(1,self.chan1_value,self.freq1,self.thresh,self.record_1,self.dc_gain_1))

    def get_input_filter(self):
        return self.input_filter

    def set_input_filter(self, input_filter):
        self.input_filter = input_filter
        self.set_input_len(len(self.input_filter))
        self.freq_xlating_fir_filter_xxx_1.set_taps((self.input_filter))

    def get_freq3(self):
        return self.freq3

    def set_freq3(self, freq3):
        self.freq3 = freq3
        self.set_F3(self.freq3-self.Fc)
        self.set_variable_static_text_0_0_0(self.freq3)
        self._freq3_text_box.set_value(self.freq3)
        self.set_chan_write_3(meteor_helper.write_chan(3,self.chan3_value,self.freq3,self.thresh,self.record_3,self.dc_gain_3))

    def get_freq2(self):
        return self.freq2

    def set_freq2(self, freq2):
        self.freq2 = freq2
        self.set_F2(self.freq2-self.Fc)
        self.set_variable_static_text_0_0(self.freq2)
        self._freq2_text_box.set_value(self.freq2)
        self.set_chan_write_2(meteor_helper.write_chan(2,self.chan2_value,self.freq2,self.thresh,self.record_2,self.dc_gain_2))

    def get_freq1(self):
        return self.freq1

    def set_freq1(self, freq1):
        self.freq1 = freq1
        self.set_F1(self.freq1-self.Fc)
        self.set_variable_static_text_0(self.freq1)
        self._freq1_text_box.set_value(self.freq1)
        self.set_chan_write_1(meteor_helper.write_chan(1,self.chan1_value,self.freq1,self.thresh,self.record_1,self.dc_gain_1))

    def get_dc_gain_3(self):
        return self.dc_gain_3

    def set_dc_gain_3(self, dc_gain_3):
        self.dc_gain_3 = dc_gain_3
        self._dc_gain_3_chooser.set_value(self.dc_gain_3)
        self.set_chan_write_3(meteor_helper.write_chan(3,self.chan3_value,self.freq3,self.thresh,self.record_3,self.dc_gain_3))
        self.blocks_multiply_const_vxx_1_0_0.set_k((self.dc_gain_3*5, ))

    def get_dc_gain_2(self):
        return self.dc_gain_2

    def set_dc_gain_2(self, dc_gain_2):
        self.dc_gain_2 = dc_gain_2
        self._dc_gain_2_chooser.set_value(self.dc_gain_2)
        self.set_chan_write_2(meteor_helper.write_chan(2,self.chan2_value,self.freq2,self.thresh,self.record_2,self.dc_gain_2))
        self.blocks_multiply_const_vxx_1_0.set_k((self.dc_gain_2*5, ))

    def get_dc_gain_1(self):
        return self.dc_gain_1

    def set_dc_gain_1(self, dc_gain_1):
        self.dc_gain_1 = dc_gain_1
        self._dc_gain_1_chooser.set_value(self.dc_gain_1)
        self.set_chan_write_1(meteor_helper.write_chan(1,self.chan1_value,self.freq1,self.thresh,self.record_1,self.dc_gain_1))
        self.blocks_multiply_const_vxx_1.set_k((self.dc_gain_1*5, ))

    def get_chan_filter(self):
        return self.chan_filter

    def set_chan_filter(self, chan_filter):
        self.chan_filter = chan_filter
        self.freq_xlating_fir_filter_xxx_0_0_0.set_taps((self.chan_filter))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.chan_filter))
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.chan_filter))
        self.set_filt_len(len(self.chan_filter))

    def get_chan3_value(self):
        return self.chan3_value

    def set_chan3_value(self, chan3_value):
        self.chan3_value = chan3_value
        self.set_chan_write_3(meteor_helper.write_chan(3,self.chan3_value,self.freq3,self.thresh,self.record_3,self.dc_gain_3))

    def get_chan2_value(self):
        return self.chan2_value

    def set_chan2_value(self, chan2_value):
        self.chan2_value = chan2_value
        self.set_chan_write_2(meteor_helper.write_chan(2,self.chan2_value,self.freq2,self.thresh,self.record_2,self.dc_gain_2))

    def get_chan1_value(self):
        return self.chan1_value

    def set_chan1_value(self, chan1_value):
        self.chan1_value = chan1_value
        self.set_chan_write_1(meteor_helper.write_chan(1,self.chan1_value,self.freq1,self.thresh,self.record_1,self.dc_gain_1))

    def get_bb_files(self):
        return self.bb_files

    def set_bb_files(self, bb_files):
        self.bb_files = bb_files
        self.set_thread_start_stats(meteor_helper.start_threads(self.bb_files))
        self.blocks_file_sink_0_0_0.open(self.bb_files[2])
        self.blocks_file_sink_0_0.open(self.bb_files[1 ])
        self.blocks_file_sink_0.open(self.bb_files[0])

    def get_Fc(self):
        return self.Fc

    def set_Fc(self, Fc):
        self.Fc = Fc
        self._Fc_text_box.set_value(self.Fc)
        self.set_F3(self.freq3-self.Fc)
        self.set_F2(self.freq2-self.Fc)
        self.set_F1(self.freq1-self.Fc)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.Fc)
        self.wxgui_fftsink2_0.set_baseband_freq(self.Fc)
        self.osmosdr_source_c_0.set_center_freq(self.Fc+(self.offset), 0)
        self.freq_xlating_fir_filter_xxx_1.set_center_freq((self.offset)+((self.Fc/1.0e6 * self.ppm))+self.fine)

    def get_variable_static_text_0_0_0(self):
        return self.variable_static_text_0_0_0

    def set_variable_static_text_0_0_0(self, variable_static_text_0_0_0):
        self.variable_static_text_0_0_0 = variable_static_text_0_0_0
        self._variable_static_text_0_0_0_static_text.set_value(self.variable_static_text_0_0_0)

    def get_variable_static_text_0_0(self):
        return self.variable_static_text_0_0

    def set_variable_static_text_0_0(self, variable_static_text_0_0):
        self.variable_static_text_0_0 = variable_static_text_0_0
        self._variable_static_text_0_0_static_text.set_value(self.variable_static_text_0_0)

    def get_variable_static_text_0(self):
        return self.variable_static_text_0

    def set_variable_static_text_0(self, variable_static_text_0):
        self.variable_static_text_0 = variable_static_text_0
        self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

    def get_trig_state_3_0_0_0(self):
        return self.trig_state_3_0_0_0

    def set_trig_state_3_0_0_0(self, trig_state_3_0_0_0):
        self.trig_state_3_0_0_0 = trig_state_3_0_0_0
        self._trig_state_3_0_0_0_static_text.set_value(self.trig_state_3_0_0_0)

    def get_trig_state_3_0_0(self):
        return self.trig_state_3_0_0

    def set_trig_state_3_0_0(self, trig_state_3_0_0):
        self.trig_state_3_0_0 = trig_state_3_0_0
        self._trig_state_3_0_0_static_text.set_value(self.trig_state_3_0_0)

    def get_trig_state_3_0(self):
        return self.trig_state_3_0

    def set_trig_state_3_0(self, trig_state_3_0):
        self.trig_state_3_0 = trig_state_3_0
        self._trig_state_3_0_static_text.set_value(self.trig_state_3_0)

    def get_trig_state_3(self):
        return self.trig_state_3

    def set_trig_state_3(self, trig_state_3):
        self.trig_state_3 = trig_state_3
        self._trig_state_3_static_text.set_value(self.trig_state_3)

    def get_trig_state_2_0_0_0(self):
        return self.trig_state_2_0_0_0

    def set_trig_state_2_0_0_0(self, trig_state_2_0_0_0):
        self.trig_state_2_0_0_0 = trig_state_2_0_0_0
        self._trig_state_2_0_0_0_static_text.set_value(self.trig_state_2_0_0_0)

    def get_trig_state_2_0_0(self):
        return self.trig_state_2_0_0

    def set_trig_state_2_0_0(self, trig_state_2_0_0):
        self.trig_state_2_0_0 = trig_state_2_0_0
        self._trig_state_2_0_0_static_text.set_value(self.trig_state_2_0_0)

    def get_trig_state_2_0(self):
        return self.trig_state_2_0

    def set_trig_state_2_0(self, trig_state_2_0):
        self.trig_state_2_0 = trig_state_2_0
        self._trig_state_2_0_static_text.set_value(self.trig_state_2_0)

    def get_trig_state_2(self):
        return self.trig_state_2

    def set_trig_state_2(self, trig_state_2):
        self.trig_state_2 = trig_state_2
        self._trig_state_2_static_text.set_value(self.trig_state_2)

    def get_trig_state_1_0_0_0(self):
        return self.trig_state_1_0_0_0

    def set_trig_state_1_0_0_0(self, trig_state_1_0_0_0):
        self.trig_state_1_0_0_0 = trig_state_1_0_0_0
        self._trig_state_1_0_0_0_static_text.set_value(self.trig_state_1_0_0_0)

    def get_trig_state_1_0_0(self):
        return self.trig_state_1_0_0

    def set_trig_state_1_0_0(self, trig_state_1_0_0):
        self.trig_state_1_0_0 = trig_state_1_0_0
        self._trig_state_1_0_0_static_text.set_value(self.trig_state_1_0_0)

    def get_trig_state_1_0(self):
        return self.trig_state_1_0

    def set_trig_state_1_0(self, trig_state_1_0):
        self.trig_state_1_0 = trig_state_1_0
        self._trig_state_1_0_static_text.set_value(self.trig_state_1_0)

    def get_trig_state_1(self):
        return self.trig_state_1

    def set_trig_state_1(self, trig_state_1):
        self.trig_state_1 = trig_state_1
        self._trig_state_1_static_text.set_value(self.trig_state_1)

    def get_thread_start_stats(self):
        return self.thread_start_stats

    def set_thread_start_stats(self, thread_start_stats):
        self.thread_start_stats = thread_start_stats

    def get_rfg(self):
        return self.rfg

    def set_rfg(self, rfg):
        self.rfg = rfg
        self._rfg_slider.set_value(self.rfg)
        self._rfg_text_box.set_value(self.rfg)
        self.osmosdr_source_c_0.set_gain(25 if self.iagc else self.rfg, 0)

    def get_post_det_rate(self):
        return self.post_det_rate

    def set_post_det_rate(self, post_det_rate):
        self.post_det_rate = post_det_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.post_det_rate)
        self.keep_one_in_n_0_0_0_0.set_n(int(self.detector_rate/self.post_det_rate))
        self.blocks_keep_one_in_n_0_0_0_1.set_n(int(self.detector_rate/self.post_det_rate))
        self.blocks_keep_one_in_n_0_0_0.set_n(int(self.detector_rate/self.post_det_rate))

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self._offset_slider.set_value(self.offset)
        self._offset_text_box.set_value(self.offset)
        self.osmosdr_source_c_0.set_center_freq(self.Fc+(self.offset), 0)
        self.freq_xlating_fir_filter_xxx_1.set_center_freq((self.offset)+((self.Fc/1.0e6 * self.ppm))+self.fine)

    def get_input_len(self):
        return self.input_len

    def set_input_len(self, input_len):
        self.input_len = input_len

    def get_iagc(self):
        return self.iagc

    def set_iagc(self, iagc):
        self.iagc = iagc
        self._iagc_check_box.set_value(self.iagc)
        self.osmosdr_source_c_0.set_gain_mode(self.iagc, 0)
        self.osmosdr_source_c_0.set_gain(25 if self.iagc else self.rfg, 0)

    def get_fine(self):
        return self.fine

    def set_fine(self, fine):
        self.fine = fine
        self._fine_slider.set_value(self.fine)
        self._fine_text_box.set_value(self.fine)
        self.freq_xlating_fir_filter_xxx_1.set_center_freq((self.offset)+((self.Fc/1.0e6 * self.ppm))+self.fine)

    def get_filt_len(self):
        return self.filt_len

    def set_filt_len(self, filt_len):
        self.filt_len = filt_len

    def get_detector_rate(self):
        return self.detector_rate

    def set_detector_rate(self, detector_rate):
        self.detector_rate = detector_rate
        self.wxgui_waterfallsink2_0_0_0_0.set_sample_rate(self.detector_rate/2)
        self.wxgui_waterfallsink2_0_0_0.set_sample_rate(self.detector_rate/2)
        self.wxgui_waterfallsink2_0_0.set_sample_rate(self.detector_rate/2)
        self.single_pole_iir_filter_xx_0_0_0.set_taps(1.0/(self.detector_rate/10))
        self.single_pole_iir_filter_xx_0_0.set_taps(1.0/(self.detector_rate/10))
        self.single_pole_iir_filter_xx_0.set_taps(1.0/(self.detector_rate/10))
        self.keep_one_in_n_0_0_0_0.set_n(int(self.detector_rate/self.post_det_rate))
        self.blocks_keep_one_in_n_0_0_0_1.set_n(int(self.detector_rate/self.post_det_rate))
        self.blocks_keep_one_in_n_0_0_0.set_n(int(self.detector_rate/self.post_det_rate))

    def get_cur_time(self):
        return self.cur_time

    def set_cur_time(self, cur_time):
        self.cur_time = cur_time
        self._cur_time_static_text.set_value(self.cur_time)

    def get_chan_write_3(self):
        return self.chan_write_3

    def set_chan_write_3(self, chan_write_3):
        self.chan_write_3 = chan_write_3

    def get_chan_write_2(self):
        return self.chan_write_2

    def set_chan_write_2(self, chan_write_2):
        self.chan_write_2 = chan_write_2

    def get_chan_write_1(self):
        return self.chan_write_1

    def set_chan_write_1(self, chan_write_1):
        self.chan_write_1 = chan_write_1

    def get_bandwidth_3(self):
        return self.bandwidth_3

    def set_bandwidth_3(self, bandwidth_3):
        self.bandwidth_3 = bandwidth_3
        self._bandwidth_3_chooser.set_value(self.bandwidth_3)
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.chan_width, self.bandwidth_3/2, (self.bandwidth_3/2)/3, firdes.WIN_HAMMING, 6.76))

    def get_bandwidth_2(self):
        return self.bandwidth_2

    def set_bandwidth_2(self, bandwidth_2):
        self.bandwidth_2 = bandwidth_2
        self._bandwidth_2_chooser.set_value(self.bandwidth_2)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.chan_width, self.bandwidth_2/2, (self.bandwidth_2/2)/3, firdes.WIN_HAMMING, 6.76))

    def get_bandwidth_1(self):
        return self.bandwidth_1

    def set_bandwidth_1(self, bandwidth_1):
        self.bandwidth_1 = bandwidth_1
        self._bandwidth_1_chooser.set_value(self.bandwidth_1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.chan_width, self.bandwidth_1/2, (self.bandwidth_1/2)/3, firdes.WIN_HAMMING, 6.76))

    def get_F3(self):
        return self.F3

    def set_F3(self, F3):
        self.F3 = F3
        self.freq_xlating_fir_filter_xxx_0_0_0.set_center_freq((-self.F3))

    def get_F2(self):
        return self.F2

    def set_F2(self, F2):
        self.F2 = F2
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((-self.F2))

    def get_F1(self):
        return self.F1

    def set_F1(self, F1):
        self.F1 = F1
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((-self.F1))


def argument_parser():
    description = 'Meteor detection using broadcast VHF'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--agc", dest="agc", type="intx", default=0,
        help="Set AGC Enable [default=%default]")
    parser.add_option(
        "", "--bw1", dest="bw1", type="intx", default=500,
        help="Set Detector Bandwidth Ch1 [default=%default]")
    parser.add_option(
        "", "--bw2", dest="bw2", type="intx", default=500,
        help="Set Detector Bandwidth Ch2 [default=%default]")
    parser.add_option(
        "", "--bw3", dest="bw3", type="intx", default=500,
        help="Set Detector Bandwidth Ch3 [default=%default]")
    parser.add_option(
        "", "--cfreq", dest="cfreq", type="eng_float", default=eng_notation.num_to_str(216.980e6),
        help="Set Center Frequency [default=%default]")
    parser.add_option(
        "", "--devid", dest="devid", type="string", default='rtl=0',
        help="Set Device ID [default=%default]")
    parser.add_option(
        "", "--dgain1", dest="dgain1", type="intx", default=1,
        help="Set DC Gain Chan 1 [default=%default]")
    parser.add_option(
        "", "--dgain2", dest="dgain2", type="intx", default=1,
        help="Set DC Gain Chan 2 [default=%default]")
    parser.add_option(
        "", "--dgain3", dest="dgain3", type="intx", default=1,
        help="Set DC Gain Chan 3 [default=%default]")
    parser.add_option(
        "", "--f1", dest="f1", type="eng_float", default=eng_notation.num_to_str(216.970e6),
        help="Set F1 Frequency [default=%default]")
    parser.add_option(
        "", "--f2", dest="f2", type="eng_float", default=eng_notation.num_to_str(216.980e6),
        help="Set F2 Frequency [default=%default]")
    parser.add_option(
        "", "--f3", dest="f3", type="eng_float", default=eng_notation.num_to_str(216.990e6),
        help="Set F3 Frequency [default=%default]")
    parser.add_option(
        "", "--ftune", dest="ftune", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set Fine Tuning [default=%default]")
    parser.add_option(
        "", "--offs", dest="offs", type="eng_float", default=eng_notation.num_to_str(25.0e3),
        help="Set LO Offset [default=%default]")
    parser.add_option(
        "", "--ppm", dest="ppm", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set PPM LO Accuracy [default=%default]")
    parser.add_option(
        "", "--rfgain", dest="rfgain", type="eng_float", default=eng_notation.num_to_str(25),
        help="Set RF Gain [default=%default]")
    parser.add_option(
        "", "--srate", dest="srate", type="eng_float", default=eng_notation.num_to_str(1.0e6),
        help="Set Sample Rate [default=%default]")
    parser.add_option(
        "", "--trig", dest="trig", type="eng_float", default=eng_notation.num_to_str(5.5),
        help="Set Trigger Threshold [default=%default]")
    return parser


def main(top_block_cls=meteor_detector, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(agc=options.agc, bw1=options.bw1, bw2=options.bw2, bw3=options.bw3, cfreq=options.cfreq, devid=options.devid, dgain1=options.dgain1, dgain2=options.dgain2, dgain3=options.dgain3, f1=options.f1, f2=options.f2, f3=options.f3, ftune=options.ftune, offs=options.offs, ppm=options.ppm, rfgain=options.rfgain, srate=options.srate, trig=options.trig)
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
