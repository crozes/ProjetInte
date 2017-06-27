#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

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
 
CENTER_COORDINATES = {"latitude":250.0,"longitude":400.0}

REGION_COORDINATES_SPAN = {"latitudeSpan":500.0,"longitudeSpan":800.0}

REGION = {"center":CENTER_COORDINATES,"span":REGION_COORDINATES_SPAN}
         

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
### GET RECETTE
@app.route("/allRecette")
def getAllRecette():
    db = Db()
    result = db.select("SELECT * FROM public.Recipe")
    db.close()
    
    resp = make_response(json.dumps(result))
    resp.mimetype = 'application/json'
    return resp  
    
## GET TEMPS
@app.route("/metrology")
def getTemps():
    db = Db()
    result = db.select("SELECT * FROM public.Weather")
    db.close()
    
    timestamp = 0
    meteoPrevision = []
    
    for forcast in result :
        timestamp = forcast['weather_timestamp']
        donnee = {"weather" : forcast['weather_temps'], "dnf" : forcast['weather_dnf']}
        meteoPrevision.append(donnee)
    
    data = {"timestamp" : timestamp, "weather" : meteoPrevision}
    
    #data = {"timestamp" : 24, "weather" : "sunny"}
    return json.dumps(data),200,{'Content-Type' : 'application/json'}          
    
## GET MAP
@app.route("/map", methods=['GET'])
def getMap():
    queryRank = "SELECT * FROM player ORDER BY player_cash;"
    db = Db()
    resultRank = db.select(queryRank)
    db.close()
    ranking=[]
    player=[]
    playersInfo= {}
    itemsByPlayers={}
    drinksByPlayer={}
    
    for player in resultRank:
        ranking.append(player['player_name'])
        print player['player_name']
        #-----------------------PLAYER_INFO-----------------------
        #infos joueur de base
        queryPlayerInfo = "SELECT * FROM player WHERE player_name LIKE \'%s\';" % (player['player_name'])
        db = Db()
        resultPlayerInfo = db.select(queryPlayerInfo)
        db.close()
        
        #ventes joueur player depuis le debut
        queryPlayerSales = "SELECT SUM(v.vendre_qte*v.vendre_prix) AS nbventesdepuisdebut FROM player AS p,vendre AS v WHERE p.player_id = %d AND v.player_id=p.player_id ;" % (player['player_id'])
        db = Db()
        resultPlayerSales = db.select(queryPlayerSales)
        db.close()
        
        overallSales=0
        for sales in resultPlayerSales:
            overallSales=sales['nbventesdepuisdebut']
            if(overallSales==None):
                overallSales=0.0
        
        #recettes du joueur player
        queryPlayerRecipes = "SELECT r.recipe_id, r.recipe_name AS nom_recette,v.vendre_prix AS prix_recette, i.ingredient_iscold AS is_cold, i.ingredient_hasalcohol AS has_alcohol FROM vendre AS v,player AS p, recipe AS r, composer AS c, ingredient AS i WHERE p.player_id=%d AND p.player_id = v.player_id AND v.recipe_id=r.recipe_id AND r.recipe_id=c.recipe_id AND c.ingredient_id = i.ingredient_id;" % (player['player_id'])
        db = Db()
        resultPlayerRecipes = db.select(queryPlayerRecipes)
        db.close()
        
        
        
        drinksOffered=[]
        
        for recette in resultPlayerRecipes:
            uneRecette={"name":recette['nom_recette'],"price":recette['prix_recette'],"hasAlcohol":recette['has_alcohol'],"isCold":recette['is_cold']}
            drinksOffered.append(uneRecette)
        
        
        info={"cash":player['player_cash'],"sales":overallSales,"profit":0,"drinksOffered":drinksOffered}
        
        playersInfo[player['player_name']]=info;
        
        #-----------------------ITEMS_BY_PLAYER-----------------------
        
        queryItemsByPlayers = "SELECT * FROM player AS p,mapitem AS m WHERE p.player_id = %d AND p.player_id=m.player_id ;" % (player['player_id'])
        db = Db()
        resultPlayerInfo = db.select(queryItemsByPlayers)
        db.close()
        
        
        for item in resultPlayerInfo:
            locationMapItem = {"latitude":item['mapitem_latitude'],"longitude":item['mapitem_longitude']}
            unMapItem={"kind":item['mapitem_kind'],"owner":player['player_name'],"location":locationMapItem,"influence":item['mapitem_rayon']}
            itemsByPlayers[player['player_name']]=unMapItem
        
        
        #-----------------------DRINKS_BY_PLAYER-----------------------
        drinks=[]
        for drink in resultPlayerRecipes:
            uneRecette={"name":drink['r.recipe_name'],"price":drink['r.recipe_sell_price'],"hasAlcohol":drink['i.ingredient_hasalcohol'],"isCold":recette['i.ingredient_iscold']}
            drinks.append(uneRecette)
        drinksByPlayer[player['player_name']]=drinks
        
    
    map = {"region":REGION,"ranking":ranking,"playerInfo":playersInfo,"itemsByPlayers":itemsByPlayers,"drinksByPlayer":drinksByPlayer}
    
    Map = {"map" : map}
    return json.dumps(Map),200,{'Content-Type' : 'application/json'}


