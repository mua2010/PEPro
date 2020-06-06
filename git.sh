#!/bin/sh

# to run use => $. ./setup.sh

# source "./env/Scripts/activate"

while [ 1 ]
do
    git add .
    read -p "Enter message: " msg
    git commit -m "$msg"
    # git commit -m "new changes"
    git push
    echo "DONE!"
    # sleep 30
done
