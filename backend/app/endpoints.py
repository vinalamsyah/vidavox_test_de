from fastapi import FastAPI, HTTPException
from schema import DocumentsData, TextsData, EntitiesData
import psycopg2 as pg
# import numpy as np
from io import BytesIO

DBNAME = 'postgres'
USER = 'postgres'
PASS = 'P@ssw0rd'
HOST = 'host.docker.internal'
PORT = '65432'
config = {
    'dbname': DBNAME,
    'user': USER,
    'password': PASS,
    'host': HOST,
    'port': PORT,
}

def query_data(query: str, params: tuple = None):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with pg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                result = cursor.fetchall()
            conn.commit()
        return result

    except (pg.DatabaseError, Exception) as error:
        raise error

def where_builder(query: str, **kwargs) -> str:
    query += ' where'
    params = tuple()

    for key, val in kwargs.items():
        if val:
            query += ' and' if params else ''
            query += f' {key} = %s'
            params += (val,)
    return query, params


app = FastAPI()

@app.get("/documents/all")
async def get_documents() -> list[DocumentsData]:
    result = query_data('select id, docpath, uploaded_at from documents')
    if result:
        return [ {'id': row[0], 'docpath': row[1], 'uploaded_at': row[2]} for row in result ]
    
    raise HTTPException(status_code=404, detail="Documents not found.")

@app.get('/documents/{docid}/texts')
async def get_texts(docid: int, pagenumber: int = None, ordernumber: int = None) -> list[TextsData]:
    query_str = 'select id, pagenumber, ordernumber, textvalue, extracted_at from extracted_texts'
    query_str, params = where_builder(query_str, docid=docid, pagenumber=pagenumber, ordernumber=ordernumber)

    result = query_data(query_str, params)
    if result:
        return [ 
            {'id': row[0], 'docid': docid, 'pagenumber': row[1], 'ordernumber': row[2], 'textvalue': row[3], 'extracted_at': row[4]} 
            for row in result 
        ]
    
    raise HTTPException(status_code=404, detail="Document not found.")

@app.get('/documents/{docid}/named-entities')
async def get_entities(docid: int, pagenumber: int = None, ordernumber: int = None) -> list[EntitiesData]:
    query_str = 'select id, pagenumber, ordernumber, entityname, entitylabel, startposition, endposition, extracted_at from ner_data'
    query_str, params = where_builder(query_str, docid=docid, pagenumber=pagenumber, ordernumber=ordernumber)

    result = query_data(query_str, params)
    if result:
        return [ 
            {
                'id': row[0], 
                'docid': docid, 
                'pagenumber': row[1], 
                'ordernumber': row[2], 
                'entityname': row[3], 
                'entitylabel': row[4],
                'startposition': row[5],
                'endposition': row[6],
                'extracted_at': row[7]
            } 
            for row in result 
        ]
    
    raise HTTPException(status_code=404, detail="Document not found.")

@app.get('/documents/{docid}/images')
async def get_images(docid: int, pagenumber: int = None):
    query_str = 'select id, pagenumber, image, imagepath, caption, extracted_at from extracted_images'
    query_str, params = where_builder(query_str, docid=docid, pagenumber=pagenumber)

    result = query_data(query_str, params)
    # print(result)
    if result:
        return [ 
            {
                'id': row[0], 
                'docid': docid, 
                'pagenumber': row[1], 
                'image': BytesIO(row[2]), 
                'imagepath': row[3], 
                'caption': row[4],
                'extracted_at': row[5]
            } 
            for row in result 
        ]
    
    raise HTTPException(status_code=404, detail="Document not found.")

@app.get('/documents/{docid}/tables')
async def get_tables(docid: int, pagenumber: int = None):
    query_str = 'select id, pagenumber, tablejson, extracted_at from extracted_tables_json'
    query_str, params = where_builder(query_str, docid=docid, pagenumber=pagenumber)

    result = query_data(query_str, params)
    if result:
        return [ 
            {'id': row[0], 'docid': docid, 'pagenumber': row[1], 'tablejson': row[2], 'extracted_at': row[3]}
            for row in result
        ]
    
    raise HTTPException(status_code=404, detail="Document not found.")

@app.get('/named-entities')
async def get_all_entities() -> list[EntitiesData]:
    query_str = 'select id, docid, pagenumber, ordernumber, entityname, entitylabel, startposition, endposition, extracted_at from ner_data'

    result = query_data(query_str)
    if result:
        return [ 
            {
                'id': row[0], 
                'docid': row[1], 
                'pagenumber': row[2], 
                'ordernumber': row[3], 
                'entityname': row[4], 
                'entitylabel': row[5],
                'startposition': row[6],
                'endposition': row[7],
                'extracted_at': row[8]
            } 
            for row in result 
        ]
    
    raise HTTPException(status_code=404, detail="Document not found.")