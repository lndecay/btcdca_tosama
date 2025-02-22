#!/bin/bash
source /opt/venv/bin/activate
python3 semanal.py &   # Ejecuta el bot semanal en segundo plano
python3 comando.py     # Ejecuta el bot principal (se mantiene en primer plano)
