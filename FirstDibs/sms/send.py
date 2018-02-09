from twilio.rest import Client

def sendMessage(numbers, message, imageurl=None):
    # ACCOUNT_SID = "AC0ca67552c700a66330c9e395429584ff"
    # AUTH_TOKEN = "e5272a4a070a49fa8f39d8ce5b739ed1"
    ACCOUNT_SID = "AC1d80775323ef3be02e7c16c3193e8a95"
    AUTH_TOKEN = "4fb9074851b5d991089dee85aad3ec07"
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