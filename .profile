#!/usr/bin/env bash
# custom initialisation tasks
# ref - https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html

echo "---- RUNNING release tasks (.profile) ------"
echo "---- Apply Migrations ------"
python manage.py migrate

echo "---- Compile SCSS ------"
python manage.py compress -f

echo "---- Collect Static Files ------"
OUTPUT=$(python manage.py collectstatic --noinput -i *.scss --clear)
mkdir -p ~/logs
echo ${OUTPUT} > ~/logs/collectstatic.txt
echo ${OUTPUT##*$'\n'}
echo "NOTE: the full output of collectstatic has been saved to ~/logs/collectstatic.txt"
echo "---- FINISHED release tasks (.profile) ------"
