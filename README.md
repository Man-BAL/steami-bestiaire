# Bestiaire STeaMi

Projet pédagogique pour le cycle 3 : des animaux-sentinelles qui embarquent une carte STeaMi
pour observer le vivant, mesurer l'environnement et comparer nos perceptions.

## Contenu

| Dossier | Contenu |
|---|---|
| `index.html` | La page de présentation du projet, publiée avec GitHub Pages |
| `presentation/generateur/` | Les scripts Python qui produisent la page et ses illustrations |
| `texte/` | Le texte seul, en Markdown, importable dans Notion |

## Régénérer la page

```bash
cd presentation/generateur
python3 site.py        # écrit la page, puis la copier vers ../../index.html
python3 export_md.py   # écrit ../../texte/bestiaire-steami-texte-notion.md
```

## État

Projet en conception : le principe, les six sentinelles de départ et la démarche sont posés,
mais rien n'est encore prototypé (dimensions de la carte et de sa batterie, assemblage,
programmes d'enregistrement).
