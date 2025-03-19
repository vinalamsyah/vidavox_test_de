import streamlit as st 
import asyncio
import copy
import json
import pandas as pd
import requests
import time

PAGE_TITLE = "Live Demo: Multi-Modal Data From Scanned Documents"

# from modules.downloadfunc import download_file,download_button
# from modules.formatting import formatting_data,plotting_data
# from job.routing import routing
# from config.conf import *    
# from objects.objects import map_visualizer,data_visualization

def get_list_documents():
    documents = requests.get('http://localhost:8080/documents/all').json()
    df_docs = pd.DataFrame(documents)
    return documents, df_docs

def paging_data(element):
    _, df_docs = get_list_documents()
    docid = st.selectbox(
        'Choose a document to show texts:',
        list(df_docs['id']),
        format_func= lambda x: df_docs.loc[df_docs['id'] == x, 'docpath'].values[0],
        index=None
    )

    result = None
    if docid:
        result = requests.get(f'http://localhost:8080/documents/{docid}/{element}').json()

        if result:
            list_pages = list(set([ row['pagenumber'] for row in result ])) + ['all']
            pagenumber = st.pills('Page', list_pages, default=list_pages[0])

            if pagenumber != 'all':
                result = requests.get(f'http://localhost:8080/documents/{docid}/{element}?pagenumber={pagenumber}').json()
            
            st.dataframe(result)

    return result

def typewriter(text):
    for word in text.split(' '):
        yield word + " "
        time.sleep(0.01)

def home_page():
    documents, _ = get_list_documents()
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
    st.sidebar.write('Welcome to', PAGE_TITLE)
    if menu == 'Routing Optimizer [JSON]':
        # download_file(r'repository\data_exp\test.json','Sample.json',True)
        st.write('huhuhu')

    if menu == 'Routing Optimizer [xlsx]':
        # download_file(r'repository\data_exp\Excel\delivery.xlsx','Delivery.xlsx',True)
        # download_file(r'repository\data_exp\Excel\vehicle.xlsx','Vehicle.xlsx',True)
        # download_file(r'repository\data_exp\Excel\depot.xlsx','Depot.xlsx',True)
        st.write('hohoho')

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