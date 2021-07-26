import spacy
import requests
from flask import Flask, render_template, request
 
app = Flask(__name__)
nlp = spacy.load("en_core_web_md")

topic = nlp("Weather conditions in a city")
exit_conditions = nlp("End of conversation.")     

def display_weather_conditions(city):
    open_weather_url = "http://api.openweathermap.org/data/2.5/weather/?appid=YOUR_API_KEY&q=" + city
    response = requests.get(open_weather_url)
    weather = response.json()["weather"][0]["description"]
    return ("Its " + weather + " in " + city)

def handle_user_input(user_input):
    # Need to convert the user text input into NLP document
    user_input = nlp(user_input) 

    # Checking the threshold
    if user_input.similarity(topic) >= 0.80: 
        for ent in user_input.ents: # Checking the entities
            if ent.label_ == "GPE": # Verifying if its is a geogrophical Entity
                city = ent.text
                return display_weather_conditions(city)
            else:
                return ("Sorry I am unable to detect a location. Please try asking something else.")
    else:
        if user_input.similarity(exit_conditions) >= 0.70:
            return "Ok. Bye for now."
        else:
            return "Sorry I don't understand that. Please try asking something else."
            
@app.route("/")
def home():
    return render_template("index.html")
 
@app.route("/get")
def bot_response():
    user_message = request.args.get('msg')
    return str(handle_user_input(user_message))
  
if __name__ == "__main__":
    app.run()
 