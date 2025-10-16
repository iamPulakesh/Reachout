import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_SID = os.getenv('TWILIO_VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_otp(phone: str) -> bool:
    try:
        verification = client.verify.v2.services(TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone, channel='sms')
        return verification.status in ('pending', 'sent')
    except Exception as e:
        print(f"Twilio Verify send error: {e}")
        return False

def verify_otp(phone: str, otp: str) -> bool:
    try:
        verification_check = client.verify.v2.services(TWILIO_VERIFY_SERVICE_SID).verification_checks.create(to=phone, code=otp)
        return verification_check.status == 'approved'
    except Exception as e:
        print(f"Twilio Verify check error: {e}")
        return False
