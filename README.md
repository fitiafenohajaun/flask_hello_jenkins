python -m venv venv
venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install Click Flask itsdangerous Jinja2 MarkupSafe Werkzeug unittest-xml-reporting
pip install Flask
pip freeze > requirements.txt
python test.py

docker build -t flask_hello .
docker run -d -p 5000:5000 --name mon_app_flask flask_hello
docker rm -f my_flask_app
docker run --rm --name flask_hello -p 5000:5000 flask_hello python ./test.py --ve

docker run -d -p 4000:5000 --name my_registre registry
docker tag flask_hello localhost:4000/flask_hello
docker push localhost:4000/flask_hello

curl http://localhost:4000/v2/_catalog

# Supprime l'image locale de ton PC
docker rmi localhost:4000/flask_hello

# Télécharge-la à nouveau depuis TON registre privé
docker pull localhost:4000/flask_hello


kubectl port-forward svc/jenkins 32000:8080
