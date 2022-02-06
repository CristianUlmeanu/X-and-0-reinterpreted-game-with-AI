# X and 0 reinterpreted game with AI
 Created a X and 0 kind of game with a bot to play against

# Game explanations:

Se va implementa urmatorul joc:
Jocul se desfasoara pe un grid NxM cu 10≥N,M≥5, macar unul dintre M, N trebuie sa fie par (utilizatorul va fi întrebat în legătură cu dimensiunea tablei).
Este turn based
Un jucator foloseste simbolul x si celalalt 0 ( o sa ii numim pe scurt jucatorii x si 0)
Jucatorul x pune simbolul primul pe tabla.
Simbolurile se pun in locurile libere ale tablei. In momentul in care o casuta libera e inconjurată (pe linie, coloana, diagonala) de minim 4 simboluri de acelasi fel (iar celalalt jucator are mai putine simboluri in jurul casutei libere), casuta este marcata cu simbolul majoritar din jurul ei. Daca in urma marcarii exista o alta casuta libera care acum are minim 4 simboluri in jurul ei, este marcata si aceea pana nu mai exista casute libere in aceasta situatie. Daca sunt in jurul unei casute sunt mai mult de 4 simboluri si de-ale lui x si de-ale lui 0, numarul de x si de 0 e egal, casuta ramane necompletata, pana se schimba situatia.
De exemplu, în imaginea de mai jos, presupunem că ultima mutare a lui x este x-ul albastru. Deoarece s-au adunat 4 simboluri x vecine față de o căsuță liberă, este adaugat automat x-ul verde. În urma adăugării lui avem o altă poziție cu 4 vecini x, cea pe care s-a pus x-ul portocaliu, care duce la adăugarea x-ului roz, și apoi a celui mov:
mutare

