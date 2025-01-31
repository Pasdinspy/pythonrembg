Docs:
rembg pour le détourage - https://pypi.org/project/rembg ;
NumPy pour le recadrage - https://numpy.org ;
Pillow pour le redimensionnement - https://pypi.org/project/pillow ;
scikit-image, OpenCV pour l’extraction de données - https://scikit-image.org, https://opencv.org
flasgger pour le swagger - https://github.com/flasgger/flasgger (http://127.0.0.1:5000/apidocs/)

Installation de python (3.10) :
Windows : [Télécharger Python 3.10.12](https://www.python.org/downloads/release/python-31012/)
Linux : sudo apt install python3.10

installation de l'espace de travail :
crée un environemnt virtuel - python -m venv venv
Activer l’environnement virtuel - venv\Scripts\activate (Windows) / source venv/bin/activate (Linux)

Installation des dépendances :
source venv/bin/activate (Linux), venv\Scripts\activate (Windows)
En une commande : pip install -r requirements.txt

ajouter de nouvel dépendances au requirements.txt :
source venv/bin/activate (Linux), venv\Scripts\activate (Windows)
pip freeze > requirements.txt