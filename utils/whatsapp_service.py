from twilio.rest import Client

ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)

def send_whatsapp(phone_number, message):

    print("\n========== WHATSAPP FUNCTION CALLED ==========")

    try:

        phone_number = str(phone_number).strip()

        if not phone_number.startswith("+"):
            phone_number = "+91" + phone_number

        print("Sending To:", phone_number)

        msg = client.messages.create(

            body=message,

            from_="whatsapp:+14155238886",

            to=f"whatsapp:{phone_number}"

        )

        print("SID:", msg.sid)
        print("Status:", msg.status)

        return True

    except Exception as e:

        print("WhatsApp Error:", str(e))

        return False