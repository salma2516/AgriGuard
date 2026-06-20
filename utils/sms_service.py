from twilio.rest import Client

ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)

def send_sms(
    phone_number,
    message
):

    try:

        msg = client.messages.create(

            body=message,

            from_="+YOUR_TWILIO_NUMBER",

            to=phone_number
        )

        print(
            "SMS Sent:",
            msg.sid
        )

    except Exception as e:

        print(
            "SMS Error:",
            e
        )