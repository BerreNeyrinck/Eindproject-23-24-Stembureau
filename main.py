import random
from jinja2 import *

achternamen = ["De Bruyn", "Peeters", "Janssen", "Mertens", "Van den Bergh", "Verheyen", "De Smet", "Van der Linden", "Van Acker", "De Clercq", "Dubois", "Lambert", "Martin", "Dupont", "Leroy", "Leclercq", "Bertrand", "Michel", "Lefebvre", "Mathieu"]
voornamen = ["Mila", "Emma","Olivia", "Noor", "Luna", "Lotte", "Marie", "Anna", "Sarah", "Evy", "Noah", "Arthur", "Liam", "Finn", "Leon", "Lucas", "Adam", "Max", "Elias", "Victor"]


class Kiezer(): #Een persoon die stemt, mag slechts één keer stemmen
    def __init__(self, voornaam, achternaam, leeftijd):
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.leeftijd = leeftijd

    def __str__(self) -> str: #string om de representatie van het object aan te passen
        return f"({self.voornaam} {self.achternaam}. Age{self.leeftijd})"

    def __repr__(self) -> str: #"repr = represent" oftewel "representeert" de return value het object. (zorgt dat je niet "object at ..." krijgt.)
        return self.__str__()

class Kandidaat(Kiezer): #Een persoon die op een lijst staat en stemmen ontvangt. inheritance for the win :)
    stemmen = 0
    pass

class Lijst(): #Een verzameling van kandidaten onder een specifieke partij of groepering.
    partijlijst = ['lijst 1', 'lijst 2', 'lijst 3', 'lijst 4', 'lijst 5'] #Hardcoded vanwege index out of range error met "stemcomputer" klasse(?) vanwege hoisting denkt de stemcomputer dat deze partijen lijst leeg is

    def __init__(self, partij, kandidaten) -> None: #vraagt lijst aan kandidaten
        self.partij = partij
        Lijst.partijlijst.append(partij)
        self.kandidaten = kandidaten #kandidaten = lijst van kandidaten!
        print(f"{self.partij} Leden: {self.kandidaten}")

    def __str__(self) -> str: #string om de representatie van het object aan te passen
        return f"'{self.partij}'"

    def __repr__(self) -> str: #"repr = represent" oftewel "representeert" de return value van het object. (zorgt dat je niet "object at <adress>" krijgt.)
        return self.__str__()
    
class Stembiljet(): #product van stemcomputer, bevat lijststem of voorkeurstem
    def __init__(self, soortStem, partij, code, namen = []) -> None:
        self.soortStem = soortStem
        self.partij = partij
        self.code = code
        self.namen = namen
    
    def __str__(self) -> str: #string om de representatie van het object aan te passen
        return f"({self.soortStem}, {self.partij}. Leden: {self.namen})"

    def __repr__(self) -> str: #"repr = represent" oftewel "representeert" de return value het object. (zorgt dat je niet "object at ..." krijgt.)
        return f"'{self.partij}'"
    

class Stembus(): #verzameld biljetten, heeft een scanner die de stemmen optelt!
    verzameldeBiljetten = []
    voorkeurstemmen = {
        "'lijst 1'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 2'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 3'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 4'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 5'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, } 
        }
    Lijststemmen = {} #wordt gemaakt door code

    actief = False
    def __init__(self, USB) -> None:
        if (USB.code == 567890):
            print("De machine staat nu aan!")
            self.scanner = Scanner(USB.code)
            self.actief = True
            self.code = USB.code
        else:
            print("De code op de USB-Stick was niet correct!")
    def voegStemToe(self, biljet, chipkaart):
        if(self.scanner.code != biljet.code):
            print("QR code komt niet overeen met dit bureau!")
        else:
            #chipkaart terug geven aan de balie
            chipkaart.initialiseer(self.code)
            self.verzameldeBiljetten.append(biljet)
            if(biljet.soortStem == "lijstStem"): #werkt door de keys van de dict de objecten zelf te maken. Wordt gedaan vanwege key errors en index out of range zoals hierboven besproken.
                if biljet.partij in self.Lijststemmen:
                    self.Lijststemmen[biljet.partij] += 1
                    USBStick.Lijststemmen[biljet.partij] += 1
                else:
                    self.Lijststemmen[biljet.partij] = 1
                    USBStick.Lijststemmen[biljet.partij] = 1
            else:
                for y in biljet.namen:
                    self.voorkeurstemmen[str(biljet.partij)][f"kandidaat{y+1}"] += 1 #key errors all the way
                    USBStick.voorkeurstemmen[str(biljet.partij)][f"kandidaat{y+1}"] += 1
            print("stem opgeslagen!")

class Scanner(): #onderdeel v.d stembus, heeft ook een code nodig.
    def __init__(self, code) -> None:
        self.code = code
        

