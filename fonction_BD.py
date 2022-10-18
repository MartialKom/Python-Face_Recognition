import psycopg2
from datetime import *
import datetime


class Etudiant():
    def __init__(self, prenom,nom,matricule,option, photo):
        self.prenom = prenom
        self.nom = nom
        self.photo = photo
        self.matricule = matricule
        self.option = option

def __eq__(self, other):
    return(self.prenom == other.prenom and self.nom ==other.nom and self.matricule == other.matricule and self.option == other.option)

#   connexion a la BD
def connexion():
    global conn
    conn = psycopg2.connect(
    user = "martial",
    password = "secret",
    host = "localhost",
    port = "5432",
    database = "campus"
    )

# retourne le nom corespondant au matricule
def getNom(matricule):
    
    try:
        connexion()
        cur = conn.cursor()        
        sql =  '''SELECT nom, prenom,option FROM etudiants
            WHERE matricule = %s'''
            
        cur.execute(sql, (matricule))
        resultat = cur.fetchall()
        
        for row in resultat:
            nom = str(row[0])
            prenom = row[1]
            opt = row[2]
            
        conn.commit()
        
        cur.close()
        conn.close
        return nom
    except(Exception, psycopg2.Error) as error:
        print ("erreur rencontree", error)
        
    except UnboundLocalError:
        pass
        
    # datep = datetime.date.today()
    # heurep = datetime.datetime.now().time()
    
    # insertP(nom, prenom, opt, datep, heurep)    
    

# Importer la photo dans la BD
def insertBLOB(matricule, nom, prenom, photo, option):
    try:
        connexion()
        cur = conn.cursor()
        
        sql = '''INSERT INTO etudiants(matricule, nom, prenom, photo, option)
			VALUES(%s, %s, %s, %s, %s)'''

		#lire les donnees du fifhier
        monFichier = open(photo,'rb').read()
        
        cur.execute(sql, (matricule, nom, prenom, psycopg2.Binary(monFichier), option, ))
        
        conn.commit()
        print("entries successful !!!")
        
        cur.close()
        conn.close()
        print("connexion fermee")
    except(Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion de l'image", error)
        
        # insere un etudiant dans la table presence
# def insertP(nomp, prenomp, optp, datep, heurep):
#     try:
#         connexion()
#         cur = conn.cursor()
        
#         sql = ''' SELECT nomP, prenomP FROM présence '''
#         cur.execute(sql)
#         res = cur.fetchall()
        
#         for row in res:
#             nome =row[0] 
#             prenome = row[1]
        
#         if nome == nomp and prenome == prenomp :
#             print("l'etudiant {}{} existe deja".format(nome, prenome))
#             pass
#         else:            
#             sql = '''INSERT INTO présence(nomP, prenomP, optP, dateP, heureP)
#                 VALUES(%s, %s, %s, %s, %s)'''
            
#             cur.execute(sql,(nomp, prenomp, optp, datep, heurep, ))
#             conn.commit()
#             print("successful")
        
#         cur.close()
#         conn.close()
    
#     except(Exception,psycopg2.Error) as error:
#         print("Erreur lors de l'insertion", error)