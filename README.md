# 🚌 Intégration STAR pour Home Assistant

Cette intégration Home Assistant permet de surveiller en temps réel les horaires des deux prochains bus d'une ligne spécifique du réseau de transport en commun **STAR** (Rennes Métropole).

Elle vous permet de :
- Choisir une **ligne de bus**,
- Sélectionner la **direction** du trajet,
- Choisir l'**arrêt** à surveiller,
- Afficher dans combien de minutes passeront les **2 prochains bus**.

## 🔧 Prérequis

Avant de pouvoir utiliser cette intégration, vous devez obtenir une **clé d'API** personnelle depuis le portail open data du STAR :

👉 [https://data.explore.star.fr](https://data.explore.star.fr)

Créez un compte, puis générez un jeton dans l’espace développeur.

## 🌐 Liens utiles

- Site officiel du réseau STAR : [https://www.star.fr](https://www.star.fr)
- Données ouvertes : [https://data.explore.star.fr](https://data.explore.star.fr)

## 🚀 Installation via HACS

1. Assurez-vous que [HACS](https://hacs.xyz/) est installé et configuré dans votre Home Assistant.
2. Dans HACS, allez dans **"Intégrations"**, puis cliquez sur le bouton **"+"**.
3. Recherchez `STAR Bus` ou ajoutez ce dépôt en tant que **dépôt personnalisé** s’il n’apparaît pas automatiquement.
4. Installez l'intégration.
5. Redémarrez Home Assistant.

## ⚙️ Configuration

L'intégration peut être configurée via l’interface utilisateur :

1. Allez dans **Paramètres > Appareils et services > Ajouter une intégration**.
2. Recherchez `STAR Bus`.
3. Entrez votre **clé d'API**.
4. Sélectionnez :
   - la **ligne de bus**,
   - la **direction**,
   - l'**arrêt de bus**.

L'intégration créera un ou plusieurs **capteurs** indiquant :
- les temps d’attente en minutes jusqu’aux deux prochains passages,
- La **localisation** des bus, si ces informations sont renvoyées par l'API.
