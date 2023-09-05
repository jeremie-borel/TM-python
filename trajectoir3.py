#######################################  a faire  ######################################################################################
#
#
#
#
#
#
#lire fichier
#finir initialisation ---------v
#finir angle entre gps et imu--> faire fonction calule d angle dans les plan et dans l espace
#cretation graphe aussi
#
#
#
#
#
#######################################  librairie  ######################################################################################



# graphique
import folium
from folium.plugins import MarkerCluster

# pour les maths
import numpy as np
from numpy import linalg as LA

#######################################  liste et variable  ######################################################################################

#constente du temps entre deux mesures
temps = 1

#liste donne, a organiser de cette magniere: [[t,accx....][t2,acc....]]

donne = []




################################### Fonction pour effectuer la rotation d'un vecteur à l'aide de quaternions  #############################
#https://pastebin.com/9aVXyUK8



# Fonction pour multiplier deux quaternions (utiliser dans rotation)
def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

# Fonction pour effectuer la rotation d'un vecteur à l'aide de quaternions
def rotationVecteur(vectorAngle, vector):
    """les angles doivent etre en radians"""


    alpha = vectorAngle[0]
    beta = vectorAngle[1]
    gamma = vectorAngle[2]


    # Calcul des composantes du quaternion
    qx = np.sin(alpha/2) * np.cos(beta/2) * np.cos(gamma/2) + np.cos(alpha/2) * np.sin(beta/2) * np.sin(gamma/2)
    qy = np.cos(alpha/2) * np.sin(beta/2) * np.cos(gamma/2) - np.sin(alpha/2) * np.cos(beta/2) * np.sin(gamma/2)
    qz = np.cos(alpha/2) * np.cos(beta/2) * np.sin(gamma/2) + np.sin(alpha/2) * np.sin(beta/2) * np.cos(gamma/2)
    qw = np.cos(alpha/2) * np.cos(beta/2) * np.cos(gamma/2) - np.sin(alpha/2) * np.sin(beta/2) * np.sin(gamma/2)
 
    # Normalisation du quaternion
    quaternion = np.array([qw, qx, qy, qz]) / LA.norm([qw, qx, qy, qz])
 
    # Conversion du vecteur en un quaternion
    vector_quaternion = np.append([0], vector)
 
    # Calcul de la conjugaison du quaternion de rotation
    conjugate_quaternion = np.array([quaternion[0], -quaternion[1], -quaternion[2], -quaternion[3]])
 
    # Calcul du quaternion résultant
    rotated_quaternion = quaternion_multiply(quaternion_multiply(quaternion, vector_quaternion), conjugate_quaternion)
 
    # Extraction du vecteur transformé à partir du quaternion
    rotated_vector = rotated_quaternion[1:]
    return rotated_vector
 
#######################################  fonction calule d angle entre vecteurs  ######################################################################################



def anglePlane(vecteur1,vecteur2):
    pass










#######################################  class point  ######################################################################################


#class des point IMU
class PointIMU :
    # liste de tout les point cree
    point = [] 
    
    def __init__(self,vec_r,vec_v,vec_t):
        self.__class__.point.append(self)
        self.r = vec_r  #position
        self.v = vec_v  #vitesse
        self.t = vec_t  #position angulaire
        self.label = 'IMU ' + str(len(self.__class__.point))

    #print
    def __str__(self):  
        return f"Point {self.label} = position : {self.r}, vitesse : {self.v}, pos angulaire : {self.t}"



# class des points GPS

class PointGPS :

    # liste de tout les point cree
    point = []

    # attention, les vecteurs seront surement en 2d
    def __init__(self,vec_r):
        self.__class__.point.append(self)
        self.r = vec_r  #position
        self.label = 'gps ' + str(len(self.__class__.point))

    # print
    def __str__(self):  
        return f"Point = position : {self.r}, vitesse : {self.v}"




#######################################  fonction  ######################################################################################

def lireFichier():
    pass






def initialisation(vec):
    """creer le referentiel unique"""
    theta_x = np.arccos(vec[0]/np.linalg.norm(vec))
    theta_y = np.arccos(vec[1]/np.linalg.norm(vec))
    theta_z = np.arccos(vec[2]/np.linalg.norm(vec))

    angle = np.array([theta_x,theta_y,theta_z])
    print(angle)
    print(np.linalg.norm(vec))

    angleg = np.array([np.pi/2,0,np.pi/2])

    deltaAngle = angleg-angle

    print(angleg)
    print(deltaAngle)


    return PointIMU()

    # quelle angles signifie quoi?, alpha plan axes x-y?  comment savoir dans quelle ordre faut tourner le vecteur, surment matrice mais pas encore fait... a documenter et comprende


def recurence(pointIMU,vecteurAcc,vecteurAng):
    """passage entre n et n+1"""

    # equation angulaire pour obtenir theta_n+1   //  new_t = thetan+1
    newOmega = vecteurAng*temps + pointIMU.t

    # passage de l'acceleration de l'IMU dans le referentiel unique
    accelUnique = rotationVecteur(newOmega,vecteurAng)

    # equation horaire pour obtenir r_n+1 et v_n+1
    new_r = accelUnique*1/2*(temps**2) + pointIMU.v*temps + pointIMU.r
    new_v = accelUnique*temps + pointIMU.v

    #creation du point_n+1
    return PointIMU(new_r, new_v, newOmega)




def creationPointGps (long, lat):

    position = np.array([long,lat])

    return PointGPS(position)




def allignement():
    """"allignement entre les point gps et imu"""

    #nescecite que l initialisation sois faite  
    nombrePoint = 1 

    #permet de creer les point uniquement jusqu il y aie un deplacement de 20 m
    while numpy.linalg.norm(PointIMU.point[nombrePoint].r[:1])> 20: 

        #construi le point IMU il faut changer les indice suivant comment est construite la liste
        recurence(PointIMU.point[nombrePoint],donne[nombrePoint][0],donne[nombrePoint][1])   

        #construi le point gps de la meme mesure   changer les indices
        creationPointGps(donne[nombrePoint][3],donne[nombrePoint][4])

        # metrs a jour la constente  
        nombrePoint = nombrePoint + 1





def creationGraphe():
    pass


def main():
    pass

if __name__ == '__main__':
    main()
