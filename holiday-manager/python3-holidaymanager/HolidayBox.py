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
import xmlrpc.client as n4dclient
import ssl
from datetime import datetime, date,timedelta


class HolidayBox(Gtk.Box):

	DATE_RANGE_INCONSISTENT_ERROR=-12
	DATE_RANGE_INCOMPLETE_ERROR=-13
	DATE_EMPTY_ERROR=-14


	def __init__(self,app_name):
		
		Gtk.Box.__init__(self)

		self.credentials=[]
		server='localhost'
		context=ssl._create_unverified_context()
		self.n4d_holiday = n4dclient.ServerProxy("https://"+server+":9779",context=context,allow_none=True)
		self.app_name=app_name
		self.holidayManager=HolidayManager.HolidayManager()
		self.render_form()

	#def __init__

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
		self.edit_message_label=builder.get_object("edit_message_label")
		self.save_day_button=builder.get_object("save_day_button")
		self.cancel_day_button=builder.get_object("cancel_day_button")
	
		self.listdays_tv=builder.get_object("listday_treeview")
		self.listdays_store=Gtk.ListStore(str,str,str,str,str)
		self.listdays_tv.set_model(self.listdays_store)


		column=Gtk.TreeViewColumn(_("Date"))
		cell=Gtk.CellRendererText()
		column.pack_start(cell,True)
		column.add_attribute(cell,"markup",0)
		column.add_attribute(cell,"cell_background",4)
		column.set_expand(False)
		column.set_property("fixed-width",200)
		self.listdays_tv.append_column(column)
		self.listdays_tv.connect("button-release-event",self.day_clicked)

		column=Gtk.TreeViewColumn(_("Comment"))
		cell=Gtk.CellRendererText()
		column.pack_start(cell,False)
		column.add_attribute(cell,"markup",1)
		column.add_attribute(cell,"cell_background",4)
		#column.set_property("fixed-width",300)
		column.set_expand(True)
		self.listdays_tv.append_column(column)

		column=Gtk.TreeViewColumn("")
		cell=Gtk.CellRendererPixbuf()
		cell.set_property("stock-size",Gtk.IconSize.BUTTON)
		column.set_expand(False)
		column.pack_start(cell,False)
		column.add_attribute(cell,"icon-name",2)
		column.add_attribute(cell,"cell_background",4)
		column.set_property("fixed-width",50)
		self.listdays_tv.append_column(column)
		self.col_edit=column

		column=Gtk.TreeViewColumn("")
		cell=Gtk.CellRendererPixbuf()
		cell.set_property("stock-size",Gtk.IconSize.BUTTON)
		column.set_expand(False)
		column.pack_start(cell,False)
		column.add_attribute(cell,"icon-name",3)
		column.add_attribute(cell,"cell_background",4)
		column.set_property("fixed-width",50)
		self.listdays_tv.append_column(column)
		self.col_remove=column

		self.export_daylist_button=builder.get_object("export_daylist_button")
		self.import_daylist_button=builder.get_object("import_daylist_button")
		self.remove_daylist_button=builder.get_object("remove_daylist_button")
		self.calendar_message=builder.get_object("calendar_message")

		self.pack_start(self.main_box,True,True,0)
		self.set_css_info()
		self.connect_signals()
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
		self.calendar_message.set_text("")

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

			else:
				self.holiday_calendar.select_day(0)
				self.range=True
				self.remove_range_button.set_sensitive(True)
				self.single_day_entry.set_text("")
	
	#def day_toggled_button

	def get_holidaylist(self):

		result=self.n4d_holiday.read_conf(self.credentials,'HolidayListManager')['return']

		holiday_list=result["info"]
		list_days=self.order_date(holiday_list)
		self.listdays_store.clear()
		color_palette=['LightGreen','bisque']
		for item in list_days:
			if "-" in item:
				bg_color=color_palette[0]
			else:
				bg_color=color_palette[1]	
			date=item
			description=holiday_list[item]["description"]

			self.listdays_store.append(("<span font='Roboto bold' size='medium'>"+date+"</span>","<span font='Roboto' size='medium'>"+description+"</span>","gtk-edit","gtk-remove",bg_color))


	#def get_holidaylist	


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



	def _get_day_clicked_action(self,event):

		action=''
		row=None

		if type(event)==type(Gtk.TreePath()):
			action='edit'
		else:
			try:
				row=self.listdays_tv.get_path_at_pos(int(event.x),int(event.y))
			except Exception as e:
				self._debug(e)
			if row:
				if row[1]==self.col_remove:
					action='remove'
				elif row[1]==self.col_edit:
					action='edit'
		return action

	#def _get_day_clicked_action	

	def day_clicked(self,x,event):	

		self.init_calendar()
		self.calendar_message.set_text("")
		self.clear_days=True
		selection=self.listdays_tv.get_selection()
		model,iter=selection.get_selected()

		if event!=None:
			action=self._get_day_clicked_action(event)

		self.day=model[iter][0]
		self.day=self.day[self.day.find("<span")+39:self.day.find("</span>")]
		#self.edit_day_button.set_sensitive(True)
		#self.remove_day_button.set_sensitive(True)
		self.coment_day=model[iter][1]
		self.coment_day=self.coment_day[self.coment_day.find("<span")+34:self.coment_day.find("</span>")]

		if action=="edit":
			self.edit_day_clicked()
		elif action=="remove":
			self.remove_day_clicked()		

	#def day_clicked	

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
							self.edit_message_label.set_text("")
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
		self.edit_message_label.set_text("")

	#def remove_range	


	def add_day_clicked(self,widget):
	
		self.init_calendar()
		self.edit_message_label.set_text("")
		self.calendar_message.set_text("")
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
						result=self.n4d_holiday.delete_day(self.credentials,"HolidayListManager",self.day)['return']
						code=result["code"]
					
				if result["status"]:			
					#result=self.holidayManager.add_day(new_day,comment)
					result=self.n4d_holiday.add_day(self.credentials,'HolidayListManager',new_day,comment)['return']
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
		
	def edit_day_clicked(self):

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
		self.coment_day_entry.set_text(self.coment_day)
		self.edit_message_label.set_text("")
		self.edit_data_window.set_title(_("Edit date"))
		self.edit_data_window.show()

	#def edit_day_clicked	


	def remove_day_clicked(self):

		error=False

		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO, self.app_name)
		dialog.format_secondary_text(_("The date will be deleted. Do you want to continue?"))
		response=dialog.run()
		dialog.destroy()
		if response == Gtk.ResponseType.YES:	
			result=self.n4d_holiday.delete_day(self.credentials,'HolidayListManager',self.day)['return']
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
			result=self.n4d_holiday.reset_holiday_list(self.credentials,'HolidayListManager')['return']

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
			result=self.n4d_holiday.export_holiday_list(self.credentials,'HolidayListManager',self.credentials[0],dest)['return']
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
				result=self.n4d_holiday.import_holiday_list(self.credentials,'HolidayListManager',orig)['return']
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
		edit_date_errors=[-1,-2,-3,-12,-13,-14]

		if error:
			if code in edit_date_errors:
				self.edit_message_label.set_name("MSG_ERROR_LABEL")
				self.edit_message_label.set_text(msg)
				self.edit_message_label.show()
			else:
				self.calendar_message.set_name("MSG_ERROR_LABEL")	
				self.calendar_message.set_text(msg)
				self.calendar_message.show()	
		else:
			self.calendar_message.set_name("MSG_CORRECT_LABEL")	
			self.calendar_message.set_text(msg)
			self.calendar_message.show()

	#def manage_message		


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
	
	