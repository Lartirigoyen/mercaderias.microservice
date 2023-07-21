from fastapi import APIRouter
from dotenv import dotenv_values
from dependencies import softcereal_connection
import requests
import json

config = dotenv_values(".env")

usr_senasa = "LycsaAgro"
pass_senasa = "LycsaAgro"
tax_id_senasa = "30-61398599-5"

router = APIRouter(
  prefix=f"{config['APP_PREFIX_BASE']}/{config['APP_VERSION']}", 
  #tags=["Endpoints disponibles"]
)

@router.get("/", tags=["Root"])
async def index():
  return {"msg": f"Hello {config['APP_TITLE']}"}

@router.get("/get_partidas_senasa", status_code=200, tags=["Senasa"], name="Senasa", summary="Obtiene todas las ultimas partidas existentes en Senasa por deposito")
async def example(senasa_cod_deposito: int):
  """   connection = await softcereal_connection()
  cursor = connection.cursor()
  query = ''
  res = None """

  senasa_data = []
  try:
    headers = {'Content-Type': 'text/html'}
    params = {"authUser": usr_senasa, "authPass": pass_senasa,"userTaxId": tax_id_senasa,"depositId":f"{senasa_cod_deposito}"}
    url = "https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Stock_Producto_Formulado"
    data = requests.get(url, headers=headers, params=params)
    senasa_data = json.loads(data.content)  
    """     records = cursor.execute(query).fetchall()
    nombres_columnas = [desc[0] for desc in cursor.description]
    data = [dict(zip(nombres_columnas, record)) for record in records]
    cursor.close()
    connection.close() """
  except Exception as e:
    print('Error ', e)
  return {
    "partidas" : senasa_data
  }
  