## GET PLAYER'S MAP
@app.route("/map/<string:playerName>", methods=['GET'])
def getPlayerSMap(playerName):
    queryPlayer = "SELECT * FROM player WHERE player_name LIKE %s;" % (playerName)
    db = Db()
    resultPlayer = db.select(queryPlayer)
    db.close()
    
    playerSIngredients={}
    playerInfo={}
    
    for player in resultPlayer:
        #ventes joueur player depuis le debut
        queryPlayerSales = "SELECT SUM(v.vendre_qte*v.vendre_prix) AS nbventesdepuisdebut FROM player AS p,vendre AS v WHERE p.player_id = %d AND v.player_id=p.player_id ;" % (player['player_id'])
        db = Db()
        resultPlayerSales = db.select(queryPlayerSales)
        db.close()
        
        overallSales=0
        for sales in resultPlayerSales:
            overallSales=sales['nbventesdepuisdebut']
            if(overallSales==None):
                overallSales=0.0
        
        
        #recettes du joueur player
        queryPlayerRecipes = "SELECT r.recipe_id, r.recipe_name AS nom_recette,v.vendre_prix AS prix_recette, i.ingredient_iscold AS is_cold, i.ingredient_hasalcohol AS has_alcohol FROM vendre AS v,player AS p, recipe AS r, composer AS c, ingredient AS i WHERE p.player_id=%d AND p.player_id = v.player_id AND v.recipe_id=r.recipe_id AND r.recipe_id=c.recipe_id AND c.ingredient_id = i.ingredient_id;" % (player['player_id'])
        db = Db()
        resultPlayerRecipes = db.select(queryPlayerRecipes)
        db.close()
        
        
        
        drinksOffered=[]
        
        for recette in resultPlayerRecipes:
            uneRecette={"name":recette['nom_recette'],"price":recette['prix_recette'],"hasAlcohol":recette['has_alcohol'],"isCold":recette['is_cold']}
            drinksOffered.append(uneRecette)
        
        playerInfo={"cash":player_cash,"sales":overallSales,"profit":player['player_profit'],"drinksOffered":drinksOffered}
    
    
    
    map = {"region":REGION}
    playerSMap={"map":map,"availableIngredients":playerSIngredients,"playerInfo":playerInfo}
    return json.dumps(PlayerSMap),200,{'Content-Type' : 'application/json'}
    


@app.route("/players")
def getPlayerTest():
    data = {"name" : "Toto", "location" : [{"latitude" : 23, "longitude" : 12}], "info" : [{"cash" : 1000.59, "sales" : 10, "profit" : 15.23, "drinksOffered" : [{"name" : "Limonade", "price" : 2.59, "hasAlcohol" : False, "isCold" : True},{"name" : "Mojito", "price" : 4.20, "hasAlcohol" : True, "isCold" : True}] }] }
    return json.dumps(data),200,{'Content-Type' : 'application/json'}
    
