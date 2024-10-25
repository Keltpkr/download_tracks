# 🎵 Script de Téléchargement de Bandes Sonores 🎶


Ce projet permet de télécharger automatiquement les morceaux d'un album depuis https://downloads.khinsider.com/ fournie. Le script utilise les cookies de session pour accéder aux fichiers protégés, ce qui nécessite l'exportation des cookies depuis votre navigateur. Il inclut une interface graphique simple pour coller l'URL de l'album, choisir le dossier de téléchargement, et suivre la progression du téléchargement.

---

## 📋 Prérequis

1. **Python 3.x** - Assurez-vous d'avoir Python installé.
2. **Librairies Python** - Installez les dépendances nécessaires avec `pip`.
3. **Extension de navigateur** - Utilisez une extension pour exporter vos cookies de session dans un fichier JSON.

---

### Librairies Python requises

## 🔧 Installation et Configuration
Clonez le dépôt :

---

```bash
git clone https://github.com/Keltpkr/download_tracks)
cd [votre-repo]
```
Installez les dépendances :

Exécutez la commande suivante dans votre terminal pour installer les bibliothèques requises :

```bash
pip install -r requirements.txt
```
Exporter les cookies de session depuis votre navigateur :

---

Utilisez une extension comme Get cookies.txt pour exporter vos cookies en fichier .json.
Dans l'extension, naviguez vers le site de téléchargement (par ex. downloads.khinsider.com), puis téléchargez le fichier de cookies au format JSON dans le dossier de votre projet sous le nom cookies.json.
Dossier de Téléchargement : Par défaut, le dossier de téléchargement sera Music dans le répertoire principal de votre utilisateur, mais vous pouvez en sélectionner un autre via l'interface.

---

## 🚀 Utilisation
Lancer le script :

Dans votre terminal, exécutez :

```bash
python download_tracks.py
```
Interface Utilisateur :

URL de l'album : Collez l'URL de l'album que vous souhaitez télécharger.
Dossier de téléchargement : Le dossier sera automatiquement nommé selon l'album (remplaçant les caractères non acceptés) et situé dans le répertoire "Music". Vous pouvez sélectionner un autre dossier si besoin.
Téléchargement : Cliquez sur Démarrer pour initier le téléchargement. Le bouton vous permet également de suspendre et de reprendre le téléchargement.

Suivi de Progression :

Une barre de progression est disponible pour l'album entier et pour chaque morceau, afin de suivre en direct l'avancée du téléchargement.

---

## 🛠️ Dépannage
Fichier cookies.json absent : Vérifiez que le fichier des cookies est bien présent dans le dossier du projet et qu'il est bien au format JSON.
Téléchargement interrompu : Le script conserve les morceaux déjà téléchargés pour reprendre là où il s'est arrêté en cas d'interruption.
Messages d’erreurs SSL : Le script désactive les avertissements SSL. Si vous rencontrez des problèmes de connexion, vérifiez votre connexion Internet ou les paramètres de votre pare-feu.

---

## 📜 Licence
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.
Note : Utilisez ce script uniquement pour des téléchargements personnels et légaux en conformité avec les droits d'auteur du site source.

---
