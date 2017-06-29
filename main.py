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

REGION_COORDINATES_SPAN = {"latitudeSpan":800.0,"longitudeSpan":500.0}

REGION = {"center":CENTER_COORDINATES,"span":REGION_COORDINATES_SPAN}

######PRIX
#Imobilier
RANGE_PRIX = 10

#Recette
CREATION_RECETTE = 700
ACHAT_NOUVELLE_RECETTE = CREATION_RECETTE + 300
         

################################################################################
### Fonction idCold
def recetteIsCold(name_recette):
    isCold = False
    query ="SELECT i.Ingredient_isCold FROM Ingredient i, Recipe r, Composer c WHERE r.Recipe_id = c.Recipe_id AND c.Ingredient_id = i.Ingredient_id AND r.Recipe_name LIKE \'"+str(name_recette)+"\'"
    db = Db()
    result = db.select(query)
    for res in result:
        if res['ingredient_iscold'] == True :
            isCold = True
    db.close()
    return isCold
    
### Fonction hasAlcohol
def recetteHasAlcohol(name_recette):
    hasAlcohol = False
    query ="SELECT i.Ingredient_hasAlcohol FROM Ingredient i, Recipe r, Composer c WHERE r.Recipe_id = c.Recipe_id AND c.Ingredient_id = i.Ingredient_id AND r.Recipe_name LIKE \'"+str(name_recette)+"\'"
    db = Db()
    result = db.select(query)
    for res in result:
        if res['ingredient_hasalcohol'] == True :
            hasAlcohol = True
    db.close()
    return hasAlcohol    

### Fonction prixProduction
def prixProduction(name_recette):
    query ="SELECT SUM(i.Ingredient_price * c.Compose_qte) AS Price, r.Recipe_name FROM Ingredient i, Recipe r, Composer c WHERE r.Recipe_id = c.Recipe_id AND c.Ingredient_id = i.Ingredient_id AND r.Recipe_name LIKE \'"+str(name_recette)+"\' GROUP BY (r.Recipe_id)"
    db = Db()
    price = ''
    result = db.select(query)
    for res in result:
        price = res['price']
    db.close()
    return price
    
    
### Fonction getIngredients
def getAviableIngredients():
    query ="SELECT * FROM ingredient "
    db = Db()
    ingredients=[]
    result = db.select(query)
    db.close()
    for res in result:
        unIngredient={"name":res['ingredient_name'],"cost":res['ingredient_price'],"isCold":res['ingredient_iscold'],"hasAlcohol":res['ingredient_hasalcohol']}
        ingredients.append(unIngredient)
    return ingredients
    
    
### Fonction Sales
def modifyStock(playerName,recipeName,productQuantity):
    
    day=0
    #on renvoie sales avec la quantité avant le débit
    jsonRetour={}
    
    #récupérer la date d'aujourd'hui
    day=getToDay()
    
    #récupérer le stock correspondant pour un joueur a l'heure actuelle
    query ="SELECT p.player_id AS player_id, r.recipe_id AS recipe_id, v.vendre_nonvendu AS stock_qte FROM player p,recipe r , vendre v WHERE p.player_name LIKE \'%s\' AND p.player_id=v.player_id AND v.recipe_id=r.recipe_id AND r.recipe_name LIKE \'%s\' AND v.vendre_date=%d" % (playerName,recipeName,day)
    db = Db()
    result = db.select(query)
    for res in result:
        if(res['stock_qte']<productQuantity):
            productQuantity=res['stock_qte']
        
        jsonRetour['player']=playerName
        jsonRetour['item']=recipeName
        jsonRetour['quantity']=res['stock_qte']
        
         #on calcule le profit
        query ="SELECT v.vendre_prix AS prix FROM player p,vendre v,recipe r WHERE p.player_id=%d AND p.player_id=v.player_id AND r.recipe_id=v.recipe_id AND r.recipe_id=%d AND v.vendre_date=%d;" % (res['player_id'],res['recipe_id'],day)
        db = Db()
        resultProfit = db.select(query)
        db.close()
        
        if(len(resultProfit)==0):
            jsonRetour['player']=playerName
            jsonRetour['item']=recipeName
            jsonRetour['quantity']=0
            return jsonRetour
        
        #on change la quantité en stock
        query ="UPDATE vendre SET vendre_nonvendu = vendre_nonvendu - %d WHERE player_id=%d AND recipe_id=%d AND vendre_date=%d;" % (productQuantity,res['player_id'],res['recipe_id'],day)
        db = Db()
        result = db.execute(query)
        #on ajoute la quantité vendue
        query ="UPDATE vendre SET vendre_qte =vendre_qte + %d WHERE player_id=%d AND recipe_id=%d AND vendre_date=%d;" % (productQuantity,res['player_id'],res['recipe_id'],day)
        db = Db()
        result = db.execute(query)
        db.close()
        
        for resPrix in resultProfit:
            #on change le profit et le bénéfice
            query ="UPDATE player SET player_profit = player_profit + %f WHERE player_id=%d;" % (resPrix['prix']*productQuantity,res['player_id'])
            db = Db()
            result = db.execute(query)
            db.close()
            
        return jsonRetour

