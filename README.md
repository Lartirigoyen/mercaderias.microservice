# microservice.base
Estructura base para la generacion de proyectos SoftCereal - Oracle 11g - [Docker](https://www.docker.com/) - [FastAPI](https://fastapi.tiangolo.com/) - Python 3.9 Stable

# Conexión a base de datos
Para realizar la conexión a cualquiera de los environments hay que completar en el archivo .env en la raiz del directorio, usuario y pass a db 

Environments: standby, production, testing

Producción (cuando se hace el deploy a AWS) se usan las bases de datos standby o production
Desarrollo (entorno local dentro de la vpn siempre es testing)
Por defecto siempre se usa testing para desarrollar

Para conectar a las dbs se usan las credenciales otorgadas a cada desarrollador, se reemplazan las variables de entorno con los datos
correspondientes.. siempre cuando se hace un deploy se ignora ese archivo y en GitHub se toman los secrets para usar el entorno 
productivo.

# Requisitos para desarrollo
1. Usuario GitHub, Active Directory, AWS y SoftCereal DB
2. Instalar Docker (Docker Desktop si el SO es Windows)
3. Descargar imagen base de Oracle 11g almacenada en AWS ECR
4. Clonar el repositorio
5. Conexion a VPN

# Instrucciones para montar entorno de desarrollo local
1. Dirigirse a la carpeta clonada desde github por terminal
2. Buildear la imagen:
  - `docker build -t nombreImagen:version .`
3. Montar la imagen en un contenedor y pasarle las variables de entorno correspondientes así como también otras configuraciones como     puerto, imagen base, volumenes, etc
  - `docker run -d --name nombreContainer.microservice -p puertoTuPC:80 -e DB_USERNAME=usuariodb -e DB_PASSWORD=passworddb -v /ruta/completa/al/repo/nombreContainer.microservice/app:/app nombreImagenBase:version`

# Información de la aplicación
Dentro de la carpeta `app` del proyecto, existe un fichero .env que contiene la información base de la aplicación, como el título, descriptión, prefijo base en el path, etc.
El archivo debería configurarse para cada app que se cree, dependiendo para que se requiera.

# Utilizando dependencias
Para manejar las dependencias en el proyecto (que despues se instalen en el pase a producción en el deploy) se usa [Poetry](https://python-poetry.org/) pero también se puede poner los requerimientos en el archivo `requirements.txt` (posteriormente hay que buildear la imágen nuevamente, con Poetry deberíamos poder saltear ese paso)