import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests

# Load the Keras model
model = load_model('best_model_class.keras', compile=False)

# Define approximate calorie values for food items
food_calories = {
    'apple_pie': 320,
    'pizza': 285,
    'omelette': 153,
    'donuts': 300,
    'cup_cakes': 206,
    'french_toast': 250,
    'falafel': 200,
    'fried_rice': 215,
    'chicken_curry': 350,
    'hot_dog': 150
}

# Function to predict calories from the image
def predict_calories(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    food_name = class_to_food_name(predicted_class)  
    calories = food_calories.get(food_name, "Calories not available")  
    return food_name, calories

# Mapping class indices to food names (Update this mapping according to your model)
def class_to_food_name(predicted_class):
    mapping = {
        0: "apple_pie",
        1: "pizza",
        2: "omelette",
        3: "donuts",
        4: "cup_cakes",
        5: "french_toast",
        6: "falafel",
        7: "fried_rice",
        8: "chicken_curry",
        9: "hot_dog",
        # Add additional classes as needed
    }
    return mapping.get(predicted_class, "Unknown Food")

# Function to fetch calorie information from USDA API
# def fetch_calories_from_api(food_name, api_key):
#     url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={api_key}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if data.get('foods'):
#             calories = data['foods'][0]['foodNutrients'][0]['value']  # Assuming calories are the first nutrient
#             return calories
#     return None

# Function to handle file selection and prediction
def upload_image():
    img_path = filedialog.askopenfilename()
    if img_path:
        food_name, calories = predict_calories(img_path)
        # api_key = api_key_entry.get()  # Get API key from entry
        # if api_key:
        #     api_calories = fetch_calories_from_api(food_name, api_key)
        #     if api_calories:
        #         calories = api_calories  # Use the calorie value from API if available
        result_label.config(text=f'Predicted Food: {food_name}\nApproximate Calories: {calories} kcal')
        display_image(img_path)

# Function to display the uploaded image
def display_image(img_path):
    img = Image.open(img_path)
    img = img.resize((250, 250), Image.ANTIALIAS)  
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  

# Create the main application window
app = tk.Tk()
app.title("Calorie Predictor")
app.geometry("400x500")

# Create API Key entry
# api_key_label = tk.Label(app, text="Enter USDA API Key:") #do not hard code the API
# api_key_label.pack(pady=5)
# api_key_entry = tk.Entry(app, width=30)
# api_key_entry.pack(pady=5)

# Create upload button
upload_button = tk.Button(app, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Label to display the prediction results
result_label = tk.Label(app, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# Label to display the image
image_label = tk.Label(app)
image_label.pack(pady=10)

# Run the application
app.mainloop()
