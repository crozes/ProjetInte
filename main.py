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
nbr_player = 0                                    #nbr_Joueur

time = 0                                          #Time

day = 1                                           # compteur de jour

budget = 1.0                                     # compteur de jour
current_weather = random.choice(WEATHER_VALUES)   # meteo du jour

weather = []
prevision_day = []
#vendu = 0

################################################################################
##### Logique de jeu

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Incremente le compteur de nombre de jours et selectionne aleatoirement une
# configuration meteo.
def moveToNextDay():  
  global day
  day += 1
  
  #global current_weather
  #current_weather = random.choice(WEATHER_VALUES)
  
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
def actPlayer(request_player):
    global nbr_player
    if request_player == "new" :
        nbr_player +=1
    elif request_player == "out":
        nbr_player -= 1
    else :
        print "bad argument in actPlayer()"
        return 1
         

######################~GET~###############################

## Reset BD
@app.route('/debug/db/reset')
def route_dbinit():
    # Initialisation/RAS base de donnee
    db = Db()
    db.executeFile("database_reset.sql")
    db.close()
    return "Done."

#A SUPPRIMER
## GET HOUR
@app.route('/getHour')
def getHour():
    # Variable global Hour
    query = "SELECT Meteo_date FROM public.Meteo ORDER BY Meteo_ID DESC LIMIT 1"
    db = Db()
    result = db.select(query)
    db.close()
    
    for date in result :
        time = date['meteo_date']
        
    return json.dumps(time),200,{'Content-Type' : 'application/json'}    

#A SUPPRIMER
## GET DAYINFO
@app.route("/dayinfo")
def getDayInfo():
    # Return Fake day Info
    global day
    global budget
    global current_weather
    data = { "day": day, "budget": budget, "weather": current_weather }
    return json.dumps(data),200,{'Content-Type' : 'application/json'}

#A SUPPRIMER    
### GET RECETTE
@app.route("/allRecette")
def getAllRecette():
    db = Db()
    result = db.select("SELECT * FROM public.Recipe")
    db.close()
    
    resp = make_response(json.dumps(result))
    resp.mimetype = 'application/json'
    return resp 

#A SUPPRIMER
## GET NBR PLAYER
@app.route("/nbrPlayer")
def getNbrPlayer():
    db = Db()
    result = DB.select("COUNT")
    db.close()
    return json.dumps(data),200,{'Content-Type' : 'application/json'} 
    
## GET TEMPS
@app.route("/metrology")
def getTemps():
    db = Db()
    result = db.select("SELECT * FROM public.Meteo")
    db.close()
    
    print result
    
    timestamp = result['Meteo_Timestamp']
    print "timestamp :" + timestamp
    #weather = result['Meteo_Temps']
    meteoPrevision = []
    
    for forcast in result :
        data = {"weather" : forcast['Meteo_Temps'], "dnf" : forcast['Meteo_Dnf']}
        meteoPrevision.append(data)
    
    data = {"timestamp" : timestamp, "weather" : meteoPrevision}
    
    print data
    
    #data = {"timestamp" : 24, "weather" : "sunny"}
    return json.dumps(data),200,{'Content-Type' : 'application/json'}          
    
## GET MAP
@app.route("/map")
def getMap():
    queryRank = "SELECT player_name, player_banque FROM player ORDER BY player_banque;"
    db = Db()
    resultRank = db.select(queryRank)
    db.close()
    ranking=[]
    player=[]
    for rank in result :
        ranking.append(rank)
        queryPlayer = "SELECT * FROM player WHERE player_name=%s;" % (rank)
        db = Db()
        resultPlayer = db.select(queryPlayer)
        db.close()
    
    Map = {"map" : map}
    return json.dumps(Map),200,{'Content-Type' : 'application/json'}


## GET PLAYER'S MAP
@app.route("/map/<string:playerName>")
def getPlayerSMap():
    playerSMap={}
    return json.dumps(PlayerSMap),200,{'Content-Type' : 'application/json'}

@app.route("/players")
def getPlayerTest():
    data = {"name" : "Toto", "location" : [{"latitude" : 23, "longitude" : 12}], "info" : [{"cash" : 1000.59, "sales" : 10, "profit" : 15.23, "drinksOffered" : [{"name" : "Limonade", "price" : 2.59, "hasAlcohol" : False, "isCold" : True}] }] }
    return json.dumps(data),200,{'Content-Type' : 'application/json'}
######################~/GET~###############################


######################~POST~###############################  

