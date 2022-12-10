# Examens (UT2J)

Script pour générer un fichier de calendrier pour un emploi du temps d'examens à
l'Université de Toulouse Jean Jaurès.

## Usage

- Installer les dépendances du projet (`ics` et `toml`).
- Télécharger le fichier excel avec toutes les dates d'examens pour la session
  voulue (disponible [ici](https://anthropologie.univ-tlse2.fr/accueil/examens))
  et le convertir au format `.csv` (format: séparateur virgule et guillemets).
- Nommer le fichier obtenu `exam_data.csv` et le placer à la racine du projet.
- Créer le fichier de configuration `config.toml` à la racine, en se basant sur
  le contenu de `config.example.toml`.
- Lancer `generate_schedule.py`.
- Ouvrir le fichier de calendrier contenant votre emploi du temps,
  `out/schedule.ics`.
