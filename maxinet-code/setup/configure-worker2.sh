#!/bin/bash
screen -dmS worker bash
screen -S worker -X stuff "sudo MaxiNetWorker\n"
