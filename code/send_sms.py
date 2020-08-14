from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
def send_sms(x):
    client = Client("AC80413213a6c8e0848e4ff54b8e0197db", "202fabb7b4f6689d887490c5d07f419b")
    client.messages.create(to=str(x), from_="+12028385263", body="You have broken the rule! Please pay fine...")