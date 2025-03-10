import psycopg2 as pg

DBNAME = 'vidavox_test'
USER = 'postgres'
PASS = 'postgres'
HOST = 'localhost'
PORT = '5432'
config = {
    'dbname': DBNAME,
    'user': USER,
    'password': PASS,
    'host': HOST,
    'port': PORT,
}

def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with pg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (pg.DatabaseError, Exception) as error:
        print(error)

def get_docid(filepath):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute( 'insert into documents (docpath) values (%s) returning id',(filepath,) )
        docid = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()
        
        return docid
    
    except (pg.DatabaseError, Exception) as error:
        raise error

def save_texts(docid: int, texts):
    conn = connect()
    cursor = conn.cursor()

    for row in texts:
        cursor.execute(
            'INSERT INTO extracted_texts (docid, pagenumber, ordernumber, textvalue) VALUES (%s, %s, %s, %s)',
            (docid, row['pagenumber'], row['ordernumber'], row['textvalue'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def save_entities(docid: int, entities):
    conn = connect()
    cursor = conn.cursor()

    for row in entities:
        cursor.execute(
            'insert into ner_data (entityname, entitylabel, docid, pagenumber, ordernumber, startposition, endposition) values (%s, %s, %s, %s, %s, %s, %s)',
            (row['entityname'], row['entitylabel'], docid, row['pagenumber'], row['ordernumber'], row['startposition'], row['endposition'])
        )

    conn.commit()
    cursor.close()
    conn.close()

def save_images(docid: int, images):
    conn = connect()
    cursor = conn.cursor()

    for row in images:
        cursor.execute(
            'INSERT INTO extracted_images (docid, pagenumber, image, imagepath, caption) VALUES (%s, %s, %s, %s, %s)',
            (docid, row['pagenumber'], row['image'], row['imagepath'], row['caption'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def save_charts(docid: int, charts):
    conn = connect()
    cursor = conn.cursor()

    for row in charts:
        cursor.execute(
            'INSERT INTO extracted_charts (docid, pagenumber, image, imagepath) VALUES (%s, %s, %s, %s)',
            (docid, row['pagenumber'], row['image'], row['imagepath'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def save_tables(docid: int, tables):
    conn = connect()
    cursor = conn.cursor()

    for row in tables:
        try:
            cursor.execute(
                'INSERT INTO extracted_tables_json (docid, pagenumber, tablejson) VALUES (%s, %s, %s) returning id',
                (docid, row['pagenumber'], row['tablejson'])
            )
            tableid = cursor.fetchone()[0]
        
        except Exception as e:
            raise e
        
        else:
            for i, tblrow in enumerate(row['tblraw']):
                for key, val in zip(tblrow.keys, tblrow.values):
                    cursor.execute(
                        'INSERT INTO extracted_tables_raw (docid, pagenumber, tableid, rownumber, columnname, value) VALUES (%s, %s, %s, %s, %s, %s)',
                        (docid, row['pagenumber'], tableid, i, key, val)
                    )
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    import sys
    sys.path.append(r'D:\Personal\vidavox_test_de\app')
    from extract import ocr
    from transform import text_processing as tp

    pdf_path = r'D:\Personal\vidavox_test_de\AR for improved learnability.pdf'
    texts, texts_str = ocr.extract_text_from_pdf(pdf_path)
    
    entities = tp.ner_analysis(texts)

    try:
        docid = get_docid(pdf_path)
    except Exception as e:
        raise e
    else:
        save_texts(docid, texts)
        save_entities(docid, entities)