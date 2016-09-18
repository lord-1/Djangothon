from __future__ import unicode_literals
import hashlib
from django.db import models

# Create your models here.

class SuperAdmin(models.Model):

	admin_name = models.CharField(blank = False, default = 'admin', max_length = 200)
	admin_password = models.CharField(blank = False, default = '5f4dcc3b5aa765d61d8327deb882cf99', max_length = 200)
	admin_id = models.CharField(blank = False, default = 'Test', max_length = 200)
	time_delta = models.DecimalField(blank = False, default = 0.500000000, max_digits = 12, decimal_places = 8)