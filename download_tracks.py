import requests
from bs4 import BeautifulSoup
import json
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from pathlib import Path
from tkinter import ttk
import urllib3

#test2
# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Charger les cookies exportés
with open("cookies.json", "r") as f:
    cookies = json.load(f)

# Convertir les cookies au format `requests`
session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

# Variables globales
is_downloading = False
stop_download = False

# Fonction pour télécharger un fichier MP3
def download_mp3(track_name, mp3_url, folder_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    file_path = folder_path / f"{track_name}.mp3"
    # Vérifie si le fichier existe déjà
    if file_path.exists():
        print(f"{track_name} est déjà téléchargé, passage au morceau suivant.")
        return  # Passe au morceau suivant sans retélécharger

    # Téléchargement si le fichier n'existe pas
    try:
        response = requests.get(mp3_url, cookies=session_cookies, headers=headers, stream=True, verify=False)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    track_progress['value'] = (dl / total_length) * 100
                    root.update_idletasks()
        print(f"Téléchargé : {track_name} à {file_path}")  # Log complet du chemin du fichier
    except Exception as e:
        print(f"Erreur lors du téléchargement de {track_name}: {e}")

# Fonction pour démarrer le téléchargement de l'album
def start_download(album_url, download_folder):
    global is_downloading, stop_download
    is_downloading = True
    stop_download = False
    response = requests.get(album_url, cookies=session_cookies, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Déterminer le nom du dossier
    album_name = soup.find('title').text.split('-')[0].strip()
    sanitized_name = "".join(c if c.isalnum() else "_" for c in album_name)
    folder_name = Path(download_folder) / sanitized_name
    folder_name.mkdir(parents=True, exist_ok=True)  # Création du dossier de l'album
    
    # Log du chemin du dossier
    print(f"Dossier de téléchargement : {folder_name}")

    # Extraire uniquement les liens vers chaque morceau se terminant par .mp3 sans doublons
    tracks = []
    for link in soup.find_all('a', href=True):
        if '/game-soundtracks/album/' in link['href'] and link['href'].endswith('.mp3') and 'change_log' not in link['href']:
            track_url = f"https://downloads.khinsider.com{link['href']}"
            if track_url not in tracks:  # Ajoute le lien si non déjà présent
                tracks.append(track_url)

    total_tracks = len(tracks)
    downloaded_tracks = 0

    for track_page_url in tracks:
        if stop_download:
            break
        print(f"Accès à la page du morceau : {track_page_url}")

        # Accéder à la page de chaque morceau
        track_response = requests.get(track_page_url, cookies=session_cookies, verify=False)
        track_soup = BeautifulSoup(track_response.text, 'html.parser')

        # Initialiser le nom du morceau
        track_name = None

        # Trouver le lien de téléchargement MP3
        download_span = track_soup.find('span', class_='songDownloadLink')
        if download_span and download_span.find_parent('a'):
            mp3_url = download_span.find_parent('a')['href']
            track_name = os.path.basename(mp3_url).split('.mp3')[0].replace('%20', ' ')
            if not mp3_url.startswith("http"):
                mp3_url = f"https://eta.vgmtreasurechest.com{mp3_url}"
            print(f"URL de téléchargement pour {track_name} : {mp3_url}")
            download_mp3(track_name, mp3_url, folder_name)
            downloaded_tracks += 1
            album_progress['value'] = (downloaded_tracks / total_tracks) * 100
            track_progress['value'] = 0
            root.update_idletasks()
            time.sleep(1)  # Pause pour éviter de surcharger le serveur
        else:
            print(f"Impossible de trouver le lien de téléchargement MP3 pour ce morceau")

    is_downloading = False
    stop_download = False
    download_button.config(text="Démarrer")

# Gestion du bouton de téléchargement
def on_download_button():
    global is_downloading, stop_download
    album_url = url_entry.get().strip()  # Enlever les espaces inutiles
    if not album_url.startswith("http"):
        # Message d'erreur si l'URL est incorrecte
        print("Erreur: L'URL de l'album est invalide ou manquante.")
        tk.messagebox.showerror("Erreur URL", "L'URL de l'album est invalide ou manquante. Veuillez saisir une URL valide.")
        return

    if not is_downloading:
        download_folder = Path(download_folder_path.get())
        download_thread = Thread(target=start_download, args=(album_url, download_folder))
        download_thread.start()
        download_button.config(text="Arrêter")
    else:
        stop_download = True
        download_button.config(text="Démarrer")

# Mise à jour automatique du nom du dossier de téléchargement
def update_folder_name(event):
    album_url = url_entry.get().strip()
    if album_url.startswith("http"):
        response = requests.get(album_url, cookies=session_cookies, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        album_name = soup.find('title').text.split('-')[0].strip()
        sanitized_name = "".join(c if c.isalnum() else "_" for c in album_name)  # Remplacement des caractères spéciaux
        default_folder = Path.home() / "Music" / sanitized_name
        download_folder_path.set(default_folder)

# Sélection du dossier avec conservation en cas d'annulation
def choose_folder():
    current_path = download_folder_path.get()
    selected_path = filedialog.askdirectory()
    if selected_path:
        download_folder_path.set(selected_path)
    else:
        download_folder_path.set(current_path)

# Interface utilisateur
root = tk.Tk()
root.title("Téléchargeur de Bandes Son")

# URL de l'album
url_label = tk.Label(root, text="URL de l'album:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.bind("<FocusOut>", update_folder_name)  # Mettre à jour le nom du dossier quand on quitte le champ
url_entry.pack(pady=5)

# Sélection du dossier de téléchargement
download_folder_label = tk.Label(root, text="Dossier de téléchargement:")
download_folder_label.pack(pady=5)
download_folder_path = tk.StringVar(value=str(Path.home() / "Music"))
download_folder_entry = tk.Entry(root, textvariable=download_folder_path, width=50)
download_folder_entry.pack(pady=5)
choose_folder_button = tk.Button(root, text="Choisir un dossier", command=choose_folder)
choose_folder_button.pack(pady=5)

# Barre de progression de l'album
album_progress_label = tk.Label(root, text="Progression de l'album:")
album_progress_label.pack(pady=5)
album_progress = ttk.Progressbar(root, length=300)
album_progress.pack(pady=5)

# Barre de progression du morceau
track_progress_label = tk.Label(root, text="Progression du morceau:")
track_progress_label.pack(pady=5)
track_progress = ttk.Progressbar(root, length=300)
track_progress.pack(pady=5)

# Bouton de téléchargement
download_button = tk.Button(root, text="Démarrer", command=on_download_button)
download_button.pack(pady=20)

root.mainloop()
