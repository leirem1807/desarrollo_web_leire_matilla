# Tarea 2 - Gestión de Adopción de Mascotas Leire Matilla 
## Descripción
Esta aplicación implementa un sistema de adopción de mascotas usando **Flask** y **MySQL**.  
Incluye:
- Portada con últimos 5 avisos.
- Agregar aviso con validaciones en cliente y servidor.
- Listado paginado de avisos (5 por página).
- Estadísticas con gráficos estáticos.

## Decisiones tomadas
- Se usó SQLAlchemy para mapear tablas a modelos Python.
- Las fotos se guardan en static/img/ y se registran en la tabla foto. Hay imágenes repetidas 
- El formulario mantiene validaciones de la Tarea 1 y agrega validación en servidor.
- ha sido creado a partir de la pagina web de la tarea 1
