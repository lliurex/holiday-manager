#!/usr/bin/env python3
#
# $Id: setup.py,v 1.32 2010/10/17 15:47:21 ghantoos Exp $
#
#    Copyright (C) 2008-2009  Ignace Mouzannar (ghantoos) <ghantoos@ghantoos.org>
#
#    This file is part of lshell
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
from distutils.core import setup
from edupals.i18n import poinstaller
import sys

if __name__ == '__main__':
	
	pinstaller = poinstaller.PoInstaller('translations','holiday-manager','')
	pinstaller.build()
	polist = pinstaller.setup_install()

	setup(name='python3-holidaymanager',
		version='0.1',
		description='API to manage holidays',
		long_description="""""",
		author='Lliurex Team',
		author_email='juapesai@hotmail.com',
		maintainer='Juan Ramon Pelegrina',
		maintainer_email='juapesai@hotmail.com',
		keywords=['software'],
		url='http://www.lliurex.net',
		license='GPL',
		platforms='UNIX',
		packages = ['holidaymanager'],
		package_dir = {'holidaymanager':'holiday-manager/python3-holidaymanager'},
		package_data = {'holidaymanager':['rsrc/*']},
		data_files = [('bin',['holiday-manager/check_holidays.py'])
			      ] +polist ,
		classifiers=[
			'Development Status :: 4 - Beta',
			'Environment :: Console'
			'Intended Audience :: End Users',
			'License :: OSI Approved :: GNU General Public License v3',
			'Operating System :: POSIX',
			'Programming Language :: Python',
			'Topic :: Software',
			'Topic :: Install apps',
			],
	)
	pinstaller.clean()
