import numpy as np
from flask import Flask, request, render_template
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageDraw  # Added import for Image and ImageDraw
import os

app = Flask(__name__)

# Load the AI model for Arduino Due detection
ai_model = load_model("./models/arduino_due_detector_transfer.h5")

# Load the ML model for UFO prediction
ml_model = pickle.load(open("./models/ufo-model.pkl", "rb"))

# Ensure the upload directory exists
upload_folder = './static/uploaded_images'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/arduino-due-detector", methods=["GET", "POST"])
def arduino_due_detector():
    result = None
    image_url = None

    if request.method == "POST":
        # Handle image upload for AI model
        uploaded_file = request.files['image']
        if uploaded_file:
            img_path = os.path.join(upload_folder, uploaded_file.filename)
            uploaded_file.save(img_path)

            # Load and preprocess the image
            img = image.load_img(img_path, target_size=(150, 150))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict with the AI model
            prediction = ai_model.predict(img_array)
            confidence = prediction[0][0]  # Confidence score (probability between 0 and 1)

            # Create bounding box image if confidence is low
            if confidence < 0.5:
                result = f"Arduino Due detected with {confidence * 100:.2f}% confidence."
                img_with_box = draw_bounding_box(img_path)
                img_with_box_path = img_path.replace(".jpg", "_boxed.jpg")
                img_with_box.save(img_with_box_path)
                image_url = img_with_box_path
            else:
                result = f"No Arduino Due detected with {100 - confidence * 100:.2f}% confidence."

    return render_template("/arduino_due_detector.html", result=result, image_url=image_url)

@app.route("/ai-models", methods=["GET", "POST"])
def ai_models():
    # Return the AI Models page
    return render_template("ai_models.html")

@app.route("/ufo-predict", methods=["GET", "POST"])
def ufo_predict():
    prediction_text = None

    if request.method == "POST":
        # Get the features from the form for UFO prediction
        int_features = [int(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        prediction = ml_model.predict(final_features)

        output = prediction[0]
        countries = ["Australia", "Canada", "Germany", "UK", "US"]
        prediction_text = f"Likely country: {countries[output]}"

    return render_template("/ufo_predict.html", prediction_text=prediction_text)

@app.route("/ml-models", methods=["GET", "POST"])
def ml_models():
    # Return the ML Models page
    return render_template("ml_models.html")

def draw_bounding_box(img_path):
    # Open the image using Pillow
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    # Simulate drawing a bounding box (for example, around a fixed area)
    # Replace these coordinates with your actual model's bounding box coordinates
    left, top, right, bottom = 30, 30, 120, 120
    draw.rectangle([left, top, right, bottom], outline="red", width=3)

    return img

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)