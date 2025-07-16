#!/bin/bash

while true
do
    echo "👉 Chạy terraform và python lúc $(date)" >> log.txt
    terraform init 
    terraform plan > plan_output.txt
    python3 demo.py

    sleep 15
done
