# Blackjack

## Instalacion

Creamos una carpeta y dentro hacemos clone de los siguientes repos:

    git clone git@github.com:Mauriciopizarro/blackjack_api_gateway.git

    git clone git@github.com:Mauriciopizarro/game_service.git

    git clone git@github.com:Mauriciopizarro/blacjack_game_management_service.git

Ahora vamos a crear el docker compose en la carpeta que contiene los servicios:

    version: '3.3'
    
    services:
    
      rabbitmq:
        image: rabbitmq:3-management-alpine
        container_name: 'rabbitmq'
        ports:
            - 5672:5672
            - 15672:15672
        restart: always
      
      mongo:
        image: mongo:4.4.18-rc0-focal
        container_name: 'mongo'
        environment:
          - MONGO_INITDB_DATABASE=blackjack
        ports:
          - "27017:27017"
    
      mysql:
        image: mysql:8.0.31
        restart: always
        container_name: 'mysql'
        environment:
          MYSQL_DATABASE: 'blackjack'
          # So you don't have to use root, but you can if you like
          MYSQL_USER: 'user'
          # You can use whatever password you like
          MYSQL_PASSWORD: 'password'
          # Password for root access
          MYSQL_ROOT_PASSWORD: 'password'
        ports:
          # <Port exposed> : < MySQL Port running inside container>
          - '3306:3306'
      
      api_gateway:
        build: ./blackjack_api_gateway
        container_name: 'api_gateway'
        ports:
          - 5000:5000
        environment:
          PORT: 5000
        depends_on:
          - mongo
          - mysql
        stdin_open: true
        tty: true
        volumes:
          - ./blackjack_api_gateway:/app
          
      game_management_service:
        container_name: 'game_management_service'
        build: ./blackjack_game_management_service
        ports:
          - 5001:5001
        environment:
          PORT: 5001
        depends_on:
          - mongo
          - mysql
          - rabbitmq
        stdin_open: true
        tty: true
        volumes:
          - ./blackjack_game_management_service:/app
     
      game_service:
        container_name: 'game_service'
        build: ./blackjack_game_service
        ports:
          - 5002:5002
        environment:
          PORT: 5002
        depends_on:
          - mongo
          - mysql
          - rabbitmq
        stdin_open: true
        tty: true
        volumes:
          - ./blackjack_game_service:/app      
      
      game_service_consumer:
        container_name: 'game_service_consumer'
        build:
          context: ./blackjack_game_service
          dockerfile: Dockerfile.consumer
        depends_on:
          - mongo
          - mysql
          - rabbitmq
        stdin_open: true
        tty: true
        volumes:
          - ./blackjack_game_service:/app
      
      send_email_consumer:
        container_name: 'api_gateway_send_email_consumer'
        build:
          context: ./blackjack_api_gateway
          dockerfile: Dockerfile.consumer
        depends_on:
          - mongo
          - mysql
          - rabbitmq
        stdin_open: true
        tty: true

  
La estructura deberia quedar asi:

    ├── blackjack_game_management_service
    ├── blackjack_api_gateway
    ├── blackjack_game_service
    └── docker-compose.yml

Ahora vamos a levantar el docker-compose.yml, para ello deben tener instalado docker y docker compose

    docker compose up --build

Una vez levantada la app ya la tenemos corriendo en el puerto 5000


## Enpoints

El juego cuenta de 3 modulos, el primero es el de creacion de usuarios, donde tenemos el sign_up, el login y el reset_password, con estos 3 endpoints un usuario podra crear su cuenta y obtendra un token para hacer las consecuentes request.


Primero vamos a crear una cuenta:

    curl --location 'http://localhost:5000/sign_up' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "username": "YOUR_USERNAME",
        "email": "YOUR_EMAIL",
        "password": "YOUR_PASSWORD"
    }'

Al registrarnos se nos enviara un mail de bienvenida con nuestro username:

![mail.png](.src%2Fmail.png)

Con el username y password creados vamos a iniciar sesion:

    curl --location 'http://localhost:5000/login' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "USERNAME",
        "password": "PASSWORD"
    }'

Tanto con el sign_up como con el login obtendremos un token, este token es el que usaremos para realizar las siguientes pegadas.

    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNzg2NTc3MDUsInN1YiI6Ik1hdXJpIn0.Mf7-HrvHaXVfNWx1kYZ7wuXUh7mEHX2guYRSQQ5c0uc",
    }

Para crear un juego:

    curl --location --request POST 'http://localhost:5000/game/create' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNzg1NjkyNDUsInN1YiI6IkFkcmk5NyJ9.YQmjojuVZGG0YRZ4mYABACgqoz5yJVAvxF21-rtXQRY' \
    --data ''

Al crear un juego obtendremos el game_id, con este game_id se pueden unir otros players a la partida, para ello se debe usar el siguiente endpoint:

    curl --location --request POST 'http://localhost:5000/game/enroll_player/GAME_ID' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNzg1NjkyNDUsInN1YiI6IkFkcmk5NyJ9.YQmjojuVZGG0YRZ4mYABACgqoz5yJVAvxF21-rtXQRY' \
    --data ''

Una vez que esten todos los players, solo el admin (el player que creo el juego) podra iniciarlo, para ello usara el siguiente endpoint:

    curl --location --request POST 'http://localhost:5000/game/start/GAME_ID' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNzg1NjkyNDUsInN1YiI6IkFkcmk5NyJ9.YQmjojuVZGG0YRZ4mYABACgqoz5yJVAvxF21-rtXQRY' \
    --data ''

Para ver el status de un game usaremos:

    curl --location 'http://localhost:5000/game/status/GAME_ID'

El jugador podra pedir una carta:

    curl --location --request POST 'http://localhost:5000/game/deal_card/GAME_ID' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNzg1NjkyNDUsInN1YiI6IkFkcmk5NyJ9.YQmjojuVZGG0YRZ4mYABACgqoz5yJVAvxF21-rtXQRY' \
    --data ''

Tambien puede plantarse:

    curl --location --request POST 'http://localhost:5000/game/stand/GAME_ID' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNzg1NjkyNDUsInN1YiI6IkFkcmk5NyJ9.YQmjojuVZGG0YRZ4mYABACgqoz5yJVAvxF21-rtXQRY'

Cuando el jugador se planta, pasa el turno al siguiente player, si ya jugaron todos los players, es turno del Croupier, con el siguiente endopoint juega:

    curl --location --request POST 'http://localhost:5000/game/croupier_play/GAME_ID'

Una vez que el Croupier juega la partida termina, si se le hace un GET a status nuevamente se podra ver los ganadores de la partida.

El player puede consultar el historial su historial de partidas:

    curl --location 'http://localhost:5000/player/history/PLAYER_ID'

