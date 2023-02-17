# Ikusi Devnet Project

## Getting started

Repositorio base para el proyectos con FastAPI y Analisis de datos aplicados a APis.

## How to run

- En el archivo docker-compose se setean las variables de ambiente
`BASE_URL` - Obligatorio, URL para API de Meraki
`API_KEY` - Obligatorio, api key para el acceso a la API
`ORG_ID` - Opcional, si deseamos obtener los datos de una organización en particular; en caso de no setear este valor, se tomará la primera disponible en la API.

- Instalar `docker` y `docker-compose`
- Ejecutar `docker-compose up -d`
- Abrir en navegador `http://localhost:8001/`
