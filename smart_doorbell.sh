#!/bin/bash
cd /home/admin/Documents/smart_doorbell/
source env/bin/activate

# Lancer le backend en arrière-plan
python3 backend/app.py &
BACKEND_PID=$!

# Attendre que le backend soit prêt (ex: 5 sec)
sleep 5

# Lancer le firmware
python3 firmware/main.py

# Optionnel : tuer le backend si le firmware s’arrête
kill $BACKEND_PID
