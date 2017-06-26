------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------
DROP TABLE IF EXISTS public.Resultat_vente;
DROP TABLE IF EXISTS public.A_besoin_pour_recette;
DROP TABLE IF EXISTS public.Achete_recette;
DROP TABLE IF EXISTS public.Meteo;
DROP TABLE IF EXISTS public.MapItem;
DROP TABLE IF EXISTS public.Ingredient;
DROP TABLE IF EXISTS public.Recipe;
DROP TABLE IF EXISTS public.Player;
DROP TABLE IF EXISTS public.Test;

------------------------------------------------------------
-- Table: Player
------------------------------------------------------------
CREATE TABLE public.Player(
	Player_ID                  SERIAL NOT NULL ,
	Player_name                VARCHAR (25)  ,
	Player_banque              FLOAT   ,
	Player_profit_depuis_impot FLOAT   ,
	CONSTRAINT prk_constraint_Player PRIMARY KEY (Player_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Ingredient
------------------------------------------------------------
CREATE TABLE public.Ingredient(
	Ingredient_ID    SERIAL NOT NULL ,
	Ingredient_name  VARCHAR (25)  ,
	Ingredient_cost FLOAT   ,
	Ingredient_hasAlcohol BOOL   ,
	Ingredient_isCold BOOL ,
	CONSTRAINT prk_constraint_Ingredient PRIMARY KEY (Ingredient_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Recipe
------------------------------------------------------------
CREATE TABLE public.Recipe(
	Recipe_ID         SERIAL NOT NULL ,
	Recipe_name       VARCHAR (25)  ,
	Recipe_isCold     BOOL   ,
	Recipe_hasAlcohol BOOL   ,
	Recipe_sell_price INT   ,
	Cree_recette_date DATE   ,
	Player_ID         INT   ,
	CONSTRAINT prk_constraint_Recipe PRIMARY KEY (Recipe_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: MapItem
------------------------------------------------------------
CREATE TABLE public.MapItem(
	MapItem_ID               SERIAL NOT NULL ,
	MapItem_kind             VARCHAR (25)  ,
	MapItem_X                INT   ,
	MapItem_Y                INT   ,
	MapItem_surface          FLOAT   ,
	Acquerir_date    		 INT   ,
	Acquerir_prix 			 FLOAT   ,
	Player_ID                INT   ,
	CONSTRAINT prk_constraint_MapItem PRIMARY KEY (MapItem_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: meteo
------------------------------------------------------------
CREATE TABLE public.Meteo(
	Meteo_ID   			SERIAL NOT NULL   ,
	Meteo_Timestamp 	INT   ,
	Meteo_Temps 		VARCHAR (25)   ,
	Meteo_Dnf			INT   ,
	CONSTRAINT prk_constraint_meteo PRIMARY KEY (Meteo_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: achete_recette
------------------------------------------------------------
CREATE TABLE public.Achete_recette(
	Achete_recette_date DATE   ,
	Player_ID           BIGINT  NOT NULL ,
	Recipe_ID           BIGINT  NOT NULL ,
	CONSTRAINT prk_constraint_achete_recette PRIMARY KEY (Player_ID,Recipe_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: a_besoin_pour_recette
------------------------------------------------------------
CREATE TABLE public.A_besoin_pour_recette(
	Besoin_Quantitee INT   ,
	Recipe_ID        BIGINT  NOT NULL ,
	Ingredient_ID    BIGINT  NOT NULL ,
	CONSTRAINT prk_constraint_a_besoin_pour_recette PRIMARY KEY (Recipe_ID,Ingredient_ID)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: resultat_vente
------------------------------------------------------------
CREATE TABLE public.Resultat_vente(
	Resultat_vente_faite   INT   ,
	Resultat_vente_rate    INT   ,
	Resultat_vente_produit INT   ,
	Resultat_vente_date    DATE   ,
	Player_ID              BIGINT  NOT NULL ,
	Recipe_ID              BIGINT  NOT NULL ,
	CONSTRAINT prk_constraint_resultat_vente PRIMARY KEY (Player_ID,Recipe_ID)
)WITHOUT OIDS;

------------------------------------------------------------
-- Table: Test
------------------------------------------------------------
CREATE TABLE public.Test(
	id_test   SERIAL NOT NULL   ,
	nom_test  VARCHAR (25)   ,
	CONSTRAINT prk_constraint_test PRIMARY KEY (id_test)
)WITHOUT OIDS;



ALTER TABLE public.Recipe ADD CONSTRAINT FK_Recipe_Player_ID FOREIGN KEY (Player_ID) REFERENCES public.Player(Player_ID);
ALTER TABLE public.MapItem ADD CONSTRAINT FK_MapItem_Player_ID FOREIGN KEY (Player_ID) REFERENCES public.Player(Player_ID);
ALTER TABLE public.achete_recette ADD CONSTRAINT FK_achete_recette_Player_ID FOREIGN KEY (Player_ID) REFERENCES public.Player(Player_ID);
ALTER TABLE public.achete_recette ADD CONSTRAINT FK_achete_recette_Recipe_ID FOREIGN KEY (Recipe_ID) REFERENCES public.Recipe(Recipe_ID);
ALTER TABLE public.a_besoin_pour_recette ADD CONSTRAINT FK_a_besoin_pour_recette_Recipe_ID FOREIGN KEY (Recipe_ID) REFERENCES public.Recipe(Recipe_ID);
ALTER TABLE public.a_besoin_pour_recette ADD CONSTRAINT FK_a_besoin_pour_recette_Ingredient_ID FOREIGN KEY (Ingredient_ID) REFERENCES public.Ingredient(Ingredient_ID);
ALTER TABLE public.resultat_vente ADD CONSTRAINT FK_resultat_vente_Player_ID FOREIGN KEY (Player_ID) REFERENCES public.Player(Player_ID);
ALTER TABLE public.resultat_vente ADD CONSTRAINT FK_resultat_vente_Recipe_ID FOREIGN KEY (Recipe_ID) REFERENCES public.Recipe(Recipe_ID);



INSERT INTO public.Test(
	id_test, nom_test)
	VALUES (1, 'Sprite');
	
INSERT INTO public.Test(
	id_test, nom_test)
	VALUES (2, 'Coca');

INSERT INTO public.Test(
	id_test, nom_test)
	VALUES (3, 'Jus');			

INSERT INTO public.Meteo(
	Meteo_Temps, Meteo_Date)
	VALUES ('NONE', 0);		