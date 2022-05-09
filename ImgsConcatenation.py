import os
from PIL import Image, ImageOps
import math

def check_is_quadratic(input_list):
    # Controlla che il numero di immagini nella cartella di input
    # siano un quadrato perfetto
    
        if not math.sqrt(len(input_list)).is_integer(): 
            print('ATTENZIONE: Numero di righe della griglia diverso dal numero di colonne')


def check_dims(folder):
    # Controlla che le immagini nella cartella di input
    # abbiano tutte la stessa dimensione
    
    for _, _, filenames in os.walk(folder):
        for i in range(len(filenames)-1):
            if Image.open(os.path.join(path, filenames[i])).size != \
               Image.open(os.path.join(path, filenames[i+1])).size:
                print(f'ATTENZIONE: l\'immagine {filenames[i+1]} ha dimensioni diverse rispetto alle altre')
                print('Controllare che tutte le immagini abbiano la stessa dimensione')


def concat_images(input_folder, output_folder, imgs_resize=None):
    """
    Crea una griglia di immagini
    
    La griglia viene popolata da sinistra verso destra, e dall'alto vero il basso
    con le immagini presenti nella cartella di input
    
    Parametri
    ---------
    input_folder : str
        La cartella contenente le immagini con cui formare la griglia
    output_folder : str
        La cartella dove viene salvata l'immagine completa della griglia
    imgs_resize : int, optional
        Dimensione a cui ridimensionare le immagini che comporranno la griglia (di default a None)
    
    """
    
    imgs_paths = [os.path.join(input_folder, f) 
                   for f in os.listdir(input_folder) if f.endswith('.jpg')]
    
    if imgs_resize:
        imgs_shapes =  Image.open(imgs_paths[0]).resize((imgs_resize, imgs_resize)).size
    else:
        imgs_shapes = Image.open(imgs_paths[0]).size
        
    canvas_shape = math.sqrt(len(imgs_paths))
    canvas_shape = (canvas_shape, canvas_shape)
    
    # Sanity check delle immgini
    check_is_quadratic(imgs_paths)    
    check_dims(input_folder)
    
    # Creazione griglia
    width, height = imgs_shapes
    images = map(Image.open, imgs_paths)
    images = [ImageOps.fit(image, imgs_shapes, Image.LANCZOS) 
              for image in images]
    
    image_size = (width * canvas_shape[1], height * canvas_shape[0])
    foo_dim = int(image_size[0])
    image = Image.new('RGB', (foo_dim, foo_dim))
    
    for row in range(int(canvas_shape[0])):
        for col in range(int(canvas_shape[1])):
            offset = width * col, height * row
            idx = int(row * canvas_shape[1] + col)
            image.paste(images[idx], offset)
            
    # Salvataggio griglia
    image.save(os.path.join(output_folder, 'canvas.jpg'), 'JPEG')

concat_images('./CustomInput', './')

# Visualizza la griglia di immagini
#Image.open('./canvas.jpg')


# In caso si volesse eseguire il codice direttamente da linea di comando
# Esempio: concat_images.py [-h] \InputDirPath \OutputDirPath --resize 128
import argparse

parser = argparse.ArgumentParser(description='Crea una griglia di immagini')

parser.add_argument('input_dir', type=str,
                   help='La directory contenente le immagini con cui creare la griglia')
parser.add_argument('output_dir', type=str,
                   help='La directory dove verrà salvata l\'immagine della griglia')
parser.add_argument('--resize', type=int, required=False,
                   help='La dimensione a cui ridimensionare le immagini, opzionale')

args = parser.parse_args()

concat_images(args.input_dir, args.output_dir)
