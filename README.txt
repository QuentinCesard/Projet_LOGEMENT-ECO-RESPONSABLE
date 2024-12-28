Dans cette archive, il y a:
Le fichier logement.sql qui contient l'ensemble des tables de la base de données, pour l'exécuter, il faut utiliser la commande "sqlite3 data.db < logement.sql"

L'ensemble du code python (backend) (serveur, post, get...) dans le fichier remplissage.py, pour l'exécuter j'utilise la commande fastapi dev remplissage.py --host 192.168.75.23  --port 8000 (remplacer l'adresse 192.168.75.23 par l'adresse ip de votre machine).
    Pour le faire fonctionner, il faut installer les dépendance suivante: 
    FastAPI
    Uvicorn : Le serveur ASGI qui sert d'hôte pour l'application FastAPI
    Pydantic : Pour la gestion des modèles de données.
    SQLite3 : pour la gestion de la base de données 
    Requests : Pour envoyer des requêtes HTTP

Le fichier Temp_capteur, permet de récupérer la température du capteur et de la poster sur notre serveur local, attention il faut modifier le STASSID et le STAPSK, mais aussi le SERVER_IP pour le remplacer par notre serveur local (ip local de votre machine).

Un dossier internet contenant toute les pages internet, pour avoir accès à ces page, il faut lancer le serveur et allé sur l'adresse http://192.168.75.23:8000/index.html (toujours en remplaçant l'adresse ip par celle de votre machine).

Les différent PartieX.txt sont les réponse aux questions ou des explications.