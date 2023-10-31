#!/bin/bash

# run flask db upgrade in venv

NAME=mytrilog
WHERE=/var/www

# apply db upgrades, if any
cd ${WHERE}/${NAME}
source ./venv/bin/activate
flask db upgrade
deactivate