class Stemcomputer(): #geactiveerd door USB, gaat per kiezer met een chipkaart af hoe en op wie ze stemmen. DRUKT BILJETTEN AF!!(returned biljetten)
    aantalLijstStemmen = 0
    aantalVoorkeurStemmen = 0
    def __init__(self, USB, stembus) -> None:
        if (USB.code == 567890):
            print("De Stemcomputer staat nu aan!")
            self.code = USB.code
            self.actief = True
            self.stembus = stembus
        else:
            print("De code op de USB-Stick was niet correct!")
    
    def lijstStem(self, chipkaart, partijKeuze) ->None: 
        if (chipkaart.code == self.code):
            biljet = Stembiljet("lijstStem", partijKeuze, self.code)
            chipkaart.maakt_gebruik()
            print("stem doorgekomen")
            self.stembus.voegStemToe(biljet, chipkaart)

    def voorkeurStem(self, chipkaart, partijKeuze, gestemdeNamen) ->None:
        if (chipkaart.code == self.code):
            biljet = Stembiljet("voorkeurStem", partijKeuze, self.code, gestemdeNamen)
            chipkaart.maakt_gebruik()
            print("stem doorgekomen")
            self.stembus.voegStemToe(biljet, chipkaart)

class Chipkaart():
    def __init__(self) -> None:
        self.code = None
    
    def initialiseer(self, code):
        self.code = code
        print("Chipkaart ge-initialiseerd, code wordt geactiveerd")
    
    def maakt_gebruik(self):
        self.code = None
        print("Chipkaart in gebruik, code wordt gedeactiveerd")

class USBStick():
    code = 0000 
    voorkeurstemmen = {
        "'lijst 1'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 2'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 3'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 4'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, },
        "'lijst 5'" : {"kandidaat1" : 0, "kandidaat2" : 0, "kandidaat3" : 0, "kandidaat4" : 0, "kandidaat5" : 0, "kandidaat6" : 0, "kandidaat7" : 0, "kandidaat8" : 0, "kandidaat9" : 0, "kandidaat10" : 0, } 
        }
    Lijststemmen = {}
    def __init__(self, code) -> None: #code instellen bij init
        self.code = code