### Get id Player by Name
def getIdPlayerByName(PlayerName) :
    query_select = "SELECT Player_id FROM Player WHERE Player_name LIKE \'%s\'" % (PlayerName)
                
    db = Db()
    result = db.select(query_select)
    player_id = ""
    
    for id_player in result :
        player_id = id_player['player_id']
        
    return player_id 
    
### Get id Player by Name
def getIdRecipeByName(RecipeName) :
    query_select = "SELECT Recipe_id FROM Recipe WHERE Recipe_name LIKE \'"+str(RecipeName)+"\'"
                
    db = Db()
    result = db.select(query_select)
    recipe_id = ""
    
    for id_recipe in result :
        recipe_id = id_recipe['recipe_id']
            
    return recipe_id      
    
    

### Get id mapitem by infos
def getIdMapitemByInfos(playerId,latitude,longitude) :
    query_select = "SELECT mapitem_id FROM mapitem WHERE player_id = %d AND mapitem_date=%d AND mapitem_latitude=%f AND mapitem_longitude=%f" % (playerId,getToDay(),latitude,longitude) 
                
    db = Db()
    result = db.select(query_select)
    mapitem_id = ''
    
    if(len(result)==0):
        mapitem_id=0
    else:
        for mapitem in result :
            mapitem_id = int(mapitem['mapitem_id'])
    print "mapitem_id"
    print mapitem_id
    return mapitem_id

### Get Cash Player by Name
def getCashByName(PlayerName) :
    query_select = "SELECT Player_cash FROM Player WHERE Player_name LIKE \'"+str(PlayerName)+"\'"   
    db = Db()
    result = db.select(query_select)
    cash = ""
    for cash_player in result :
        cash = cash_player['player_cash']    
    return cash
###

### Get Day
def getToDay() :
    valueDay = ''
    queryPreviousTime = "SELECT Weather_timestamp FROM Weather WHERE Weather_dfn = 0"
    db = Db()
    today = db.select(queryPreviousTime)
    for day in today:
        valueDay = day['weather_timestamp']
        valueDay = int(valueDay) / 24
    db.close()
    
    return valueDay 

### Fonction Traitement des actions minuit
def traitementMinuit():
    #on récupère les players
    query_select = "SELECT Player_id FROM Player ;"
    db = Db()
    result = db.select(query_select)
    
    for player in result:
        
        #on passe le profit dans cash
        query ="UPDATE player SET player_cash = player_profit, player_profit = 0 WHERE player_id=%d ;" % (player['player_id'])
        db = Db()
        result = db.execute(query)
    
    return 0
    
### Fonction GetMeteo
def getMeteo():
    weather_name = ''
    query_select = "SELECT Weather_name FROM Weather WHERE Weather_dfn = 0;"
    db = Db()
    result = db.select(query_select)
    
    for weather in result:
        weather_name = weather["weather_name"]
        
    return weather_name
    
    
