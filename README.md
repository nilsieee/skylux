## **Skylux koepelbeheer**



Project - Niels Follens 2CYB(Programming in Python)





##### Beschrijving

--------------------

Dit is een eenvoudig command line interface(CLI) applicatie geschreven in python voor het beheren van lichtkoepels (Skylux) en bijhorende interventies zoals (installatie, onderhoud, herstellingen) en alsook het verwijderen ervan.





De applicatie laat toe om:

* Koepels toe te voegen en om te bekijken 
* Interventies toe te voegen aan een koepel
* Interventies per koepel te bekijken 
* Interventies te exporteren naar een CSV-bestand, + als optie met automatische datum van vandaag
* Koepels te verwijderen (met bijhorende interventie(s))




De data wordt opgeslagen in een SQLite DB(zoals we in de les hebben geleerd).



##### Projectstructuur

--------------------------

skylux/

│

├── main.py

├── requirements.txt

├── README.md

├── .gitignore

├── .env.example

│

├── db/

│ └── skylux.db # sample database

│

├── reports/ # CSV exports

│

└── src/

├── cli/

│ └── app.py

├── data/

│ ├── db.py

│ └── repositories.py

└── services/

└── exporter.py





##### Installatie

------------------



###### 1\. Repository clonen

git clone https://github.com/nilsieee/skylux.git

cd skylux



###### 2\. Virtuele omgeving aanmaken

python -m venv .venv



###### 3\. Virtuele omgeving activeren

.venv\Scripts\Activate.ps1 of .venv\\Scripts\\Activate.ps1



###### 4\. Vereiste packages installeren

pip install -r requirements.txt







##### Configuratie

-------------------



###### 1.Maak een .env bestand op basis van .env example

copy .env.example .env



###### 2.Inhoud van .env

notepad .env
DB\_PATH=db/skylux.db





##### Database

-------------

De applicatie gebruikt een SQLite database met twee tabellen:

-domes (koepels)

-interventions (interventies)



Een sample database met wat testdata is aanwezig in

db/skylux.db







##### Applicatie starten 

------------------

python main.py





##### 

##### CSV export

----------------

Interventies kunnen geëxporteerd worden naar een CSV bestand.

Wanneer geen bestandsnaam wordt opgegeven, wordt automatisch een bestandsnaam met datum van vandaag gebruikt:



























