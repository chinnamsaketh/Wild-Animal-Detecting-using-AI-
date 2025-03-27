from ultralytics import YOLO
import cv2
import torch
from twilio.rest import Client

# Twilio credentials (replace with your own)
account_sid = "AC95884d8ab5a111a547b54e981a5b28c9"
auth_token = "7d39f714927a5e37e09d392d9633d509"
twilio_number = "+14017561808"
to_number = "+919100527255"

# List of dangerous animals
dangerous_animals = ["tiger", "lion", "bear", "leopard", "wolf"]

# Function to send SMS alert
def send_alert(animal):
    message = f"🚨 Warning! A {animal} has been detected! Stay safe!"
    
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )
    print(f"Alert sent for {animal}!")

# Load YOLOv8 model
model = YOLO("C:/YOLO/yolov8n.pt")

# Load image
image_path = "C:/YOLO/tiger.JPEG"
img = cv2.imread(image_path)

# Run detection
results = model.predict(image_path, save=True)

# Process results
for result in results:
    for box in result.boxes:
        cls = int(box.cls[0])  # Class index
        label = model.names[cls]  # Get class name
        
        if label in dangerous_animals:
            send_alert(label)  # Send alert if dangerous animal is detected

print("Detection completed!")