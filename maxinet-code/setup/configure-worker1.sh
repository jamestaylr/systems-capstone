#!/bin/bash
screen -dmS pox_forwarding bash
screen -S pox -X stuff "cd ~/pox\n"
screen -S pox -X stuff "./pox.py forwarding.l2_learning\n"

screen -dmS frontend bash
screen -S frontend -X stuff "MaxiNetFrontendServer\n"

screen -dmS worker bash
screen -S worker -X stuff "sudo MaxiNetWorker\n"
