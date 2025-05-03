from bs4 import BeautifulSoup
import requests

# Question 2
class NonValide(Exception) :

    def __init__(self, message) :
        super().__init__(message)


# Question 1
def getsoup(page) : 
    html_content = requests.get(page).text
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


#Question 3
def prix(soup) :
    prix = soup.find("p", class_ = "product-price")
    if(prix == None) :
        raise NonValide("Prix non trouvé")
    prix = prix.text
    prix = prix.replace(" ", "")
    prix = prix.replace("€", "")
    prixInt = int(prix)
    if prixInt <= 10000 : 
        raise NonValide("Prix inférieur à 10 000€")
    return prix


#Question 4
def ville(soup) : 
    lieu = soup.find("h2", class_ = "mt-0")
    if(lieu == None) :
        raise NonValide("Ville non trouvée")
    lieu = lieu.text
    DerniereVirgule = lieu.rfind(",")
    ville = lieu[DerniereVirgule + 2:] #pour sauter l'espace
    return ville


#Question 5

def caracteristiqueHTML(soup) :
    caracteristiquesHTML = soup.find("div", class_= "product-features").find("div").find("ul")
    if(caracteristiquesHTML == None) :
        raise NonValide("Caractéristiques non trouvées")
    return caracteristiquesHTML


#Type de logement
def type(soup) :
    list = caracteristiqueHTML(soup).find_all("li")
    for li in  list:
        if(li.find("span", class_="text-muted").text == "Type" and
          (li.find("span", "fw-bold").text == "Maison" or li.find("span", "fw-bold").text == "Appartement")) :
            try : 
                prix(soup)
                return li.find("span", "fw-bold").text
            except NonValide as erreur :
                print("Annonce :", erreur)
        
    raise NonValide("Type différent de Maison ou Appartement")

#Surface
def surface(soup) : 
    list = caracteristiqueHTML(soup).find_all("li")
    for li in  list:
        if(li.find("span", class_="text-muted").text == "Surface") :
            surface = li.find("span", "fw-bold").text
            return surface.split(" ")[0]
        
    if(type(soup) == "Maison" or type(soup) == "Appartement") :
        try : 
            prix(soup)
            return "-"
        except NonValide as erreur :
            print("Annonce :", erreur)
    else :
        raise NonValide("N'est pas une maison ou un appartement")


#nbr de piece
def nbrpieces(soup) : 
    list = caracteristiqueHTML(soup).find_all("li")
    for li in  list:
        if(li.find("span", class_="text-muted").text == "Nb. de pièces") :
            return li.find("span", "fw-bold").text
        
    if(type(soup) == "Maison" or type(soup) == "Appartement") :
        try : 
            prix(soup)
            return "-"
        except NonValide as erreur :
            print("Annonce :", erreur)
    else :
        raise NonValide("N'est pas une maison ou un appartement")



#nbr de chambres
def nbrchambres(soup) : 
    list = caracteristiqueHTML(soup).find_all("li")
    for li in  list:
        if(li.find("span", class_="text-muted").text == "Nb. de chambres") :
            return li.find("span", "fw-bold").text
        
    if(type(soup) == "Maison" or type(soup) == "Appartement") :
        try : 
            prix(soup)
            return "-"
        except NonValide as erreur :
            print("Annonce :", erreur)
    else :
        raise NonValide("N'est pas une maison ou un appartement")


#nbr salle bain 
def nbrsdb(soup) : 
    list = caracteristiqueHTML(soup).find_all("li")
    for li in  list:
        if(li.find("span", class_="text-muted").text == "Nb. de sales de bains") :
            return li.find("span", "fw-bold").text
        
    if(type(soup) == "Maison" or type(soup) == "Appartement") :
        try : 
            prix(soup)
            return "-"
        except NonValide as erreur :
            print("Annonce :", erreur)
    else :
        raise NonValide("N'est pas une maison ou un appartement")


#dpe Consommation d'énergie (DPE)
def dpe(soup) : 
    list = caracteristiqueHTML(soup).find_all("li")
    for li in  list:
        if(li.find("span", class_="text-muted").text == "Consommation d'énergie (DPE)") :
            dpe = li.find("span", "fw-bold").text
            return dpe.split(' ')[0]
        
    if(type(soup) == "Maison" or type(soup) == "Appartement") :
        try : 
            prix(soup)
            return "-"
        except NonValide as erreur :
            print("Annonce :", erreur)
    else :
        raise NonValide("N'est pas une maison ou un appartement")

#Question 6
def informations(soup) : 
    info = ville(soup) + "," + type(soup) + "," + surface(soup) + "," + nbrpieces(soup) + "," +  nbrchambres(soup) + "," + nbrsdb(soup) + "," + dpe(soup) +  "," + prix(soup)
    if(info == None) :
        raise NonValide("Information non trouvée ou n'est pas une maison ou un appartement")
    return info

#Question 7
def getListOfAnnoncesLink(soup) :
    listAnnonces = soup.find_all("div", class_="row product shadow p-2 rounded-3")
    return listAnnonces

def getNextPage(soup) :
    nextPage = soup.find("ul", class_="pagination").find("li", class_="next").find("a")
    if(nextPage == None) :
        raise NonValide("Fin des annonces")
    return "https://www.immo-entre-particuliers.com" + nextPage.get("href")

def writeInCSV(soup, nbrPage) :
    listAnnonces = getListOfAnnoncesLink(soup)
    f = open("annonces.csv", "a")
    if nbrPage == 1 :
        f.write("Ville,Type,Surface,NbPieces,NbChambres,NbSDB,DPE,Prix\n")

    for annonces in listAnnonces :
        a = "https://www.immo-entre-particuliers.com" + annonces.find("a", class_="box-link").get("href")
        soupAnnonce = getsoup(a)
        information = ""
        try :
            information = informations(soupAnnonce)
            print(information)
            f.write(information + "\n")
        except NonValide as erreur :
            print("Annonce :", erreur)

    f.close()
    try :
        nextPage = getNextPage(soup)
        soupNextPage = getsoup(nextPage)
        nbrPage += 1
        print("Changement de Page, page : ", nbrPage)
        writeInCSV(soupNextPage, nbrPage)
    except NonValide as erreur :
        print(erreur)

#MAIN
soup = getsoup("https://www.immo-entre-particuliers.com/annonces/france-ile-de-france/vente/ta-offer/")
writeInCSV(soup, 1)