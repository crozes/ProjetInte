------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------
 
DROP TABLE IF EXISTS public.Vendre;
DROP TABLE IF EXISTS public.Avoir;
DROP TABLE IF EXISTS public.Composer;
DROP TABLE IF EXISTS public.Weather;
DROP TABLE IF EXISTS public.MapItem;
DROP TABLE IF EXISTS public.Ingredient;
DROP TABLE IF EXISTS public.Recipe;
DROP TABLE IF EXISTS public.Player;

------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------


------------------------------------------------------------
-- Table: Player
------------------------------------------------------------
CREATE TABLE public.Player(
	Player_id        BIGSERIAL  NOT NULL ,
	Player_name      VARCHAR (255)  ,
	Player_cash      FLOAT   ,
	Player_profit    FLOAT   ,
	Player_longitude FLOAT   ,
	Player_latitude  FLOAT   ,
	CONSTRAINT prk_constraint_Player PRIMARY KEY (Player_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Recipe
------------------------------------------------------------
CREATE TABLE public.Recipe(
	Recipe_id            BIGSERIAL  NOT NULL ,
	Recipe_name          VARCHAR (255)  ,
	Recipe_pricePurchase FLOAT   ,
	CONSTRAINT prk_constraint_Recipe PRIMARY KEY (Recipe_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Ingredient
------------------------------------------------------------
CREATE TABLE public.Ingredient(
	Ingredient_id         BIGSERIAL  NOT NULL ,
	Ingredient_name       VARCHAR (255)  ,
	Ingredient_isCold     BOOL   ,
	Ingredient_hasAlcohol BOOL   ,
	Ingredient_price      FLOAT   ,
	CONSTRAINT prk_constraint_Ingredient PRIMARY KEY (Ingredient_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: MapItem
------------------------------------------------------------
CREATE TABLE public.MapItem(
	MapItem_id        BIGSERIAL  NOT NULL ,
	MapItem_kind      VARCHAR (255)  ,
	MapItem_latitude  FLOAT   ,
	MapItem_longitude FLOAT   ,
	MapItem_rayon     FLOAT   ,
	MapItem_date      INT   NOT NULL,
	Player_id         INT   NOT NULL,
	CONSTRAINT prk_constraint_MapItem PRIMARY KEY (MapItem_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Weather
------------------------------------------------------------
CREATE TABLE public.Weather(
	Weather_id        BIGSERIAL  NOT NULL ,
	Weather_timestamp INT   ,
	Weather_temps     VARCHAR (255)  ,
	Weather_dfn       INT   ,
	CONSTRAINT prk_constraint_Weather PRIMARY KEY (Weather_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Avoir
------------------------------------------------------------
CREATE TABLE public.Avoir(
	Player_id INT  NOT NULL ,
	Recipe_id INT  NOT NULL ,
	Avoir_date INT NOT NULL ,
	CONSTRAINT prk_constraint_Avoir PRIMARY KEY (Player_id,Recipe_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Composer
------------------------------------------------------------
CREATE TABLE public.Composer(
	Compose_qte   INT   ,
	Ingredient_id INT  NOT NULL ,
	Recipe_id     INT  NOT NULL ,
	CONSTRAINT prk_constraint_Composer PRIMARY KEY (Ingredient_id,Recipe_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Vendre
------------------------------------------------------------
CREATE TABLE public.Vendre(
	Vendre_meteo 	 VARCHAR (255)  ,
	Vendre_qte   	 INT   ,
	Vendre_nonVendu  INT   ,
	Vendre_prix  	 FLOAT   ,
	Vendre_date  	 INT  NOT NULL ,
	Player_id   	 INT  NOT NULL ,
	Recipe_id    	 INT  NOT NULL ,
	CONSTRAINT prk_constraint_Vendre PRIMARY KEY (Player_id, Recipe_id, Vendre_date)
)WITHOUT OIDS;


ALTER TABLE public.MapItem ADD CONSTRAINT FK_MapItem_Player_id FOREIGN KEY (Player_id) REFERENCES public.Player(Player_id);
ALTER TABLE public.Avoir ADD CONSTRAINT FK_Avoir_Player_id FOREIGN KEY (Player_id) REFERENCES public.Player(Player_id);
ALTER TABLE public.Avoir ADD CONSTRAINT FK_Avoir_Recipe_id FOREIGN KEY (Recipe_id) REFERENCES public.Recipe(Recipe_id);
ALTER TABLE public.Composer ADD CONSTRAINT FK_Composer_Ingredient_id FOREIGN KEY (Ingredient_id) REFERENCES public.Ingredient(Ingredient_id);
ALTER TABLE public.Composer ADD CONSTRAINT FK_Composer_Recipe_d FOREIGN KEY (Recipe_id) REFERENCES public.Recipe(Recipe_id);
ALTER TABLE public.Vendre ADD CONSTRAINT FK_Vendre_Player_id FOREIGN KEY (Player_id) REFERENCES public.Player(Player_id);
ALTER TABLE public.Vendre ADD CONSTRAINT FK_Vendre_Recipe_id FOREIGN KEY (Recipe_id) REFERENCES public.Recipe(Recipe_id);
	
INSERT INTO public.Ingredient(
	Ingredient_name, Ingredient_price, Ingredient_hasAlcohol, Ingredient_isCold)
	VALUES ('Citron', 0.40, False, False);
	
INSERT INTO public.Ingredient(
	Ingredient_name, Ingredient_price, Ingredient_hasAlcohol, Ingredient_isCold)
	VALUES ('Galçon', 0.05, False, True);
	
INSERT INTO public.Ingredient(
	Ingredient_name, Ingredient_price, Ingredient_hasAlcohol, Ingredient_isCold)
	VALUES ('Eau Gazeuse', 0.30, False, False);
	
INSERT INTO public.Ingredient(
	Ingredient_name, Ingredient_price, Ingredient_hasAlcohol, Ingredient_isCold)
	VALUES ('Sucre', 0.30, False, False);
	
INSERT INTO public.Ingredient(
	Ingredient_name, Ingredient_price, Ingredient_hasAlcohol, Ingredient_isCold)
	VALUES ('Rhum', 0.80, True, False);

INSERT INTO public.Ingredient(
	Ingredient_name, Ingredient_price, Ingredient_hasAlcohol, Ingredient_isCold)
	VALUES ('Menthe', 0.40, False, False);
	
INSERT INTO public.Recipe(
	Recipe_name, Recipe_pricePurchase)
	VALUES ('Limonade', 0);
	
INSERT INTO public.Recipe(
	Recipe_name, Recipe_pricePurchase)
	VALUES ('Mojito', 100);		

INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (2,1,1);
	
INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (4,2,1);
	
INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (1,3,1);
	
INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (2,4,1);	

INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (3,1,2);

INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (5,2,2);

INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (1,3,2);

INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (2,4,2);
	
INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (1,5,2);
	
INSERT INTO public.Composer(
	Compose_qte, Ingredient_id, Recipe_id)
	VALUES (2,6,2);
	
INSERT INTO public.Player(
	Player_name, Player_cash, Player_profit, Player_longitude, Player_latitude)
	VALUES ('Toto',150,12,25,56);
	
INSERT INTO public.MapItem(
	MapItem_kind, MapItem_latitude, MapItem_longitude, MapItem_rayon, MapItem_date, Player_id)
	VALUES ('stand',25,56,10,0,1);

INSERT INTO public.Avoir(
	Player_id, Recipe_id, Avoir_date)
	VALUES (1,1,0);
	
INSERT INTO public.Avoir(
	Player_id, Recipe_id, Avoir_date)
	VALUES (1,2,0);	
	
INSERT INTO public.Vendre(
	Vendre_meteo, Vendre_qte, Vendre_nonVendu, Vendre_prix, Vendre_date, Player_id, Recipe_id)
	VALUES ('sunny',23,4,8.0,154,1,1);
	
INSERT INTO public.Vendre(
	Vendre_meteo, Vendre_qte, Vendre_nonVendu, Vendre_prix, Vendre_date, Player_id, Recipe_id)
	VALUES ('rainny',27,4,12.0,178,1,1);		