from twilio.rest import Client

def sendMessage(numbers, message, imageurl=None):
# need to define ACCOUNT_SID AND AUTH_TOKEN
    # twilioNumber = "+12153020189"
    twilioNumber = "+12153302374"
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if imageurl is None:
        for number in numbers:
            message = client.messages.create(
                to=number,
                from_=twilioNumber,
                body=message)
    else:
        for number in numbers:
            message = client.messages.create(
                to=number,
                from_=twilioNumber,
                body=message,
                media_url=imageurl)

if __name__ == '__main__':
    sendMessage()