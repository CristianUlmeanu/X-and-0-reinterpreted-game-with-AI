import time
import statistics

import pygame, sys, copy

#ADANCIME_MAX = 6


# def elem_identice(lista):
#     if (all(elem == lista[0] for elem in lista[1:])):
#         return lista[0] if lista[0] != Joc.GOL else False
#     return False

counter_nod_min=0 #Variabila globala pentru nodurile din min-max
counter_nod_alpha=0 #Variabila globala pentru nodurile din alpha-bet

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE =1
    NR_LINII=1
    JMIN = None
    JMAX = None
    GOL = '#'

    @classmethod
    def initializeaza(cls, display, dim_celula=60):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        #Initializam in functie de randuri+coloane
        for linie in range(Joc.NR_LINII):
            cls.celuleGrid.append([])
            for coloana in range(Joc.NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid[linie].append(patr)

    def deseneaza_grid(self,cul):  # tabla de exemplu este ["#","x","#","0",......]

        for linie in range(Joc.NR_LINII):
            for coloana in range(Joc.NR_COLOANE):
                if self.matr[linie][coloana] in ['x','0']:
                    culoare = (255, 255, 255)
                else:
                    #Stabilim culoarea pentru a afisa pozitiile posibile de mutare
                    culoare=cul
                pygame.draw.rect(self.__class__.display, culoare,
                                 self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                if self.matr[linie][coloana] == 'x':
                    self.__class__.display.blit(self.__class__.x_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
                elif self.matr[linie][coloana] == '0':
                    self.__class__.display.blit(self.__class__.zero_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)

    # pygame.display.update()

    def __init__(self, tabla=None):
        if tabla:
            self.matr = tabla
        else:
            self.matr = []
            for i in range(self.__class__.NR_LINII):
                self.matr.append([self.__class__.GOL] * self.__class__.NR_COLOANE)

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        # Pentru conditia finala verificam daca mai exista pozitii goale sau nu si verificam semnul predominant
        ok=0
        cnt_x=0
        cnt_0=0
        for lini in range(Joc.NR_LINII):
            for coloane in range(Joc.NR_COLOANE):
                if self.matr[lini][coloane] not in ['x','0']:
                    ok=1
                    break
                else:
                    if self.matr[lini][coloane]=='x':
                        cnt_x+=1
                    elif self.matr[lini][coloane]=='0':
                        cnt_0+=1
            if ok==1:
                break
        if ok==0:
            if cnt_x>cnt_0:
                return 'x'
            elif cnt_x<cnt_0:
                return '0'
            elif cnt_x==cnt_0:
                return 'remiza'
        else:
            return False
        # rez = (elem_identice(self.matr[0])
        #        or elem_identice(self.matr[1])
        #        or elem_identice(self.matr[2])
        #        or elem_identice([self.matr[0][0], self.matr[1][0], self.matr[2][0]])
        #        or elem_identice([self.matr[0][1], self.matr[1][1], self.matr[2][1]])
        #        or elem_identice([self.matr[0][2], self.matr[1][2], self.matr[2][2]])
        #        or elem_identice([self.matr[0][0], self.matr[1][1], self.matr[2][2]])
        #        or elem_identice([self.matr[0][2], self.matr[1][1], self.matr[2][0]]))
        # if (rez):
        #     return rez
        # elif self.__class__.GOL not in self.matr[0] + self.matr[1] + self.matr[2]:
        #     return 'remiza'
        # else:
        #     return False

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        # Pentru generarea de mutari, am implementat prin functia "test_vecini" auto-completarea tablei in functie de conditia problemei
        l_mutari = []
        for i in range(self.__class__.NR_LINII):
            for j in range(self.__class__.NR_COLOANE):
                if self.matr[i][j] == Joc.GOL:
                    copie_matr = copy.deepcopy(self.matr)
                    copie_matr[i][j] = jucator
                    copie_matr=test_vecini(copie_matr,i,j,"")[0]
                    l_mutari.append(Joc(copie_matr))
        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    # def linie_deschisa(self, lista, jucator):
    #     jo = self.jucator_opus(jucator)
    #     # verific daca pe linia data nu am simbolul jucatorului opus
    #     if not jo in lista:
    #         return 1
    #     return 0
    #
    # def linii_deschise(self, jucator):
    #     return self.linie_deschisa(self.matr[0], jucator)
    #     + self.linie_deschisa(self.matr[1], jucator)
    #     + self.linie_deschisa(self.matr[2], jucator)
    #     + self.linie_deschisa([self.matr[0][0], self.matr[1][0], self.matr[2][0]], jucator)
    #     + self.linie_deschisa([self.matr[0][1], self.matr[1][1], self.matr[2][1]], jucator)
    #     + self.linie_deschisa([self.matr[0][2], self.matr[1][2], self.matr[2][2]], jucator)
    #     + self.linie_deschisa([self.matr[0][0], self.matr[1][1], self.matr[2][2]], jucator)
    #     + self.linie_deschisa([self.matr[0][2], self.matr[1][1], self.matr[2][0]], jucator)

    def puncte(self,jucator):
        #Functia este folosita pentru estimarea scorului in functie de numaru de puncte pe care il obtine robotu, verificand numaru de semne de tabla
        count_jucator=0
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if(self.matr[i][j]==jucator):
                    count_jucator+=1
        return count_jucator

    def nr_umpleri(self,jucator):
        ##Functia este folosita pentru estimarea scorului in functie de numaru de patratele pe care le poate umple automat cand se pune un semn
        count_umpleri=0
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                count_umpleri=test_vecini(self.matr,i,j,jucator)[1]
        return count_umpleri

    def estimeaza_scor(self, adancime, tip_estimare="estimare2"):
        ##1. Estimare scor curent
        ##2. Estimare cate s-ar autocompleta daca s-ar pune acl
        t_final = self.final()
        if (tip_estimare=="estimare1"):
            if t_final == self.__class__.JMAX:
                return (99 + adancime)
            elif t_final == self.__class__.JMIN:
                return (-99 - adancime)
            elif t_final == 'remiza':
                return 0
            else:
                return (self.puncte(self.__class__.JMAX) - self.puncte(self.__class__.JMIN))
        elif (tip_estimare=="estimare2"):
            if t_final == self.__class__.JMAX:
                return (99 + adancime)
            elif t_final == self.__class__.JMIN:
                return (-99 - adancime)
            elif t_final == 'remiza':
                return 0
            else:
                return (self.nr_umpleri(self.__class__.JMAX) - self.nr_umpleri(self.__class__.JMIN))

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i+1) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE) * 2 + "\n"
        for i in range(self.NR_LINII):  # itereaza prin linii
            sir += str(i+1) + " |" + " ".join([str(x) for x in self.matr[i]]) + "\n"
        return sir

    def Marcare_raspuns(self, castigator):
        # Functie ce coloreaza configuratia castigatoare
        for linie in range(self.NR_LINII):
            for coloana in range(self.NR_COLOANE):
                if self.matr[linie][coloana] == castigator:
                    culoare = (124, 252, 0)
                else:
                    culoare = (255,255,255)
                pygame.draw.rect(self.__class__.display, culoare,
                                 self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                if self.matr[linie][coloana] == 'x':
                    self.__class__.display.blit(self.__class__.x_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
                elif self.matr[linie][coloana] == '0':
                    self.__class__.display.blit(self.__class__.zero_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Jucator curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    global counter_nod_min
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    counter_nod_min=counter_nod_min+len(stare.mutari_posibile)

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    global counter_nod_alpha
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    counter_nod_alpha=counter_nod_alpha+len(stare.mutari_posibile)

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta,tabla):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            Joc.Marcare_raspuns(tabla,final)
            print("A castigat " + final)

        return True

    return False

def afis_scor(stare_curenta):
    #Functie ce calcuelaza scorul curent
    scor_x=0
    scor_0=0
    for i in range(Joc.NR_LINII):
        for j in range(Joc.NR_COLOANE):
            if stare_curenta.tabla_joc.matr[i][j] == 'x':
                scor_x = scor_x + 1
            elif stare_curenta.tabla_joc.matr[i][j] == '0':
                scor_0 = scor_0 + 1
    return scor_x,scor_0

def test_vecini(matrice,linie,coloana,jucator):
    #Functia care este folosita pentru autocompletarea spatiilor goale in cazu in care vecinii pozitiei care a fost marcata. Pentru fiecare vecin ii verificam iar vecinii pentru a afla nr.
    #De vecini de acelasi semn, daca unu din semne este ed 4+ ori si numarul semnului respectiv este predominant se umpple, totoadta contorizam acest lucru
    ### Parcurgem matricea in latime
    count_umpleri=0
    queue = []
    queue.append([linie,coloana])
    parc_linii=[-1,-1,-1,0,0,1,1,1]
    parc_col=[-1,0,1,-1,1,-1,0,1]
    while len(queue) != 0:
        pozitie = queue.pop(0)
        for i in range(len(parc_linii)):
            linie_vecin = pozitie[0] + parc_linii[i]
            coloana_vecin = pozitie[1] + parc_col[i]
            counter_x = 0
            counter_0 = 0
            if linie_vecin in range(Joc.NR_LINII) and coloana_vecin in range(Joc.NR_COLOANE) and matrice[linie_vecin][coloana_vecin]==Joc.GOL:
                for j in range(len(parc_linii)):
                    linie_vecin2 = linie_vecin + parc_linii[j]
                    coloana_vecin2 = coloana_vecin + parc_col[j]
                    if linie_vecin2 in range(Joc.NR_LINII) and coloana_vecin2 in range(Joc.NR_COLOANE) and matrice[linie_vecin2][coloana_vecin2]=='x':
                        counter_x += 1
                    elif linie_vecin2 in range(Joc.NR_LINII) and coloana_vecin2 in range(Joc.NR_COLOANE) and matrice[linie_vecin2][coloana_vecin2]=='0':
                        counter_0 += 1
            if counter_x >=4 and counter_x > counter_0:
                matrice[linie_vecin][coloana_vecin] ='x'
                #print(linie_vecin,coloana_vecin)
                queue.append([linie_vecin,coloana_vecin])
                if jucator=='x':
                    count_umpleri+=1
            elif counter_0 >=4 and counter_0 > counter_x:
                #print(linie_vecin,coloana_vecin)
                matrice[linie_vecin][coloana_vecin] ='0'
                count_umpleri+=1
                queue.append([linie_vecin,coloana_vecin])
                if jucator=='0':
                    count_umpleri+=1
    return matrice,count_umpleri

def main():
    # initializare algoritm
    time_initial=time.time()
    lista_mutari=[]
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    raspuns_valid = False
    while not raspuns_valid:
        adancime_max=input("Alegeti dificultatea pe care doriti sa jucati: \n 1. Incepator\n 2. Intermediar\n 3. Avansat\n(Raspundeti cu 1, 2 sau 3)\n")
        if adancime_max in ['1','2','3']:
            raspuns_valid=True
            adancime_max=int(adancime_max)
        else:
            print("Dificultatea aleasa nu este corecta, reincercati!")

    # initializare tabla
    raspuns_valid=False
    while not raspuns_valid:
        while not raspuns_valid:
            NR_COLOANE =int(input("Alegeti numarul de coloane pentru tabla de joc, numarul trebuie sa fie mai mare decat 5\n"))
            if NR_COLOANE>5:
                raspuns_valid=True
                Joc.NR_COLOANE = NR_COLOANE
            else:
                print("Numarul de coloane nu a fost ales corect, reincercati!")
        raspuns_valid=False
        while not raspuns_valid:
            NR_LINII=int(input("Alegeti numarul de linii pentru tabla de joc, numarul trebuie sa fie mai mic decat 10\n"))
            if NR_LINII<10:
                raspuns_valid=True
                Joc.NR_LINII = NR_LINII
            else:
                print("Numarul de linii nu a fost ales corect, reincercati!")
        if NR_LINII%2!=0 and NR_COLOANE%2!=0:
            raspuns_valid=False
            print("Macar unul din numere trebuie sa fie par, reincercati!")
    tabla_curenta = Joc()
    print(str(tabla_curenta))


    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', adancime_max)
    lista_mutari.append(copy.deepcopy(stare_curenta))
    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('253_Ulmeanu_Cristian: ex-jocuri-exemple-modificate')
    # dimensiunea ferestrei in pixeli
    # dim_celula=..
    ecran = pygame.display.set_mode(
        size=(60*NR_COLOANE+(NR_COLOANE-1), 60*NR_LINII+(NR_LINII-1)))  # N *100+ (N-1)*dimensiune_linie_despartitoare (dimensiune_linie_despartitoare=1)
    Joc.initializeaza(ecran)

    de_mutat = False
    if Joc.JMIN=='x':
        tabla_curenta.deseneaza_grid(cul=(0,0,255))
    else:
        tabla_curenta.deseneaza_grid(cul=(0, 255, 255))
    time_list_robot=[]
    scor_x=0
    scor_0=0
    t_init_user = time.time() * 1000
    lista_noduri=[]
    counter_mutari_robot=0
    counter_mutari_player=0
    global counter_nod_min
    global counter_nod_alpha

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #In cazu in care se opreste programu+afisari
                    scor_x = afis_scor(stare_curenta)[0]#Preluam scoru de la momentul respectiv
                    scor_0 = afis_scor(stare_curenta)[1]#Preluam scoru de la momentul respectiv
                    print(f"Scorurile sunt X:{scor_x}, 0:{scor_0}.\n")
                    print(
                        f"Timpul minim de rulare a robotului a fost {min(time_list_robot)} milisecunde.\nTimpul maxim de rulare a robotului a fost {max(time_list_robot)} milisecunde.")
                    print(
                        f"Numarul minim de noduri a fost de {min(lista_noduri)},iar numarul maxim a fost {max(lista_noduri)}.")
                    timp_total = 0
                    for i in range(len(time_list_robot)):
                        timp_total = timp_total + time_list_robot[i]
                    print(
                        f"Timpul mediu de rulare a robotului a fost {round(timp_total / len(time_list_robot), 2)}.")
                    nr_total_nod = 0
                    for i in range(len(lista_noduri)):
                        nr_total_nod = nr_total_nod + lista_noduri[i]
                    print(
                        f"Numarul mediu de noduri este de {round(nr_total_nod / len(lista_noduri), 2)}, iar mediana nodurilor este {statistics.median(lista_noduri)}.")
                    print("__________________________________________")
                    time_final = time.time()
                    print(f"Timpul total al rularii este de: {round(time_final - time_initial, 2)} secunde.")
                    pygame.quit()  # inchide fereastra
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    #Optiunea de undo pentru randul jucatorului
                    if event.key == pygame.K_u:
                        lista_mutari.pop()
                        stare_curenta = lista_mutari.pop()
                        print(str(stare_curenta))
                        stare_curenta.tabla_joc.deseneaza_grid(cul=(255, 255, 255))
                        stare_curenta.j_curent = Joc.jucator_opus(Joc.JMIN)
                        pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click
                    pos = pygame.mouse.get_pos()  # coordonatele clickului
                    for linie in range(Joc.NR_LINII):
                        for coloana in range(Joc.NR_COLOANE):

                            if Joc.celuleGrid[linie][coloana].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                ###############################
                                if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                    stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                    stare_curenta.tabla_joc.matr=test_vecini(stare_curenta.tabla_joc.matr, linie, coloana,"")[0]
                                    # for i in range(Joc.NR_LINII):
                                    #     for j in range(Joc.NR_COLOANE):
                                    #         if stare_curenta.tabla_joc.matr[i][j] == Joc.GOL:
                                    #             count_x = 0
                                    #             count_0 = 0
                                    #             if (j - 1) in range(Joc.NR_COLOANE):
                                    #                 if stare_curenta.tabla_joc.matr[i][j - 1] == 'x':
                                    #                     count_x += 1
                                    #                 if stare_curenta.tabla_joc.matr[i][j - 1] == '0':
                                    #                     count_0 += 1
                                    #             if (j + 1) in range(Joc.NR_COLOANE):
                                    #                 if stare_curenta.tabla_joc.matr[i][j + 1] == 'x':
                                    #                     count_x += 1
                                    #                 if stare_curenta.tabla_joc.matr[i][j + 1] == '0':
                                    #                     count_0 += 1
                                    #             if (i - 1) in range(Joc.NR_LINII):
                                    #                 if stare_curenta.tabla_joc.matr[i - 1][j] == 'x':
                                    #                     count_x += 1
                                    #                 if stare_curenta.tabla_joc.matr[i - 1][j] == '0':
                                    #                     count_0 += 1
                                    #                 if (j - 1) in range(Joc.NR_COLOANE):
                                    #                     if stare_curenta.tabla_joc.matr[i - 1][j - 1] == 'x':
                                    #                         count_x += 1
                                    #                     if stare_curenta.tabla_joc.matr[i - 1][j - 1] == '0':
                                    #                         count_0 += 1
                                    #                 if (j + 1) in range(Joc.NR_COLOANE):
                                    #                     if stare_curenta.tabla_joc.matr[i - 1][j + 1] == 'x':
                                    #                         count_x += 1
                                    #                     if stare_curenta.tabla_joc.matr[i - 1][j + 1] == '0':
                                    #                         count_0 += 1
                                    #             if (i + 1) in range(Joc.NR_LINII):
                                    #                 if stare_curenta.tabla_joc.matr[i + 1][j] == 'x':
                                    #                     count_x += 1
                                    #                 if stare_curenta.tabla_joc.matr[i + 1][j] == '0':
                                    #                     count_0 += 1
                                    #                 if (j - 1) in range(Joc.NR_COLOANE):
                                    #                     if stare_curenta.tabla_joc.matr[i + 1][j - 1] == 'x':
                                    #                         count_x += 1
                                    #                     if stare_curenta.tabla_joc.matr[i + 1][j - 1] == '0':
                                    #                         count_0 += 1
                                    #                 if (j + 1) in range(Joc.NR_COLOANE):
                                    #                     if stare_curenta.tabla_joc.matr[i + 1][j + 1] == 'x':
                                    #                         count_x += 1
                                    #                     if stare_curenta.tabla_joc.matr[i + 1][j + 1] == '0':
                                    #                         count_0 += 1
                                    #             if count_x >= 4 and count_x>count_0:
                                    #                 stare_curenta.tabla_joc.matr[i][j] = 'x'
                                                # elif count_0 >= 2:
                                                #     stare_curenta.tabla_joc.matr[i][j] = '0'
                                    # afisarea starii jocului in urma mutarii utilizatorului
                                    counter_mutari_player+=1
                                    print(f"\nTabla dupa mutarea {counter_mutari_player} a jucatorului")
                                    print(str(stare_curenta))
                                    lista_mutari.append(copy.deepcopy(stare_curenta))#Adaugam in stiva mutarile jucatorului
                                    scor_x=afis_scor(stare_curenta)[0]#Preluam scoru de la momentul respectiv
                                    scor_0=afis_scor(stare_curenta)[1]#Preluam scoru de la momentul respectiv
                                    # print(lista_mutari)
                                    stare_curenta.tabla_joc.deseneaza_grid(cul=(255,255,255))
                                    t_final_user=time.time()*1000
                                    print(f"Userul a stat {t_final_user-t_init_user} milisecunde sa aleaga.\n")
                                    # testez daca jocul a ajuns intr-o stare finala
                                    # si afisez un mesaj corespunzator in caz ca da
                                    if (afis_daca_final(stare_curenta,stare_curenta.tabla_joc)):
                                        print(f"Scorurile sunt X:{scor_x}, 0:{scor_0}.\n")
                                        print(
                                            f"Timpul minim de rulare a robotului a fost {min(time_list_robot)} milisecunde.\nTimpul maxim de rulare a robotului a fost {max(time_list_robot)} milisecunde.")
                                        print(
                                            f"Numarul minim de noduri a fost de {min(lista_noduri)},iar numarul maxim a fost {max(lista_noduri)}.")
                                        timp_total = 0
                                        for i in range(len(time_list_robot)):
                                            timp_total = timp_total + time_list_robot[i]
                                        print(
                                            f"Timpul mediu de rulare a robotului a fost {round(timp_total / len(time_list_robot),2)}.")
                                        nr_total_nod = 0
                                        for i in range(len(lista_noduri)):
                                            nr_total_nod = nr_total_nod + lista_noduri[i]
                                        print(
                                            f"Numarul mediu de noduri este de {round(nr_total_nod / len(lista_noduri),2)}, iar mediana nodurilor este {statistics.median(lista_noduri)}.")
                                        print("__________________________________________")
                                        time_final = time.time()
                                        print(f"Timpul total al rularii este de: {round(time_final - time_initial,2)} secunde.")
                                        break

                                    # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                    stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            # counter_noduri_min =0
            # counter_noduri_alpha =0
            # preiau timpul in milisecunde de dinainte de mutare
            ok=0
            init_wait_time=time.time()
            final_wait_time=0
            while final_wait_time-init_wait_time<3:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_u:
                            ok=1
                            lista_mutari.pop()
                            stare_curenta = lista_mutari.pop()
                            print(str(stare_curenta))
                            stare_curenta.tabla_joc.deseneaza_grid(cul=(0, 0, 255))
                            stare_curenta.j_curent = Joc.jucator_opus(Joc.JMAX)
                            pygame.display.flip()
                final_wait_time=time.time()
            if ok==1:
                continue
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                counter_nod_min=0
                stare_actualizata = min_max(stare_curenta)
                lista_noduri.append(counter_nod_min)
            else:  # tip_algoritm==2
                counter_nod_alpha = 0
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                lista_noduri.append(counter_nod_alpha)
            print(F"Estimarea facuta de robot este:{stare_actualizata.estimare}.")
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            counter_mutari_robot += 1
            print(f"Tabla dupa mutarea {counter_mutari_robot} a calculatorului")
            print(str(stare_curenta))
            lista_mutari.append(copy.deepcopy(stare_curenta))#Adaugam in stiva mutarile robotului
            scor_x = afis_scor(stare_curenta)[0]
            scor_0 = afis_scor(stare_curenta)[1]
            stare_curenta.tabla_joc.deseneaza_grid(cul=(0,0,255))
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            if tip_algoritm=='1':
                print(f"Numarul de noduri al acestei mutari este de: {counter_nod_min}.")
                # print(stare_actualizata.mutari_posibile)
            else:
                print(f"Numarul de noduri al acestei mutari este de: {counter_nod_alpha}.")
                # print(stare_actualizata.mutari_posibile)
            t_init_user = time.time() * 1000
            time_list_robot.append(t_dupa-t_inainte)
            scor_x = afis_scor(stare_curenta)[0]  # Preluam scoru de la momentul respectiv
            scor_0 = afis_scor(stare_curenta)[1]  # Preluam scoru de la momentul respectiv
            if (afis_daca_final(stare_curenta,stare_curenta.tabla_joc)):
                print(f"Scorurile sunt X:{scor_x}, 0:{scor_0}.\n")
                print(
                    f"Timpul minim de rulare a robotului a fost {min(time_list_robot)} milisecunde.\nTimpul maxim de rulare a robotului a fost {max(time_list_robot)} milisecunde.")
                print(f"Numarul minim de noduri a fost de {min(lista_noduri)},iar numarul maxim a fost {max(lista_noduri)}.")
                timp_total = 0
                for i in range(len(time_list_robot)):
                    timp_total = timp_total + time_list_robot[i]
                print(f"Timpul mediu de rulare a robotului a fost {round(timp_total / len(time_list_robot),2)} milisecunde, iar mediana este {statistics.median(time_list_robot)} milisecunde"
                      f".")
                nr_total_nod=0
                for i in range(len(lista_noduri)):
                    nr_total_nod=nr_total_nod+lista_noduri[i]
                print(f"Numarul mediu de noduri este de {round(nr_total_nod/len(lista_noduri),2)}, iar mediana nodurilor este {statistics.median(lista_noduri)}.")
                print("__________________________________________")
                time_final=time.time()
                print(f"Timpul total al rularii este de: {round(time_final-time_initial,2)} secunde.")
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()