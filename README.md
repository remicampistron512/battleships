# Bataille navale (terminal Python)

Ce projet propose une version simple de la bataille navale en terminal.

## Installation

1. Assurez-vous d'avoir Python 3 installé.
2. Clonez le dépôt.
3. Lancez le jeu :

```bash
python battleships.py
```

## Utilisation

Le jeu vous demande des coordonnées de tir.

Formats acceptés : `A1`, `c7`, `J10`.

Pour quitter : `q`.

## Règles du jeu

- Si le tir touche un navire : `touché`
- Si toutes les cases d'un navire sont touchées : `coulé !!!`
- Quand tous les navires sont coulés : `GAME OVER`

## Structure du code

- `battleships.py` : boucle principale + classe `Game`
- `UserInput.py` : validation et normalisation des coordonnées
- `Ship.py` : modèle navire (coordonnées, impacts, état coulé)
- `Grid.py` : rendu de la grille
- `tests/` : tests unitaires de base

## Lancer les tests

```bash
python -m unittest discover -s tests
```

## Limitations connues

- Placement des navires statique (pas encore aléatoire)
- Jeu solo uniquement

## Roadmap

- Ajouter un placement aléatoire des navires
- Ajouter un mode debug pour afficher les navires non touchés
- Ajouter plus de tests sur l'affichage de la grille
