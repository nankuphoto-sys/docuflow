# DocuFlow — plan del proyecto

Plataforma donde una empresa sube documentos (facturas, cotizaciones, contratos) y un sistema los procesa en segundo plano: extrae los datos con IA, los valida, marca los dudosos para revisión humana y muestra el avance en tiempo real.

**Objetivo de portafolio:** demostrar un sistema con varios servicios, colas, tiempo real, Python, AWS y IA con control de calidad. Son las brechas que más se repitieron en las ofertas.

---

## Arquitectura

```
 Next.js (frontend) ──HTTP──▶ FastAPI (API, Python) ──▶ PostgreSQL
        ▲                          │
        │ WebSocket (avance)       │ encola trabajo
        │                          ▼
        └──────── Redis ◀──── Worker(s) Python ──▶ Claude (extracción)
                 (cola + eventos)        │
                                         └──▶ almacenamiento de archivos (local → S3)
```

| Pieza | Tecnología | Qué aprendes |
| --- | --- | --- |
| API | Python + FastAPI + Pydantic | Python, APIs tipadas |
| Base de datos | PostgreSQL + SQLAlchemy + Alembic | ORM y migraciones en Python |
| Cola | Redis + RQ (o Celery) | trabajos en segundo plano, reintentos |
| Worker | Python | procesamiento asíncrono e idempotencia |
| IA | Claude con salida estructurada | extracción + umbrales de confianza |
| Tiempo real | WebSockets (FastAPI) + Redis pub/sub | eventos en vivo |
| Frontend | Next.js + TypeScript | lo que ya sabes |
| Infraestructura | Docker Compose → AWS (ECS o EC2, RDS, S3, SQS) | nube real |
| Calidad | pytest, evaluación de precisión, GitHub Actions | pruebas en Python |

---

## Fases (cada una termina funcionando y publicada en GitHub)

### Fase 0 — Preparar el entorno (1 día)
- Instalar Python 3.12 (python.org, marcando "Add to PATH") y `uv` (gestor de paquetes).
- Crear el repo `docuflow` en GitHub.
- Aprender lo básico de Python que cambia frente a TypeScript: tipos, `async`/`await`, entornos virtuales.

### Fase 1 — API y base de datos (1 semana)
- FastAPI con endpoints: subir documento, listar documentos, ver uno.
- PostgreSQL en Docker, modelos con SQLAlchemy y migraciones con Alembic.
- Estados del documento: `pendiente → procesando → listo / requiere_revision / error`.
- Pruebas con pytest.
- **Entregable:** subes un PDF por la API y queda guardado como `pendiente`.

### Fase 2 — Cola y worker (1 semana)
- Redis en Docker; al subir un documento se encola un trabajo.
- Worker que toma el trabajo, lee el PDF y cambia el estado.
- Reintentos con espera creciente; un trabajo procesado dos veces no duplica nada (idempotencia).
- **Entregable:** subes 100 documentos y se procesan en segundo plano sin bloquear la API.

### Fase 3 — Extracción con IA y control de calidad (1 semana)
- Claude extrae los campos (proveedor, fecha, ítems, total) con salida estructurada validada con Pydantic.
- Validaciones deterministas: que la suma de los ítems dé el total y que las fechas sean válidas.
- Si algo no cuadra o la confianza es baja, pasa a `requiere_revision`.
- Evaluación con 20 documentos de ejemplo: precisión por campo.
- **Entregable:** tabla de precisión en el README, como en tus otros proyectos.

### Fase 4 — Frontend y tiempo real (1 semana)
- Next.js: subir archivos, lista con el estado en vivo y pantalla de revisión humana.
- WebSockets: el worker publica eventos en Redis y la API los reenvía al navegador.
- **Entregable:** subes 10 documentos y ves cómo cambia cada uno en vivo.

### Fase 5 — AWS y observabilidad (1 a 2 semanas)
- Archivos en S3, base en RDS y la cola en SQS (o Redis administrado).
- Despliegue con Docker en ECS o EC2; CI/CD con GitHub Actions.
- Métricas: latencia por documento, tasa de error y costo de IA por documento.
- **Entregable:** demo pública en AWS y diagrama de arquitectura en el README.

---

## Reglas de trabajo
- **Tú escribes el código**; Claude explica, guía y revisa. Tienes que poder explicar cada parte en una entrevista.
- Commits pequeños y un pull request por funcionalidad, aunque trabajes solo.
- Cada fase cierra con su README actualizado y una prueba en vivo.
- Mientras tanto, sigue postulando a ofertas junior.

## Cómo se ve en la hoja de vida (al terminar)
> **DocuFlow — procesamiento de documentos con IA** · Python, FastAPI, Redis, PostgreSQL, Next.js, AWS
> Sistema de varios servicios que procesa documentos en segundo plano con colas y reintentos, extrae datos con IA validada y envía el avance en tiempo real por WebSockets; desplegado en AWS con métricas de latencia, errores y costo.
