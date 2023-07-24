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

@router.get("/get_contrato", status_code=200, tags=["Contrato"], name="Contrato", summary="Obtiene todos los contratos de un Productor en una cosecha especifica")
async def get_contrato(cuit_productor: str, consecha: int):
  connection = await softcereal_connection()
  cursor = connection.cursor()
  query = f"""
    SELECT
      *
    FROM
      (
      /* Consulta sobre confirmaciones de venta*/
      SELECT
        CNV_COSECHA AS campaniaPPal,
        CNV_KILOS / 1000 AS cantidadPactada,
        ESP_CODIGO_SAGPYA AS codGrano,
        CNV_TIPO_CONFIRMACION AS contratoTipo,
        NULL AS cuitCorredor,
        NULL AS cuitCorredorVentaPrimaria,
        NULL AS cuitCorredorVentaSecundaria,
        NULL AS cuitDestinatario,
        '30-61398599-5' AS cuitDestino,
        NULL AS cuitEntregador,
        NULL AS CuitMercadoTermino,
        DEST.ENT_CUIT AS cuitProveedor,
        NULL AS cuitRecibidor,
        NULL AS cuitRemitenteComercialVentaPri,
        NULL AS cuitRemitenteComercialVentaSec,
        NULL AS cuitRemitenteComercialVentaSc2,
        CONFIRMACIONES_VENTAS_TIPOS.COT_DESCRIPCION AS descripcion,
        CNV_FECHA_ENTREGA_HASTA AS fechaMaximaEntrega,
        CNV_FECHA_ENTREGA_DESDE AS fechaMinimaEntrega,
        CNV_FECHA_VENTA AS fechaOperacion,
        CNV_MONEDA AS moneda,
        to_char (CNV_NUMERO) AS NumeroContrato,
        NULL AS numeroContratoCorredor,
        DECODE (CNV_PRECIO_QQ,
        NULL,
        'A FIJAR',
        CNV_PRECIO_QQ) AS precio,
        CNV_PORCENTAJE_LIQUIDACION AS porcentajeParcial,
        1 AS ProduccionPrimaria,
        'TT' AS unidad
      FROM
        CONFIRMACIONES_VENTAS,
        ENTIDADES DEST,
        ESPECIES,
        CONFIRMACIONES_VENTAS_TIPOS
      WHERE
        CNV_PRODUCTOR = DEST.ENT_CODIGO
        AND CNV_ESPECIE = ESP_ESPECIE
        AND CNV_TIPO_CONFIRMACION =
                  CONFIRMACIONES_vENTAS_TIPOS.COT_TIPO_CONFIRMACION
        AND CNV_INDICADOR = 1
        AND CNV_COSECHA >= {consecha}
    UNION 
      /* Consulta sobre contratos*/
      SELECT
        CNT_COSECHA AS campaniaPPal,
        CNT_KILOS_PROMEDIO / 1000 AS cantidadPactada,
        ESP_CODIGO_SAGPYA AS codGrano,
        CNT_TIPO_NEGOCIO AS contratoTipo,
        COR.ENT_CUIT AS cuitCorredor,
        NULL AS cuitCorredorVentaPrimaria,
        NULL AS cuitCorredorVentaSecundaria,
        DESTI.ENT_CUIT AS cuitDestinatario,
        '30-61398599-5' AS cuitDestino,
        ENTREG.ENT_cUIT AS cuitEntregador,
        NULL AS CuitMercadoTermino,
        DEST.ENT_CUIT AS cuitProveedor,
        NULL AS cuitRecibidor,
        CNT_CUENTA_ORDEN1 AS cuitRemitenteComercialVentaPri,
        CNT_CUENTA_ORDEN2 AS cuitRemitenteComercialVentaSec,
        NULL AS cuitRemitenteComercialVentaSc2,
        TIPOS_NEGOCIO.TNE_DESCRIPCION AS descripcion,
        CNT_FECHA_HASTA_ENTREGAS AS fechaMaximaEntrega,
        CNT_FECHA_DESDE_ENTREGAS AS fechaMinimaEntrega,
        CNT_FECHA AS fechaOperacion,
        CNT_MONEDA AS moneda,
        CNT_NUMERO AS NumerContrato,
        CNT_CONTRATO_CORREDOR AS numeroContratoCorredor,
        DECODE(CNT_PRECIO_TT, NULL, 'A FIJAR', CNT_PRECIO_TT) AS precio,
        CNT_PORCENTAJE_FACTURA AS porcentajeParcial,
        2 AS ProduccionPrimaria,
        'TT' AS unidad
      FROM
        CONTRATOS,
        ENTIDADES DEST,
        ENTIDADES DESTI,
        ENTIDADES COR,
        ENTIDADES ENTREG,
        ESPECIES,
        TIPOS_NEGOCIO
      WHERE
        CNT_CORREDOR = COR.ENT_CODIGO(+)
        AND CNT_ENTREGADOR = ENTREG.ENT_CODIGO(+)
        AND CNT_VENDEDOR = DEST.ENT_CODIGO(+)
        AND CNT_CUENTA_ORDEN3 = DESTI.ENT_cODIGO(+)
        AND CNT_ESPECIE = ESP_ESPECIE
        AND CNT_TIPO_NEGOCIO = TIPOS_NEGOCIO.TNE_CODIGO
        AND CNT_TIPO_CONTRATO = 'C'
        AND CNT_COSECHA >= {consecha}
    )
    WHERE 
      campaniappal = '{consecha}'
      AND 
        cuitproveedor = '{cuit_productor}'
  """

  contratos = []
  try: 
    records = cursor.execute(query).fetchall()
    nombres_columnas = [desc[0] for desc in cursor.description]
    contratos = [dict(zip(nombres_columnas, record)) for record in records]
    cursor.close()
    connection.close()
  except Exception as e:
    print('Error ', e)
  return {
    "contratos" : contratos
  }

@router.get("/get_partidas_senasa", status_code=200, tags=["Senasa"], name="Senasa", summary="Obtiene todas las ultimas partidas existentes en Senasa por deposito")
async def get_depositos_senasa(senasa_cod_deposito: int):
  senasa_data = []
  try:
    headers = {'Content-Type': 'text/html'}
    params = {"authUser": usr_senasa, "authPass": pass_senasa,"userTaxId": tax_id_senasa,"depositId":f"{senasa_cod_deposito}"}
    url = "https://aps2.senasa.gov.ar/agrotraza/src/api/Consulta_Stock_Producto_Formulado"
    data = requests.get(url, headers=headers, params=params)
    senasa_data = json.loads(data.content)  
  except Exception as e:
    print('Error ', e)
  return {
    "partidas" : senasa_data
  }
  
