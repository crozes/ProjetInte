------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------

DROP TABLE IF EXISTS public.Avoir;
DROP TABLE IF EXISTS public.Composer;
DROP TABLE IF EXISTS public.Weather;
DROP TABLE IF EXISTS public.MapItem;
DROP TABLE IF EXISTS public.Ingredient;
DROP TABLE IF EXISTS public.Recipe;
DROP TABLE IF EXISTS public.Player;
DROP TABLE IF EXISTS public.Test;

------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------

------------------------------------------------------------
-- Table: Player
------------------------------------------------------------
CREATE TABLE public.Player(
	Player_id        BIGSERIAL NOT NULL ,
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
	Recipe_id    BIGSERIAL NOT NULL ,
	Recipe_name  VARCHAR (255)  ,
	Recipe_price FLOAT   ,
	CONSTRAINT prk_constraint_Recipe PRIMARY KEY (Recipe_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Ingredient
------------------------------------------------------------
CREATE TABLE public.Ingredient(
	Ingredient_id         BIGSERIAL NOT NULL ,
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
	MapItem_id        BIGSERIAL NOT NULL ,
	MapItem_kind      VARCHAR (255)  ,
	MapItem_latitude  FLOAT   ,
	MapItem_longitude FLOAT   ,
	MapItem_surface   FLOAT   ,
	Player_id         INT   ,
	CONSTRAINT prk_constraint_MapItem PRIMARY KEY (MapItem_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Weather
------------------------------------------------------------
CREATE TABLE public.Weather(
	Weather_id        BIGSERIAL NOT NULL ,
	Weather_timestamp INT   ,
	Weather_temps     VARCHAR (255)  ,
	Weather_dnf       INT   ,
	CONSTRAINT prk_constraint_Weather PRIMARY KEY (Weather_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Avoir
------------------------------------------------------------
CREATE TABLE public.Avoir(
	Player_id INT  NOT NULL ,
	Recipe_id INT  NOT NULL ,
	CONSTRAINT prk_constraint_Avoir PRIMARY KEY (Player_id,Recipe_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Composer
------------------------------------------------------------
CREATE TABLE public.Composer(
	Compose_qte   INT			,
	Ingredient_id INT  NOT NULL ,
	Recipe_id     INT  NOT NULL ,
	CONSTRAINT prk_constraint_Composer PRIMARY KEY (Ingredient_id,Recipe_id)
)WITHOUT OIDS;


ALTER TABLE public.MapItem ADD CONSTRAINT FK_MapItem_Player_id FOREIGN KEY (Player_id) REFERENCES public.Player(Player_id);
ALTER TABLE public.Avoir ADD CONSTRAINT FK_Avoir_Player_id FOREIGN KEY (Player_id) REFERENCES public.Player(Player_id);
ALTER TABLE public.Avoir ADD CONSTRAINT FK_Avoir_Recipe_id FOREIGN KEY (Recipe_id) REFERENCES public.Recipe(Recipe_id);
ALTER TABLE public.Composer ADD CONSTRAINT FK_Composer_Ingredient_id FOREIGN KEY (Ingredient_id) REFERENCES public.Ingredient(Ingredient_id);
ALTER TABLE public.Composer ADD CONSTRAINT FK_Composer_Recipe_id FOREIGN KEY (Recipe_id) REFERENCES public.Recipe(Recipe_id);



------------------------------------------------------------
-- Table: Test
------------------------------------------------------------
CREATE TABLE public.Test(
	id_test 	 BIGSERIAL NOT NULL ,
	nom_test     VARCHAR (255) ,
	CONSTRAINT prk_constraint_test PRIMARY KEY (id_test)
)WITHOUT OIDS;

INSERT INTO public.Test(
	id_test, nom_test)
	VALUES (1, 'Sprite');
	
INSERT INTO public.Test(
	id_test, nom_test)
	VALUES (2, 'Coca');

INSERT INTO public.Test(
	id_test, nom_test)
	VALUES (3, 'Jus');
	
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


								