# ETL Pipeline for Multi-Modal Data
---
### Pre-requisites
Before setting-up this project, please make sure that these following have to be installed already.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://github.com/oschwartz10612/poppler-windows)
---
### Setup
It is recommended to use virtual environment so that package requirements for this project doesn't interfere with your other projects.
1. Change your terminal directory to the project's folder
2. Install the required packages
`pip install -r requirements.txt`
4. to start the automated pipeline `python ./app/watcher.py`
6. to start the REST API by FastAPI
```
cd ./app/api
uvicorn endpoints:app --port 8080
```
6. to start Demo UI by Streamlit
`streamlit run ./app/ui/home.py`
