import streamlit as st
import requests
import time

PAGE_TITLE = "Live Demo: Multi-Modal Data From Scanned Documents"
BACKEND_URL = 'http://localhost:8080'


def paging_data(element):
    # _, df_docs = get_list_documents()
    documents = requests.get(f'{BACKEND_URL}/documents/all').json()
    documents = { doc['id']: doc['docpath'] for doc in documents }
    docid = st.selectbox(
        'Choose a document to show texts:',
        documents.keys(),
        format_func= lambda x: documents[x],
        index=None
    )

    result = None
    if docid:
        result = requests.get(f'{BACKEND_URL}/documents/{docid}/{element}').json()

        if result:
            pages = list(set([ row['pagenumber'] for row in result ])) + ['all']
            pagenumber = st.pills('Page', pages, default=pages[0])

            if pagenumber != 'all':
                result = requests.get(f'{BACKEND_URL}/documents/{docid}/{element}?pagenumber={pagenumber}').json()
            
            st.dataframe(result)

    return result

def typewriter(text):
    for word in text.split(' '):
        yield word + " "
        time.sleep(0.01)

def home_page():
    documents = requests.get(f'{BACKEND_URL}/documents/all').json()
    st.write('How To Use: ')
    st.write("""
    1. Pilih menu data yang ingin ditampilkan
    2. Pilih dokumen
    3. Bisa mem-filter halaman jika diinginkan
    4. Daftar dokumen yang bisa ditampilkan juga bisa dilihat di tabel berikut.
    """)
    if documents:
        st.dataframe(documents)

def texts_page():
    texts = paging_data('texts')
    if texts:
        for txt in texts:
            st.write_stream(typewriter(txt['textvalue']))


def images_page():
    images = paging_data('images')
    if images:
        for img in images:
            st.image(img['imagepath'])


def entities_page():
    entities = paging_data('named-entities')
    if entities:
        st.dataframe(entities)


def tables_page():
    tables = paging_data('tables')
    if tables:
        for i, tbl in enumerate(tables):
            st.write(f'Table {i+1}')
            st.dataframe(tbl['tablejson'])
            st.write('---')


def _tab_definition():
    st.set_page_config(page_title=PAGE_TITLE,initial_sidebar_state='expanded',layout='centered')

def _sidebar_definition():
    """
    Disini diisi content yang cuma ada di sidebar
    biasanya untuk config hyperparameter dan config config lainnya
    nanti hyper param ini dibungkus terus di return dalam satu paket
    """

    param = "INI PARAM DISINI MESTINYA"
    return param

def _wall_definition(param):
    """
    DISINI DIISI CONTENT YANG CUMA ADA DI WALL
    KALAU PERLU BIKIN FUNCTION LAGI TINGGAL BIKIN KAPAN AJA
    """
    st.title(PAGE_TITLE)

    if menu == 'Home':
        home_page()
    elif menu == 'Text':
        texts_page()
    elif menu == 'Image':
        images_page()
    elif menu == 'Entity':
        entities_page()
    elif menu == 'Table':
        tables_page()

    
if __name__ == "__main__":
    _tab_definition()
    menu = st.sidebar.selectbox('Menu',['Home','Text','Image','Entity', 'Table'])
    param = _sidebar_definition()
    _wall_definition(param)