### ActionCash
def actionCash(playerName,cash_to_add) :
    cash = ''
    querry = "UPDATE player SET Player_cash = Player_cash + %f WHERE player_id=%d" % (cash_to_add,getIdPlayerByName(playerName)) 
    
    db = Db()
    result = db.execute(querry)
    
          
### Fonction Traitement d'un pb de metrology
def resetMetrology():
    
    return 0
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
        donnee = {"weather" : forcast['weather_temps'], "dfn" : forcast['weather_dfn']}
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
    day=getToDay()
    
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
        queryPlayerSales = "SELECT SUM(v.vendre_qte) AS nbventesdepuisdebut FROM player AS p,vendre AS v WHERE p.player_id = %d AND v.player_id=p.player_id ;" % (player['player_id'])
        db = Db()
        resultPlayerSales = db.select(queryPlayerSales)
        db.close()
        
        overallSales=""
        
        for sales in resultPlayerSales:
            overallSales=sales['nbventesdepuisdebut']
            if(overallSales==None):
                overallSales=0
        
       #recettes produites du joueur player avec prix de vente
        queryPlayerRecipes = "SELECT BOOL(COUNT(nullif(i.ingredient_iscold, false))>0) AS is_cold, BOOL(COUNT(nullif(i.ingredient_hasalcohol, false))>0) AS has_alcohol, r.recipe_name AS nom_recette,v.vendre_prix AS prix_recette FROM weather AS w,vendre AS v,player AS p, recipe AS r, composer AS c, ingredient AS i WHERE p.player_id=%d AND p.player_id = v.player_id AND v.recipe_id=r.recipe_id AND r.recipe_id=c.recipe_id AND c.ingredient_id = i.ingredient_id AND v.vendre_date<=w.weather_timestamp/24 GROUP BY r.recipe_id, v.vendre_prix;"% (player['player_id'])
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
        
        queryItemsByPlayers = "SELECT * FROM player AS p,mapitem AS m WHERE p.player_id = %d AND p.player_id=m.player_id AND m.mapitem_date <= %d;" % (player['player_id'],day)
        db = Db()
        resultPlayerInfo = db.select(queryItemsByPlayers)
        db.close()
        
        mapitems_player = []
        for item in resultPlayerInfo:
            locationMapItem = {"latitude":item['mapitem_latitude'],"longitude":item['mapitem_longitude']}
            unMapItem={"kind":item['mapitem_kind'],"owner":player['player_name'],"location":locationMapItem,"influence":(item['mapitem_rayon']*item['mapitem_rayon']*RANGE_PRIX)}
            mapitems_player.append(unMapItem)
            
        itemsByPlayers[player['player_name']]=mapitems_player
        
        
        #-----------------------DRINKS_BY_PLAYER-----------------------
        
        #recettes connue du joueur player avec prix de prod
        queryPlayerKnownRecipes = "SELECT BOOL(COUNT(nullif(i.ingredient_iscold, false))>0) AS is_cold, BOOL(COUNT(nullif(i.ingredient_hasalcohol, false))>0) AS has_alcohol, r.recipe_name AS nom_recette FROM weather AS w, avoir AS a,player AS p, recipe AS r, composer AS c, ingredient AS i WHERE p.player_id=%d AND p.player_id = a.player_id AND a.recipe_id=r.recipe_id AND r.recipe_id=c.recipe_id AND c.ingredient_id = i.ingredient_id AND a.avoir_date<=w.weather_timestamp/24 GROUP BY r.recipe_id,a.recipe_id;"% (player['player_id'])
        db = Db()
        resultPlayerKnownRecipes = db.select(queryPlayerKnownRecipes)
        db.close()
        
        
        drinks=[]
        for drink in resultPlayerKnownRecipes:
            uneRecette={"name":drink['nom_recette'],"price":prixProduction(drink['nom_recette']),"hasAlcohol":drink['has_alcohol'],"isCold":drink['is_cold']}
            drinks.append(uneRecette)
        drinksByPlayer[player['player_name']]=drinks
        
    
    map = {"region":REGION,"ranking":ranking,"playerInfo":playersInfo,"itemsByPlayers":itemsByPlayers,"drinksByPlayer":drinksByPlayer}
    
    Map = {"map" : map}
    return json.dumps(Map),200,{'Content-Type' : 'application/json'}





