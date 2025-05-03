import pandas as pd

#DEUXIEME JALON

# Question 8
annonces = pd.read_csv("annonces.csv", encoding="ISO-8859-1")

# Question 9
annonces.DPE = annonces.DPE.replace("-","Vierge")

# Question 10
annonces.Surface = annonces.Surface.replace("-", pd.NA).astype("Int64")
annonces.Surface = annonces.Surface.replace(pd.NA, int(annonces.Surface.mean()))

annonces.NbPieces = annonces.NbPieces.replace("-", pd.NA).astype("Int64")
annonces.NbPieces = annonces.NbPieces.replace(pd.NA, int(annonces.NbPieces.mean()))

annonces.NbChambres = annonces.NbChambres.replace("-", pd.NA).astype("Int64")
annonces.NbChambres = annonces.NbChambres.replace(pd.NA, int(annonces.NbChambres.mean()))

annonces.NbSDB = annonces.NbSDB.replace("-", pd.NA).astype("Int64")
annonces.NbSDB = annonces.NbSDB.replace(pd.NA, int(annonces.NbSDB.mean()))

# Question 11
annonces = pd.get_dummies(annonces, columns=["Type", "DPE"], dtype=int)

# Question 12
villes = pd.read_csv("cities.csv")

# Question 13
villes = villes[villes.region_name == "île-de-france"]

# Paris
villes.loc[villes['city_code'] == "paris 01", 'label'] = "paris 1er"

for i in range (2,11) : 
    villes.loc[villes['city_code'] == "paris 0" + str(i), 'label'] = "paris " + str(i) + "eme"
for i in range (10,21) :
    villes.loc[villes['city_code'] == "paris " + str(i), 'label'] = "paris " + str(i) + "eme"

villes = villes.drop_duplicates(subset="label")

annonces.Ville = annonces.Ville.str.replace("-", " ")
annonces.Ville = annonces.Ville.str.replace("'", " ")
annonces.Ville = annonces.Ville.str.lower()
annonces.Ville = annonces.Ville.str.replace(r"[éèê]", "e", regex=True)
annonces.Ville = annonces.Ville.str.replace("â", "a", regex=True)
annonces.Ville = annonces.Ville.str.replace("ÿ", "y")
annonces.Ville = annonces.Ville.str.replace("saint", "st")

#cas particulier
annonces.Ville = annonces.Ville.str.replace("le chesnay", "le chesnay rocquencourt")
annonces.Ville = annonces.Ville.str.replace("eragny", "eragny sur oise")
annonces.Ville = annonces.Ville.str.replace("perigny", "perigny sur yerres")
annonces.Ville = annonces.Ville.str.replace("evry", "evry gregy sur yerre")
annonces.Ville = annonces.Ville.str.replace("franconville", "franconville la garenne")
annonces.Ville = annonces.Ville.str.replace("courcouronnes", "evry courcouronnes")
annonces.Ville = annonces.Ville.str.replace("sts", "beautheil saints")


# Question 14
annonces = annonces.merge(villes[["label", "latitude", "longitude"]], left_on="Ville", right_on="label")
annonces = annonces.drop(columns=["Ville", "label"])

print(annonces)
annonces.to_csv("annonces_modifié.csv", index=False)
