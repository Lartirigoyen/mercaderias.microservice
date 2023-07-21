import cx_Oracle
import os

"""
Environments: standby, production, testing
Produccion (cuando se hace el deploy a AWS) se usan las bases de datos standby o production
Desarrollo (entorno local dentro de la vpn siempre es testing)
Por defecto siempre se usa testing para desarrollar

Para conectar a las dbs se usan las credenciales otorgadas a cada desarrollador, se reemplazan las variables de entorno en el SO con los datos
correspondientes.. siempre cuando se hace un deploy se ignora ese archivo y en GitHub se toman los secrets para usar el entorno 
productivo

"""

async def softcereal_connection(environment=os.environ['DB_ENVIRONMENT'], username=os.environ['DB_USERNAME'], password=os.environ['DB_PASSWORD'], port='1521', service_name='BASE' ):
  try:
    if environment == 'testing':
      host='192.168.199.180'
    elif environment == 'standby':
      host='192.168.199.199'
      service_name='STBY'
    elif environment == 'replica_aws':
      host='172.19.1.208'
      service_name='STBY'
    else:
      host='192.168.199.201'
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn, encoding="UTF-8")
    return connection
  except Exception as e:
    print('Error ', e)