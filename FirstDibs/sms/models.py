from django.db import models

class Phone(models):
	phone_number = models.
	want_dibs = models.BooleanField()

class Dib(models):
	photo = models.ImageField()
	text = models.TextField()
	accepted = models.BooleanField()
	sender = models.CharField()
	receiver =  models.CharField()
	ident = models.CharField()
