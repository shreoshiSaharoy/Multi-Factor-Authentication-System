from twilio.rest import Client
from django.conf import settings

def send_sms_otp(to_phone_number, otp):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Your login OTP is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        print(f"SMS sent successfully. SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS OTP: {e}")
