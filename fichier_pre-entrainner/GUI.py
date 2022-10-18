# coding=utf-8

from tkinter import *
import tkinter as tk
import sys
import os
from pathlib import Path
from fonction import recognise_face, cv2, savefile 
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
#from formulaire import *
from tkinter import ttk
from camera import *
import subprocess
from tkinter.messagebox import showerror, showinfo
from PIL import Image, ImageTk
from fonction_BD import Etudiant, insertBLOB

        
def choisir_dossier():
    dir = fd.askdirectory(initialdir="/home/")
    chooseDirectory(dir)
    chemindoss.configure(text=dir)
    
def value(t):
    x=t.get('1.0','end-1c')
    return x
 
def saveVideo():
    global files1
    files = [('Video Files', '*.avi'),
             ('Video Files', '*.mp4')]
    files = fd.asksaveasfile(initialdir="/home/" ,filetypes= files, defaultextension=files)
    files1 = os.fspath(files.name)
    chemin.configure(text=files1)
    #print(files1)
    
def takeVideo():
    video_capture = cv2.VideoCapture(s)
    record = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(files1, record, 4.0, (640,480))

    while True:
        ret, frame = video_capture.read()
        recognise_face(frame, known_face_encodings, known_face_names)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(frame)
        cv2.imshow('Call APP Students face Recognise', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
    
def open_text_file():
        
    global f
        
    # file type
    filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    open_Toplevel2()

def SubmitVideo():
    global s
    s = int(value(t1))
    top3.destroy()
    takeVideo()

def SubmitCamera():
    global s
    s = int(value(t1))
    top4.destroy()
    lancer_camera()

def lancer_camera():
    App(Toplevel(), "Call App Student Face Recognise", s)
        
def select_file():
    global file_to_print

    file_to_print = fd.askopenfilenames(
      initialdir="/home/", title="Select file", 
      filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    fichier.configure(text=file_to_print)

def print_file():
    if file_to_print:
        os.system("lpr -P {}".format(file_to_print))
        try:
            subprocess.run(['lpr'], check= True)
        except subprocess.CalledProcessError:
            showerror(title="Erreur", message="Aucune imprimante branchee")
        
    
# Creation de la fenetre principale
root = Tk()
root.resizable(False, False)
root.geometry("610x400")
root.title("Call App Student Face Recognise")
root.minsize(400,400)
#root.iconbitmap("RFC1.ico")

#creation de l'interface de connexion+++++++++++++++

top = Toplevel()
top.geometry('300x200')
top.title('Connexion')
top.configure(background = 'white')

def parcourir():
    
    ch = fd.askopenfile(initialdir="/home/", title="Aucune video selectionnee",
        filetypes = (("Video Files", "*.avi"),("Video Files","*.mp4"),("Video Files","*.mkv")))
    print(ch.name)
    video_source =ch.name
    App(Toplevel(), "Call App Student Face Recognise", video_source)

def command1(event):
    if entry1.get() == 'admin' and entry2.get() == 'password' or entry1.get() == 'test' and entry2.get() == 'pass':
        root.deiconify()
        top.destroy()
  
def command2():
        top.destroy()
        root.destroy()
        sys.exit()
   

    #creation d'une zone travaille dans top
frmlog = Frame(top , bg='#3C3C3C' )
frmlog . place (x=0, y=0, width=300,height=200)

    #tete de l'application
lblco=Label(frmlog, text="connecter vous", bg='#E1E1E1', font={'Arial',15})
lblco.place(x=41, y=2, width=205,height=20)
    #login
lbl1= Label(frmlog, text = 'Login:', bg='#E1E1E1', font = ('helvetica',15))
lbl1.place(x=2, y=67, width=95,height=23)

entry1=Entry(frmlog, bd=2, font = ('helvetica',10))
entry1.place(x=98, y=67, width=135,height=25)
    #password
lbl2 = Label(frmlog, text = 'Password:', bg='#E1E1E1', font = ('helvetica',15))
lbl2.place(x=2, y=100, width=95,height=23)

entry2=Entry(frmlog, bd=2, show="*", font = ('helvetica',10))
entry2.place(x=98, y=100, width=135,height=25)
    #bouton quit
buttonquit2= Button(frmlog, text='cancel',font=(" Rockwell Extra Bold", 15), bg='#AA0000', command=lambda:command2())
buttonquit2.place(x=118, y=165, width=80,height=26)
entry2.bind('<Return>', command1)


img =PhotoImage(file = "plan22.gif")  
label =Label(root, image = img)
width=610
height=400
label.grid()

def open_Toplevel1():
    
    fen = Toplevel()
    fen.geometry("420x300")
    fen.title("formulaire")

    #creation des section dans la fenetre
    cont2= Frame(fen , bg='#3C3C3C' )
    cont2.place (x=0, y=0, width=420,height=350)
    contenu=Canvas(cont2, bg="#D2D2D2")
    contenu.place(x=10, y=10, width=400,height=200)

    def parcourir():
        global imageName
        imn= fd.askopenfilename(initialdir="/", title="selectionner une image",
            filetypes = (("jpeg files", "*.jpeg"),("jpeg files", "*.png"),("jpeg files","*.jpg")))

        if imn:
            imageName=imn
        if imageName:
            texte=imageName.split()
            photoEntre.configure(text= texte)

    def appartient(liste, val):
        for i in range (len(liste)):
            if liste[i].__eq__(val): 
                return 1
        global liste1 
        liste1 = liste
        return 0
        
    global listePersonne, imageName

    def valider():
     
        photo=imageName
        if prenomEntre.get() and nomEntre.get() and matriculeEntre.get() and optionEntre.get() and photo:
      
            insertBLOB(matriculeEntre.get(), nomEntre.get(), prenomEntre.get(), photo, optionEntre.get())
            etudiant=Etudiant(matriculeEntre.get(), nomEntre.get(), prenomEntre.get(), optionEntre.get(), photo)
            if appartient(listePersonne, etudiant):
                showerror(title="erreur", message="cette étudiant existe deja!")
        
            else:
                listePersonne.append(etudiant)
                showinfo(title="validation réussie", message="{} a bien été enregistré". format(matriculeEntre.get()))	
        
        else:
            showinfo(title="Formulaire invalide", message="veulliez renseigné tout les champs")

    def Reinitialiser():
        global listePersonne, imageName
        prenomEntre.delete(0,END)
        nomEntre.delete(0,END)
        matriculeEntre.delete(0,END)
        optionEntre.delete(0,END)
        imageName=''
        photoEntre.configure(text="selectionner une image")
    imageName, listePersonne='',[]

# forme couleur et style d'ecriture de bouton et label

    fontLabel='arial 13 bold'
    fontEntre='arial 11 bold'

    #identification des different etudiants============
 
    matricule = Label (contenu, text="Matricule:", font= fontLabel, fg='black',bg='#D2D2D2' )
    matricule.grid(row=1, column=0, sticky=E, padx=5, pady=5)

    nom = Label(contenu, text="nom:", font= fontLabel, fg='black', bg='#D2D2D2')
    nom.grid(row=2, column=0, sticky=E, padx=5, pady=5)

    prenom = Label (contenu, text="prenom:", font= fontLabel, fg='black',bg='#D2D2D2' )
    prenom.grid(row=3, column=0, sticky=E, padx=5, pady=5)

    option = Label (contenu, text="Option:", font= fontLabel, fg='black',bg='#D2D2D2' )
    option.grid(row=4, column=0, sticky=E, padx=5, pady=5)

    photo = Label(contenu, text="votre photo:", font= fontLabel, fg='black', bg='#D2D2D2')
    photo.grid(row=5, column=0, sticky=E, padx=5, pady=5)

    validation = Label(contenu, text="Entrer vos information ici", font= fontLabel, fg='black', bg="#D2D2D2")
    validation.grid( row=0, column=0, columnspan=2)

    #creation des zone decriture
 
    matriculeEntre = Entry(contenu,font= fontLabel )
    matriculeEntre.grid(row=1, column=1, padx=5, pady=5)

    nomEntre = Entry(contenu, font= fontLabel)
    nomEntre.grid(row=2, column=1, padx=5, pady=5)

    prenomEntre = Entry (contenu, font= fontEntre)
    prenomEntre.grid(row=3, column=1, padx=5, pady=5)

    optionEntre = Entry(contenu,font= fontLabel )
    optionEntre.grid(row=4, column=1, padx=5, pady=5)

    photoEntre = Label(contenu, text="selectionner une image", font='arial 8 bold', fg='black')
    photoEntre.grid(row=5, column=1, padx=5, pady=5,sticky=W)
 
    buttonParcourir= Button (contenu,text="Parcourir", command= parcourir, fg="#FF7800", bg='white')
    buttonParcourir.grid(row=5, column=1, padx=7, pady=5,sticky=E)

    #boutton de gestion de l'enregistrement

    b1= Button (fen, text="Valider",command= valider,width=10, fg='white', bg='#5A5A5A')
    b1.place(x=160, y=230, width=90,height=25)

    b2= Button (fen, text="Reinitialiser", command= Reinitialiser,width=10, fg='white', bg='#5A5A5A')
    b2.place(x=160, y=260, width=90,height=25)

    fen.mainloop()

def open_Toplevel2():
    
    top2 = Toplevel()
    top2.title("Editeur de texte")
    top2.geometry("550x250")
    
    # Editeur
    text = Text(top2, height=12)
    text.grid(column=0, row=0, sticky='nsew')
    text.insert('1.0', f.readlines())
    
    top2.mainloop()

def open_Toplevel3():
    
    global chemin, chemindoss, t1, top3
    
    top3= Toplevel()
    top3.title("Video")
    top3.geometry("360x260")
    # Save video
    labela8 = Label(top3, text = "Enregistrer une video",font=("times new romen", 10 ))
    labela8.pack(side=RIGHT, pady=65, fill=X)
    labela8.place(x=50, y=5, width=212,height=17)

        
    nom = Label(top3, text = 'Nom', bg='#E1E1E1', font = ('helvetica',10))
    nom.place(x=2, y=35, width=60,height=23)
 
    chemin = Label(top3, text = 'Aucune video enregistrer', bg='#E1E1E1', font = ('helvetica',8))
    chemin.place(x=70, y=35, width=280,height=23)

    btn = ttk.Button(top3, text='Enregistrer', command=lambda : saveVideo())
    btn.place(x=250, y=65, width=100,height=25)
 
    #choose directory
    labela50 = Label(top3, text = "selectionner un dossier contenant les images",font=("times new romen", 10 ))
    labela50.pack(side=RIGHT, pady=65, fill=X)
    labela50.place(x=10, y=95, width=350,height=17)

    doss = Label(top3, text = 'Dossier', bg='#E1E1E1', font = ('helvetica',10))
    doss.place(x=2, y=115, width=60,height=23)

    chemindoss = Label(top3, text = 'Aucun dossier selectionner', bg='#E1E1E1', font = ('helvetica',8))
    chemindoss.place(x=70, y=115, width=280,height=23)

    butn = ttk.Button(top3, text='Select', command=lambda : choisir_dossier())
    butn.place(x=250, y=140, width=100,height=25)
 
    #choose source
    sl = Label(top3,text="Numero de la camera source",font=("times new romen", 10 ))
    sl.pack(side=RIGHT, pady=65, fill=X)
    sl.place(x=55, y=170, width=212,height=17)
 
    cam = Label(top3, text = 'Camera', bg='#E1E1E1', font = ('helvetica',10))
    cam.place(x=2, y=190, width=60,height=23)
 
    t1=Text(top3, height=23, width=40)
    t1.place(x=70, y=190, width=40,height=23)
 
    btns = ttk.Button(top3, text='Submit', command=lambda : SubmitVideo())
    btns.place(x=260, y=210, width=80,height=25)

    top3.mainloop()

def open_Toplevel4():
    
    global cheminfile, chemindoss, t1, top4
    
    top4= Toplevel()
    top4.title("Demarrer la camera")
    top4.geometry("360x260")
    # Save video
    label12 = Label(top4, text = "veulliez saisir le nom du fichier",font=("times new romen", 10 ))
    label12.pack(side=RIGHT, pady=65, fill=X)
    label12.place(x=50, y=5, width=212,height=17)

        
    nom = Label(top4, text = 'Nom', bg='#E1E1E1', font = ('helvetica',10))
    nom.place(x=2, y=35, width=60,height=23)
 
    cheminfile = Label(top4, text = 'aucun fichier enregister', bg='#E1E1E1', font = ('helvetica',8))
    cheminfile.place(x=70, y=35, width=280,height=23)

    btn = ttk.Button(top4, text='Enregistrer', command=lambda : savefile(cheminfile))
    btn.place(x=250, y=65, width=100,height=25)
 
    #choose directory
    labela50 = Label(top4, text = "selectionner un dossier contenant les images",font=("times new romen", 10 ))
    labela50.pack(side=RIGHT, pady=65, fill=X)
    labela50.place(x=10, y=95, width=350,height=17)

    doss = Label(top4, text = 'Dossier', bg='#E1E1E1', font = ('helvetica',10))
    doss.place(x=2, y=115, width=60,height=23)

    chemindoss = Label(top4, text = 'Aucun dossier selectionner', bg='#E1E1E1', font = ('helvetica',8))
    chemindoss.place(x=70, y=115, width=280,height=23)

    butn = ttk.Button(top4, text='Select', command=lambda : choisir_dossier())
    butn.place(x=250, y=140, width=100,height=25)
 
    #choose source
    sl = Label(top4,text="Numero de la camera source",font=("times new romen", 10 ))
    sl.pack(side=RIGHT, pady=65, fill=X)
    sl.place(x=55, y=170, width=212,height=17)
 
    cam = Label(top4, text = 'Camera', bg='#E1E1E1', font = ('helvetica',10))
    cam.place(x=2, y=190, width=60,height=23)
 
    t1=Text(top4, height=23, width=40)
    t1.place(x=70, y=190, width=40,height=23)
 
    btns = ttk.Button(top4, text='Submit', command=lambda : SubmitCamera())
    btns.place(x=260, y=210, width=80,height=25)

    top4.mainloop()

def open_Toplevel5():
    global top5
    top5= Toplevel()
    top5.title("Liste des etudiants")
    top5.geometry("650x350")
    #definition de l'organisation de la fenetre

    cont1 = Frame(top5 , bg='#3C3C3C' )
    cont1.place (x=0, y=0, width=700,height=400)

    listeCan=Canvas(cont1, bg="#D2D2D2")
    listeCan.grid(row=0, column=0)
  
    fonttLabel='arial 11 bold'

    #organisation de la liste d'enregistrement des etudiant

    resultat = Label(listeCan, text="liste des étudiants", font= fonttLabel, fg='black',bg='#D2D2D2')
    resultat.grid(row=0, column=0, columnspan=3)
  
    matricule = Label(listeCan, text="Matricule",width=15, font=fonttLabel, fg="black", bg='#D2D2D2')
    matricule.grid(row=1, column=1,padx=5, pady=5)

    nom = Label(listeCan, text="nom",width=15, font=fonttLabel, fg="black", bg='#D2D2D2')
    nom.grid(row=1, column=2,padx=5, pady=5)

    prenom = Label(listeCan, text="prenom",width=15, font=fonttLabel, fg="black", bg='#D2D2D2')
    prenom.grid(row=1, column=3,padx=5, pady=5)

    option = Label(listeCan, text="Option",width=15, font=fonttLabel, fg="black", bg='#D2D2D2')
    option.grid(row=1, column=4,padx=5, pady=5)

    photo = Label(listeCan, text="photo",width=12, font=fonttLabel, fg="black", bg='#D2D2D2')
    photo.grid(row=1, column=5,padx=5, pady=5)

    status = Label(listeCan, text="aucun étudiant pour le moment", font='arial 9 bold', fg="black", bg='#D2D2D2')
    status.grid(row=2, column=0,columnspan=3)

    

    if liste:
        r=2
        for e in liste:
            photoLab= Label(listeCan, height=60)
            photoLab.grid(row= r, column=5, pady=2)

    #organisation de la photo dans la fenetre
            img=Image.open(e.photo)
            img=img.resize((85,60),Image.ANTIALIAS)
            photoLab.img=ImageTk.PhotoImage(img)
            photoLab.configure(image=photoLab.img)
   
            ma=Label(listeCan, text=e.matricule, font= fonttLabel,fg='black', bg='#FF7800')
            ma.grid(row= r, column=1)
   
            no=Label(listeCan, text=e.nom, font= fonttLabel,fg='black', bg='#FF7800')
            no.grid(row= r, column=2)

            pre=Label(listeCan, text=e.prenom, font= fonttLabel,fg='black', bg='#FF7800')
            pre.grid(row= r, column=3)
            
            op=Label(listeCan, text=e.option, font= fonttLabel,fg='black', bg='#FF7800')
            op.grid(row= r, column=4)
            

            listeCan.create_line(9,55,355,55,width=1,fill='black')

            r+=1

            status.configure(text="{} Etudiants". format(len(liste)))
            status.grid(row=r, column=0, columnspan=3, pady= 2)


 
    top5.mainloop()

def open_Toplevel6():

    top6= Toplevel()
    top6.title("Imprimer les fiches de presence")
    top6.geometry("320x120")
    labeli6= Label(top6, text = "Choisir le fichier a imprimer",font=("times new romen", 10 ))
    labeli6.pack(side=RIGHT, pady=65, fill=X)
    labeli6.place(x=8, y=5, width=212,height=25)
    
    global fichier
    
    fichier = Label(top6, text="Aucun fichier selectionner ", bd=2, font = ('helvetica',10))
    fichier.place(x=8, y=50, width=227,height=30)

    buttonParcourir= Button (top6,text="Parcourir", command= select_file, fg="#FF7800", bg='white')
    buttonParcourir.place(x=230, y=50, width=80,height=30)
 
    Bt_c4= Button(top6, text ="Imprimer", command=print_file, font=(" Broadway", 10))
    Bt_c4.place(x=70, y=80, width=80,height=30)
    
    top6.mainloop()
    
    
def open_Toplevel7():

    top7= Toplevel()
    top7.title("Visualiser les presences")
    top7.geometry("280x160")        

    labelg7= Label(top7, text = "Choisir le fichier a visualiser",font=("times new romen", 10 ))
    labelg7.pack(side=RIGHT, pady=65, fill=X)
    labelg7.place(x=38, y=5, width=195,height=25)


    #les sour bouton de la fen....
    Bt_m4= Button(top7, text ="liste de presences",command = open_text_file, font=(" Broadway", 10))
    Bt_m4.pack(side=RIGHT, pady=65, fill=X)
    Bt_m4.place(x=48, y=40, width=180,height=25)

    Bt_ma4= Button(top7, text ="Visualiser une video", command=parcourir, font=(" Broadway", 10))
    Bt_ma4.pack(side=RIGHT, pady=65, fill=X)
    Bt_ma4.place(x=48, y=100, width=180,height=25)

    
    top7.mainloop()

#Creation  frame arriere plan vert pour le haut
frm = Frame(root , bg='#E1E1E1', bd=2 )
img0 =PhotoImage(file = "plan22.gif")
canvas=Canvas(frm, width=600, height=300, bg='#5A5A5A')
canvas.create_image(width/2, height/2, image=img0)
canvas.pack()
# Emplacement du frame
frm . place (x=10, y=0, width=590,height=75)

#Creation frame arriere plan vert pour le bas
frm1 = Frame(root , bg='#002B00' )
img1 =PhotoImage(file = "plan5.gif")
canvas=Canvas(frm1, width=600, height=300, bg='#5A5A5A')
canvas.create_image(width/2, height/2, image=img1)
canvas.pack()
# Emplacement du frame
frm1 . place (x=10, y=90, width=200,height=300)

#Creation  frame arriere plan vert
frm2 = Frame(root , bg='#5A5A5A' )
img2 =PhotoImage(file = "plan1.gif")
canvas=Canvas(frm2, width=600, height=300, bg='#5A5A5A')
canvas.create_image(width/3, height/3, image=img2)
canvas.pack()
# Emplacement du frame
frm2 . place (x=220, y=90, width=380,height=300)

#fin de la cration des differente section de lapplication

#sous-titre interne au logiciel
soustitre= Label(frm, text="C.AP.S.FA.RE", font=("Britannic Bold", 18 ), bg='#5A5A5A', fg='#000000')
soustitre.pack(expand=YES)
soustitre.place(x=125, y=2, width=364,height=25)

acceuil_bt= Button(frm, text="acceuil", font=(" Rockwell Extra Bold", 15 ),bg='#41B77F' ,command = root)
acceuil_bt.pack(expand=YES, pady=65, fill=X)
acceuil_bt.place(x=10, y=32, width=130,height=33)

#ferme le logiciel
Boutquit = Button(frm1, text = 'Quitter', font=(" Rockwell Extra Bold", 15), bg='#AA0000',command =root.destroy)
Boutquit.pack(side=RIGHT,pady=65, fill=X)
Boutquit.place(x=10, y=255, width=130,height=33)
    # Ajouter une image au boutton gere presence
imgequit =PhotoImage(file = "rouge Quit.png")  
labelquit =Label(Boutquit, image = imgequit)
labelquit.grid()

#differente tache a realiser dans lapplication
btn_fill2 = Button(frm1, text="Ajouter un etudiant", font=(" Broadway", 10), bg='#D2D2D2',command = lambda:open_Toplevel1)
btn_fill2.pack(expand=YES, pady=65, fill=X)
btn_fill2.place(x=8, y=10, width=185,height=33)
        # Ajouter une image au boutton etudiant
imgetudiant =PhotoImage(file = "etudiant.png")  
labelet =Label(btn_fill2, image = imgetudiant)
labelet.grid()

btn_fill5 = Button(frm1, text="liste des etudiants", font=(" Broadway", 10), bg='#D2D2D2',command = open_Toplevel5)
btn_fill5.pack(expand=YES, pady=65, fill=X)
btn_fill5.place(x=8, y=50, width=185,height=33)
        # Ajouter une image au boutton source
imgeadmin =PhotoImage(file = "adimin.png")  
labeladmin =Label(btn_fill5, image = imgeadmin)
labeladmin.grid()

btn_fill4 = Button(frm1, text="Lancer la caméra", bg='#D2D2D2', font=(" Broadway", 10),command =open_Toplevel4)
btn_fill4.pack(expand=YES, pady=65, fill=X)
btn_fill4.place(x=8, y=90, width=185,height=33)
# Ajouter une image au boutton camera
imgelancer =PhotoImage(file = "lancer camera.png")  
labellancer =Label(btn_fill4, image = imgelancer)
labellancer.grid()

btn_fill3 = Button(frm1, text="Prendre une video", bg='#D2D2D2', font=(" Broadway", 10),command = open_Toplevel3)
btn_fill3.pack(expand=YES, pady=65, fill=X)
btn_fill3.place(x=8, y=130, width=185,height=33)
# Ajouter une image au boutton departement
imgedepart =PhotoImage(file = "Gere departement.png")  
labeldepar =Label(btn_fill3, image = imgedepart)
labeldepar.grid()

btn_fill6 = Button(frm1, text="Imprimer les fiches", font=(" Broadway", 9), bg='#D2D2D2', command = open_Toplevel6)
btn_fill6.pack(expand=YES, pady=65, fill=X)
btn_fill6.place(x=8, y=170, width=185,height=33)
        # Ajouter une image au boutton imprimer
imgedoc =PhotoImage(file = "imprimer doc.png")  
labeldoc =Label(btn_fill6, image = imgedoc)
labeldoc.grid()

Bouton1 = Button(frm1, text = "Visualiser les presences", bg='#D2D2D2', font=(" Broadway", 10), command = open_Toplevel7 )
Bouton1.pack(side=RIGHT, pady=65, fill=X)
Bouton1.place(x=8, y=210, width=185,height=33)
    # Ajouter une image au boutton gere présence
imgeajout =PhotoImage(file = "Ajout presence.png")  
labelajout =Label(Bouton1, image = imgeajout)
labelajout.grid()

#root. config (menu=menuBar)
root.withdraw()
root.mainloop()










