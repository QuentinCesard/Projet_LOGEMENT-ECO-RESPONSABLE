#python -m uvicorn "remplissage:app" --reload
#fastapi dev remplissage.py --host 192.168.1.16  --port 8000
import sqlite3, random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import requests
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing purposes)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def serve_static():
    """ 
    Revoie un fichier
    """
    file = Path('./'+"index.html")
    if file.exists():
        return FileResponse(file)
    else:
        return HTTPException(detail=f"Le fichier index n'existe pas", status_code=404)

# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('database.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

#############################1.2 Remplissage de la base de données ##########################

# fonction pour rajouter des valeurs pour le capteur
def ajouter_mesures(id_capt,valeur):
    # ouverture/initialisation de la base de donnee 
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Insérer une nouvelle mesure pour le capteur trouvé
    cursor.execute("INSERT INTO Mesure(idCapteur, valeur) VALUES(?, ?)", (id_capt, valeur))
    conn.commit()
    print(f"Mesure ajoutée : Capteur {id_capt}, Valeur {valeur}")
 
#valeur = round(random.uniform(10, 100), 2)  # Génère une valeur de mesure entre 10 et 100
#ajouter_mesures(1,valeur);

# fonction pour rajouter des valeurs pour les factures
def ajouter_facture(logement_id, type, montant, valeur_conso):
    # ouverture/initialisation de la base de donnee 
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Insérer une nouvelle mesure pour le capteur trouvé
    cursor.execute("INSERT INTO Facture(logement_id, type, montant, valeur_conso) VALUES(?, ?, ?, ?)", (logement_id, type ,montant, valeur_conso))
    conn.commit()

#facture=ajouter_facture(1, 'Fenetre',200, 0.4)

##########################################################################################

###################2.1 Exercice 1 : remplissage de la base de données#####################
class Mesure(BaseModel):
    id_Capteur: int
    valeur: float

#ajoute des mesures à la database
@app.post("/mesures/")
def api_ajouter_mesures(mesure: Mesure):
    print(mesure)
    ajouter_mesures(mesure.id_Capteur, mesure.valeur)
    return {"message": f"Mesure ajoutée : Capteur {mesure.id_Capteur}, Valeur {mesure.valeur}"}

#affiche les mesures brut
@app.get("/les_mesures/")
def api_get_all_factures():
     # ouverture/initialisation de la base de donnee 
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM Mesure")#renvoi tous ce qu'il y a dans la table Facture
    rows = cursor.fetchall()#le mets sous forme de liste
    return rows

class Facture(BaseModel):
    logement_id: int
    type: str
    montant:int
    valeur_conso: float

#ajoute des factures à la database
@app.post("/factures/")
def api_ajouter_mesures(fact: Facture):
    print(fact)
    ajouter_facture(fact.logement_id, fact.type, fact.montant, fact.valeur_conso )
    return {"message": f"Mesure ajoutée : Logement {fact.logement_id}, Type {fact.type}, Montant {fact.montant}, Valeur de consommation {fact.valeur_conso}"}

#affiche les facture brut
@app.get("/les_factures/")
def api_get_all_factures():
     # ouverture/initialisation de la base de donnee 
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM Facture")#renvoi tous ce qu'il y a dans la table Facture
    rows = cursor.fetchall()#le mets sous forme de liste
    return rows

##########################################################################################

###################2.2 Exercice 2 : serveur web#####################

#affiche le graph pour les factures
@app.get("/Afficher_graph_facture/", response_class=HTMLResponse)
def api_get_all_factures():
    # Connexion à la base de données
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Récupérer les montants par type de facture
    cursor.execute("SELECT type, montant FROM Facture GROUP BY type")
    factures = cursor.fetchall()

    # Préparer les données pour Google Charts
    chart_data = [['Task', 'Amount']]  # En-tête pour Google Charts
    for facture in factures:
        chart_data.append([facture['type'], facture['montant']])

    # Transformer les données en chaîne pour JavaScript
    chart_data_js = str(chart_data).replace("'", '"')

    # Code HTML avec JavaScript pour Google Charts
    http = f"""
        <div id="piechart" style="width: 900px; height: 500px;"></div>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {{'packages':['corechart']}});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {{
                var data = google.visualization.arrayToDataTable({chart_data_js});

                var options = {{
                    title: 'Factures'
                }};

                var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                chart.draw(data, options);
            }}
        </script>
        """
    return HTMLResponse(content=http)

##########################################################################################
#################################2.3 Exercice 3 : météo###################################
#afficher une page pour la météo


