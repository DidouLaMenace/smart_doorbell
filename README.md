# Smart Doorbell – Sonnette Connectée (pas si) Intelligente

> Projet IoT réalisé dans le cadre du cours d’Internet des Objets – UQAC

## Description

La **Smart Doorbell** est une sonnette connectée conçue pour moderniser un dispositif domestique classique. Elle permet de :

- détecter une présence (mouvement ou bruit) devant la porte,
- reconnaître l’appui sur un bouton physique,
- émettre un signal sonore via un haut-parleur,
- notifier l'utilisateur à distance via **Pushbullet**,
- consulter un tableau de bord web des événements enregistrés.

Le projet repose sur un **Raspberry Pi**, plusieurs capteurs/actionneurs, et un backend Python/Flask.

## Architecture du projet

```
project_root/
├── firmware/                  # Code embarqué sur le Raspberry Pi
│   ├── main.py                # Boucle principale
│   ├── sensors/               # Capteurs (son, ultrason, bouton)
│   ├── actuators/             # Effecteurs (haut-parleur)
│   └── shared.py              # ADC + initialisation commune
├── backend/                   # API Flask, DB et interface web
│   ├── app.py                 # API Flask principale
│   ├── database/              # SQLite + init DB
│   ├── events/                # Logger
│   ├── notifications/         # Intégration Pushbullet
│   └── templates/             # Frontend HTML (dashboard)
├── .env                       # Clé API Pushbullet (non versionnée)
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
```

## Fonctionnalités

### Capteurs & détection
- **Capteur sonore (DFR0034)** – détecte les bruits
- **Capteur ultrasonique (SEN0307)** – détecte les présences à moins de 50 cm
- **Bouton poussoir** – sonnette classique

### Réaction & notification
- Lecture des capteurs via ADC (ADS1115)
- Émission sonore via haut-parleur (PWM GPIO)
- Envoi d’événement au backend Flask
- Journalisation SQLite
- Notification push via **Pushbullet**

### Interface web
- Accès à `/dashboard` (tableau d’événements)
- Rafraîchissement en temps réel (JS)

## Installation

### 1. Matériel utilisé
- Raspberry Pi Model 4B with 4GB
- ADS1115 (convertisseur ADC I2C)
- DFR0034 (capteur son)
- SEN0307 (capteur ultrason)
- FIT0449 (Haut-parleur)
- DFR0029 (Bouton poussoir)

## 2. Installation de l’environnement Python

Avant de lancer le projet, assurez-vous que les paquets de base sont installés :

```bash
sudo apt update
sudo apt install -y python3 python3-pip
sudo apt install -y sqlite3 libsqlite3-dev
```

Créez ensuite un environnement virtuel Python pour isoler les dépendances du projet :

```bash
python3 -m venv env/
source env/bin/activate
```


### 3. Dépendances Python

Sur le Raspberry Pi :
```bash
pip3 install -r requirements.txt
```

## Configuration

### `.env` à la racine (non partagé sur GitHub) :

```
PUSHBULLET_TOKEN=your_pushbullet_access_token
```

## Lancement

### Pré-requis

Assurez-vous de travailler dans un environnement Python configuré comme indiqué précédemment.

### Raspberry Pi (firmware) :
```bash
python3 firmware/main.py
```

### Backend Flask :
```bash
python3 backend/app.py
```

Puis accéder à :
- `http://localhost:5000/dashboard` pour l’interface

## Calibration du capteur ultrason

La distance est calculée via :
```python
distance = (voltage / VCC) * 520
```

Assurez-vous que `VCC` correspond à la tension réelle d’alimentation du capteur (typiquement 5V).

## Améliorations possibles

- Intégration caméra (détection de visage)
- Notification push via OneSignal ou Firebase
- Application mobile en .apk (Flutter ou React Native)
- Conception de PCB personnalisé
- Déploiement cloud du backend

