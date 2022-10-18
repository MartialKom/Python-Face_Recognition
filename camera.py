import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

from imutils.convenience import resize
from fonction import recognise_face, encode_face
import ntpath
import PIL.Image
from pathlib import Path
import argparse
import os
from tkinter.messagebox import showerror, showinfo
import numpy as np


parser = argparse.ArgumentParser(description='Call APP Students Recognise')
parser.add_argument('-i','--input', type=str, required=True, help='Repertoire des images/photos')
args= vars (parser.parse_args())

args = parser.parse_args()

face_to_encode_path = Path(args.input)
files = [file_ for file_ in face_to_encode_path.rglob('*.jpeg')]

for file_ in face_to_encode_path.rglob('*.png'):
    files.append(file_)
if len(files)==0:
    raise ValueError('No faces detect in the directory: {}'.format(face_to_encode_path))
known_face_names = [os.path.splitext(ntpath.basename(file_))[0] for file_ in files]


known_face_encodings = []
for file_ in files:
    image = PIL.Image.open(file_)
    image = np.array(image)
    face_encoded = encode_face(image)[0][0]
    known_face_encodings.append(face_encoded)
  
class App:
    def __init__(self, window, window_title, video_source):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
 
         # source vidéo ouverte (par défaut, cela essaiera d'ouvrir la webcam de l'ordinateur)
        self.vid = MyVideoCapture(self.video_source)
 
         # Créez un canevas pouvant s'adapter à la taille de la source vidéo ci-dessus
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
 
         # Bouton qui permet à l'utilisateur de prendre une photo
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
 
         # Après avoir été appelée une fois, la méthode de mise à jour sera automatiquement appelée toutes les millisecondes de retard
        self.delay = 15
        self.update()
 
        self.window.mainloop()
 
    def snapshot(self):
        # Obtenir une image de la source vidéo
        ret, frame = self.vid.get_frame()
 
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
    def update(self):
        try:
            # Obtenir une image de la source vidéo
            ret, frame = self.vid.get_frame()
 
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
            self.window.after(self.delay, self.update)
        except TypeError :
            self.window.destroy()
            showinfo(title="video", message="Video terminee")
 
 
class MyVideoCapture:
    def __init__(self, video_source):
        # Ouvrir la source vidéo
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        # Obtenir la largeur et la hauteur de la source vidéo
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
        try:
            if self.vid.isOpened():
                ret, frame = self.vid.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                recognise_face(frame, small_frame, known_face_encodings, known_face_names)
                if ret:
                    # Renvoie un indicateur de réussite booléen et la trame actuelle convertie en RVB
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (None)
        except (Exception, cv2.error) as error:
            pass
 
    # Relâchez la source vidéo lorsque l'objet est détruit
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        cv2.destroyAllWindows()
 
# Créer une fenêtre et la passer à l'objet Application ,"/home/shisui/Bureau/@filmsseriesshoww Ip Man Kung Fu Master FRENCH 2021.avi"
# App(tkinter.Tk(), "Call App Student Face Recognise")

