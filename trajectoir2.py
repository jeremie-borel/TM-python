




#######################################  structure du code  ######################################################################################
#
#
# package
# liste et variable
# class vecteur
# class point
# pas de recurence
# extraction position et vitesse pour les listes pour le graphe
# creation du graphe
# main
#
#
#######################################  a faire  ##############################################################################################
#
#
# de quoi pouvoir lire le dossier de l'arduino et en extraire les données
# matrice de merde
# toute la partie gps pour pouvoir comparer les resultats on a position et vitesse normalement
#
#
# optimisation du code genre limitation de vitesse, de chaangement d'angle
#
#
#################################################################################################################################################








# graphique
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# pour les maths
import numpy as np      

# temp entre chaque mesure des acceleration utiliser dans step
t = 0.5  

# liste des position pour l'affichage graphique
x_coords = []       
y_coords = []
z_coords = []

# liste des vitesse pour graph
vx_velo = []        
vy_velo = []
vz_velo = []




# code vecteurs 3d et ces operations : vecteurs d'angle compris
class Vec :     

    # defni quand on le cree
    def __init__(self,x,y,z):   
        self.x = x
        self.y = y
        self.z = z

    # addition
    def __add__(self,other):
        return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

    # soustraction
    def __sub__(self,other):    
        return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

    # multiplication
    def __mul__(self,x):    
        return Vec(self.x * x, self.y * x, self.z * x)

    # division
    def __truediv__(self,x):    
        return Vec(self.x / x, self.y / x, self.z / x)

    # pour print
    def __str__(self):      
        return f"({self.x},{self.y},{self.z})"

    # pour tester les matrice
    def norme (self) :
        return  np.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)




#######################################  a changer  ######################################################################################



    def matrice (self, a) :     # a = vecteur angle  multiplication d'un vecteur par une matrice de rotation (les angles sont donner par un angle de rotation) le plus simple est de faire matrice axe x ensuite matrice axe y ... 
        x1 = self.x     # matrice x
        y1 = self.y * np.cos(-a.x) - self.z * np.sin(-a.x)     # matrice x        - devant tout les angle parce que les matrices sont R(-alpha)+...
        z1 = self.y * np.sin(-a.x) + self.z * np.cos(-a.x)     # matrice x
        x2 = x1 * np.cos(-a.y) + z1 * np.sin(-a.y)     # matrice y
        y2 = y1     # matrice y
        z2 = - x1 * np.sin(-a.y) + z1 * np.cos(-a.y)     # matrice y
        x3 = x2 * np.cos(-a.z) - y2 * np.sin(-a.z)     # matrice z
        y3 = x2 * np.sin(-a.z) + y2 * np.cos(-a.z)     # matrice z
        z3 = z2     # matrice z
        return Vec(x3, y3, z3)


#######################################  a changer  ######################################################################################







# point de chaque prise de données
class Point :

    # liste de tout les point cree
    point = [] 
    
    def __init__(self,vec_r,vec_v,vec_t):
        self.__class__.point.append(self)
        self.r = vec_r
        self.v = vec_v
        self.t = vec_t

    #print
    def __str__(self):  
        return f"Point = position : {self.r}, vitesse : {self.v}, pos angulaire : {self.t}"




# pas de recurence  //  acc pour acceleration 
def step (point_n, acc_n, omega_n):     

    # equation angulaire pour obtenir theta_n+1   //  new_t = thetan+1
    new_t = omega_n*t + point_n.t

    # passage de l'acceleration de l'IMU dans le referentiel unique
    uni_acc = acc_n.matrice(nt)

    # equation horaire pour obtenir r_n+1 et v_n+1
    new_r = uni_acc*1/2*t*t + point_n.v*t + point_n.r
    new_v = uni_acc*t + point_n.v

    #creation du point_n+1
    return Point(new_r, new_v, new_t)




# fonction pour extraire les coordonnées et les vitesses des points
def list_graphe ():
    
    for point in Point.point:

        # extraction des coordonnées de position
        x_coords.append(point.r.x)
        y_coords.append(point.r.y)
        z_coords.append(point.r.z)
        
        # extraction des vitesses
        vx_velo.append(point.v.x)
        vy_velo.append(point.v.y)
        vz_velo.append(point.v.z)




# creation d un graphique //  utilisation des listes de positions et de vitesses    //  utilisable pour gps et IMU
def graphics (listrx, listry, listrz, listvx, listvy, listvz):

    # calcule la norme de chaque vitesse
    velocities = np.sqrt(np.array(u_velocities)**2 + np.array(v_velocities)**2 + np.array(w_velocities)**2)

    # indique le point avec la plus grande vitesse
    max_velocity_idx = np.argmax(velocities)

    # creation de la figure
    fig = plt.figure()

    # module de la figure
    ax = fig.add_subplot(111, projection='3d')
    
    # enleve axes et le fond
    ax.axis('off')
    
    # cree les points // c='k' fait que les points sont en noir
    ax.scatter(listrx, listry, listrz, c='k', marker='o')

    # cree le point avec la plus grande vitesse en rouge
    ax.scatter(listrx[max_velocity_idx], listry[max_velocity_idx], listrz[max_velocity_idx], c='r', marker='o')

    # cree les vecteurs de vitesse pour chaque points
    ax.quiver(listrx, listry, listrz, listvx, listvy, listvz)

    # affiche le graphe
    plt.show()      












def main():
    r0 = Vec(4, 5, 6)
    v0 = Vec(7 , 8, 9)
    t0 = Vec(1,1,1)
    base = Point(r0, v0, t0)
    o1 = Vec(1,2,3)
    a1 = Vec(1,2,3)
    step1 = base.step(a1, o1)
    #print(step1)
    #print(step1.r.norme())
    unit = Vec(9.4567,6.6324,3.6234)
    angle = Vec(5,34,76)
    nunit = unit.matrice(angle)
    #print(unit, unit.norme())
    #print(nunit, nunit.norme())

if __name__ == '__main__':
    main()
