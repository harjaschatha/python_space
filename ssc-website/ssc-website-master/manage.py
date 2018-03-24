#!/usr/bin/env python
import os
import sys
#==============================================================
import os
import sys
import shutil
import random
import datetime
if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stephens.settings")

from django.core.files import File
import mainsite,attendance,office,events,admission

from django.contrib.auth.models import User,Group
from django.core.management import execute_from_command_line
from django.utils import timezone

#==============================================================
if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stephens.settings")

	from django.core.management import execute_from_command_line
	if sys.argv[1]=='runserver':
		from stephens import settings
		if len(sys.argv)>2:
			sys.argv[2]=settings.domain_name.split('//')[1]
			print('To change the port change in stephens/settings.py')
	else:
		sys.argv.append(settings.domain_name.split('//')[1])
	execute_from_command_line(sys.argv)
