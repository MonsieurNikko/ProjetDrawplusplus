# draw++ - Un Langage de Dessin Personnaliséw

## Aperçu du Projet

Bienvenue dans le projet **draw++**, développé dans le cadre de notre projet semestriel en Python de 2024. L'objectif de ce projet est de concevoir un langage de programmation personnalisé, *draw++*, qui permet aux utilisateurs de créer et manipuler des formes graphiques sur un écran à partir d'instructions définies. Nous nous concentrons sur la création du langage ainsi que d'un environnement de développement intégré (IDE) pour faciliter la création, l'édition et l'exécution du code *draw++*.

## Fonctionnalités

### Instructions Élémentaires
Le langage *draw++* prend en charge les fonctionnalités de dessin de base, notamment :
- **Création de Curseur** : Créez un curseur (un point de référence) avec une position spécifique sur l'écran, définie par des coordonnées (x, y).
- **Déplacement du Curseur** : Déplacez un curseur de manière relative en pixels.
- **Changement de Couleur ou d'Épaisseur** : Modifiez la couleur et l'épaisseur des tracés effectués par un curseur.
- **Dessin de Formes** : Dessinez des formes simples comme des lignes, des carrés, des cercles, des arcs, etc.

### Instructions Évoluées
En plus des instructions élémentaires, *draw++* propose des fonctionnalités évoluées comme :
- **Assignation** : Affectez des valeurs à des variables.
- **Blocs d'Instructions** : Regroupez plusieurs instructions dans une seule unité.
- **Conditions et Boucles** : Utilisez des instructions conditionnelles (`if`, `else`) et des boucles (`for`, `while`) pour des dessins dynamiques et répétitifs.

## Objectifs du Projet

1. **Langage de Programmation** : Développer un langage simple et intuitif pour dessiner des formes.
2. **Environnement de Développement (IDE)** : Créer une interface utilisateur qui permet d'écrire, de modifier et d'exécuter du code *draw++* avec des outils d'édition et de débogage.
3. **Compilateur** : Implémenter un compilateur qui analyse le code *draw++* et génère un code intermédiaire en C.
4. **Documentation Interactive** : Fournir une documentation claire et complète pour aider les utilisateurs à apprendre le langage *draw++*.

## Structure du Projet

Le projet est divisé en plusieurs parties :
- **Conception du Langage** : Définition de la syntaxe et de la grammaire du langage *draw++*.
- **Développement du Compilateur** : Détection des erreurs dans le code et génération de code intermédiaire en C.
- **Création de l'IDE** : Un éditeur avec des fonctionnalités de gestion de fichiers, de visualisation de dessins, et de correction automatique des erreurs.
- **Documentation et Tests** : Rédaction d'une documentation complète et réalisation de tests pour garantir la qualité du projet.


## Comment Contribuer

### Pré-requis

1. **Créer un compte GitHub** : Si vous n'avez pas encore de compte GitHub, créez-en un en visitant [github.com](https://github.com/).

### Étapes pour se connecter à GitHub et configurer Git

1. **Configurer Git avec votre identité** : Avant de commencer à utiliser Git, vous devez définir votre nom d’utilisateur et votre adresse e-mail, qui apparaîtront avec vos commits.

   Ouvrez un terminal et entrez ces commandes :
   
   ```bash
   git config --global user.name "Votre Nom"
   git config --global user.email "votre-email@example.com"
   ```

2. **Générer une clé SSH** : Afin de pouvoir se connecter à GitHub et envoyer des modifications sans entrer vos identifiants à chaque fois, vous pouvez configurer une clé SSH.

   - Générez une clé SSH avec cette commande (appuyez sur "Entrée" pour toutes les options) :
     ```bash
     ssh-keygen -t rsa -b 4096 -C "votre-email@example.com"
     ```

   - Ajoutez la clé SSH à votre agent SSH :
     ```bash
     eval "$(ssh-agent -s)"
     ssh-add ~/.ssh/id_rsa
     ```

   - Copiez le contenu de la clé publique (elle se trouve dans le fichier `id_rsa.pub`) :
     ```bash
     cat ~/.ssh/id_rsa.pub
     ```

   - Allez sur GitHub, puis dans **Settings** > **SSH and GPG keys** et cliquez sur **New SSH key**. Collez la clé que vous avez copiée.

