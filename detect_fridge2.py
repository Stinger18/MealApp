from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')

# Load the image
image_path = './fruits2.jpg' #whatever the path is for your picture

# Perform inference
results = model(image_path)

# Map class IDs to names using the model's class names
detected_items = [model.names[int(item.cls)] for item in results[0].boxes]

# Print the list of items
print("Items in the fridge:", detected_items)
