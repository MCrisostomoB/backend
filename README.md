# Ejecución
## Creación de containers:
`docker network create artificial` crea la red para los container.

`docker-compose build` crea las imagenes.

## Ejecución:
`docker-compose up`

## Ejecutar comando dentro de un container:
`docker-compose exec <container> <comando>`

Donde container es el nombre que se define en el _docker compose_. Un ejemplo seria:

- `docker-compose exec stock-db psql artificial -U artificial`

## Migraciones:

- `docker-compose exec stock flask db migrate -m "mensaje"` crea una nueva migración. **OJO** es necesario ver el archivo de la migración para saber que todos los cambios se hacen como uno quiere.
- `docker-compose exec stock flask db upgrade` hace los ultimos cambios.


## Editar archivos con permisos sudo:
`sudo chown -R user:user .` 

Donde _user_ es el nombre de usuario del equipo. De esta manera cualquier archivo generado con sudo puede ser editar por un tiempo sin tener que hacer sudo.

## Entrar a la consola de la base de datos en el container:
`docker-compose exec stock-db bash` entrar al terminal del container.

`psql artificial artificial`

## Ver todas las tablas creadas en psql:
`\dt`

## Ver el detalle de una tabla creada en psql:
`\d+ <table_name>`

## Salir de la linea de comandos de psql y del container:
`\q`
`exit`

# Endpoints:

## Pasillos:
### `GET /pasillo`
Obtener todos los pasillos
TODO las camaras de estas y la prediccion mas actual.
```JSON
[{ 
    "categoria": "nombre_categoria",
    "numero": int numero_pasillo ,
    "predicciones": [{
        "id": int, //cuadrados
        "id_camara": int, //foto
        "total_boxes": int //total espacios vaacios
    } ...]

}]
```

### `POST /pasillo`
Crea un nuevo pasillo
- Cuerpo: 
```JSON
{ 
    "categoria": "nombre_categoria",
    "numero": int numero_pasillo 
}
```

### TODO `GET /pasillo?id=int`

## Camaras:
TODO: lo mismo que en pasillo + GET por _id_.

## Predicciones:
```json
{
    "id": int,
    "id_camara": int,
    "fecha": string,
    "total_boxes": int,
    "area_boxes": int
}
```

### `POST /prediccion`
A partir del nombre de la camara se busca su id, se crea la predicción con esta información y todos sus cuadrados.
- Cuerpo:
```JSON
{
    "camera": "nombre_camara",
    "data": [
        {
            "label": 0,
            "confidence": 0.1,
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0
        }
    ]
}
```
- Respuesta: La predicción con la estructura expuesta arriba.

### `GET /prediccion`
Obtener todas las predicciones.

## Cuadrados:
```json
{
    "id": int,
    "prediccion_id": int,
    "clase": int,
    "center_x": int,
    "center_y": int,
    "width": int,
    "height": int,
    "accuracy": float
}
```

### `GET /cuadrados?prediccion_id=int`
Obtener todos los cuadrados a partir del id de la predicción.

## Fotos:
### TODO: `POST /foto`
Crear una foto a partir del id de la camara

### TODO: `GET /foto?camara_id=int`
Obtener ultima foto a partir del id de la camara