@app.get("/meteo/", response_class=HTMLResponse)
def afficher_previsions_meteo(city: str = "Paris"):
    """
    Affiche les prévisions météo pour une ville donnée.
    :param city: Nom de la ville (par défaut : Paris)
    :return: Une page HTML avec les prévisions météo
    """
    # Paramètres de la requête API OpenWeatherMap
    params = {
        "q": city,
        "units": "metric",
        "appid": "aa24ca73c758ec2293e154225b35d65f"
    }

    try:
        # Envoi de la requête et récupération des données
        response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données météo.") from e

    # Vérification si les données sont valides
    if "list" not in data or "city" not in data:
        raise HTTPException(status_code=404, detail="Données météo introuvables pour cette ville.")

    # Récupération des prévisions météo toutes les 8 heures pour les 5 prochains jours
    forecasts = data['list'][8:40:8]

    # Création de la page HTML
    html = f"""
<html>
<head>
    <title>Prévisions météo</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 50%;
            margin: auto;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        th:hover {{
            background-color: #45a049;
        }}
        td:hover {{
            background-color: #f1f1f1;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        h1 {{
            text-align: center;
            color: #333;
            font-family: Arial, sans-serif;
        }}
        p {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>Prévisions météo pour {data['city']['name']}</h1>
    <table>
        <tr>
            <th>Date</th>
            <th>Température (°C)</th>
            <th>Température min (°C)</th>
            <th>Humidité (%)</th>
            <th>Vitesse du vent (m/s)</th>
        </tr>
    """
    # Boucle pour afficher les prévisions météo
    for forecast in forecasts:
        html += f"""
        <tr>
            <td>{forecast['dt_txt'].split(' ')[0]}</td>
            <td>{forecast['main']['temp']} °C</td>
            <td>{forecast['main']['temp_min']} °C</td>
            <td>{forecast['main']['humidity']} %</td>
            <td>{forecast['wind']['speed']} m/s</td>
        </tr>
        """
    # Fermeture de la page HTML
    html += """
    </table>
    <p>Mise à jour des prévisions météo toutes les heures.</p>
</body>
</html>
    """
    return HTMLResponse(content=html)


##########################################################################################

###################2.4 Exercice 4 : intégration###################
class TempESP(BaseModel):
    id: int
    temperature: float
    humidity: float
    
@app.post("/postplain/", response_class=JSONResponse)
async def post_capteur_mesure(data: TempESP):
    """
    Ajoute une mesure envoyée par un capteur à la base de données.
    """
    print("recu d'un capteur:", data)
    ajouter_mesures(data.id,data.temperature)
    return JSONResponse("")
##########################################################################################

@app.get("/Afficher_graph_mesures/", response_class=HTMLResponse)
def afficher_graph_mesures():
    # Connexion à la base de données
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Récupérer les données des mesures
    cursor.execute("SELECT * FROM Mesure")
    mesures = cursor.fetchall()

    # Préparer les données pour Chart.js
    capteurs = [mesure['idCapteur'] for mesure in mesures]
    valeurs = [mesure['valeur'] for mesure in mesures]
    dates = [mesure['date_intégration'] for mesure in mesures]

    # Créer des labels qui combinent le jour, le mois, l'heure et l'ID du capteur
    labels = [
        f"Le {date.split()[0][5:7]}/{date.split()[0][8:10]} à {date.split()[1][:5]} (Capteur {capteur})"
        for date, capteur in zip(dates, capteurs)
    ]
    

    # Code HTML avec JavaScript pour Chart.js
    html = f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <canvas id="myChart" width="400" height="200"></canvas>
        <script>
            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels},  // Labels avec jour/mois, heure:minute et ID du capteur
                    datasets: [{{
                        label: 'Valeurs des mesures',
                        data: {valeurs},  // Les valeurs des mesures
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

#affiche les mesures brut
@app.get("/les_capteurs/")
def api_get_all_factures():
     # ouverture/initialisation de la base de donnee 
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM Capteur")#renvoi tous ce qu'il y a dans la table Facture
    rows = cursor.fetchall()#le mets sous forme de liste
    return rows

def ajouter_capteur(Ref_Commercial, type_capteur_id, idPiece, Port_communication):
    # ouverture/initialisation de la base de donnee 
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Insérer une nouvelle mesure pour le capteur trouvé
    cursor.execute("INSERT INTO Capteur(Ref_Commercial, type_capteur_id, idPiece, Port_communication) VALUES(?, ?, ?, ?)", (Ref_Commercial, type_capteur_id, idPiece, Port_communication))
    conn.commit()
    print(f"Capteur ajoutée ")
    
class Capteur(BaseModel):
    Ref_Commercial: str
    type_capteur_id: str
    idPiece:int
    Port_communication: int

#ajoute des capteurs à la database
@app.post("/capteurs/")
def api_ajouter_mesures(capt: Capteur):
    print(capt)
    ajouter_capteur(capt.Ref_Commercial, capt.type_capteur_id, capt.idPiece, capt.Port_communication )
    return {"message": f"Capteur bien ajoutée"}


@app.delete("/capteurs/{id}")
def delete_capteur(id: int):
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Capteur WHERE id = ?", (id,))
    conn.commit()
    return {"message": f"Capteur {id} supprimé"}


#fermeture
# conn.commit()
# conn.close()

@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    """
    Servir les fichiers statiques depuis le dossier www.
    """
    if not '.' in file_path:
        file_path += '.html'
    file = Path("internet") / file_path
    if file.exists() and file.is_file():
        return FileResponse(file)
    raise HTTPException(status_code=404, detail=f"Fichier {file_path} introuvable.")