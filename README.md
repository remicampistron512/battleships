# Bataille navale

Ce programme permet de jouer à la bataille navale.

## Table des matières
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Règles du jeu](#règles-du-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Structure du code](#structure-du-code)

### Installation

1. Assurez-vous d’avoir **Python 3** installé sur votre machine.
2. Téléchargez les fichiers suivants dans un répertoire de votre choix :
    
    - `battleships.py`
    - `UserInput.py`
    - `Ship.py`
    - `Grid.py`
3. Ouvrez un terminal et exécutez le script : `python battleships.py`

### Utilisation

Lancez le script. Le jeu commence.

Rentrez une coordonnée correspondant à une case de la grille et appuyez sur *Entrée*.

### Règles du jeu

Il s'agit d'une transposition du jeu de la bataille navale. Des navires sont placés sur une grille et se voient
attribuer des coordonnées.  
  Si l'utilisateur tire sur la bonne case, le navire est touché. Si toutes les cases occupées par le navire sont
atteintes, alors le navire est coulé. Quand tous les navires sont coulés, le jeu se termine.

### Fonctionnalités

Propose à un seul joueur de tirer sur une grille et de jouer à la bataille navale

### Structure du code

Le programme se compose de 4 fichiers :

- **`battleships.py`**  
 Fichier principal qui va s'occuper de la logique du jeu et importer les différentes classes.
- **`UserInput.py`**  
 Classe permettant de gérer les inputs utilisateur
- **`Ship.py`**  
 Classe contenant les fonctionnalités liées aux données des navires, et permettant de tirer
- **`Grid.py`**  
 Classe effectuant l'affichage de la grille


