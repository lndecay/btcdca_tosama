#!/bin/bash
source /opt/venv/bin/activate  # Activa el entorno virtual en Railway
python3 semanal.py &  # Ejecuta el bot semanal en segundo plano
python3 comando.py  # Ejecuta el bot de comandos
