from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .models import Dib, Phone
from .send import sendMessage

@csrf_exempt
def sms_response(request):
	body = request.POST.get('Body', '')
	image = request.POST.get('MediaUrl0', '')
	sender = request.POST.get('From', '')

	resp = MessagingResponse()

	if body.lower().replace(" ","") == "givemedibs":
		try:
			received_phone = Phone.objects.get(phone_number=sender)
			received_phone.want_dibs = True
			received_phone.save()
			resp.message("You will now receive future dibs. \nType enddibs to stop receiving dibs.")
		except Phone.DoesNotExist:
			new_phone = Phone.objects.create(phone_number=sender, want_dibs=False)
			new_phone.save()
			resp.message("Your number is now registered. Please type dibshelp for a list of available commands.")
	elif body.lower().replace(" ","") == "stopdibs":
		try:
			received_phone = Phone.objects.get(phone_number=sender)
			received_phone.want_dibs = False
			received_phone.save()
			resp.message("You will now no longer receive dibs. \nType givemedibs to receive dibs.")
		except Phone.DoesNotExist:
			resp.message("This number is not registered! Please type givemedibs to register.")
	elif image:
		dib_instance = Dib.objects.create(text=body, sender=sender, image_url=image)
		dib_instance.save()
		dib_instance.get_remote_image()
		phones_that_want_dibs = Phone.objects.filter(want_dibs=True)
		desc = "New dib with ID: DIB%s \nDescription: %s" % (dib_instance.id, dib_instance.text)
		phones_that_want_dibs_list = []
		for phone in phones_that_want_dibs:
			phones_that_want_dibs_list.append(phone.phone_number)
		sendMessage(phones_that_want_dibs_list, desc, imageurl=dib_instance.image_url)
		resp.message("Created dib with ID: DIB%s" % dib_instance.id)
	elif "getdib" in body.lower().replace(" ",""):
		model_query = int(body[10:])
		try:
			dib = Dib.objects.get(id=model_query)
			if dib.accepted:
				resp.message("DIB%s has already been taken :(" % model_query)
			else:
				dib.accepted = True
				dib.receiver = sender
				dib.save()
				sender_list = [dib.sender]
				sendMessage(sender_list, "%s has accepted your dib!" % dib.receiver)
				resp.message("You have taken DIB%s contact: %s to get your food!" % (model_query, dib.sender))
		except Dib.DoesNotExist:
			resp.message("That dib does not exist!")
	else:
		resp.message("Unrecognized command!")
	return HttpResponse(str(resp))

