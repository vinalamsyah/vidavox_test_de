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
        cursor.execute( 'insert into documents (docpath) values (%s) returning id',(filepath) )
        docid = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        
        return docid
    
    except (pg.DatabaseError, Exception) as error:
        print(error)

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

def save_images(docid: int, images):
    conn = connect()
    cursor = conn.cursor()

    for row in images:
        cursor.execute(
            'INSERT INTO extracted_images (docpath, image, imagepath) VALUES (%s, %s, %s)',
            (docid, row['docpath'], row['image'], row['imagepath'])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def save_entities(docid: int, entities):
    conn = connect()
    cursor = conn.cursor()