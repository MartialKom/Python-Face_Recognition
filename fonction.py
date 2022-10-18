
from tkinter.messagebox import showerror
import dlib
import cv2
import numpy as np
from tkinter import filedialog as fd
from imutils import face_utils, video
from fonction_BD import getNom
import os


pose_predictor_68_point = dlib.shape_predictor("fichier_pre-entrainner/shape_predictor_68_face_landmarks.dat")
face_encoder = dlib.face_recognition_model_v1("fichier_pre-entrainner/dlib_face_recognition_resnet_model_v1.dat")
face_detector = dlib.get_frontal_face_detector()

def transform(image, face_locations):
    coord_faces = []
    for face in face_locations:
        rect = face.top(), face.right(), face.bottom(), face.left()
        coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
        coord_faces.append(coord_face)
    return coord_faces


def encode_face(image):
    face_locations = face_detector(image, 1)
    face_encodings_list = []
    landmarks_list = []
    for face_location in face_locations:
        #localisation du visage
        shape = pose_predictor_68_point(image, face_location)
        face_encodings_list.append(np.array(face_encoder.compute_face_descriptor(image, shape, num_jitters=1)))
        # recuperer la position des points
        shape = face_utils.shape_to_np(shape)
        landmarks_list.append(shape)
    face_locations = transform(image, face_locations)
    return face_encodings_list, face_locations, landmarks_list


def recognise_face(frame, small_frame, known_face_encodings, known_face_names):
    rgb_small_frame = small_frame[:, :, ::-1]
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    face_names = []
    process_this_frame = True
    
    if process_this_frame:
        for face_encoding in face_encodings_list:
            if len(face_encoding) == 0:
                return np.empty((0))
        
            #calculer la norme de tout les visages connus(phase reconnaissance)
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            tolerance = 1
            result = []
            for vector in vectors:
                if vector <= tolerance:
                    result.append(True)
                else:
                    result.append(False)
            if True in result:
                first_match_index = result.index(True)
                matricule = known_face_names[first_match_index]
                #name = getNom(matricule)
                #writeName(name)
                face_names.append(matricule)
            
            else:
                name = "Inconnu"
                face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations_list, face_names):

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
        cv2.rectangle(frame, (left, bottom + 30), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left - 2, bottom + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    process_this_frame = not process_this_frame
                
    # for shape in landmarks_list:
    #     for (x, y) in shape:
    #        cv2.circle(frame, (x, y), 1, (200, 229, 100), -1)
     
     
# Cette fonction verifie si un nom est present ou non dans la liste
def getLine(line, name):
    if line.rstrip() != name.rstrip():
        return False
    else:
        return True

#sauvegarde un fichier
def savefile(chemin):
    global files2
    try:
        files3 = [('Text Files', '*.txt')]
        files3 = fd.asksaveasfile( initialdir="/home/" ,filetypes= files3, defaultextension=files3, initialfile="presence.txt")
        files2 = os.fspath(files3.name)
        files2
        chemin.configure(text=files2)
    
    except PermissionError:
        showerror(title="Permissions", message="Vous n'avez pas le droit de sauvegarde a cet emplacement")
    
    except AttributeError:
        pass
def writeName(name):
    
    try:
       files2
       if os.path.isfile(files2):
            with open(files2, 'r+') as file:
                file.write('Liste de presence des etudiants\n')
                file.seek(0, os.SEEK_SET)
                line = file.readline()
                line = line.strip()
                while line:
                    # print("line : "+line.strip()+"\n")
                    # print("name : "+name.strip())
                    exist = getLine(line, name.strip())
                    if exist:
                        break
                    #exist = False;
                    line = file.readline()
    
                #print(exist)
            if exist:
                print("le nom {} existe deja".format(name.rstrip()))
            else:
                with open(files2, 'a') as file:
                    file.write(name.rstrip()+'\n')
                    file.seek(0, os.SEEK_SET)
                    print("successful")               

    except NameError:
        showerror(title="echec d'enregistrement", 
                  message="les noms ne peuvent pas etre enregistrer car aucun fichier n'a ete specifie")
        pass
    
    except IOError as erreur:
        print(erreur)
        exit(1)