from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import traceback

from extract import image_processing as ip, ocr
from transform import text_processing as tp
from load import local, postgresql_db as pg


def _text_pipeline(entry, docid, doc):
    layouts = [ ip.layouting(page_image) for page_image in doc ] # Layouting(Image) --> Layouts
    texts_data, texts_str = ocr.extract_text(layouts) # OCR (Layouts) --> textsdata
    entities_data = tp.ner_analysis(texts_data)

    pg.save_texts(docid, texts_data)
    pg.save_entities(docid, entities_data)
    local.save_layouts(entry, layouts) #Saving Layouts (Layouts)

def _image_pipeline(entry, docid, doc):
    clips = [ (i+1, ip.image_clipping(page_image)) for i, page_image in enumerate(doc) ] # Image Clipping (Image) --> Images
    images_data = local.save_images(entry, clips) # Saving Images (Images) --> Images Paths

    pg.save_images(docid, images_data)

def _table_pipeline(entry, docid, doc):
    tables_data = ocr.extract_table(doc)
    pg.save_tables(docid, tables_data)



def run_etl_pipeline(filepath_input: str, entry: str):
    status_code, message = (0, 'PIPELINE STARTED')

    doc = ip.pdf_to_image(filepath_input) # Read File Convert to Image
    docid = pg.get_docid(filepath_input)

    _text_pipeline(entry, docid, doc)

    _image_pipeline(entry, docid, doc)

    _table_pipeline(entry, docid, doc)
    
    status_code, message = (1, 'PIPELINE COMPLETED')
    return status_code, message


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

    def on_created(self, event):
        print("on_created", event.src_path)
        try:
            entry = local.init_dir()
        except Exception:
            print(print(traceback.format_exc()))
            print('Failed init entry, just try re-inserting the file')
        else:
            print("created entry #", entry[-20:])
            status_code, message = run_etl_pipeline(event.src_path, entry)
            print("status_code: ", status_code, " | message: ", message)

    def on_modified(self, event):
        print("on_modified", event.src_path)    
        try:
            entry = local.init_dir()
        except Exception:
            print(print(traceback.format_exc()))
            print('Failed init entry, just try re-inserting the file')
        else:
            print("created entry #", entry[-20:])
            status_code, message = run_etl_pipeline(event.src_path, entry)
            print("status_code: ", status_code, " | message: ", message)


if __name__ == '__main__':
    # Create observer and event handler
    observer = Observer()
    event_handler = MyHandler()

    # Set up observer to watch a specific directory
    directory_to_watch = f"{os.getcwd()}\\input"
    observer.schedule(event_handler, directory_to_watch)

    # Start the observer
    observer.start()

    # Keep the script running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()