## GET PLAYER'S MAP
@app.route("/map/<string:playerName>", methods=['GET'])
def getPlayerSMap(playerName):
    
    queryRank = "SELECT * FROM player ORDER BY player_cash;"
    db = Db()
    resultRank = db.select(queryRank)
    db.close()
    day=getToDay()
    
    ranking=[]
    playerSIngredients=getAviableIngredients()
    playerInfo={}
    itemsByPlayers={}
    
    for player in resultRank:
        ranking.append(player['player_name'])
    
    
#-----------------------PLAYER_INFO-----------------------
    #infos joueur de base
    queryPlayer = "SELECT * FROM player WHERE player_name LIKE \'%s\';" % (playerName)
    db = Db()
    resultPlayer = db.select(queryPlayer)
    db.close()
    
    
    for player in resultPlayer:
        #ventes joueur player depuis le debut
        queryPlayerSales = "SELECT SUM(v.vendre_qte) AS nbventesdepuisdebut FROM player AS p,vendre AS v WHERE p.player_id = %d AND v.player_id=p.player_id ;" % (player['player_id'])
        db = Db()
        resultPlayerSales = db.select(queryPlayerSales)
        db.close()
        
        overallSales=0
        for sales in resultPlayerSales:
            overallSales=sales['nbventesdepuisdebut']
            if(overallSales==None):
                overallSales=0.0
        
        
        #recettes du joueur player avec prix de vente 
        queryPlayerRecipes = "SELECT BOOL(COUNT(nullif(i.ingredient_iscold, false))>0) AS is_cold, BOOL(COUNT(nullif(i.ingredient_hasalcohol, false))>0) AS has_alcohol, r.recipe_id, r.recipe_name AS nom_recette FROM weather AS w, avoir AS a,player AS p, recipe AS r, composer AS c, ingredient AS i WHERE p.player_id=%d AND p.player_id = a.player_id AND a.recipe_id=r.recipe_id AND r.recipe_id=c.recipe_id AND c.ingredient_id = i.ingredient_id AND a.avoir_date<=w.weather_timestamp/24 GROUP BY r.recipe_id, a.recipe_id;"% (player['player_id'])
        db = Db()
        resultPlayerRecipes = db.select(queryPlayerRecipes)
        db.close()
        
        
        
        drinksOffered=[]
        
        for recette in resultPlayerRecipes:
            uneRecette={"name":recette['nom_recette'],"price":prixProduction(recette['nom_recette']),"hasAlcohol":recette['has_alcohol'],"isCold":recette['is_cold']}
            drinksOffered.append(uneRecette)
        
        playerInfo={"cash":player['player_cash'],"sales":overallSales,"profit":player['player_profit'],"drinksOffered":drinksOffered}
    
        queryItemsByPlayers = "SELECT * FROM player AS p,mapitem AS m WHERE p.player_id = %d AND p.player_id=m.player_id AND m.mapitem_date <= %d;" % (player['player_id'],day)
        db = Db()
        resultPlayerInfo = db.select(queryItemsByPlayers)
        db.close()
        
        
        mapitems_player = []
        for item in resultPlayerInfo:
            locationMapItem = {"latitude":item['mapitem_latitude'],"longitude":item['mapitem_longitude']}
            unMapItem={"kind":item['mapitem_kind'],"owner":player['player_name'],"location":locationMapItem,"influence":(item['mapitem_rayon']*item['mapitem_rayon']*RANGE_PRIX)}
            mapitems_player.append(unMapItem)
        itemsByPlayers[player['player_name']]=mapitems_player
        
        
        
        map = {"region":REGION,"ranking":ranking,"itemsByPlayers":itemsByPlayers}
        playerSMap={"map":map,"availableIngredients":playerSIngredients,"playerInfo":playerInfo}
        return json.dumps(playerSMap),200,{'Content-Type' : 'application/json'}

    
