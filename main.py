#!/usr/bin/env python2.7

from flask import Flask, request
from flask_cors import CORS
import random
import json

app = Flask(__name__)
app.debug = True
CORS(app)

################################################################################
##### Quelques constantes

COST_PER_GLASS  = 0.15 # le cout de production
PRICE_PER_GLASS = 0.35 # le prix de vente

# les conditions meteo
WEATHER_VALUES = ["SUNNY AND HOT", "SUNNY", "CLOUDY", "RAINY"]

# la probabilite maximale (entre 0 et 1) de vente pour chaque condition meteo.
SALES_MAX = {
  "SUNNY AND HOT" : 1.0, 
  "SUNNY"         : 0.8,
  "CLOUDY"        : 0.5,
  "RAINY"         : 0.1
}

# la probabilite minimale (entre 0 et 1) de vente pour chaque condition meteo.
SALES_MIN = {
  "SUNNY AND HOT" : 0.6, 
  "SUNNY"         : 0.2,
  "CLOUDY"        : 0.0,
  "RAINY"         : 0.0
}

################################################################################
##### Global variables

day = 1                                           # compteur de jour

budget = 1.0                                      # compteur de jour
current_weather = random.choice(WEATHER_VALUES)   # meteo du jour
vendu = 0

################################################################################
##### Logique de jeu

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Incremente le compteur de nombre de jours et selectionne aleatoirement une
# configuration meteo.
def moveToNextDay():  
  global day
  day += 1
  
  global current_weather
  current_weather = random.choice(WEATHER_VALUES)
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# En fonction de la meteo un nombre de ventes est choisi aleatoirement et le
# budget est mis a jour.
def simulateSales(requested_glasses):
  global budget
  
  proba = random.uniform(SALES_MIN[current_weather], SALES_MAX[current_weather])
  sales = int(requested_glasses * proba)
  
  expenses = requested_glasses * COST_PER_GLASS
  earnings = sales * PRICE_PER_GLASS
  
  budget += earnings - expenses
  
  return sales  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
@app.route("/dayinfo")
def getDayInfo():
    global day
    global budget

    data = { "day": day, "budget": budget, "weather": current_weather }
    
    return json.dumps(data),201,{'Content-Type' : 'application/json'}
    
@app.route('/order', methods=['POST'])
def postOrder():
  # game over
  if budget < COST_PER_GLASS:
    # http status 412 = "Precondition Failed"
    return '"Insufficient funds."', 412, {'Content-Type' : 'application/json'}
  
  data = request.get_json()
  # if not game over...
  sales = simulateSales(float(data['requested_glasses']))
  
  #TODO
  
  moveToNextDay()
  
  data = { "sales": sales }
  return json.dumps(data), 200, {'Content-Type' : 'application/json'}


if __name__ == "__main__":
    app.run()