######################~/GET~###############################


######################~POST~###############################  
        
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
        
## POST Metrology
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
            query = "INSERT INTO public.Weather (Weather_id, Weather_timestamp, Weather_temps, Weather_Dnf) VALUES (%s,%s,\'%s\',%s) ON CONFLICT (Weather_id) DO UPDATE SET Weather_temps = \'%s\', Weather_timestamp = %s, Weather_Dnf = %s" %(cpt,time,forcast['weather'],forcast['dnf'],forcast['weather'],time,forcast['dnf'])
            db = Db()
            db.execute(query)
            db.close()
            cpt += 1;
        
        return json.dumps(data),201,{'Content-Type' : 'application/json'} 
        
## POST Player
@app.route('/players', methods=['POST'])
def postPlayer() :
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
            if player['player_name'] == data['name'] :
                query = "SELECT Player_latitude, Player_longitude, Player_cash, Player_profit, Recipe_name  FROM public.Player p, public.Recipe r, public.Avoir a WHERE p.Player_id = a.Player_id AND a.Recipe_id = r.Recipe_id AND public.Player.Player_name LIKE \'"+ data['name']+"\'"
                res_query = db.select(query)
                
                data_final = ''
                
                recipe = []
                
                for res in res_query :
                    recip = {"name" : res['name']  , "price" : 0, "hasAlcohol" : False, "isCold" : True}
                    recipe.append(recip)
                    data_final = {"name" : data['name'], "location" : {"latitude" : res['player_latitude'], "longitude" : res['Player_longitude']}, "info" : [{"cash" : res['Player_cash'], "sales" : 0, "profit" : res['player_profit'],"drinksOffered" : recipe}]  }
                #data = {"IsAccepted" : False}
                
                db.close()
                return json.dumps(data_final),200,{'Content-Type' : 'application/json'}
        
        random_longitude = random.uniform(0,REGION_COORDINATES_SPAN['longitudeSpan'])
        random_latitude = random.uniform(0,REGION_COORDINATES_SPAN['latitudeSpan'])
        print random_latitude
        print random_longitude 
        query_addPlayer = "INSERT INTO public.Player (Player_name, Player_cash, Player_profit, Player_latitude, Player_longitude) VALUES (\'"+data['name']+"\',100.0,0.0,"+str(random_latitude)+","+str(random_longitude)+")"
        db.execute(query_addPlayer)
        query_select = db.select("SELECT Player_id, Player_latitude, Player_longitude FROM public.Player WHERE public.Player.Player_name LIKE \'"+ data['name']+"\'")
        
        for res in query_select :
            query = "INSERT INTO public.MapItem (MapItem_kind, MapItem_latitude, MapItem_longitude, MapItem_rayon, Player_id) VALUES (\'stand\',"+str(res['player_latitude'])+","+str(res['player_longitude'])+",10,"+str(res['player_id'])+")"
            db.execute(query)
            query = "INSERT INTO public.Avoir (Player_id, Recipe_id) VALUES ("+str(res['player_id'])+",1)"
            db.execute(query)
        
        query = "SELECT p.Player_latitude, p.Player_longitude, p.Player_cash, p.Player_profit FROM public.Player p WHERE p.Player_name LIKE \'"+data['name']+"\'"
        
        query_select = db.select(query)
        
        data_final = ''
        
        for res in query_select :
            data_final = {"name" : data['name'], "location" : {"latitude" : res['player_latitude'], "longitude" : res['player_longitude']}, "info" : [{"cash" : res['player_cash'], "sales" : 0, "profit" : res['player_profit'], "drinksOffered" : [{"name" : "Limonade", "price" : 0, "hasAlcohol" : False, "isCold" : True}] }] }
        
        db.close()
        
        return json.dumps(data_final),201,{'Content-Type' : 'application/json'} 
        
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
        return '"Insufficient Funds."', 412, {'Content-type' : 'Application/Json'}
  
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
    
