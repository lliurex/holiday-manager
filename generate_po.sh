#!/bin/bash

xgettext --join-existing ./holiday-manager/python3-holidaymanager/HolidayBox.py -o ./translations/holiday-manager.pot
xgettext --join-existing ./holiday-manager/python3-holidaymanager/rsrc/holiday-manager.ui -o ./translations/holiday-manager.pot