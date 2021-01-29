PASI:
1. Trebuie instalat python 3(in linux el este) 
2. instalam git
3. deschidem terminalul sau cmd si navigam in folderul in care vrem sa lucram 
4. clonam cu git spatiu de stocare de pe github in folderul in care vrem sa lucram; de ex cu http: 

                         git clone https://github.com/iamarcadie/project_face_app.git 

                        *link la proiect: https://github.com/iamarcadie/project_face_app

5. creem un mediu virtual: 

            linux(sau git bash care se instaleaza pe windows o data cu git):(~$)    
                            python3 -m venv env
            cmd(windows):   python -m venv env

6. activam mediul virtual:

                        linux: source env/bin/activate
                        cmd: env\Scripts\activate.bat

7. instalam bibliotecile necesare cu pip(Cele mai recente versiuni de Python vin cu PIP preinstalat):

        nu am tinut cont de versiunile bibiotecilor si deci se vor instala ultimele versiuni 

                         pip install -r requirements.txt

8. acum putem incepe... sunt doua abordari: 

        I.  rulam fisierul app.py ( pyhon app.py ) dupa deschidem in browser: http://0.0.0.0:5000/
          
            pagina este vizibila in reteaua locala deci cu adresa ip a dispozitivului la portul 5000 putem accesa aplicatia de pe alt dispozitiv decat cel de pe care ruleaza : http://ip:5000/

            daca vrem sa adaugam o fata noua si sa antrenam modelul urmam pasii:

            1. dam click pe CREATE DATASET 
            2. scriem in forma numele si dam click pe Colect data button
                    acum in linia de comanda trebuie sa introduci numele (dupa urmariti pagina web) 
                    pe pagina web o data ce a fost detectata o fata, incepe colectarea setului de date(se captureaza 50 de poze cu zona fetei)
                    _cu opencv nu putem controla un framerate a camerei web, depinde de capacitatile hardware a dispozitivului pe care ruleaza aplicatia
            3. antrenam modelul:
            Dam click pe TRAIN MODEL (astemtam putin pana se incarca pagina)
            4. important!! 
            
                        oprim aplicatia din linia de comanda si o rulam din nou
               
            din motiv ca folosim fisiere pentru a pastra date in sistem si
            la initializarea aplicatiei creem variabile direct dependente de fisiere
            a caror valoare va ramane constanta pe parcursul executiei, in timp ce facem modificari in fisiere,
            apar conflicte (la sfarsit propun o solutie pentru imbunatatire) 

            5. acum ca am rulat din nou aplicatia ,pe pagina Recognise aplicatia este capabila sa recunoasca
                fata recent adaugata in setul de date,antrenata.( in cmd sunt printate date despre obiectul situat in fata camerei,
                am reusit sa le pun intr un camp txt cu scoll in browser dar nu am implimentat asta in
                "versiunea finala")

A doua abordare: rulam fiecare fisier din terminal fara a apela la aplicatia web:
            (ambele programe afiseaza o fereastra dupa rulare cu imaginea prelucrata de la camera)

            1. Rulam Train_cmd.py
                ( python3 Train_cmd.py )(in windows cmd: python Train_cmd.py)
                acest program colecteaza setul de date si antreneaza modelul
                dupa ce rulam oferim datele cerute in cmd
            2. Rulam Recognise.py

Pentru a vedea cum functioneaza algoritmul de detectare a culorii pielii:

rulam skin_seg.py
sciem in linia de comanda:
        
        python3 skin_seg.py images/img1.jpg
        
unde "images/img1.jpg" poate fi calea catre oricare alta imagine

Pentru a vedea cum functioneaza algoritmul LBPH:
rulam LPB.py

        python3 LPB.py

in linia 254 
dupa 'if __name__ == "__main__":' este variabila path_img careia ii putem atribui calea catre imaginea dorita



                            !!! upgrade:


daca folosim pentru stocarea datelor o baza de date problema cu repornirea aplicatiei poate fi depasita
putem folosi bibioteca 'sqlalchemy' care permite lucru efectiv cu o baza de date in python 
 
problema cu scrierea numelui in terminal la colectarea setului de date la fel va disparea.

presupun ca nu reuseam sa aduc numele in fuctia dorita ptru ca foloseam functiile de vizualizare din flask
din care incercam sa extrag numele intr o variabila globala de tip lista...ceea ce nu am reusit
totusi poluarea programului cu variabile globale este o deprindere proasta, 
asa ca mai bine renunt la acea idee


                calitatea recunoasterii poate scadea din cauza calitatii setului de date
                ( imaginile trebuie sa fie cat mai calitative )

                trebuie evitate miscarile bruste in tipul colectarii pozelor

                si pozele trebuie sa contina nu doar partea frontala a fetei, dar si putin din laterala 
         
        
                !!!! IMPORTANT !!!!
                pentru raspberryPI exista multe dependente 
                mai jos este un link cu pasii pentru a crea un mediu virtual si pentru a instala opencv!
                (avem nevoie si de opencv-contrib ptru ca detine functii de care avem nevoie)
                
https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
