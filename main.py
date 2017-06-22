#!/usr/bin/env python2.7

from flask import Flask, request, make_response
from db import Db
from flask_cors import CORS
import json, os, psycopg2, urlparse
import random

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

time = 0                                          #Time

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
# Return if value is a int
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


######################~GET~###############################

## Reset BD
@app.route('/debug/db/reset')
def route_dbinit():
    # Initialisation/RAS base de donnee
    db = Db()
    db.executeFile("database_reset.sql")
    db.close()
    return "Done."

## GET HOUR
@app.route('/getHour')
def getHour():
    # Variable global Hour
    global time
    data = {"time": time}
    return json.dumps(data),201,{'Content-Type' : 'application/json'}

## GET DAYINFO
@app.route("/dayinfo")
def getDayInfo():
    # Return Fake day Info
    global day
    global budget
    data = { "day": day, "budget": budget, "weather": current_weather }
    return json.dumps(data),201,{'Content-Type' : 'application/json'}

######################~POST~###############################  

## POST HOUR
@app.route('/postHour', methods=['POST'])
def postHour() :
    global time
    #print request.get_data() 
    data = request.get_json() 
    if data == None :
        print request.get_data()
        return '"None in postHour"',400,{'Content-Type' : 'application/json'}
    else :
        print data['time'] 
        time = data['time']
        return json.dumps(time),201,{'Content-Type' : 'application/json'}
        
## POST Ingredient
@app.route('/postIngredient', methods=['POST'])
def postAddIngredient() :
    print request.get_data() 
    data = request.get_json() 
    if data == None :
        print request.get_data()
        return '"None in postIngredient"',400,{'Content-Type' : 'application/json'}
    else :
        print data 
        query = "INSERT INTO pulbic.Ingredient (Ingredient_name, Ingredient_cost, Ingredient_hasAlcohol, Ingredient_isCold) VALUES (\'"+data['name']+"\',\'"+data['cost']+"\',"+data['hasAlcohol']+","+data['isCold']+")"
        db = Db()
        result = db.select(query)
        db.close()
        return json.dumps(time),201,{'Content-Type' : 'application/json'}        
   
  
    
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
    
### Get all recette
@app.route("/allrecette")
def getAllRecette():
    db = Db()
    result = db.select("SELECT * FROM public.\"Recipe\"")
    db.close()
    
    resp = make_response(json.dumps(result))
    resp.mimetype = 'application/json'
    return resp

@app.route('/postIngredient', methods=['POST']) 
def postIngredient():
    data = request.get_json()
    print data
    if data == None :
        print "None :" + request.get_data()
        return request.get_data(), 400, {'Content-Type' : 'application/json'}
    else :
        db = Db()
        db.execute(data);
        db.close()
        
            
### To deleted    
@app.route('/posttest', methods=['POST'])
def postSimple():
    # game over
    data = request.get_json()
    if data == None :
        print "None :" + request.get_data()
        return request.get_data(), 400, {'Content-Type' : 'application/json'} 
    else :
        print(json.dumps(data))
        return json.dumps(data), 200, {'Content-Type' : 'application/json'}   

### To deleted
@app.route("/")
def getHelloWord():
    print("hello word")
    return "hello word"

### To deleted
@app.route("/coucou")
def getCoucou():
    db = Db()
    result = db.select("SELECT nom_test FROM public.Test")
    db.close()
    
    resp = make_response(json.dumps(result)) 
    resp.mimetype = 'application/json'
    return resp

if __name__ == "__main__":
    app.run()
    