def main():
    kiezers = []
    USB = USBStick(567890)
    Stembus1 = Stembus(USB)

    for x in range(0, 1200): #Eerst maken we de kiezers
        name = f"kiezer {x}"
        name = Kiezer(voornamen[random.randint(0,19)], achternamen[random.randint(0,19)], leeftijd = random.randint(18,90))
        kiezers.append(name)

    gekozenKandidaten = []
    lijstObjecten = []
    for x in range(0, 5): #hier maken we de lijsten aan
        name = f"lijst {x+1}" 
        kandidaten = []
        while(len(kandidaten) < 10): #hier vullen we de lijsten met 10 kandidaten elks.
            r = random.randint(0, len(kiezers)-1)
            if(r not in gekozenKandidaten):
                kiezer = kiezers[r]
                voornaam = kiezer.voornaam
                achternaam = kiezer.achternaam
                leeftijd = kiezer.leeftijd
                gekozenKandidaten.append(r)
                kandidaat = Kandidaat(voornaam, achternaam, leeftijd)
                kandidaten.append(kandidaat) #Q22/05 Sommige lijsten hebbe maar 9/10 kandidaten? [A: gefixt met while loop]
            else:
                continue
        name = Lijst(name, kandidaten)
        lijstObjecten.append(name)
    chipkaarten = []
    for x in range(0,60): #hier maken en initialiseren we de chipkaarten voor de stemcomputers
        name = f"chipkaart{x+1}"
        name = Chipkaart()
        name.initialiseer(USB.code) #gewoon simpel de code van de usb pakken, handig als de code zou veranderen
        chipkaarten.append(name)
        
    
    #check na of kiezer al aanwezig is in "gestemd"
    #random (1 op 3), voor stemcomputer. 
    #foreach met kiezer list.
    computer1 = Stemcomputer(USB, Stembus1)
    computer2 = Stemcomputer(USB, Stembus1)
    computer3 = Stemcomputer(USB, Stembus1)

    gestemd = [] #hier laten we de kiezers een voor een een "keuze" maken voor welke stemcomputer en stem ze zullen doen.
    for x in kiezers:
        if(x in gestemd):
            continue
        else:
            randomComputer = random.randint(1,3)
            keuzeSoort = random.randint(1,2)
            lijstKeuze = random.randint(0,4)

            match (randomComputer):
                case 1: 
                    gestemd.append(x)
                    if(keuzeSoort == 1):
                        computer1.lijstStem(chipkaarten[random.randint(0, 59)],lijstObjecten[lijstKeuze]) #random chipkaart met random lijststem :)
                        # print("een lijststem werd uitgevoerd op computer1")
                    else:

                        #hier maken we een random length list voor x aantal naamstemmingen mee te geven
                        hvlheid = random.randint(1,10)
                        persoonStemmen = []
                        for x in range(0, hvlheid):
                            # keuze = lijstObjecten[lijstKeuze].kandidaten[random.randint(0,8)]
                            keuze = random.randint(0,9) #index i.p.v naam om tellingen makkelijker te coderen.
                            if(keuze not in persoonStemmen):
                                persoonStemmen.append(keuze) #help
                            else:
                                x -= 1 #opnieuw proberen

                        computer1.voorkeurStem(chipkaarten[random.randint(0, 59)],lijstObjecten[lijstKeuze], persoonStemmen)
                        # print("een voorkeurstem werd uitgevoerd op computer1")
                    continue

                case 2:
                    gestemd.append(x)
                    if(keuzeSoort == 1):
                        computer2.lijstStem(chipkaarten[random.randint(0, 59)],lijstObjecten[lijstKeuze]) #random chipkaart met random lijststem :)
                        # print("een lijststem werd uitgevoerd op computer2")
                    else:

                        #hier maken we een random length list voor x aantal naamstemmingen mee te geven
                        hvlheid = random.randint(1,10)
                        persoonStemmen = []
                        for x in range(0, hvlheid+1):
                            # keuze = lijstObjecten[lijstKeuze].kandidaten[random.randint(0,8)]
                            keuze = random.randint(0,9)
                            if(keuze not in persoonStemmen):
                                persoonStemmen.append(keuze) #help
                            else:
                                x -= 1 #opnieuw proberen

                        computer2.voorkeurStem(chipkaarten[random.randint(0, 59)],lijstObjecten[lijstKeuze], persoonStemmen)
                        # print("een voorkeurstem werd uitgevoerd op computer2")
                    continue

                case 3:
                    gestemd.append(x)
                    if(keuzeSoort == 1):
                        computer3.lijstStem(chipkaarten[random.randint(0, 59)],lijstObjecten[lijstKeuze]) #random chipkaart met random lijststem :)
                        # print("een lijststem werd uitgevoerd op computer3")
                    else:

                        #hier maken we een random length list voor x aantal naamstemmingen mee te geven
                        hvlheid = random.randint(1,10)
                        persoonStemmen = []
                        for x in range(0, hvlheid+1):
                            # keuze = lijstObjecten[lijstKeuze].kandidaten[random.randint(0,8)]
                            keuze = random.randint(0,9)
                            if(keuze not in persoonStemmen):
                                persoonStemmen.append(keuze) #help
                            else:
                                x -= 1 #opnieuw proberen

                        computer3.voorkeurStem(chipkaarten[random.randint(0, 59)],lijstObjecten[lijstKeuze], persoonStemmen)
                        # print("een voorkeurstem werd uitgevoerd op computer3")
                    continue

    #lezen!!! Om de html output leesbaarder en meer variabel te maken gaan we "kandidaat X" vervangen door zijn echte naam op het einde van de code.
    for x in range(0,5):
        for y in range(1, 11):
            USBStick.voorkeurstemmen[f"'lijst {x+1}'"][lijstObjecten[x-1].kandidaten[y-1]] = USBStick.voorkeurstemmen[f"'lijst {x+1}'"].pop(f"kandidaat{y}")

    #hieronder passen we de formule van d'Hondt toe om de zetelverdeling toe te passen. We veronderstellen dat er ZEVEN zetels te verdelen zijn!
    def deling(x):
        return round(x / _, 2)
    
    def kiesdeler(x):
        kiesdeler = sum(USB.Lijststemmen.values()) / 10 #aangepast voor een meer variabele zetelverdeling
        if(x <= kiesdeler):
            return
        else:
            return x
        
    zetelResultaat = {1:0, 2:0, 3:0, 4:0} #de lijst zetelResultaat behoud nu de zetels die kunnen worden uitgedeeld
    partijZetels = {1:0, 2:0, 3:0, 4:0, 5:0}
    for _ in range(1,5): #we voeren 4 delingen uit | Deze for loop gaat nu effectief elke partij af en deelt de totale stemmen door "_"(1 tot 4) Je kan "print(zetelResultaat)" uitvoeren voor een mooi beeld van de map te krijgen
        result = map(deling, list(USB.Lijststemmen.values()))
        result = map(kiesdeler, result)
        zetelResultaat[_] = list(result)

    for x in range(0, len(zetelResultaat)):
        for y in range(0, len(zetelResultaat[x+1])):
            if(zetelResultaat[x+1][y] != None):
                partijZetels[y+1] += 1
    # print(zetelResultaat)
    # print(partijZetels)
    
    res = {}
    res2 = {}
    for key, val in USB.voorkeurstemmen.items():
        max_val = 0
        sec_max_val = 0
        for elem in val.values():
            if elem > max_val:
                max_val = elem
            else:
                sec_max_val = elem
        res[key] = max_val
        res2[key] = sec_max_val

    # for x in len(partijZetels):
    #     if(partijZetels[x] != 0):
    #         print(USB.voorkeurstemmen[x].values())


    #jinja2 html template vullen met onze waardes
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('Week11_Eindopdracht/Jinja_Templates/template.html')
    output = template.render(voorkeur=USBStick.voorkeurstemmen, lijst = USBStick.Lijststemmen, zetels = partijZetels)

    with open("Week11_Eindopdracht/output.html", 'w', encoding='utf-8') as f:
        f.write(output)
    print("\n code uitgevoerd.")
main()