3. **Tester la connexion avec GitHub** :
   
   Pour vérifier si la connexion SSH fonctionne, utilisez la commande suivante :
   ```bash
   ssh -T git@github.com
   ```

   Si tout fonctionne, vous verrez un message de succès.

---

> **Note** : Pour cloner le dépôt sur Ubuntu, évitez de sauvegarder dans le dossier `data`. Utilisez plutôt un autre emplacement, tel que votre dossier personnel (`~/`) ou tout autre dossier spécifique pour vos projets, afin d'éviter des conflits ou des permissions limitées.

### Étapes pour contribuer au projet

1. **Cloner le dépôt** : La première étape consiste à cloner le dépôt GitHub sur votre machine locale. Cela vous permet de récupérer le projet et de commencer à y travailler.

   Ouvrez un terminal et entrez la commande suivante :
   ```bash
   git clone https://github.com/MonsieurNikko/ProjetDrawplusplus.git
   ```

   Cette commande téléchargera tout le projet dans un répertoire local.

2. **Créer une branche** : Avant de commencer à modifier le code, créez une nouvelle branche. Cela permet de travailler sur une fonctionnalité sans affecter le travail des autres membres de l’équipe.

   Utilisez cette commande pour créer une nouvelle branche et y basculer :
   ```bash
   git checkout -b nom-de-votre-branche
   ```

   Exemple :
   ```bash
   git checkout -b ajout-curseur
   ```

3. **Faire des modifications** : Après avoir créé votre branche, vous pouvez faire les modifications nécessaires dans le projet à l'aide de votre éditeur de texte préféré.

4. **Suivre les modifications** : Vérifiez quels fichiers ont été modifiés après vos changements.

   ```bash
   git status
   ```

5. **Ajouter les modifications** : Ajoutez les fichiers modifiés au suivi (staging area).

   Pour ajouter un fichier spécifique :
   ```bash
   git add nom-du-fichier
   ```

   Ou pour ajouter tous les fichiers modifiés :
   ```bash
   git add .
   ```

6. **Créer un commit** : Une fois les fichiers ajoutés, validez vos modifications en créant un commit.

   ```bash
   git commit -m "Description de vos changements"
   ```

   Exemple :
   ```bash
   git commit -m "Ajout de la fonctionnalité de création de curseur"
   ```

7. **Pousser les modifications vers GitHub (Push)** : Maintenant que vos changements sont commités, envoyez-les vers votre branche sur GitHub.

   ```bash
   git push origin nom-de-votre-branche
   ```

8. **Créer une pull request** : Une fois les modifications poussées sur GitHub, allez sur la page du dépôt et cliquez sur **Compare & pull request**. Décrivez brièvement les modifications et soumettez la pull request pour que vos coéquipiers puissent la réviser.

---

### Récapitulatif des commandes Git essentielles

| Commande | Description |
|----------|-------------|
| `git clone URL` | Clone le dépôt sur votre machine locale. |
| `git checkout -b nom-branche` | Crée et passe sur une nouvelle branche. |
| `git status` | Affiche les fichiers modifiés ou ajoutés. |
| `git add .` | Ajoute tous les fichiers modifiés pour un commit. |
| `git commit -m "message"` | Crée un commit avec un message descriptif. |
| `git push origin nom-branche` | Envoie vos modifications vers GitHub. |
| `git pull origin main` | Récupère les dernières modifications de la branche principale. |


### Compilation

Pour compiler le projet avec SDL, utilisez la commande suivante :

```bash
gcc -o nomdufichier nomdufichier.c -Isrc/include -Lsrc/lib -lmingw32 -lSDL2main -lSDL2

./nomdufichier
```

### Conseils 

- **Faites des commits régulièrement** : Il est conseillé de faire des commits fréquents avec des messages clairs.
- **Messages descriptifs** : Soyez précis dans vos messages de commit pour faciliter le suivi du projet.
- **Toujours travailler sur une branche** : Ne travaillez jamais directement sur la branche `main`. Créez toujours une nouvelle branche pour vos modifications.

## Équipe

- **Membres de l'équipe** : Duc Duy HUYNH, Thomas NGUYEN, Thomas PISANESCHI, Owen PAIMBA-SAIL, Axel COTTRANT, Maëlys PICAULT



