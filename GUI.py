# coding=utf-8

from tkinter import *
import tkinter as tk
import sys
import os
from pathlib import Path
from fonction import recognise_face, cv2, savefile
from simple_facerec import SimpleFacerec
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from tkinter import ttk
from camera import *
import subprocess

def value(t):
    x=t.get('1.0','end-1c')
    try:
        x
        return x
    except ValueError:
        showerror(title="Erreur Fatale", message="entrer la source")  
 
    


    

def lancer_camera():
    video_capture = cv2.VideoCapture(s)

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        recognise_face(frame, small_frame, known_face_encodings, known_face_names)
        cv2.imshow('Reconnaissance faciale', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    release = video_capture.release()
    try:
        release
        cv2.destroyAllWindows()
    except ValueError:
        showerror(title="Fatal Error", message="entrer le numero de la camera source")
        
def SubmitCamera():
    global s
    try:
        value(t1)
        s = int(value(t1))
        top4.destroy()
        lancer_camera()
       
        
    #capture l'exception lever au cas ou la source de la camera n'est pas definie
    except ValueError:
        showerror(title="Erreur fatal", message="entrer le numero de la camera source")

def select_file():
    global file_to_print

    file_to_print = fd.askopenfilename(
      initialdir="/home/", title="Select file", 
      filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    fichier.configure(text=file_to_print)


        
    
# **************************Creation de la fenetre principale**************************
root = Tk()
root.resizable(False, False)
root.geometry("610x400")
root.title("Fiche de presence")
root.minsize(400,400)
#root.iconbitmap("RFC1.ico")


#**************************Lorsqu'on clique sur login**************************
def command1(event):
    if entry1.get() == 'admin' and entry2.get() == 'password' or entry1.get() == 'test' and entry2.get() == 'pass':
        root.deiconify()
        top.destroy()

#**************************Lorsqu'on clique sur lquitter**************************  
def command2():
        top.destroy()
        root.destroy()
        sys.exit()



#**************************creation de l'interface de connexion**************************
top = Toplevel()
top.geometry('300x200')
top.title('Connexion')
top.configure(background = 'white')

    #creation d'une zone travaille dans top
frmlog = Frame(top , bg='#3C3C3C' )
frmlog . place (x=0, y=0, width=300,height=200)

    #tete de l'application
lblco=Label(frmlog, text="connecter vous", bg='#3C3C3C',fg='#FFFFFF', font = ('purisa',20))
lblco.place(x=41, y=15, width=220,height=25)
    #login
lbl1= Label(frmlog, text = 'Login', bg='#3C3C3C',fg='#FFFFFF', font = ('purisa',15))
lbl1.place(x=2, y=67, width=95,height=23)

entry1=Entry(frmlog, bd=2, font = ('purisa',15))
entry1.place(x=110, y=67, width=135,height=25)
    #password
lbl2 = Label(frmlog, text = 'Password', bg='#3C3C3C',fg='#FFFFFF', font = ('purisa',15))
lbl2.place(x=2, y=100, width=100,height=23)

entry2=Entry(frmlog, bd=2, show="*", font = ('purisa',15))
entry2.place(x=110, y=100, width=135,height=25)
    #bouton quit
buttonquit2= Button(frmlog, text='cancel',font = ('purisa',15), bg='#AA0000', command=lambda:command2())
buttonquit2.place(x=118, y=165, width=80,height=26)
entry2.bind('<Return>', command1)


img =PhotoImage(file = "icones/plan22.gif")  
label =Label(root, image = img)
width=610
height=400
label.grid()




def open_Toplevel2():
    
    top2 = Toplevel()
    top2.title("Editeur de texte")
    top2.geometry("550x250")
    
    # Editeur
    text = Text(top2, height=12)
    text.grid(column=0, row=0, sticky='nsew')
    text.insert('1.0', f.readlines())
    
    top2.mainloop()

#********************************Lorsqu'on appuie sur submit**********************
def principale():
    
    sfr= SimpleFacerec()
    sfr.load_encoding_images("image/")
    value(t1)
    s = int(value(t1))
#Démarrer la caméra (webcam)
    cap= cv2.VideoCapture(s)

    while True:
        ret, frame= cap.read()
    
    #Deetction fasciale
        face_locations, face_names =sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            top, left, bottom, right= face_loc[0], face_loc[1],face_loc[2], face_loc[3]
            if name == "Inconnue":
                cv2.putText(frame,name,(left,top-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,200 ),2)
                cv2.rectangle(frame, (left,top),(right,bottom),(0,0,200),4)
            else:
                cv2.putText(frame,name,(left,top-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0 ),2)
                cv2.rectangle(frame, (left,top),(right,bottom),(0,255,0),4)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


#************************Lorsqu'on appuie sur lancer la camera************************
def open_Toplevel4():
    
    global cheminfile, chemindoss, t1, top4
    
    top4= Toplevel()
    top4.resizable(False, False)
    top4.title("Demarrer la camera")
    top4.geometry("360x150")
    fen= Frame(top4 , bg='#3C3C3C' )
    fen.place (x=0, y=0, width=360,height=150)
    
    # Save file
    label12 = Label(fen, text = "veulliez selectionner un fichier",bg='#3C3C3C',fg='#AF9564',font=("purisa", 12 ))
    label12.pack(side=RIGHT, pady=65, fill=X)
    label12.place(x=57, y=5, width=270,height=20)

        
    nom = Label(fen, text = 'Nom',bg='#3C3C3C',fg='#AF9564',font=("purisa", 12 ))
    nom.place(x=2, y=35, width=60,height=23)
 
    cheminfile = Label(fen, text = 'aucun fichier enregister',bg='#3C3C3C',fg='#FFFFFF', font = ('purisa',12))
    cheminfile.place(x=70, y=35, width=280,height=23)

    btn = Button(fen, text='Enregistrer',bg='#3C3C3C',fg='#AF9564',font=("purisa", 12 ), command=lambda : savefile(cheminfile))
    btn.place(x=250, y=65, width=100,height=25)
    #choose source
    sl = Label(fen,text="Numero de la camera source",bg='#3C3C3C',fg='#AF9564',font=("purisa", 11 ))
    sl.pack(side=RIGHT, pady=65, fill=X)
    sl.place(x=47, y=95, width=235,height=17)
 
    cam = Label(fen, text = 'Camera', bg='#3C3C3C',fg='#AF9564',font=("purisa", 12 ))
    cam.place(x=2, y=115, width=70,height=23)
 
    t1=Text(fen, height=23, width='40', font = ('purisa',12))
    t1.place(x=80, y=115, width=40,height=23)
 
    btns = Button(fen, text='Submit',bg='#3C3C3C',fg='#AF9564',font=("purisa", 12 ), command=lambda :principale() )
    btns.place(x=250, y=115, width=80,height=25)

    top4.mainloop()


#******************************Elements de création de l'interface***********************
#Creation  frame arriere plan vert pour le haut
frm = Frame(root , bg='#E1E1E1', bd=2 )
img0 =PhotoImage(file = "icones/plan22.gif")
canvas=Canvas(frm, width=600, height=300, bg='#5A5A5A')
canvas.create_image(width/2, height/2, image=img0)
canvas.pack()
# Emplacement du frame
frm . place (x=10, y=0, width=590,height=75)

#Creation frame arriere plan vert pour le bas
frm1 = Frame(root , bg='#002B00' )
img1 =PhotoImage(file = "icones/plan5.gif")
canvas=Canvas(frm1, width=600, height=300, bg='#5A5A5A')
canvas.create_image(width/2, height/2, image=img1)
canvas.pack()
# Emplacement du frame
frm1 . place (x=10, y=90, width=200,height=300)

#Creation  frame arriere plan vert
frm2 = Frame(root , bg='#5A5A5A' )
img2 =PhotoImage(file = "icones/plan1.gif")
canvas=Canvas(frm2, width=600, height=300, bg='#5A5A5A')
canvas.create_image(width/3, height/3, image=img2)
canvas.pack()
# Emplacement du frame
frm2 . place (x=220, y=90, width=380,height=300)
#fin de la cration des differente section de lapplication

#sous-titre interne au logiciel
soustitre= Label(frm, text="Fiche de presence", font = ('purisa',18), bg='#5A5A5A', fg='#000000')
soustitre.pack(expand=YES)
soustitre.place(x=125, y=2, width=364,height=25)


acceuil_bt= Button(frm, text="Acceuil", font = ('purisa',15),bg='#41B77F' ,command = root)
acceuil_bt.pack(expand=YES, pady=65, fill=X)
acceuil_bt.place(x=10, y=32, width=130,height=33)

#ferme le logiciel
Boutquit = Button(frm1, text = 'Quitter', font = ('purisa',13), bg='#AA0000',command =root.destroy)
Boutquit.pack(side=RIGHT,pady=65, fill=X)
Boutquit.place(x=22, y=255, width=130,height=33)
    # Ajouter une image au boutton gere presence
imgequit =PhotoImage(file = "icones/rouge Quit.png")  
labelquit =Label(Boutquit, image = imgequit)
labelquit.grid()



btn_fill4 = Button(frm1, text="Lancer la caméra", bg='#D2D2D2', font = ('purisa',9),command =open_Toplevel4 )
btn_fill4.pack(expand=YES, pady=65, fill=X)
btn_fill4.place(x=8, y=90, width=185,height=33)
# Ajouter une image au boutton camera
imgelancer =PhotoImage(file = "icones/lancer camera.png")  
labellancer =Label(btn_fill4, image = imgelancer)
labellancer.grid()





root.withdraw()
root.mainloop()










