# NeoReg

## Descripción general

NeoReg es un sistema distribuido basado en microservicios que ofrece funcionalidades relacionadas con gestión de usuarios, trabajadores y servicios de consultas inteligentes (RAG).

## Arquitectura

El sistema está compuesto por los siguientes servicios:

- **User Service**: Gestión de usuarios y personas
- **Worker Service**: Gestión de trabajadores
- **RAG Service**: Servicio de consultas con Retrieval Augmented Generation
- **API Gateway (Traefik)**: Enrutamiento centralizado de peticiones
- **Base de datos PostgreSQL**: Almacenamiento de datos

## Configuración inicial

### Requisitos previos

- Docker y Docker Compose
- Variables de entorno configuradas en un archivo `.env`

### Variables de entorno requeridas

## Iniciando el sistema

### Gestión de servicios individuales

## Endpoints disponibles

### User Service

**Base URL**: `http://localhost/api/users/`

| Método | Endpoint                    | Descripción                               |
| ------ | --------------------------- | ----------------------------------------- |
| POST   | `/api/v1/personas/`         | Crear una nueva persona                   |
| PUT    | `/api/v1/personas/{id}`     | Actualizar datos de una persona           |
| DELETE | `/api/v1/personas/{id}`     | Eliminar una persona                      |
| POST   | `/api/v1/photos/upload`     | Subir una foto al servidor                |
| GET    | `/api/v1/photos/{filename}` | Obtener una foto por su nombre de archivo |
| DELETE | `/api/v1/photos/{filename}` | Eliminar una foto del servidor            |

### Gestión de Fotos

El sistema permite la gestión de imágenes mediante los siguientes endpoints:

#### Subir una foto

```bash
curl -X POST "http://localhost/api/users/api/v1/photos/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/ruta/a/tu/imagen.jpg"
```

# Respuesta

{
"filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
"original_filename": "mi_foto.jpg",
"size": 102400,
"content_type": "image/jpeg",
"url": "/api/v1/photos/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg"
}

### Worker Service

**Base URL**: `http://localhost/api/workers/`

| Método | Endpoint               | Descripción                   |
| ------ | ---------------------- | ----------------------------- |
| GET    | `/api/v1/workers/`     | Listar todos los trabajadores |
| GET    | `/api/v1/workers/{id}` | Obtener un trabajador por ID  |

### RAG Service

**Base URL**: `http://localhost/api/rag/`

| Método | Endpoint                | Descripción                                               |
| ------ | ----------------------- | --------------------------------------------------------- |
| POST   | `/api/v1/rag/query`     | Realizar consulta de información en lenguaje natural      |
| POST   | `/api/v1/rag/sql-query` | Convertir pregunta en lenguaje natural a SQL y ejecutarla |

## Monitoreo y Logging

El sistema incluye un sistema de logging integral que captura información detallada de todas las solicitudes y respuestas API.

### Acceso a los logs

Los logs están disponibles a través de los siguientes endpoints:

| Método | Endpoint                              | Descripción                                  |
| ------ | ------------------------------------- | -------------------------------------------- |
| GET    | `rutaMicroServicio/api/v1/logs`       | Obtener logs con filtros opcionales          |
| GET    | `rutaMicroServicio/api/v1/logs/stats` | Obtener estadísticas de los logs             |
| DELETE | `rutaMicroServicio/api/v1/logs/clear` | Limpiar todos los logs (usar con precaución) |

### Filtrado de logs

El endpoint `/api/users/api/v1/logs` acepta los siguientes parámetros de consulta:

- `limit`: Número máximo de logs a devolver (por defecto: 100)
- `type_filter`: Filtrar por tipo (request, response, error)
- `path_filter`: Filtrar por ruta de API (coincidencia parcial)
- `method_filter`: Filtrar por método HTTP (GET, POST, PUT, DELETE)
- `status_code`: Filtrar por código de estado HTTP
- `since`: Mostrar logs desde una marca de tiempo ISO o tiempo relativo (ej. '1h', '30m', '1d')

### Ejemplo de uso

## Ejemplos de uso

### Crear una persona

(Agregar ejemplo de cómo hacer un POST para crear una persona aquí)

### Consultar trabajadores

(Agregar ejemplo de cómo hacer un GET para consultar trabajadores aquí)

### Hacer una consulta en lenguaje natural

(Agregar ejemplo de cómo hacer un POST para realizar una consulta aquí)

## Acceso a interfaces

- **API Gateway**: [http://localhost/](http://localhost/)
- **Dashboard Traefik**: [http://localhost:8080/](http://localhost:8080/)
- **Acceso directo a servicios**:
  - User Service: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Worker Service: [http://localhost:8002/docs](http://localhost:8002/docs)
  - RAG Service: [http://localhost:8001/docs](http://localhost:8001/docs)

## Solución de problemas

- **Verificar logs de un servicio**:
  (Incluir pasos para verificar logs aquí)

- **Reiniciar todos los servicios**:
  `docker-compose down`

- **Limpiar volúmenes para empezar desde cero**:
  (Incluir pasos para limpiar volúmenes aquí)

## Notas adicionales

- El sistema utiliza Traefik como API Gateway para enrutar las peticiones a los servicios correspondientes.
- PostgreSQL almacena los datos en un volumen persistente.
- Cada servicio tiene su propio Swagger/OpenAPI disponible en la ruta `/docs`.
