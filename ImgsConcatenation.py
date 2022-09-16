/*
Scritpt che crea una griglia (collage) di immagini
*/

import shutil
import os

os.mkdir('PROVA')
dst = './PROVA'
path = '../input/glomertopi/trainTiles/6533668'
dim_test = 16

i = 0
for _, _, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith('.jpg') and i < dim_test:
            shutil.copyfile(os.path.join(path, filename), os.path.join(dst, filename))
            i += 1

###############################################
# https://gist.github.com/njanakiev/1932e0a450df6d121c05069d5f7d7d6f
import os
from PIL import Image, ImageOps
import math

def is_square(apositivenum):
    # Controlla che il numero di immagini nella cartella di input
    # siano un quadrato perfetto
    
    x = apositivenum // 2
    seen = set([x])
    while x * x != apositivenum:
        x = (x + (apositivenum // x)) // 2
        if x in seen:
            print('ATTENZIONE: Numero di righe della griglia diverso dal numero di colonne')
            break
        seen.add(x)


def check_dims(folder):
    # Controlla che le immagini nella cartella di input
    # abbiano tutte la stessa dimensione
    
    for _, _, filenames in os.walk(folder):
        for i in range(len(filenames)-1):
            if Image.open(os.path.join(path, filenames[i])).size != \
               Image.open(os.path.join(path, filenames[i+1])).size:
                print(f'ATTENZIONE: l\'immagine {filenames[i+1]} ha dimensioni diverse rispetto alle altre')
                print('Controllare che tutte le immagini abbiano la stessa dimensione')

def sort_imgs_list(paths_to_imgs):
    # Effettua l'ordinamento (riga-colonna) delle immagini della cartella 
    # Esempio: [1x1, 1x2, 1x3, ..., 2x1, 2x2, 2x3, ....]
    # Si devono fornire in input tutte le tile relative al glomerulo selezionato
    
    foo_imgs_paths = [Path(e).stem for e in paths_to_imgs]
    numbers = [str(i) for i in range(10)] + list('x')
    foo_imgs_paths = [re.sub(r'^.*?_', '', c) for c in foo_imgs_paths]     
    foo_imgs_paths = [    
        "".join(char for char in img_path if char in numbers)
        for img_path in foo_imgs_paths
    ]
    foo_imgs_paths = sorted(foo_imgs_paths, key=lambda item: [int(part) for part in item.split('x')])
    foo_imgs_paths = ['../input/glomertopi/trainTiles/6533668/56_tile' +
                      elem for elem in foo_imgs_paths]
    foo_imgs_paths = [elem + '.jpg' for elem in foo_imgs_paths]
    sorted_imgs_paths = foo_imgs_paths
    return sorted_imgs_paths

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
    imgs_paths = sort_imgs_list(imgs_paths)
    
    if imgs_resize:
        imgs_shapes =  Image.open(imgs_paths[0]).resize((imgs_resize, imgs_resize)).size
    else:
        imgs_shapes = Image.open(imgs_paths[0]).size
        
    canvas_shape = math.sqrt(len(imgs_paths))
    canvas_shape = (canvas_shape, canvas_shape)
    
    # Sanity check delle immgini
    is_square(canvas_shape[0])    
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

concat_images('./PROVA', './')
Image.open('./canvas.jpg')
