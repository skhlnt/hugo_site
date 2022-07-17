#!/bin/bash

pip install -r requirements.txt
hugo -D --gc
python hugo-encryptor.py