######################~/GET~###############################
    
    
######################~POST~###############################  
        
## POST Sales
@app.route('/sales', methods=['POST'])
def postSales():
    data = request.get_json()
    sales=data['sales']
    salesArray=[]
    for sale in sales:
        #on récupère les infos du json avant de demander une modification du stock
        salesArray.append(modifyStock(sale['player'],sale['item'],sale['quantity']))
    
    retour = {"sales":salesArray}
    return json.dumps(retour),200,{'Content-Type' : 'application/json'}

        
## POST Actions playerName
@app.route('/actions/<string:playerName>', methods=['POST'])
def postActionPlayer(playerName) :
    # {'action' : [], 'simulated' : true} 
    allData = request.get_json() 
    
    if allData == None :
        print request.get_data()
        return '"None in postActionPlayer"',400,{'Content-Type' : 'application/json'}
    else :
        
        print allData
        
        data = allData['actions']
        if(len(data)==0):
            return '{"status":"OK"}',200,{'Content-Type' : 'application/json'}
            #DROP toutes les lignes du player a la date de demain######################################################"
            
        id_player = getIdPlayerByName(playerName)
        today = int(getToDay())
        getTomorrow = today+1
        
        for actions in data :    
            
            if actions['kind'] == 'ad' :
                location = actions['location']
                radius = float(actions['radius'])
                longitude = ''
                latitude = ''
                
                for locate in location :
                    longitude = locate['longitude']
                    latitude = locate['latitude']
                
                newPrice = (radius * radius * RANGE_PRIX)
                
                queryPriceB4 = "SELECT * FROM mapitem WHERE MapItem_kind='ad' AND MapItem_date=%d AND MapItem_latitude=%f AND MapItem_longitude=%f AND player_id=%d;" %(getTomorrow,latitude,longitude,id_player)
                db = Db()
                resultPriceB4 = db.select(queryPriceB4)
                db.close()
                
                currentPrice=''
                if (len(resultPriceB4)==0):
                    currentPrice =0.0
                else:
                    for prixDuMapitem in resultPriceB4:
                        print prixDuMapitem['mapitem_rayon']
                        currentPrice = float(prixDuMapitem['mapitem_rayon'])*float(prixDuMapitem['mapitem_rayon'])*float(RANGE_PRIX)
                print "newPrice"
                print newPrice
                print "currentPrice"
                print currentPrice
                #si on est couramment à un prix de 0, la différence correspond au nouveau prix
                diff = newPrice - currentPrice
                print "diff"
                print diff
                
                #donc on compare le cash avec la différence
                if getCashByName(playerName) > diff :
                
                    query =''
                
                    id_mapitem = getIdMapitemByInfos(id_player,latitude,longitude)
                    if(id_mapitem==0):
                        query = "INSERT INTO MapItem (MapItem_kind, MapItem_latitude, MapItem_longitude, MapItem_rayon, MapItem_date, Player_id) VALUES ('ad',"+str(latitude)+","+str(longitude)+","+str(radius)+","+str(getToDay())+","+str(id_player)+");"
                    else:
                        query = "UPDATE mapitem SET mapitem_rayon = mapitem_rayon + (%f) WHERE mapitem_id=%d;" %(diff,id_mapitem)
                        
                    db = Db()
                    db.execute(query)
                    db.close()
                    
                    
                    actionCash(playerName, -diff)

                    data = {"sufficientFunds" : True, "totalCost" : currentPrice+diff}

                    #return {"sufficientFunds" : boolean, "totalCost" : float}
                    return json.dumps(data),201,{'Content-Type' : 'application/json'}

                else :
                    data = {"sufficientFunds" : False, "totalCost" : currentPrice}
                    return json.dumps(data),200,{'Content-Type' : 'application/json'}
               
                 
            elif actions['kind'] == 'drinks' :
                string_drinks = ''
                for prepare in actions['prepare'] :
                    string_drinks = prepare
                qte = actions['prepare'][string_drinks]
                
                newPrice = prixProduction(string_drinks) * qte
                
                queryPriceB4 = "SELECT * FROM vendre WHERE recipe_id=%d AND player_id = %d AND vendre_date=%d;" %(getIdRecipeByName(actions['prepare']),getIdPlayerByName(playerName),getTomorrow)
                db = Db()
                resultPriceB4 = db.select(queryPriceB4)
                db.close()
                
                currentPrice=''
                if (resultPriceB4==None):
                    currentPrice =0
                else:
                    for prixDeLaRecipe in resultPriceB4:
                        currentPrice = float(prixDeLaRecipe['vendre_prix'])*float(prixDeLaRecipe['vendre_qte'])
                
                #si on est couramment à un prix de 0, la différence correspond au nouveau prix
                diff = newPrice - currentPrice
                
                #donc on compare le cash avec la différence
                if getCashByName(playerName) > diff :
                    price = actions['price'][string_drinks]
                    id_recipe = getIdRecipeByName(string_drinks)
                    meteo = getMeteo()
                    
                    querry_insert_vendre = "INSERT INTO public.Vendre (Vendre_meteo, Vendre_qte, Vendre_nonVendu, Vendre_prix, Vendre_date, Player_id, Recipe_id) VALUES (\'"+str(meteo)+"\',0,"+str(qte)+","+str(price)+","+str(getTomorrow)+","+str(id_player)+","+str(id_recipe)+") ON CONFLICT (Player_id,Vendre_date,Recipe_id) DO UPDATE SET Vendre_meteo = \'"+str(meteo)+"\' ,Vendre_qte = 0, Vendre_nonVendu = "+str(qte)+", Vendre_prix = "+str(price)+", Vendre_date = "+str(getTomorrow)+", Player_id = "+str(id_player)+", Recipe_id ="+str(id_recipe)+";"
                    
                    actionCash(playerName, -diff )
                    
                    data = {"sufficientFunds" : True, "totalCost" : currentPrice+diff}

                    #return {"sufficientFunds" : boolean, "totalCost" : float}
                    return json.dumps(data),201,{'Content-Type' : 'application/json'}
                else :
                    data = {"sufficientFunds" : False, "totalCost" : currentPrice}
                    return json.dumps(data),200,{'Content-Type' : 'application/json'}
                
                    
            
            #elif actions['kind'] == 'recipe' :
            #   
            #   
            #   
            #    recipes = actions['recipe']
            #    name_recipe = ""
            #    tab_ingredient = []
            #    for recipe in recipes :
            #        name_recipe = recipe['name']
            #        for ingredient in recipe['ingredient'] :
            #            tab_ingredient.append(ingredient)
            #            
            #    query_insert_recipe = "INSERT INTO Recipe (Recipe_name,Recipe_pricePurchase) VALUES (\'"+name_recipe+"\’,"+str(ACHAT_NOUVELLE_RECETTE)+")"
            #    db.execute(query_insert_recipe)
            #    id_recipe = getIdRecipeByName(name_recipe)
            #    query_insert_avoir = "INSERT INTO Avoir (Player_id,Recipe_id) VALUES ("+id_player+","+id_recipe+")"
            #    db.execute(query_insert_avoir)
                
            else :
                return '"Bad kind Action"',400,{'Content-Type' : 'application/json'} 
                            
        #TODO
        query = ""
        #db = Db()
        #db.execute(query)
        #db.close()
        
        #return {"sufficientFunds" : boolean, "totalCost" : float}

        return json.dumps(''),200,{'Content-Type' : 'application/json'}        

        
