#!/usr/bin/env python

import sys, os
import pango
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class GTK_Main:

	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Webcam Streamer")
		window.set_default_size(600, 400)
		window.connect("destroy", gtk.main_quit, "WM destroy")
                self.sstate = 'preparing'

                red=gtk.gdk.color_parse('grey')
                eb=gtk.EventBox()
                eb.modify_bg(gtk.STATE_NORMAL, red)
                window.add(eb)

		windows = gtk.ScrolledWindow()
		windows.set_size_request(600, 400)
		eb.add(windows)

		hbox0 = gtk.HBox(True)
		windows.add_with_viewport(hbox0)

		vbox = gtk.VBox()
		vbox.set_border_width(10)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		hbox.set_border_width(10)
		hbox.pack_start(gtk.Label())
		self.button = gtk.Button("Start Stream")
		self.button.connect("clicked", self.start_stop)
		hbox.pack_start(self.button, False)
		self.button2 = gtk.Button("Quit")
		self.button2.connect("clicked", self.exit)
		hbox.pack_start(self.button2, False)
                self.statuslabel = gtk.Label()
                self.statuslabel.modify_font(pango.FontDescription("sans bold 14"))
                self.statuslabel.set_justify(gtk.JUSTIFY_RIGHT);
                self.statuslabel.set_markup("<span background='blue'>Camera started...Ready to stream</span>")
		vbox.pack_start(self.statuslabel, False)
                hbox0.pack_start(vbox, False)

		vbox2 = gtk.VBox()
		vbox2.set_border_width(10)

                self.devlabel = gtk.Label("Input devices")
                self.devlabel.modify_font(pango.FontDescription("sans bold 10"))
                self.devlabel.set_justify(gtk.JUSTIFY_RIGHT);
		vbox2.pack_start(self.devlabel, False)
		vbox2.pack_start(gtk.HSeparator(), False)

		hbox2 = gtk.HBox(True)
		vbox2.pack_start(hbox2, False)
                self.combodevice = gtk.combo_box_new_text()
                self.combodevice.append_text("/dev/video0")
                self.combodevice.append_text("/dev/video1")
                self.combodevice.append_text("/dev/video2")
                self.combodevice.append_text("/dev/video3")
                self.combodevice.set_active(0)
		hbox2.pack_start(gtk.Label("Video device : "), True)
		hbox2.pack_start(self.combodevice, True)

		hbox21 = gtk.HBox(True)
		vbox2.pack_start(hbox21, False)
                self.vdevicetype = gtk.combo_box_new_text()
                self.vdevicetype.append_text("v4l")
                self.vdevicetype.append_text("v4l2")
                self.vdevicetype.set_active(1)
		hbox21.pack_start(gtk.Label("Driver type : "), True)
		hbox21.pack_start(self.vdevicetype, True)

		hbox3 = gtk.HBox(True)
		vbox2.pack_start(hbox3, False)
		hbox3.pack_start(gtk.Label("Audio device : "), True)
                self.comboadevice = gtk.combo_box_new_text()
                self.comboadevice.append_text("/dev/dsp")
                self.comboadevice.append_text("/dev/dsp1")
                self.comboadevice.append_text("/dev/dsp2")
                self.comboadevice.append_text("/dev/dsp3")
                self.comboadevice.set_active(0)
		hbox3.pack_start(self.comboadevice, True)

                self.vparamslabel = gtk.Label("Video parameters")
                self.vparamslabel.set_justify(gtk.JUSTIFY_RIGHT);
                self.vparamslabel.modify_font(pango.FontDescription("sans bold 10"))
		vbox2.pack_start(self.vparamslabel, False)
		vbox2.pack_start(gtk.HSeparator(), False)

		hbox4 = gtk.HBox(True)
		vbox2.pack_start(hbox4, False)
                self.combovsize = gtk.combo_box_new_text()
                self.combovsize.append_text("160x128")
                self.combovsize.append_text("320x240")
                self.combovsize.append_text("360x288")
                self.combovsize.append_text("640x480")
                self.combovsize.append_text("720x576")
                self.combovsize.set_active(1)
		hbox4.pack_start(gtk.Label("Video size : "), True)
		hbox4.pack_start(self.combovsize, True)

		hbox5 = gtk.HBox(True)
		vbox2.pack_start(hbox5, False)
		hbox5.pack_start(gtk.Label("Framerate : "), True)
                self.comboframerate = gtk.combo_box_new_text()
                self.comboframerate.append_text("25")
                self.comboframerate.append_text("25:2")
                self.comboframerate.append_text("25:3")
                self.comboframerate.append_text("25:4")
                self.comboframerate.append_text("25:5")
                self.comboframerate.set_active(1)
		hbox5.pack_start(self.comboframerate, True)

		hbox6 = gtk.HBox(True)
		vbox2.pack_start(hbox6, False)
		hbox6.pack_start(gtk.Label("Video quality : "), True)
                self.combovquality = gtk.combo_box_new_text()
                self.combovquality.append_text("0")
                self.combovquality.append_text("1")
                self.combovquality.append_text("2")
                self.combovquality.append_text("3")
                self.combovquality.append_text("4")
                self.combovquality.append_text("5")
                self.combovquality.append_text("6")
                self.combovquality.append_text("7")
                self.combovquality.append_text("8")
                self.combovquality.append_text("9")
                self.combovquality.append_text("10")
                self.combovquality.append_text("11")
                self.combovquality.append_text("12")
                self.combovquality.append_text("13")
                self.combovquality.append_text("14")
                self.combovquality.append_text("15")
                self.combovquality.append_text("16")
                self.combovquality.append_text("17")
                self.combovquality.append_text("18")
                self.combovquality.append_text("19")
                self.combovquality.append_text("20")
                self.combovquality.append_text("21")
                self.combovquality.append_text("22")
                self.combovquality.append_text("23")
                self.combovquality.append_text("24")
                self.combovquality.append_text("25")
                self.combovquality.append_text("26")
                self.combovquality.append_text("27")
                self.combovquality.append_text("28")
                self.combovquality.append_text("29")
                self.combovquality.append_text("30")
                self.combovquality.append_text("31")
                self.combovquality.append_text("32")
                self.combovquality.append_text("33")
                self.combovquality.append_text("34")
                self.combovquality.append_text("35")
                self.combovquality.append_text("36")
                self.combovquality.append_text("37")
                self.combovquality.append_text("38")
                self.combovquality.append_text("39")
                self.combovquality.append_text("40")
                self.combovquality.append_text("41")
                self.combovquality.append_text("42")
                self.combovquality.append_text("43")
                self.combovquality.append_text("44")
                self.combovquality.append_text("45")
                self.combovquality.append_text("46")
                self.combovquality.append_text("47")
                self.combovquality.append_text("48")
                self.combovquality.append_text("49")
                self.combovquality.append_text("50")
                self.combovquality.append_text("51")
                self.combovquality.append_text("52")
                self.combovquality.append_text("53")
                self.combovquality.append_text("54")
                self.combovquality.append_text("55")
                self.combovquality.append_text("56")
                self.combovquality.append_text("57")
                self.combovquality.append_text("58")
                self.combovquality.append_text("59")
                self.combovquality.append_text("60")
                self.combovquality.append_text("61")
                self.combovquality.append_text("62")
                self.combovquality.append_text("63")
                self.combovquality.set_active(16)
		hbox6.pack_start(self.combovquality, True)

                self.aparamslabel = gtk.Label("Audio parameters")
                self.aparamslabel.set_justify(gtk.JUSTIFY_RIGHT);
                self.aparamslabel.modify_font(pango.FontDescription("sans bold 10"))
		vbox2.pack_start(self.aparamslabel, False)
		vbox2.pack_start(gtk.HSeparator(), False)

		hbox7 = gtk.HBox(True)
		vbox2.pack_start(hbox7, False)
                self.comboaquality = gtk.combo_box_new_text()
                self.comboaquality.append_text("-0.1")
                self.comboaquality.append_text("0")
                self.comboaquality.append_text("0.1")
                self.comboaquality.append_text("0.2")
                self.comboaquality.append_text("0.3")
                self.comboaquality.append_text("0.4")
                self.comboaquality.append_text("0.5")
                self.comboaquality.append_text("0.6")
                self.comboaquality.append_text("0.7")
                self.comboaquality.append_text("0.8")
                self.comboaquality.append_text("0.9")
                self.comboaquality.append_text("1.0")
                self.comboaquality.set_active(3)
		hbox7.pack_start(gtk.Label("Audio quality : "), True)
		hbox7.pack_start(self.comboaquality, True)

		hbox8 = gtk.HBox(True)
		vbox2.pack_start(hbox8, False)
		hbox8.pack_start(gtk.Label("Audio channels : "), True)
                self.comboachannels = gtk.combo_box_new_text()
                self.comboachannels.append_text("1")
                self.comboachannels.append_text("2")
                self.comboachannels.set_active(0)
		hbox8.pack_start(self.comboachannels, True)

		hbox9 = gtk.HBox(True)
		vbox2.pack_start(hbox9, False)
		hbox9.pack_start(gtk.Label("Audio rate : "), True)
                self.comboarate = gtk.combo_box_new_text()
                self.comboarate.append_text("11025")
                self.comboarate.append_text("22050")
                self.comboarate.append_text("44100")
                self.comboarate.append_text("48000")
                self.comboarate.set_active(1)
		hbox9.pack_start(self.comboarate, True)

                self.sconfiglabel = gtk.Label("Server Configuration")
                self.sconfiglabel.set_justify(gtk.JUSTIFY_RIGHT);
                self.sconfiglabel.modify_font(pango.FontDescription("sans bold 10"))
		vbox2.pack_start(self.sconfiglabel, False)
		vbox2.pack_start(gtk.HSeparator(), False)

		hbox10 = gtk.HBox(True)
		vbox2.pack_start(hbox10, False)
		hbox10.pack_start(gtk.Label("Server : "), True)
                self.servername = gtk.Entry()
                self.servername.set_text("www.giss.tv")
		hbox10.pack_start(self.servername, True)

		hbox11 = gtk.HBox(True)
		vbox2.pack_start(hbox11, False)
		hbox11.pack_start(gtk.Label("Port : "), True)
                self.portnumber = gtk.Entry()
                self.portnumber.set_text("8000")
		hbox11.pack_start(self.portnumber, True)

		hbox12 = gtk.HBox(True)
		vbox2.pack_start(hbox12, False)
		hbox12.pack_start(gtk.Label("Mountpoint : "), True)
                self.mountpoint = gtk.Entry()
                self.mountpoint.set_text("mountpoint.ogg")
		hbox12.pack_start(self.mountpoint, True)

		hbox13 = gtk.HBox(True)
		vbox2.pack_start(hbox13, False)
		hbox13.pack_start(gtk.Label("Password : "), True)
                self.password = gtk.Entry()
                self.password.set_text("xxxxx")
		hbox13.pack_start(self.password, True)

                self.smdatalabel = gtk.Label("Icecast Meta Data")
                self.smdatalabel.set_justify(gtk.JUSTIFY_RIGHT);
                self.smdatalabel.modify_font(pango.FontDescription("sans bold 10"))
		vbox2.pack_start(self.smdatalabel, False)
		vbox2.pack_start(gtk.HSeparator(), False)

		hbox14 = gtk.HBox(True)
		vbox2.pack_start(hbox14, False)
		hbox14.pack_start(gtk.Label("Name : "), True)
                self.name = gtk.Entry()
                self.name.set_text("")
		hbox14.pack_start(self.name, True)

		hbox15 = gtk.HBox(True)
		vbox2.pack_start(hbox15, False)
		hbox15.pack_start(gtk.Label("Description : "), True)
                self.description = gtk.Entry()
                self.description.set_text("")
		hbox15.pack_start(self.description, True)

		hbox16 = gtk.HBox(True)
		vbox2.pack_start(hbox16, False)
		hbox16.pack_start(gtk.Label("Genre : "), True)
                self.genre = gtk.Entry()
                self.genre.set_text("")
		hbox16.pack_start(self.genre, True)

		hbox17 = gtk.HBox(True)
		vbox2.pack_start(hbox17, False)
		hbox17.pack_start(gtk.Label("Url : "), True)
                self.url = gtk.Entry()
                self.url.set_text("")
		hbox17.pack_start(self.url, True)

                self.srecordlabel = gtk.Label("Recording")
                self.srecordlabel.set_justify(gtk.JUSTIFY_RIGHT);
                self.srecordlabel.modify_font(pango.FontDescription("sans bold 10"))
		vbox2.pack_start(self.srecordlabel, False)
		vbox2.pack_start(gtk.HSeparator(), False)

		hbox18 = gtk.HBox(True)
		vbox2.pack_start(hbox18, False)
		hbox18.pack_start(gtk.Label("Dump to file : "), True)
                self.recfile = gtk.Entry()
                self.recfile.set_text(".ogg")
		hbox18.pack_start(self.recfile, True)
                self.fcbutton = gtk.Button("Browse")
		self.fcbutton.connect("clicked", self.on_file_dialog)
		hbox18.pack_start(self.fcbutton, True)

                hbox0.pack_start(vbox2, False)

		window.show_all()

		# Set up the gstreamer pipeline
                devname = self.combodevice.get_active_text()
                if self.vdevicetype.get_active_text() == "v4l":
		  self.player = gst.parse_launch ("v4lsrc device="+devname+" !  video/x-raw-yuv,width=320,height=240 ! autovideosink")
                else:
		  self.player = gst.parse_launch ("v4l2src device="+devname+" ! video/x-raw-yuv,width=320,height=240 ! autovideosink")

		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		self.player.set_state(gst.STATE_PLAYING)

	def stop_stream(self):
		self.button.set_label("Start Stream")
		self.player.set_state(gst.STATE_NULL)
                devname = self.combodevice.get_active_text()
                if self.vdevicetype.get_active_text() == "v4l":
		   self.player = gst.parse_launch ("v4lsrc device="+devname+" !  video/x-raw-yuv,width=320,height=240 ! autovideosink")
                else:
		   self.player = gst.parse_launch ("v4l2src device="+devname+" !  video/x-raw-yuv,width=320,height=240 ! autovideosink")
		bus = self.player.get_bus()
	        bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		self.player.set_state(gst.STATE_PLAYING)

	def stop_cam(self):
		self.button.set_label("Start Stream")
		self.player.set_state(gst.STATE_NULL)

	def start_stop(self, w):
		if self.button.get_label() == "Start Stream":
			self.button.set_label("Stop Stream")
			self.player.set_state(gst.STATE_NULL)
                        dumpfile = self.recfile.get_text()
                        if dumpfile  == ".ogg":
                           print "No dump file" 	 
                        else:
                           print "Dumping to :", dumpfile
                        pipelist= []
                        devname = self.combodevice.get_active_text()
                        if self.vdevicetype.get_active_text() == "v4l":
                           pipelist.append("v4lsrc device="+devname)
                        else:
                           pipelist.append("v4l2src device="+devname)
                        pipelist.append("video/x-raw-yuv,width=320,height=240") 
                        pipelist.append("queue")
                        pipelist.append("videorate")
                        framerate=self.comboframerate.get_active_text()
                        framerate=framerate.replace(":","/")
                        pipelist.append("video/x-raw-yuv,framerate="+framerate)
                        pipelist.append("videoscale")
                        size=self.combovsize.get_active_text()
                        sizes=size.split("x");
                        pipelist.append("video/x-raw-yuv,width="+sizes[0]+",height="+sizes[1])
                        pipelist.append("ffmpegcolorspace")
                        pipelist.append("tee name=tscreen")
                        pipelist.append("queue")
                        pipelist.append("autovideosink tscreen.")
                        pipelist.append("queue")
                        vquality = self.combovquality.get_active_text()
                        pipelist.append("theoraenc quality="+vquality)
                        pipelist.append("queue")

                        #audio input
                        adevice=self.comboadevice.get_active_text()
                        pipelist.append("oggmux name=mux osssrc device="+adevice)
                        arate=self.comboarate.get_active_text()
                        achannels=self.comboachannels.get_active_text()
                        pipelist.append("audio/x-raw-int,rate="+arate+",channels="+achannels)
                        pipelist.append("queue")
                        pipelist.append("audioconvert")
                        aquality=self.comboaquality.get_active_text()
                        pipelist.append("vorbisenc quality="+aquality)
                        pipelist.append("queue")
                        pipelist.append("mux. mux.")
                        pipelist.append("queue")

                        #recording part
                        if dumpfile  != ".ogg":
                          pipelist.append("tee name= tfile")
                          pipelist.append("queue")
                          pipelist.append("filesink location="+dumpfile+" tfile.")
                          pipelist.append("queue")

                        #last but not least streaming
                        server=self.servername.get_text()
                        port=self.portnumber.get_text()
                        mount=self.mountpoint.get_text()
                        password=self.password.get_text()
                        sname=self.name.get_text()
                        sdesc=self.description.get_text()
                        sgenre=self.genre.get_text()
                        surl=self.url.get_text()
                        pipelist.append("shout2send ip="+server+" port="+port+" mount="+mount+" password="+password+" streamname="+sname+" description="+sdesc+" genre="+sgenre+" url="+surl)

                        # ouf!
                        pipeline = " ! ".join(pipelist)
                        print "gstreamer command : ", pipeline
		        self.player = gst.parse_launch (pipeline)
		        bus = self.player.get_bus()
	        	bus.add_signal_watch()
		        bus.enable_sync_message_emission()
		        bus.connect("message", self.on_message)
		        bus.connect("sync-message::element", self.on_sync_message)
		        self.player.set_state(gst.STATE_PLAYING)
                        self.statuslabel.set_markup("<span background='green'>Streaming at "+framerate+" frames per second</span>")
                        self.sstate = 'running'

		else:
                        self.statuslabel.set_markup("<span background='blue'>Camera started...Ready to stream</span>")
                        self.stop_stream()
                        self.sstate = 'preparing'

	def exit(self, widget, data=None):
		gtk.main_quit()

	def on_file_dialog(self, w):
                self.fchooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                self.fchooser.set_default_response(gtk.RESPONSE_OK)
                response = self.fchooser.run()
                if response == gtk.RESPONSE_OK:
                  self.recfile.set_text(self.fchooser.get_filename())
                response = self.fchooser.destroy()

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_ERROR:
                   if self.sstate == 'preparing':
                      self.statuslabel.set_markup("<span background='red'>Error initializing camera...Check your devices</span>")
                      self.stop_cam()
                   if self.sstate == 'running':
                      self.statuslabel.set_markup("<span background='red'>Error starting stream...Check your parameters</span>")
                      self.stop_stream()
                      self.sstate = 'preparing'
		   err, debug = message.parse_error()
		   print "Error: %s" % err, debug

	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)

GTK_Main()
gtk.gdk.threads_init()
gtk.main()

