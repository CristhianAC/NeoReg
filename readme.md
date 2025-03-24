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

| Método | Endpoint                | Descripción                     |
| ------ | ----------------------- | ------------------------------- |
| GET    | `/api/v1/personas/`     | Listar todas las personas       |
| GET    | `/api/v1/personas/{id}` | Obtener una persona por ID      |
| POST   | `/api/v1/personas/`     | Crear una nueva persona         |
| PUT    | `/api/v1/personas/{id}` | Actualizar datos de una persona |
| DELETE | `/api/v1/personas/{id}` | Eliminar una persona            |

### Worker Service

**Base URL**: `http://localhost/api/workers/`

| Método | Endpoint               | Descripción                       |
| ------ | ---------------------- | --------------------------------- |
| GET    | `/api/v1/workers/`     | Listar todos los trabajadores     |
| GET    | `/api/v1/workers/{id}` | Obtener un trabajador por ID      |
| POST   | `/api/v1/workers/`     | Crear un nuevo trabajador         |
| PUT    | `/api/v1/workers/{id}` | Actualizar datos de un trabajador |
| DELETE | `/api/v1/workers/{id}` | Eliminar un trabajador            |

### RAG Service

**Base URL**: `http://localhost/api/rag/`

| Método | Endpoint                | Descripción                                               |
| ------ | ----------------------- | --------------------------------------------------------- |
| POST   | `/api/v1/rag/query`     | Realizar consulta de información en lenguaje natural      |
| POST   | `/api/v1/rag/sql-query` | Convertir pregunta en lenguaje natural a SQL y ejecutarla |

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
