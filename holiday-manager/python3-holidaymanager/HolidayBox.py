#!/usr/bin/env python3


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib,Gdk

from . import HolidayManager
from . import settings
import gettext
gettext.textdomain(settings.TEXT_DOMAIN)
_ = gettext.gettext


import signal
import os
from datetime import datetime, date,timedelta
import n4d.client


class HolidayBox(Gtk.Box):

	DATE_RANGE_INCONSISTENT_ERROR=-12
	DATE_RANGE_INCOMPLETE_ERROR=-13
	DATE_EMPTY_ERROR=-14


	def __init__(self,app_name):
		
		Gtk.Box.__init__(self)

		'''
		context=ssl._create_unverified_context()
		self.n4d_holiday = n4dclient.ServerProxy("https://"+server+":9779",context=context,allow_none=True)
		'''
		self.app_name=app_name
		self.holidayManager=HolidayManager.HolidayManager()
		self.render_form()

	#def __init__

	def create_n4dClient(self,ticket):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)
					

	def render_form(self):
	
		builder=Gtk.Builder()
		builder.set_translation_domain(settings.TEXT_DOMAIN)
		ui_path=settings.RSRC_DIR + "/holiday-manager.ui"
		builder.add_from_file(ui_path)	

		self.css_file=settings.RSRC_DIR+"/holiday-manager.css"

		self.main_box=builder.get_object("holiday_box")
		self.edit_data_window=builder.get_object("edit_data_window")
		self.holiday_calendar=builder.get_object("calendar")
		self.date_separator_label=builder.get_object("date_separaror_label")
		self.date_separator=builder.get_object("date_separator")
		self.single_day_rb=builder.get_object("single_day_rb")
		self.single_day_entry=builder.get_object("single_day_entry")
		self.range_day_rb=builder.get_object("range_day_rb")
		self.range_day1_entry=builder.get_object("range_day1_entry")
		self.range_day2_entry=builder.get_object("range_day2_entry")
		self.remove_range_button=builder.get_object("remove_range_button")
		self.comment_label_separator=builder.get_object("comment_label_separator")
		self.comment_separator=builder.get_object("comment_separator")
		self.coment_day_entry=builder.get_object("day_comment_entry")
		self.add_day_button=builder.get_object("add_day_button")
		self.message_box=builder.get_object("message_box")
		self.edit_error_img=builder.get_object("edit_error_img")
		self.edit_message_label=builder.get_object("edit_message_label")
		self.save_day_button=builder.get_object("save_day_button")
		self.cancel_day_button=builder.get_object("cancel_day_button")
		
		self.list_day_box=builder.get_object("list_day_box")
	
		self.export_daylist_button=builder.get_object("export_daylist_button")
		self.import_daylist_button=builder.get_object("import_daylist_button")
		self.remove_daylist_button=builder.get_object("remove_daylist_button")
		self.calendar_message_box=builder.get_object("calendar_message_box")
		self.calendar_ok_img=builder.get_object("calendar_ok_img")
		self.calendar_error_img=builder.get_object("calendar_error_img")
		self.calendar_message=builder.get_object("calendar_message")

		self.pack_start(self.main_box,True,True,0)
		self.set_css_info()
		self.connect_signals()
		self.calendar_ok_img.hide()
		self.calendar_error_img.hide()
		self.edit_error_img.hide()
		self.edit_data_window.hide()
		self.init_calendar()
		#self.clear_days=True
		#self.day=""

	#def render_form	


	def set_css_info(self):
		
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path(self.css_file)
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.holiday_calendar.set_name("CALENDAR")
		self.coment_day_entry.set_name("CUSTOM-ENTRY")
		self.single_day_entry.set_name("CUSTOM-ENTRY")
		self.range_day1_entry.set_name("CUSTOM-ENTRY")
		self.range_day2_entry.set_name("CUSTOM-ENTRY")
		self.date_separator_label.set_name("HEADER-LABEL")
		self.date_separator.set_name("HEADER_SEPARATOR")
		self.comment_label_separator.set_name("HEADER-LABEL")
		self.comment_separator.set_name("HEADER_SEPARATOR")
		self.list_day_box.set_name("LIST_BACKGROUND")


	#def set_css_info	


	def connect_signals(self):
	
		self.single_day_rb.connect("toggled",self.day_toggled_button,"singleDay")
		self.range_day_rb.connect("toggled",self.day_toggled_button,"rangeDay")
		self.holiday_calendar.connect("month-changed",self.month_changed)
		self.holiday_calendar.connect("day_selected",self.day_selected)
		self.remove_range_button.connect("clicked",self.remove_range)
		self.add_day_button.connect("clicked",self.add_day_clicked)
		self.save_day_button.connect("clicked",self.save_day_clicked)
		self.cancel_day_button.connect("clicked",self.cancel_day_clicked)
		self.export_daylist_button.connect("clicked",self.export_daylist_clicked)
		self.import_daylist_button.connect("clicked",self.import_daylist_clicked)
		self.remove_daylist_button.connect("clicked",self.remove_daylist_clicked)

		self.edit_data_window.connect("delete_event",self.on_edit_delete_event)

	#def connect_signals	

	def on_edit_delete_event(self,window,event):

		window.hide()
		return True


	#def on_edit_delete_event

	def start_api_connect(self):

		gettext.textdomain(settings.TEXT_DOMAIN)
		self.init_calendar()
		self.get_holidaylist()
		self.hide_calendar_message_items()

	#def _start_api_connect	


	def init_calendar(self):

		self.range=False
		self.clear_days=False
		self.day=""
		self.days_inrange=[]
		current_date=date.today().strftime('%d/%m/%Y').split("/")
		current_month=int(current_date[1])-1
		current_year=int(current_date[2])

		self.holiday_calendar.select_day(0)
		self.holiday_calendar.select_month(current_month,current_year)
		self.single_day_rb.set_active(True)
		self.remove_range_button.set_sensitive(False)
		self.single_day_entry.set_text("")
		self.range_day1_entry.set_text("")
		self.range_day2_entry.set_text("")
		self.coment_day_entry.set_text("")
		self.edit_day=False


	#def init_calendar	
		

	def day_toggled_button (self,button,name):


		if button.get_active():
			self.holiday_calendar.clear_marks()


			if name=="singleDay":
				self.range=False
				self.range_day1_entry.set_text("")
				self.range_day2_entry.set_text("")
				self.remove_range_button.set_sensitive(False)
				self.hide_edit_message_items()

			else:
				self.holiday_calendar.select_day(0)
				self.range=True
				self.remove_range_button.set_sensitive(True)
				self.single_day_entry.set_text("")
				self.hide_edit_message_items()
	
	#def day_toggled_button

	def init_day_list(self):

		tmp=self.list_day_box.get_children()
		for item in tmp:
			self.list_day_box.remove(item)

	#def init_day_list

	def get_holidaylist(self):

		#Old n4d:result=self.n4d_holiday.read_conf(self.credentials,'HolidayListManager')['return']
		self.init_day_list()
		result=self.client.HolidayListManager.read_conf()

		holiday_list=result["info"]
		list_days=self.order_date(holiday_list)
		count=len(list_days)
	
		for item in list_days:
			date=item
			description=holiday_list[item]["description"]
			self.new_day_box(date,description,count)
			count-=1

	#def get_holidaylist	
	def new_day_box(self,date,description,count):

		day_vbox=Gtk.VBox()
		day_vbox.day=date
		day_vbox.description=description

		hbox=Gtk.HBox()

		if "-" in date:
			img=settings.RSRC_DIR + "/calendar_range_day.png"
		else:
			img=settings.RSRC_DIR +"/calendar_day.png"

		image=Gtk.Image.new_from_file(img)
		image.set_margin_left(5)
		image.set_margin_top(5)
		image.set_margin_bottom(5)
		image.set_halign(Gtk.Align.CENTER)
		image.set_valign(Gtk.Align.CENTER)
		
		day=Gtk.Label()
		day.set_text(date)
		day.set_margin_left(10)
		day.set_margin_right(5)
		day.set_margin_top(5)
		day.set_margin_bottom(5)
		day.set_width_chars(30)
		day.set_xalign(-1)
		day.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		day.set_name("DAY_NAME")

		day_description=Gtk.Label()
		day_description.set_text(description)
		day_description.set_margin_left(10)
		day_description.set_margin_right(5)
		day_description.set_margin_top(5)
		day_description.set_margin_bottom(5)
		day_description.set_width_chars(50)
		day_description.set_xalign(-1)
		day_description.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		day_description.set_name("DAY_NAME")


		manage_date=Gtk.Button()
		manage_date_image=Gtk.Image.new_from_file(settings.RSRC_DIR + '/manage_bell.svg')
		manage_date.add(manage_date_image)
		manage_date.set_margin_right(15)
		manage_date.set_halign(Gtk.Align.CENTER)
		manage_date.set_valign(Gtk.Align.CENTER)
		manage_date.set_name("EDIT_ITEM_BUTTON")
		manage_date.connect("clicked",self.manage_date_options,hbox)
		manage_date.set_tooltip_text(_("Manage date"))

		popover = Gtk.Popover()
		manage_date.popover=popover
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		edit_box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		edit_box.set_margin_left(10)
		edit_box.set_margin_right(10)
		edit_eb=Gtk.EventBox()
		edit_eb.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
		edit_eb.connect("button-press-event", self.edit_day_clicked,day_vbox)
		edit_eb.connect("motion-notify-event", self.mouse_over_popover)
		edit_eb.connect("leave-notify-event", self.mouse_exit_popover)
		edit_label=Gtk.Label()
		edit_label.set_text(_("Edit date"))
		edit_eb.add(edit_label)
		edit_eb.set_name("POPOVER_OFF")
		edit_box.add(edit_eb)
		
		delete_box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		delete_box.set_margin_left(10)
		delete_box.set_margin_right(10)
		delete_eb=Gtk.EventBox()
		delete_eb.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
		delete_eb.connect("button-press-event", self.remove_day_clicked,day_vbox)
		delete_eb.connect("motion-notify-event", self.mouse_over_popover)
		delete_eb.connect("leave-notify-event", self.mouse_exit_popover)
		delete_label=Gtk.Label()
		delete_label.set_text(_("Delete date"))
		delete_eb.add(delete_label)
		delete_eb.set_name("POPOVER_OFF")
		delete_box.add(delete_eb)

		vbox.pack_start(edit_box, True, True,8)
		vbox.pack_start(delete_box, True, True,8)
		
		vbox.show_all()
		popover.add(vbox)
		popover.set_position(Gtk.PositionType.BOTTOM)
		popover.set_relative_to(manage_date)

		hbox.pack_start(image,False,False,5)
		hbox.pack_start(day,False,False,5)
		hbox.pack_start(day_description,False,False,5)
		hbox.pack_end(manage_date,False,False,5)

		list_separator=Gtk.Separator()
		#list_separator.set_margin_top(5)
		list_separator.set_margin_left(80)
		list_separator.set_margin_right(20)

		if count!=1:
			list_separator.set_name("SEPARATOR")
		else:
			list_separator.set_name("WHITE_SEPARATOR")	

		day_vbox.pack_start(hbox,False,False,5)
		day_vbox.pack_end(list_separator,False,False,0)

		day_vbox.show_all()
		self.list_day_box.pack_start(day_vbox,False,False,0)
		self.list_day_box.queue_draw()
		day_vbox.queue_draw()			


	def order_date(self,listdays):

		tmp=[]
		order_date=[]

		if len(listdays)>0:
			for item in listdays:
				if "-" in item:
					date_toformat=item.split("-")[0]
				else:
					date_toformat=item

				datef=datetime.strptime(date_toformat,"%d/%m/%Y")
				x=()
				x=item,datef
				tmp.append(x)

		tmp.sort(key=lambda date:date[1])
		for item in tmp:
			order_date.append(item[0])

		return order_date

	#def order_date		


	def month_changed(self,widget):	

		self.holiday_calendar.select_day(0)
		self.holiday_calendar.clear_marks()


		if  self.clear_days:
			self.marked_range_days(0)

		else:
			date=self.range_day1_entry.get_text()
			if date!="":
				month_ref=self.holiday_calendar.get_date().month
				year_ref=self.holiday_calendar.get_date().year	

				split_date=self._splited_date(date)
				tmp_day=split_date[0]
				tmp_month=split_date[1]
				tmp_year=split_date[2]
	
				if tmp_month==month_ref and tmp_year==year_ref:
					self.holiday_calendar.mark_day(tmp_day)				
		

	#def month_changed							

	def day_selected(self,widget):
		

		date_selected=self.holiday_calendar.get_date()
		

		day_selected=date_selected.day
		if int(day_selected)!=0:
			if day_selected<10:
				day_selectedf="0"+str(day_selected)
			else:
				day_selectedf=day_selected	
			month_selected=date_selected.month+1
			if month_selected<10:
				month_selected="0"+str(month_selected)

			year_selected=date_selected.year
			date_format=str(day_selectedf)+"/"+str(month_selected)+"/"+str(year_selected)

			if not self.range:
				self.holiday_calendar.clear_marks()
				self.single_day_entry.set_text(date_format)
				self.range=False
				self.clear_days=True
			else:
				if self.range_day1_entry.get_text()=="":
					self.clear_days=False
					self.holiday_calendar.clear_marks()
					self.range_day1_entry.set_text(date_format)
					self.holiday_calendar.mark_day(day_selected)
					self.holiday_calendar.select_day(0)

				else:
					if self.range_day2_entry.get_text()=="":
						date1=datetime.strptime(self.range_day1_entry.get_text(),"%d/%m/%Y")
						date2=datetime.strptime(date_format,"%d/%m/%Y")
						if date2>date1:
							self.range=True
							self.clear_days=True
							self.range_day2_entry.set_text(date_format)	
							range_day=self.range_day1_entry.get_text()+"-"+self.range_day2_entry.get_text()
							self.marked_range_days(2,range_day)
							self.holiday_calendar.select_day(0)
							self.hide_edit_message_items()
						else:
							self.holiday_calendar.select_day(0)
							self.manage_message(True,HolidayBox.DATE_RANGE_INCONSISTENT_ERROR)	
	#def day_selected						

	
	def marked_range_days(self,monthref,range_day=None):


		if range_day!=None:
			if self.range:
				self.days_inrange=self.holidayManager.get_days_inrange(range_day)

		if monthref==0:
			ref_month=self.holiday_calendar.get_date().month
			ref_year=self.holiday_calendar.get_date().year

		elif monthref==1:
			if self.range:
				ref_date=self.range_day1_entry.get_text()
			else:
				ref_date=self.single_day_entry.get_text()
				
			split_date=self._splited_date(ref_date)
			ref_month=split_date[1]
			ref_year=split_date[2]

			self.holiday_calendar.select_month(ref_month,ref_year)

		else:
			split_date=self._splited_date(self.range_day2_entry.get_text())
			ref_month=split_date[1]
			ref_year=split_date[2]

		if self.range:
			for i in self.days_inrange:
				split_date=self._splited_date(i)
				tmp_day=split_date[0]
				tmp_month=split_date[1]
				tmp_year=split_date[2]
				if tmp_month==ref_month and tmp_year==ref_year:
					self.holiday_calendar.mark_day(tmp_day)
			
		else:
			if self.single_day_entry.get_text()!="":
				split_date=self._splited_date(self.single_day_entry.get_text())
				tmp_day=split_date[0]
				tmp_month=split_date[1]
				tmp_year=split_date[2]
				
				if tmp_month==ref_month and tmp_year==ref_year:
					self.holiday_calendar.mark_day(tmp_day)		

	#def marked_range_days			

	def _splited_date(self,date):

		splited_date=[]
		tmp_date=date.split("/")
		tmp_day=int(tmp_date[0])
		tmp_month=int(tmp_date[1])-1
		tmp_year=int(tmp_date[2])

		splited_date=[tmp_day,tmp_month,tmp_year]
		
		return splited_date

	#def _splited_date	

	def remove_range(self,widget):

		self.holiday_calendar.clear_marks()
		self.clear_days=False
		self.holiday_calendar.select_day(0)
		self.range_day1_entry.set_text("")
		self.range_day2_entry.set_text("")
		self.hide_edit_message_items()

	#def remove_range	


	def add_day_clicked(self,widget):
	
		self.init_calendar()
		self.hide_edit_message_items()
		self.hide_calendar_message_items()
		self.edit_data_window.set_title(_("Add date"))
		self.edit_data_window.show()

	#def add_day_clicked	


	def save_day_clicked(self,widget):

		result={}
		result["status"]=True
		error=False
		
		if self.range:
			day1=self.range_day1_entry.get_text()
			day2=self.range_day2_entry.get_text()
			new_day=day1+"-"+day2

		else:
			new_day=self.single_day_entry.get_text()

		comment=self.coment_day_entry.get_text()	

		if self.range and (day1=="" or day2=="") :
			error=True
			code=HolidayBox.DATE_RANGE_INCOMPLETE_ERROR
		else:	
			if new_day!="":
				if self.edit_day:
					if self.day!="" and self.day!=new_day:
						#Old n4d: result=self.n4d_holiday.delete_day(self.credentials,"HolidayListManager",self.day)['return']
						result=self.client.HolidayListManager.delete_day(self.day)
						code=result["code"]
					
				if result["status"]:			
					#result=self.holidayManager.add_day(new_day,comment)
					#Old n4d: result=self.n4d_holiday.add_day(self.credentials,'HolidayListManager',new_day,comment)['return']
					result=self.client.HolidayListManager.add_day(new_day,comment)					
					code=result["code"]
					if result["status"]:
						self.get_holidaylist()
						self.init_calendar()

					else:
						error=True
				else:
					error=True	
			else:
				error=True	
				code=HolidayBox.DATE_EMPTY_ERROR	

		if error:	
			self.manage_message(error,code)	
		else:
			self.edit_data_window.hide()
			self.manage_message(error,code)	

	#def save_day_clicked	

	def cancel_day_clicked(self,widget):

		self.edit_data_window.hide()

	#def cancel_day_clicked			
		
	def edit_day_clicked(self,widget,event,box):

		popover=box.get_children()[0].get_children()[3].popover.hide()

		self.init_calendar()
		self.hide_calendar_message_items()
		self.clear_days=True
		self.day=box.day
		comment_day=box.description
		self.edit_day=True
	
		if "-" in self.day:
			self.range=True
			self.holiday_calendar.clear_marks()
			tmp=self.day.split("-")
			self.range_day_rb.set_active(True)
			self.range_day1_entry.set_text(tmp[0])
			self.range_day2_entry.set_text(tmp[1])
			
		else:
			self.range=False
			self.holiday_calendar.clear_marks()
			self.single_day_rb.set_active(True)
			self.single_day_entry.set_text(self.day)
			
		self.marked_range_days(1,self.day)
		self.coment_day_entry.set_text(comment_day)
		self.hide_edit_message_items()
		self.edit_data_window.set_title(_("Edit date"))
		self.edit_data_window.show()

	#def edit_day_clicked	


	def remove_day_clicked(self,widget,event,box):

		popover=box.get_children()[0].get_children()[3].popover.hide()
		error=False

		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO, self.app_name)
		dialog.format_secondary_text(_("The date will be deleted. Do you want to continue?"))
		response=dialog.run()
		dialog.destroy()
		if response == Gtk.ResponseType.YES:	
			#Old n4d: result=self.n4d_holiday.delete_day(self.credentials,'HolidayListManager',self.day)['return']
			day=box.day
			result=self.client.HolidayListManager.delete_day(day)
	
			if result['status']:
				self.get_holidaylist()
				self.init_calendar()
			else:
				error=True

			self.manage_message(error,result['code'])	

	#def remove_day_clicked		


	def remove_daylist_clicked(self,widget):

		error=False
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO, self.app_name)
		dialog.format_secondary_text(_("The current list of dates will be deleted. Do you want to continue?"))
		response=dialog.run()
		dialog.destroy()
		if response == Gtk.ResponseType.YES:	
			#Old n4d: result=self.n4d_holiday.reset_holiday_list(self.credentials,'HolidayListManager')['return']
			result=self.client.HolidayListManager.reset_holiday_list()

			if result['status']:
				self.get_holidaylist()
				self.init_calendar()
			else:
				error=True

			self.manage_message(error,result['code'])

	#def remove_daylist_clicked		


	def export_daylist_clicked(self,widget):
	
		error=False
		dialog = Gtk.FileChooserDialog(_("Please choose a file to save day list"), None,
		Gtk.FileChooserAction.SAVE,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
		Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		dialog.set_do_overwrite_confirmation(True)
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			dest=dialog.get_filename()
			dialog.destroy()
			#Old n4d: result=self.n4d_holiday.export_holiday_list(self.credentials,'HolidayListManager',self.credentials[0],dest)['return']
			result=self.client.HolidayListManager.export_holiday_list(self.credentials[0],dest)

			if not result["status"]:
				error=True

			self.manage_message(error,result["code"])
		else:
			dialog.destroy()
		

	#def export_daylist_clicked
	

	def import_daylist_clicked(self,widget):

		error=False
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO, self.app_name)
		dialog.format_secondary_text(_("New dates list will be loaded and replace the existing configutarion. Do you want to continue?"))
		response=dialog.run()
		dialog.destroy()
		if response == Gtk.ResponseType.YES:
			dialog = Gtk.FileChooserDialog(_("Please choose a file to load dates list"), None,
			Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				orig=dialog.get_filename()
				dialog.destroy()
				#Old n4d: result=self.n4d_holiday.import_holiday_list(self.credentials,'HolidayListManager',orig)['return']
				result=self.client.HolidayListManager.import_holiday_list(orig)

				if result['status']:
					self.get_holidaylist()
				else:
					error=True	
			else:
				dialog.destroy()		
				
			self.manage_message(error,result["code"])	

	#def import_daylist_clicked			

	def manage_message(self,error,code):

		msg=self.get_msg(code)
		edit_date_errors=[self.holidayManager.LIST_BLOCK_ERROR,self.holidayManager.WRITE_LIST_ERROR,HolidayBox.DATE_RANGE_INCONSISTENT_ERROR,HolidayBox.DATE_RANGE_INCOMPLETE_ERROR,HolidayBox.DATE_EMPTY_ERROR]

		if error:
			if code in edit_date_errors:
				#self.edit_message_label.set_name("MSG_ERROR_LABEL")
				self.edit_error_img.show()
				self.message_box.set_name("ERROR_BOX")
				self.edit_message_label.set_text(msg)
				self.edit_message_label.show()
			else:
				#self.calendar_message.set_name("MSG_ERROR_LABEL")	
				self.calendar_message_box.set_name("ERROR_BOX")
				self.calendar_error_img.show()
				self.calendar_ok_img.hide()
				self.calendar_message.set_text(msg)
				self.calendar_message.show()	
		else:
			#self.calendar_message.set_name("MSG_CORRECT_LABEL")	
			self.calendar_message_box.set_name("SUCCESS_BOX")
			self.calendar_ok_img.show()
			self.calendar_error_img.hide()
			self.calendar_message.set_text(msg)
			self.calendar_message.show()

	#def manage_message	

	def hide_edit_message_items(self):

		self.message_box.set_name("HIDE_BOX")
		self.edit_error_img.hide()
		self.edit_message_label.set_text("")

	#def hide_edit_message_items

	def hide_calendar_message_items(self):

		self.calendar_message_box.set_name("HIDE_BOX")
		self.calendar_error_img.hide()
		self.calendar_ok_img.hide()
		self.calendar_message.set_text("")		

	#def hide_calendar_message_items

	def get_msg(self,code):	

		if 	code==-1:
			msg_text=_("Unabled to apply changes. List blocked for other user")
		elif code==2:
			msg_text=_("Changes apply succesfully")
		elif code==-3:
			msg_text=_("Error saving changes")
		elif code==6:
			msg_text=_("List of dates imported successfully")
		elif code==-7:	
			msg_text=_("Unabled to import list. List blocked for other user")
		elif code==-8:
			msg_text=_("Error importing the list of dates")
		elif code==-9:
			msg_text=_("The list of dates to be imported does not exist")
		elif code==10:
			msg_text=_("List of dates exported successfully")
		elif code==-11:
			msg_text=_("Error exporting the list of dates")			
		elif code==-12:
			msg_text=_("Last date in range must be major than init date")	
		elif code==-13:
			msg_text=_("You must indicate the two dates of range")	
		elif code==-14:
			msg_text=_("You must indicate the date")	

		return(msg_text)	

	#def get_msg	
	
	def manage_date_options(self,button,hbox,event=None):
		
		self.hide_calendar_message_items()
		button.popover.show()

	#def manage_date_options	

	def mouse_over_popover(self,widget,event=None):

		widget.set_name("POPOVER_ON")

	#def mouser_over_popover	

	def mouse_exit_popover(self,widget,event=None):

		widget.set_name("POPOVER_OFF")		
