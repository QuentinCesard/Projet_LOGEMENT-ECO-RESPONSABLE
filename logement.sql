-- data: /Users/quentincesard/Desktop/IOT/Hilaire/TP/data.db
-- Détruit les tables dans la database
DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Ville;
DROP TABLE IF EXISTS Adresse;
DROP TABLE IF EXISTS Pieces;
DROP TABLE IF EXISTS Capteur;
DROP TABLE IF EXISTS Actionneur;
DROP TABLE IF EXISTS TypeCapteur;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Facture;

-- Création des tables
--Table Logement, cette table permettera de créer un logement
--Les champs sont :id qui s'incrémentera automatiquement, l'adresse qui ira chercher l'adresse dans la table adresse en fonction de l'id,
--un téléphone qui sera aussi à rentrer, j'ai imaginer qu'on pouvais rentrer une IP,
--pour terminer la date d'insertion qui se rajoutera directement au moment de l'ajout
CREATE TABLE Logement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Adresse_id INTEGER NOT NULL,
    Telephone TEXT NOT NULL,
    IP TEXT NOT NULL,
    Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Adresse_id) REFERENCES Adresse(code)
);

--La table Adresse, qui va permettre de créer les adresse qui vont être utilisé dans le logement
--Les champs sont : code qui s'incrémentera automatiquement, la Numéro qui est à rentrer, la Voie qui est à rentrer,
--le Nom de voie qui est à rentrer, et la ville qui ira chercher la ville dans la table ville en fonction de l'id
CREATE TABLE Adresse (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    Numero INTEGER NOT NULL,
    Voie TEXT NOT NULL,
    Nom_voie TEXT NOT NULL,
    Ville_id INTEGER NOT NULL,
    FOREIGN KEY (Ville_id) REFERENCES Ville(City)
);

--La table ville a comme champ le code postal (city) et le de la ville 
CREATE TABLE Ville (
    City INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL
);

--La table Pieces a comme champ le id qui s'incrémentera automatiquement,
--le logement auquelle il est relié il ira chercher le logement dans la tabke logement en fonction de l'ID,
--Le nom de la pièce à rentrer, et sa loclisation dans la maison
CREATE TABLE Pieces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idlogement INTEGER NOT NULL,
    Nom TEXT NOT NULL,
    Localisation TEXT NOT NULL,
    FOREIGN KEY (idlogement) REFERENCES Logement(id)
);

--La table capteur a comme champ un id qui s'incrémente automatiquement,
--la ref commerciale à rentrer, le type de capteur qui ira chercher sa valeur dans la table type de capteur,
--la pièces ou il est le programme ira chercher cette information dans la table pièce,Un port de communication à rentrer,
--et la date d'insertion qui se rajoutera directement au moment de l'ajout
CREATE TABLE Capteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Ref_Commercial TEXT NOT NULL,
    type_capteur_id TEXT NOT NULL,
    idPiece INTEGER NOT NULL,
    Port_communication INTEGER NOT NULL,
    date_intégration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_capteur_id) REFERENCES TypeCapteur(id),
    FOREIGN KEY (idPiece) REFERENCES Pieces(type_capteur)
);

--La table Type capteur a un id qui s'incrémente automatiquement, un type de cpteur à rentrer,
--une unité qui dépend du type de capteur, et une précision qui est  rentrer
CREATE TABLE TypeCapteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_capteur TEXT NOT NULL,
    unité TEXT NOT NULL,
    précision INTEGER NOT NULL
);

-- La table mesure, a comme champ un id qui s'incrémente automatiquement, un id capteur qui récupère dans la table capteur,
--une valeur à rentrer, et une date d'intégration qui se mets automatiquement à l'ajout
CREATE TABLE Mesure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idCapteur INTEGER NOT NULL,
    valeur REAL NOT NULL,
    date_intégration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idCapteur) REFERENCES Capteur(id)
);

--La table facture à comme champ un id qui s'incrémente automatiquement, un id logement qui ira chercher l'information dans la tabkle logement,
-- un type qui sera à rentrer, uen date qui se mettera automatiquement, et un montant à rentrer, et une valeur de consomation à rentrer
CREATE TABLE Facture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logement_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    la_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    montant INTEGER NOT NULL,
    valeur_conso REAL NOT NULL,
    FOREIGN KEY (logement_id) REFERENCES Logement(id)
);

-- Insert data into tables
INSERT INTO Adresse (Numero, Voie, Nom_voie, Ville_id) VALUES
    (4, 'allée', 'des groseilliers', 92140),
    (14, 'rue', 'Berthelot', 94200),
    (18, 'rue', 'd Estrée', 75007),
    (56, 'rue', 'Arthur Rimbaud', 93300);

INSERT INTO Ville (City, Nom) VALUES 
    (92140, 'Clamart'),
    (94200, 'Ivry sur Seine'),
    (75007, 'Paris'),
    (93300, 'Aubervilliers');

INSERT INTO Logement (Adresse_id, Telephone, IP) VALUES
    (1, '0680589870', '192.168.2.4');

INSERT INTO Pieces (idlogement, Nom, Localisation) VALUES
    (1, 'Cuisine', 'RDC'),
    (1, 'Chambre', '1er étage'),
    (1, 'Salon', 'RDC'),
    (1, 'Salle de bain', '1er étage');

INSERT INTO TypeCapteur (type_capteur, unité, précision) VALUES
    ('Humidité', 'g/m3', 95),
    ('Température', '°C', 90),
    ('Distance', 'm', 80),
    ('Fumé', '0', 100);

INSERT INTO Capteur (Ref_Commercial, type_capteur_id, idPiece, Port_communication) VALUES
    ('DK32pz2', 'Humidité', 4, 500),
    ('102MSA1', 'Température', 2, 4000);

INSERT INTO Mesure (idCapteur, valeur) VALUES
    (1, 3),
    (2, 50);

INSERT INTO Facture (logement_id, type, montant, valeur_conso) VALUES
    (1, 'Humidité', 150, 0.5),
    (1, 'Température', 30, 1.0),
    (1, 'Eau', 800, 3.0),
    (1, 'Déchet', 80, 0.01);
