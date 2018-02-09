from django.db import models
import urllib.request
import os
import requests
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class Phone(models.Model):
 	phone_number = models.CharField(max_length=12, unique=True)
 	want_dibs = models.BooleanField(default=False)

class Dib(models.Model):
	image_file = models.ImageField()
	image_url = models.URLField()
	text = models.TextField()
	accepted = models.BooleanField(default=False)
	sender = models.CharField(max_length=12)
	receiver =  models.CharField(max_length=12, default="empty")

# https://stackoverflow.com/questions/16381241/django-save-image-from-url-and-connect-with-imagefield
	def get_remote_image(self):
		saved = False
		file_num = 0
		subdir = 'img/'
		try:
			os.mkdir(subdir)
		except:
			pass
		while saved == False:
			if os.path.isfile(os.path.join(subdir, 'food_picture' + str(file_num) + ".jpg")):
				print (os.path.join(subdir, 'food_picture' + str(file_num)))
				file_num += 1
			else:
				req = requests.head(self.image_url, allow_redirects=True)
				print (os.path.join(subdir, 'food_picture' + str(file_num)))
				print (req.url)
				urllib.request.urlretrieve(req.url, os.path.join(subdir,
					'food_picture' + str(file_num) + ".jpg"))
				saved = True