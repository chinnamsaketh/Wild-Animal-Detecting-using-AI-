import geocoder
import cv2
from ultralytics import YOLO
from twilio.rest import Client

# Twilio credentials (replace with your actual details)
account_sid = "your_account_sid_here"
auth_token = "your_auth_token_here"
twilio_number = "+your_twilio_phone_number"
to_number = "+your_verified_phone_number"

# List of dangerous animals
dangerous_animals = ["tiger", "lion", "bear", "leopard", "wolf"]

# Function to send an SMS alert
def send_alert(animal):
    # Get live location using IP address
    location = geocoder.ip("me")
    lat, lon = location.latlng if location.latlng else ("Unknown", "Unknown")

    # Format the alert message with location
    message = f"🚨 Warning! A {animal} has been detected!\n📍 Location: {lat}, {lon}"
    
    # Send SMS alert
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=twilio_number, to=to_number)

    print(f"Alert sent for {animal} at location: {lat}, {lon}")

# Load YOLOv8 model
model = YOLO("C:/YOLO/yolov8n.pt")

# Open webcam (change 0 to a URL for CCTV)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model.predict(frame)

    # Process detected objects
    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])  # Class index
            label = model.names[cls]  # Get class name
            print(f"Detected: {label}")
            
            if label in dangerous_animals:
                send_alert(label)  # Send SMS alert

    # Show video with detections
    cv2.imshow("Live Animal Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()