## POST Hour
@app.route('/postHour', methods=['POST'])
def postHour() :
    global time
    #print request.get_data() 
    data = request.get_json() 
    if data == None :
        print request.get_data()
        return '"None in postHour"',400,{'Content-Type' : 'application/json'}
    else :
        time = data['timestamp']
        temps = data['temps']
        
        query = "INSERT INTO public.Meteo(Meteo_Temps, Meteo_Date)VALUES (\'"+temps['weather']+"\',"+data['timestamp']+");"
        
        db = Db()
        db.execute(query)
        db.close()
        
        return json.dumps(time),201,{'Content-Type' : 'application/json'}
        
        
## POST Sales
@app.route('/sales', methods=['POST'])
def postSales():
    #TODO
    return json.dumps("coucou"),200,{'Content-Type' : 'application/json'}
    
## POST Action
@app.route('/actions/<playerName>', methods=['POST'])
def postAction():
    #TODO
    return json.dumps("coucou"),200,{'Content-Type' : 'application/json'}
        
## POST Temps
@app.route('/metrology', methods=['POST'])
def postTemps() :
    #print request.get_data() 
    data = request.get_json(force=True) 
    if data == None :
        print request.get_data()
        return '"None in postTemps verifier le Header"',400,{'Content-Type' : 'application/json'}
    else :
        #print data 
        time = data['timestamp']
        temps = data['weather']
        cpt = 1
        
        for forcast in temps :
            query = "INSERT INTO public.Meteo (Meteo_ID, Meteo_Timestamp, Meteo_Temps, Meteo_Dnf) VALUES (%s,%s,\'%s\',%s) ON CONFLICT (Meteo_ID) DO UPDATE SET Meteo_Temps = \'%s\', Meteo_Timestamp = %s, Meteo_Dnf = %s" %(cpt,time,forcast['weather'],forcast['dnf'],forcast['weather'],time,forcast['dnf'])
            db = Db()
            db.execute(query)
            db.close()
            cpt += 1;
        
        return json.dumps(data),201,{'Content-Type' : 'application/json'} 
        
## POST Player
@app.route('/players', methods=['POST'])
def postNewPlayer() :
    data = request.get_json(force=True) 
    if data == None :
        #print request.get_data()
        return '"None in postNewPlayer verifier le Header"',400,{'Content-Type' : 'application/json'}
    else :
        #print data #{u'Player_name': u'Toto'}
        query_getName = "SELECT Player_name FROM public.Player"
        
        db = Db()
        result = db.select(query_getName)
        
        for player in result :
            #print player['player_name'] #Player_name
            if player['player_name'].upper() == data['name'].upper() :
                return 
                #data = {"IsAccepted" : False}
                db.close()
                return json.dumps(data),200,{'Content-Type' : 'application/json'}
                
        query_addPlayer = "INSERT INTO public.Player (Player_name, Player_banque, Player_profit_depuis_impot) VALUES (\'"+data['name']+"\',100,0)"
        db.execute(query_addPlayer)
        
        db.close()
        
        #TODO Add Latitude et tout 
        
        data = {"name" : "Toto", "location" : [{"latitude" : 23, "longitude" : 12}], "info" : [{"cash" : 1000.59, "sales" : 10, "profit" : 15.23, "drinksOffered" : [{"name" : "Limonade", "price" : 2.59, "hasAlcohol" : False, "isCold" : True}] }] }
        
        return json.dumps(data),201,{'Content-Type' : 'application/json'} 
        
## POST Ingredient
@app.route('/postIngredient', methods=['POST'])
def postAddIngredient() :
    #print request.get_data() 
    data = request.get_json() 
    if data == None :
        print request.get_data()
        return '"None in postIngredient"',400,{'Content-Type' : 'application/json'}
    else :
        #print data 
        #TODO
        query = "INSERT INTO public.Ingredient (Ingredient_name, Ingredient_cost, Ingredient_hasAlcohol, Ingredient_isCold) VALUES (\'"+data['name']+"\',\'"+data['cost']+"\',"+data['hasAlcohol']+","+data['isCold']+")"
        db = Db()
        db.execute(query)
        db.close()
        return json.dumps(query),201,{'Content-Type' : 'application/json'}                             

######################~/POST~###############################  


######################~TEST~###############################    
### To deleted
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
    return json.dumps(data), 201, {'Content-Type' : 'application/json'}    
            
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

######################~/TEST~###############################    


if __name__ == "__main__":
    app.run()
    
