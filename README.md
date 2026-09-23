# Le Bestiaire STeaMi

**Observer le vivant, mesurer l'environnement, comparer nos perceptions.**

Un projet scientifique et créatif pour le cycle 3, autour de la carte programmable
[STeaMi](https://steami.cc). Des animaux-sentinelles embarquent une carte et permettent aux élèves
de passer d'une observation du vivant à une mesure, puis à une proposition pour leur école.

👉 **[Voir la présentation du projet](https://steamicc.github.io/bestiaire-cycle3/)**

---

## L'idée

Chaque animal est choisi pour un comportement documenté, lié à une grandeur que la carte sait
mesurer. La STeaMi ne reproduit pas les sens de l'animal : elle apporte un troisième point de vue,
à confronter aux deux autres.

| Le regard du vivant | Le regard humain | Le regard du capteur |
|---|---|---|
| Ce que l'animal perçoit et le comportement qu'il adopte | Ce que les élèves observent et ressentent | Ce que la carte mesure et transforme en données |

Les écarts entre ces trois lectures font naître les questions à explorer en classe.

## Les six sentinelles de départ

| Animal | Comportement | Capteur intégré | Grandeur |
|---|---|---|---|
| L'abeille | Perception particulière des couleurs des fleurs | APDS-9960 | Couleur |
| Le crocodile | Thermorégulation comportementale | WSEN-HIDS | Température |
| La chouette | Vision adaptée à la faible lumière | APDS-9960 | Éclairement |
| La rainette | Sensibilité à l'humidité du milieu | WSEN-HIDS | Humidité |
| La chauve-souris | Estimation des distances par écholocation | VL53L1X | Distance |
| Le fennec | Perception de sons faibles | IMP34DT05 | Niveau sonore |

Le martinet (pression), le chat (mouvement) et la tortue caouanne (orientation et lumière)
pourront rejoindre le bestiaire dans un second temps.

Tous ces capteurs sont **intégrés à la carte** : aucun câblage n'est nécessaire.

## Trois exemples d'investigation

- **Nos nuits sont-elles vraiment noires ?** — la chouette, la lumière nocturne et notre sommeil.
- **Où et quand l'école est-elle trop bruyante ?** — le fennec, le paysage sonore et la concentration.
- **Où fait-il bon dans la cour quand il fait chaud ?** — le crocodile, les microclimats et le confort d'été.

## Contenu du dépôt

| Chemin | Contenu |
|---|---|
| `index.html` | La page de présentation, publiée avec GitHub Pages |
| `presentation/generateur/` | Les scripts Python qui produisent la page, ses illustrations et ses schémas |
| `texte/bestiaire-steami-texte-notion.md` | Le texte seul, en Markdown, importable dans Notion |

### Régénérer la page

Les illustrations, les schémas et la mise en page sont générés par des scripts Python, sans
dépendance à installer (Python 3 suffit).

```bash
cd presentation/generateur
python3 site.py        # produit la page
python3 export_md.py   # produit l'export Markdown
```

La page est autonome : un seul fichier HTML, avec toutes ses illustrations en SVG.
Seules les polices sont chargées depuis Google Fonts.

## État du projet

Projet **en conception**. Le principe, les sentinelles et la démarche d'investigation sont posés ;
la présentation sert à en discuter avec des enseignant·es et des partenaires.

Restent à valider :

- les dimensions de la carte équipée de sa batterie, et le principe de fixation ;
- la fabrication d'un premier prototype ;
- un programme d'enregistrement et la récupération des données par les élèves ;
- l'autonomie de la carte en enregistrement continu.

## Ancrage dans le programme

Le projet s'appuie sur le programme de sciences et technologie du cycle 3
([BO n° 24 du 11 juin 2026](https://www.education.gouv.fr/bo/2026/Hebdo24-0)), notamment :
relier les êtres vivants aux caractéristiques physiques de leur milieu, réaliser des mesures avec
des capteurs, aborder la variabilité des mesures, concevoir et fabriquer un objet technique,
et le programmer.

## Crédits

Projet porté par le [L.A.B — Laboratoire d'Aix-périmentation et de Bidouille](https://labaixbidouille.fr),
dans le cadre du programme I-NOVMICRO. Carte STeaMi : [steamicc](https://github.com/steamicc).
