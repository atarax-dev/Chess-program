#Programme tournoi d'échecs
Projet n°4 OC 
#Introduction: 
Ce programme peut être utilisé pour gérer des tournois d'échecs à 8 joueurs et 4 rondes.
Il permet de générer les matchs, d'entrer les scores et d'obtenir un classement à jour à chaque fin de round
Le programme dispose également d'une base de données qui permet la sauvegarde des joueurs et des tournois.
Ainsi vous pourrez reprendre un tournoi là où vous l'aviez arrêté.

Lancez un terminal

Récupérez l'ensemble du projet :

git clone https://github.com/atarax-dev/Chess-program.git

Placez-vous dans le répertoire qui contient le fichier main.py

Pour pouvoir lancer le programme, créez un environnement virtuel:

python -m venv venv

Activez l'environnement :

source venv/Scripts/activate (sous windows)
source venv/bin/activate (sous Mac ou linux)

Installez les packages requis à l'aide de la commande suivante:

pip install -r requirements.txt
#Utilisation 
Toujours depuis le répertoire qui contient main.py dans le terminal, exécutez le programme:

python main.py

#Générer un nouveau rapport flake8-html:

Placez-vous dans le répertoire qui contient le fichier main.py et exécutez la commande suivante:

flake8 --format=html --htmldir=flake-report

Le rapport flake8 se trouvera dans /flake-report/index.html