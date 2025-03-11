import streamlit as st 
import asyncio
import copy
import json
import pandas as pd
import requests
import time

PAGE_TITLE = "Live Demo: Multi-Modal Data From Scanned Documents"
PAGE_ICON_TAB = r"repository\image\agit.png"

# from modules.downloadfunc import download_file,download_button
# from modules.formatting import formatting_data,plotting_data
# from job.routing import routing
# from config.conf import *    
# from objects.objects import map_visualizer,data_visualization

documents = requests.get('http://localhost:8080/documents/all').json()
df_docs = pd.DataFrame(documents)

def typewriter(text):
    for word in text.split(' '):
        yield word + " "
        time.sleep(0.01)

def home_page():
    st.write('How To Use: ')
    st.write("""
    1. Pilih menu data yang ingin ditampilkan
    2. Pilih dokumen
    3. Bisa mem-filter halaman jika diinginkan
    4. Daftar dokumen yang bisa ditampilkan juga bisa dilihat di tabel berikut.
    """)
    st.dataframe(documents)

def texts_page():
    #VARIABLE INITIALIZATION
    # file = st.file_uploader('Input the data')

    docid = st.selectbox(
        'Choose a document to show texts:',
        list(df_docs['id']),
        format_func= lambda x: df_docs.loc[df_docs['id'] == x, 'docpath'].values[0]
    )
    
    texts = requests.get(f'http://localhost:8080/documents/{docid}/texts').json()
    df_texts = pd.DataFrame(texts)
    
    pagenumber = st.pills('Page', df_texts['pagenumber'].sort_values(inplace=False).unique())
    
    if pagenumber:
        texts = requests.get(f'http://localhost:8080/documents/{docid}/texts?pagenumber={pagenumber}').json()
    st.dataframe(texts)

    for txt in texts:
        st.write_stream(typewriter(txt['textvalue']))


def images_page():
    docid = st.selectbox(
        'Choose a document to show texts:',
        list(df_docs['id']),
        format_func= lambda x: df_docs.loc[df_docs['id'] == x, 'docpath'].values[0]
    )

    images = requests.get(f'http://localhost:8080/documents/{docid}/images').json()
    df_images = pd.DataFrame(images)

    pagenumber = st.pills('Page', df_images['pagenumber'].sort_values(inplace=False).unique())

    if pagenumber:
        images = requests.get(f'http://localhost:8080/documents/{docid}/images?pagenumber={pagenumber}').json()
    st.dataframe(images)

    for path in df_images['imagepath']:
        st.image(path)

def entities_page():
    docid = st.selectbox(
        'Choose a document to show texts:',
        list(df_docs['id']),
        format_func= lambda x: df_docs.loc[df_docs['id'] == x, 'docpath'].values[0]
    )
    
    entities = requests.get(f'http://localhost:8080/documents/{docid}/named-entities').json()
    df_entities = pd.DataFrame(entities)

    pagenumber = st.pills('Page', df_entities['pagenumber'].sort_values(inplace=False).unique())
    
    if pagenumber:
        entities = requests.get(f'http://localhost:8080/documents/{docid}/named-entities?pagenumber={pagenumber}').json()
    st.dataframe(entities)

def _tab_definition():
    st.set_page_config(page_title=PAGE_TITLE,page_icon=PAGE_ICON_TAB,initial_sidebar_state='expanded',layout='centered')

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

    
if __name__ == "__main__":
    _tab_definition()
    menu = st.sidebar.selectbox('Menu',['Home','Text','Image','Entity'])
    param = _sidebar_definition()
    _wall_definition(param)