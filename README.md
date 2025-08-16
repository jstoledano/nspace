# nspace

> Plataforma de blogging escalable con backend en Django y caché de Redis para máxima velocidad. Arquitectura moderna orientada a contenedores, lista para orquestación con Kubernetes y pipelines de CI/CD.

---

### Nota sobre el Estado del Proyecto

Este proyecto se encuentra en una fase de modernización. La base de código actual utiliza componentes legacy (como Django 1.6) y el objetivo es actualizarla por completo a un stack tecnológico moderno, seguro y escalable.

## Arquitectura Actual

La aplicación funciona sobre una arquitectura monolítica con los siguientes componentes principales:

*   **Framework:** Django 1.6.1
*   **Base de Datos:** PostgreSQL
*   **Sistema de Caché:** Se utilizan tanto Redis como Memcached para diferentes propósitos de caché.
*   **Cola de Tareas Asíncronas:** Celery para procesar tareas en segundo plano.
*   **Servidor WSGI:** Gunicorn

## Instalación Local

Para ejecutar el proyecto en un entorno de desarrollo, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/jstoledano/nspace.git
    cd nspace
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Instala las dependencias:**
    > **Aviso:** Necesitarás tener las cabeceras de desarrollo de Python y PostgreSQL instaladas en tu sistema.
    ```bash
    pip install -r requisitos.txt
    ```

4.  **Configura los servicios:**
    Asegúrate de tener instancias de PostgreSQL, Redis y Memcached en ejecución. Deberás configurar los detalles de conexión en los archivos de settings, ubicados en `src/namespace/settings/`.

5.  **Aplica las migraciones:**
    ```bash
    python src/manage.py migrate
    ```

6.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python src/manage.py runserver
    ```

## Roadmap y Futuro del Proyecto

El plan a futuro es modernizar completamente la aplicación.

*   **[TODO] Actualización del Core:**
    *   Migrar de Django 1.6 a la versión LTS más reciente.
    *   Actualizar todas las dependencias a versiones estables y seguras.
    *   Refactorizar el código para ajustarse a las prácticas modernas de Django.

*   **[UPCOMING] Contenerización:**
    *   Crear un `Dockerfile` para la aplicación Django/Gunicorn.
    *   Definir la infraestructura como código usando `docker-compose.yml` para el entorno de desarrollo local.

*   **[UPCOMING] Orquestación con Kubernetes:**
    *   Desarrollar manifiestos de Kubernetes (Deployments, Services, etc.) para cada componente (app, workers, base de datos, caché).
    *   Configurar un Ingress Controller para gestionar el tráfico externo.

*   **[UPCOMING] Integración y Despliegue Continuo (CI/CD):**
    *   Implementar un pipeline en GitHub Actions o similar.
    *   Automatizar la ejecución de tests, análisis estático de código, construcción de imágenes Docker y despliegue en un entorno de staging/producción.
