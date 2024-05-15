# TP 

## Instruction d’utilisation

### Charger des images 

- Allez dans une platforme de test Api par exemple : Postman
- Taper l'url http://milanfayel.gjf4b4axcrdyd9hm.francecentral.azurecontainer.io:5000/images
- Sélectionnez la route POST 
- Initialisez un body application/json 
- Choisissez votre image que vous voulez charger
- Envoyez la requête 

### Récuperer la liste des tags 

- Allez dans une platforme de test Api par exemple : Postman
- Taper l'url http://milanfayel.gjf4b4axcrdyd9hm.francecentral.azurecontainer.io:5000/tags
- Sélectionnez la route GET 
- Envoyez la requête 

### Récuperer la liste des images 

- Allez dans une platforme de test Api par exemple : Postman
- Taper l'url http://milanfayel.gjf4b4axcrdyd9hm.francecentral.azurecontainer.io:5000/images
- Sélectionnez la route GET 
- Envoyez la requête 

### Récuperer la liste des images par tag

- Allez dans une platforme de test Api par exemple : Postman
- Taper l'url http://milanfayel.gjf4b4axcrdyd9hm.francecentral.azurecontainer.io:5000/image/"mettre le tag"
- Sélectionnez la route GET 
- Envoyez la requête 

### Récuperer la liste des images par description 

- Allez dans une platforme de test Api par exemple : Postman
- Taper l'url http://milanfayel.gjf4b4axcrdyd9hm.francecentral.azurecontainer.io:5000/images/description 
- Sélectionnez la route POST 
- Initialisez un body application/json 
- Mettre la description dans le body
- Envoyez la requête 

## Description / explication de l’architecture mise en place

#### Base de données 
fayelmilandb<p>
Serveur flexible Azure Database pour MySQL<p>
Permet de stocker l'url de l'image, son id, ses tags et sa description

#### Conteneur (Object Storage)
fayelmilan<p>
Compte de stockage<p>
Permet de stocker les images

#### ComputerVision
CVFayelMilan<p>
Vision par ordinateur<p>
Permet de créer des tags et des descriptions d'une image grâce a l'ia 

#### Backend
Python Framework(Flask)<p>
Permet de créer l'API REST charger les images ,faire des recherches ...