![alt text](https://github.com/CristianUlmeanu/X-and-0-reinterpreted-game-with-AI/blob/Local/x-si-0-simbol-majoritar(mutare).png?raw=true)

Jocul se termina cand se umple tabla. Castiga jucatorul cu cele mai multe simboluri pe tabla.
La afișarea gridului în consolă, se vor afișa în dreptul liniilor și coloanelor și numerele lor (indicii începând de la 0) ca să poată identifica utilizatorul mai ușor coordonatele locului în care vrea să mute.


# Requirements

 1. Să se păstreze următoare lucruri deja implementate în exemplu (sau să se implementeze daca cineva decide să refacă programul de la zero):
    - La inceputul programului utilizatorul va fi intrebat ce algoritm doreste sa foloseasca (minimax sau alpha-beta)
    - Utilizatorul va fi întrebat cu ce simbol sa joace (la jocurile unde are sens aceasta intrebare)
    - Se va încerca evitarea sau tratarea situației în care utilizatorul ar putea răspunde greșit (de exemplu, nu poate selecta decât opțiunile corecte dintre care sunt selectate valorile default; sau, unde nu se poate așa ceva, jocul nu pornește până nu se primește un răspuns corect).
    - Afisarea a cui este rândul să mute.
    - Indicarea, la finalul jocului, a câstigatorului sau a remizei daca este cazul.
 2. Utilizatorul va fi întrebat care sa fie nivelul de dificultate a jocului (incepator, mediu, avansat). In functie de nivelul ales se va seta adancimea arborelui de mutari (cu cat nivelul ales e mai mare, cu atat adancimea trebuie sa fie mai mare ca sa fie mai precisa predictia jocului). Posibilitatea utilizatorului de a face eventuale alte setări cerute de enunț. Se va verifica dacă utilizatorul a oferit un input corect, iar dacă nu se va trata acest caz (i se poate reafișa ecranul cu setările afișând și un mesaj de atenționare cu privire la inputul greșit).
 3. Generarea starii initiale
 4. Desenarea tablei de joc (interfața grafică) si afișarea în consolă a tablei (pentru debug; în ce format vreți voi). Titlul ferestrei de joc va fi numele vostru + numele jocului.
 5. Functia de generare a mutarilor (succesorilor) + eventuala functie de testare a validitatii unei mutari (care poate fi folosita si pentru a verifica mutarea utilizatorului)
 6. Realizarea mutarii utilizatorului. Utilizatorul va realiza un eveniment în interfață pentru a muta (de exemplu, click). Va trebui verificata corectitudinea mutarilor utilizatorului: nu a facut o mutare invalida.
 7. Functia de testare a starii finale, stabilirea castigatorului și, dacă e cazul conform cerinței, calcularea scorului. Se va marca în interfața grafică configurația câștigătoare (sau simbolurile câștigătoare, în funcție de regulile jocului). Marcarea se poate face colorând, de exemplu, simbolurile sau culoare de fundal a eventualelor căsuțe în care se află.
 8. Doua moduri diferite de estimare a scorului (pentru stari care nu sunt inca finale)
 9. Afisari (în consolă).
    - Afisarea timpului de gandire, dupa fiecare mutare, atat pentru calculator (deja implementat în exemplu) cat si pentru utilizator. Pentru timpul de găndire al calculatorului: afișarea la final a timpului minim, maxim, mediu și a medianei.
    - Afișarea scorurilor (dacă jocul e cu scor), atat pentru jucator cat si pentru calculator și a estimărilor date de minimax și alpha-beta (estimarea pentru rădacina arborelui; deci cât de favorabilă e configurația pentru calculator, în urma mutării sale - nu se va afișa estimarea și când mută utilizatorul).
    - Afișarea numărului de noduri generate (în arborele minimax, respectiv alpha-beta) la fiecare mutare. La final se va afișa numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare.
    - Afisarea timpului final de joc (cat a rulat programul) si a numarului total de mutari atat pentru jucator cat si pentru calculator (la unele jocuri se mai poate sari peste un rand și atunci să difere numărul de mutări).
 10. La fiecare mutare utilizatorul sa poata si sa opreasca jocul daca vrea, caz in care se vor afisa toate informațiile cerute pentru finalul jocului ( scorul lui si al calculatorului,numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare, timpul final de joc și a numarului total de mutari atat pentru jucator cat si pentru calculator) Punctajul pentru calcularea efectivă a acestor date e cel de mai sus; aici se punctează strict afișarea lor în cazul cerut.
 11. Comentarii. Explicarea algoritmului de generare a mutarilor, explicarea estimarii scorului si dovedirea faptului ca ordoneaza starile cu adevarat in functie de cat de prielnice ii sunt lui MAX (nu trebuie demonstratie matematica, doar explicat clar). Explicarea pe scurt a fiecarei functii si a parametrilor.

## Bonuses

Bonus 1. Ordonarea succesorilor înainte de expandare (bazat pe estimare) astfel încât alpha-beta să taie cât mai mult din arbore.

Bonus 2. Opțiuni în meniu (cu butoane adăugate) cu:
     - Jucator vs jucător
     - Jucător vs calculator (selectată default)
     - Calculator (cu prima funcție de estimare) vs calculator (cu a doua funcție de estimare)
     
Bonus 3. Cand vine randul jucatorului sa mute, sa se marcheze pe interfata grafica pozitiile valide in care poate plasa un simbol.

Bonus 4. Pentru adancimi mai mari de 3 sa se salveze arborele alphabeta si sa se plece de la ce este calculat deja pentru aflarea urmatoarei mutari a calculatorului (ca sa nu fie recalculate mutarile la urmatoarea iteratie). Practic memoram subarborele mutarii alese din arborele alpha-beta generat anterior. Apoi jucatorul face mutarea M. Cautam in subarborele salvat mutarea jucatorului si pornim de la subarborele generat deja pentru ea si il continuam pentru a afla noua mutare a calculatorului.

Bonus 5. Implementati optiunea de undo. La apasarea tastei u, se da undo ultimei mutari facute a utilizatorului. De la al doilea "undo" incolo se anuleaza mutarea calculatorului + mutarea jucatorului (practic se anuleaza mutarea jucatorului si raspunsul calculatorului).

Bonus 6. La apasarea tastei n la inceputul turn-ului jucatorului (cand jucatorul inca nu a facut vreo mutare) calculatorul isi va schimba (inlocui) mutarea cu urmatoarea cea mai buna dintre mutarile posibile. Apasari succesive ale lui n, ar afisa pe tabla pe rand de la cea mai buna mutare la cea mai slaba. Daca se apasa n si dupa cea mai slaba se reafiseaza cea mai buna (lista e luata de la inceput).

Bonus 7. Optiunile de inrerupere, salvare si continuare joc. La apasarea tastei s, starea jocului se va salva intr-un fisier text (numele fisierului va fi cerut utilizatorului - acesta poate introduce numele fie in interfata grafica fie in consola). Fisierul va fi salvat intr-un folder numit "salvari" al jocului. La intrarea in joc, utulizatorul va primi ca prima intrebare din partea programului daca vrea sa incarce un joc si i se va afisa continutul fiserului de salvari, fiecare fisier avand un numar de ordine. Utilizatorul va raspunde cu numarul de ordine si va putea continua jocul din stadiul in care l-a lasat (tabla si alti parametri se vor incarca din fisier).
