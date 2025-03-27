from twilio.rest import Client

# Twilio credentials (replace with your own)
account_sid = "AC95884d8ab5a111a547b54e981a5b28c9"
auth_token = "7d39f714927a5e37e09d392d9633d509"
saketh = "+14017561808"  # Your Twilio phone number
to_number = "+919100527255"  # Your mobile number

def send_alert(animal):
    message = f"Warning! A {animal} has been detected!"
    
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=saketh,
        to=to_number
    )
    print("Alert sent!")

# Example usage
send_alert("tiger")  # Replace with detected animal name