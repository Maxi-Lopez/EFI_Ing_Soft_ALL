REQUISITOS:
Si bien pueden elegir entre una variedad de temáticas, cada sistema debe estar creado desde cero e incluir los siguientes requisitos:

Bases de datos:
Al menos 10 modelos en la base de datos.
Los modelos deben ser relevantes para la temática elegida.
Deben existir relaciones entre los modelos.
Planificación de las tablas y relaciones antes de desarrollar la misma, ya sea a través de un diagrama o escrito. Dicha planificación se debe adjuntar al README.md.
API:
El proyecto de django debe habilitar una API REST para comunicarse con un proyecto de frontend.
Al menos 8 de los 10 modelos deben habilitar un endpoint a través un Viewset, ya sea para habilitar un CRUD o sólo de lectura.
Como mínimo 2 de los Viewsets para CRUD deben mostrar datos anidados sólo si se consulta un list (get all), usando NestedSerializers.
Los endpoints deben estar protegidos según corresponda con autenticación de Sesión y por Tokens.
Deben existir por lo menos 2 funciones personalizadas en los viewset que usen el decorador @action.
Los endpoints de get all deben traer datos paginados.
Por lo menos 1 viewset debe permitir filtros y búsquedas.
Además, se deben servir endpoints de documentación de API (openapi, swagger y/o redoc), además de habilitar la api navegable.
Vistas:
Debe existir una vista principal que renderice un template y que sirva de bienvenida. No es necesario que se habilite crud a través de formularios.
Se debe permitir control total con el panel de administración. Modelos relevantes deben permitir filtros, ordenamiento y búsqueda desde el panel.
Otros requisitos:
Se debe usar uv como gestor de entornos virtuales.
Se deberá configurar CORS para permitir la conexión hacia un frontend.
El proyecto de Django debe estar dockerizado.
Se debe evidenciar un buen trabajo organizacional con Git (ramas, pull requests, commits descriptivos, etc.)




Entrega:
La entrega debe ser a través de un repositorio de Github (donde la última versión sea en la rama main/master).
El repositorio de Github debe tener un README.md trabajado con capturas del proyecto en funcionamiento.