## POST Metrology
@app.route('/metrology', methods=['POST'])
def postMetrology() :
    #print request.get_data() 
    data = request.get_json(force=True) 
    
    previous_day=getToDay()
    
    if data == None :
        print request.get_data()
        return '"None in postTemps verifier le Header"',400,{'Content-Type' : 'application/json'}
    else :
        #print data 
        time = data['timestamp']
        temps = data['weather']
        cpt = 1
        
        for forcast in temps :
            query = "INSERT INTO public.Weather (Weather_id, Weather_timestamp, Weather_temps, Weather_dfn) VALUES (%s,%s,\'%s\',%s) ON CONFLICT (Weather_id) DO UPDATE SET Weather_temps = \'%s\', Weather_timestamp = %s, Weather_dfn = %s" %(cpt,time,forcast['weather'],forcast['dfn'],forcast['weather'],time,forcast['dfn'])
            db = Db()
            db.execute(query)
            db.close()
            cpt += 1;
            
        today=getToDay()
        #on compare le jour précédent avec le jour courant
        
        if(today - previous_day>0):
            traitementMinuit()
        else:
            if(today - previous_day<0):
                resetMetrology()
        
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
                query = "SELECT Player_latitude, Player_longitude, Player_cash, Player_profit, Recipe_name  FROM public.Player p, public.Recipe r, public.Avoir a WHERE p.Player_id = a.Player_id AND a.Recipe_id = r.Recipe_id AND p.Player_name LIKE \'"+ data['name']+"\'"
                res_query = db.select(query)
                data_final = ''
                recipe = []
                for res in res_query :
                    recip = {"name" : res['recipe_name']  , "price" : str(prixProduction(res['recipe_name'])), "hasAlcohol" : recetteHasAlcohol(res['recipe_name']), "isCold" : recetteIsCold(res['recipe_name'])}
                    recipe.append(recip)
                    sales = prixProduction(data['name'])
                    data_final = {"name" : data['name'], "location" : {"latitude" : res['player_latitude'], "longitude" : res['player_longitude']}, "info" : {"cash" : res['player_cash'], "sales" : 0, "profit" : res['player_profit'],"drinksOffered" : recipe }  }
                db.close()
                return json.dumps(data_final),200,{'Content-Type' : 'application/json'}
        
        random_longitude = random.uniform(0,REGION_COORDINATES_SPAN['longitudeSpan'])
        random_latitude = random.uniform(0,REGION_COORDINATES_SPAN['latitudeSpan'])
        query_addPlayer = "INSERT INTO public.Player (Player_name, Player_cash, Player_profit, Player_latitude, Player_longitude) VALUES (\'"+data['name']+"\',100.0,0.0,"+str(random_latitude)+","+str(random_longitude)+")"
        db.execute(query_addPlayer)
        query_select = db.select("SELECT Player_id, Player_latitude, Player_longitude FROM public.Player WHERE public.Player.Player_name LIKE \'"+ data['name']+"\'")
        
        print getToDay()
        
        for res in query_select :
            query = "INSERT INTO public.MapItem (MapItem_kind, MapItem_latitude, MapItem_longitude, MapItem_rayon, MapItem_date, Player_id) VALUES (\'stand\',"+str(res['player_latitude'])+","+str(res['player_longitude'])+",10,"+str(getToDay())+","+str(res['player_id'])+")"
            db.execute(query)
            query = "INSERT INTO public.Avoir (Player_id, Recipe_id, Avoir_date) VALUES ("+str(res['player_id'])+",1,"+str(getToDay())+")"
            db.execute(query)
        
        query = "SELECT p.Player_latitude, p.Player_longitude, p.Player_cash, p.Player_profit FROM public.Player p WHERE p.Player_name LIKE \'"+data['name']+"\'"
        query_select = db.select(query)
        data_final = ''
        
        for res in query_select :
            data_final = {"name" : data['name'], "location" : {"latitude" : res['player_latitude'], "longitude" : res['player_longitude']}, "info" : {"cash" : res['player_cash'], "sales" : 0, "profit" : res['player_profit'], "drinksOffered" : [{"name" : "Limonade", "price" : 0, "hasAlcohol" : False, "isCold" : True}] } }

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
    
