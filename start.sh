#!/bin/bash
source /opt/venv/bin/activate
python3 semanal.py &
python3 comando.py
python3 inversion.py
