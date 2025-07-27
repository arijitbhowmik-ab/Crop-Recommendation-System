import joblib
from flask import Flask, render_template, request, redirect, jsonify
import google.generativeai as genai


genai.configure(api_key="AIzaSyDZUqQThj5vvjDXUdEMW4-NJChpyZ6sPTs")  # Replace with your Gemini API key

model = genai.GenerativeModel("gemini-1.5-flash")
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('Home_1.html')

# Prediction page route   
@app.route('/Predict')
def prediction():
    return render_template('index.html')

# @app.route("/chatbot")
# def chatbot():
#     return render_template("chatbot.html")



@app.route("/chatbot_response", methods=["POST"])
def chatbot_response():
    user_msg = request.json.get("message", "")
    # if "Hi" or "Hello" in user_msg.lower():
    #     reply = "How can I help you"
    #     return jsonify({"reply": reply})
    
    try:
        response = model.generate_content([input_prompt,user_msg])
        reply = response.text.strip()
    except Exception as e:
        reply = "Sorry, something went wrong: " + str(e)
    return jsonify({"reply": reply})

input_prompt = "You are a crop recommendation sysytem, you recommend crops as per soil and weather condition give answer in briefly"

# Form submission route
@app.route('/form', methods=["POST"])
def brain():
    # Get form values and convert them to float
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    Humidity = float(request.form['Humidity'])
    Ph = float(request.form['ph'])
    Rainfall = float(request.form['Rainfall'])

    # Combine values into a list (or 2D array for model input)
    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]

     # Simple validation before predicting
    if Ph > 0 and Ph < 14 and Temperature < 100 and Humidity > 0:

        joblib.load('crop_app', 'r')
        # Load the trained model
        model = joblib.load(open('crop_app', 'rb'))

        # Predict using the model
        prediction = model.predict([values])[0]

        # Return result in a template
        return render_template('prediction.html', prediction=str(prediction))
    else:
        return "Sorry... Error in entered values in the form. Please check the values and fill them correctly."

if __name__ == '__main__':
    app.run(debug=True)