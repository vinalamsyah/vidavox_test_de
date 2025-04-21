import os
from datetime import datetime
from io import BytesIO
from PIL import Image
import traceback

# SAVE_PATH = f'{os.getcwd()}\\tmp'
SAVE_PATH = f'/data/output'

def init_dir():
    entry = f'{SAVE_PATH}/{datetime.now().strftime('%Y%m%d%H%M%S%f')}'
    try:
        os.makedirs(f'{entry}/layouts')
        os.makedirs(f'{entry}/images')
    
    except FileExistsError:
        pass
    except Exception:
        raise

    return entry

def save_layouts(entry: str, layouts):
    print('saving layouts')
    for i, layout in enumerate(layouts):
        Image.fromarray(layout['full']).save(f'{entry}/layouts/{i+1}-0.png') # Save full layout

        for j, sgmt in enumerate(layout['segments']):
            Image.fromarray(sgmt).save(f'{entry}/layouts/{i+1}-{j+1}.png') # Save segments

def save_images(entry: str, clips):
    print('saving images')
    images_data = []
    k = 0
    img_binary = BytesIO()

    for pagenumber, clip in clips:
        for j, img in enumerate(clip):
            save_path = f'{entry}/images/{k+1}.png'
            try:
                Image.fromarray(img).save(save_path)
                Image.fromarray(img).save(img_binary, format='PNG')

            except Exception:
                save_path = traceback.format_exc()

            finally:
                images_data += [ 
                    { 'pagenumber': pagenumber, 'imagepath': save_path, 'image': img_binary.getvalue(), 'caption': None }
                ]
                k += 1

    return images_data