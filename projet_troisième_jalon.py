from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

annonces = pd.read_csv("annonces_modifié.csv", encoding="ISO-8859-1")

X = annonces.drop(columns=["Prix"])
Y = annonces.Prix
X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.75, test_size=0.25, random_state=49)


#Premier modèle : LinearRegression

    #LinearRegression sans prétraitement
linear = LinearRegression()
linear.fit(X_train, y_train)
y_pred = linear.predict(X_test)
print("LinearRegression : ", r2_score(y_test, y_pred))
    #LinearRegression avec normalisation
mmPipeline = make_pipeline(MinMaxScaler(), LinearRegression())
mmPipeline.fit(X_train, y_train)
y_pred = mmPipeline.predict(X_test)
print("LinearRegression + Normalisation : ", r2_score(y_test, y_pred))
    #LinearRegression avec StandardScaler
ssPipeline = make_pipeline(StandardScaler(), LinearRegression())
ssPipeline.fit(X_train, y_train)
y_pred = ssPipeline.predict(X_test)
print("LinearRegression + Standardisation : ", r2_score(y_test, y_pred))

print("On constate aucune amélioration sur les prédictions avec les prétraitement,\n On constate une légere augmentation dans le score quand on standardise le jeu de données")
print("--------------------")

# Deuxième modèle : Arbre de Décision

    #MaxDepth 4 
ad = DecisionTreeRegressor(max_depth=4, random_state=0)
ad.fit(X_train, y_train)
y_pred = ad.predict(X_test)
print("Arbre de décision maxdepth : 4 ", r2_score(y_test, y_pred))
    # MaxDepth 4 avec Normalisation
admmPipeline = make_pipeline(MinMaxScaler(), ad)
admmPipeline.fit(X_train, y_train)
y_pred = admmPipeline.predict(X_test)
print("Arbre de décision, maxdepth : 4 + Normalisation ", r2_score(y_test, y_pred))
    #MaxDepth 4 avec StandardScaler
adssPipeline = make_pipeline(StandardScaler(), ad)
adssPipeline.fit(X_train, y_train)
y_pred = adssPipeline.predict(X_test)
print("Arbre de décision, maxdepth : 4 + Standardisation ", r2_score(y_test, y_pred))

print("Le résultat pour AD maxdepth 4 avec Normalisation ou Standardisation ou sans prétraiment sont exactement les même")
print("--------------------")

    #MaxDepth 5
ad = DecisionTreeRegressor(max_depth=5, random_state=0)
ad.fit(X_train, y_train)
y_pred = ad.predict(X_test)
print("Arbre de décision, maxdepth : 5 ", r2_score(y_test, y_pred))
    # MaxDepth 5 avec Normalisation
admmPipeline = make_pipeline(MinMaxScaler(), ad)
admmPipeline.fit(X_train, y_train)
y_pred = admmPipeline.predict(X_test)
print("Arbre de décision, maxdepth : 5 + Normalisation ", r2_score(y_test, y_pred))
    #MaxDepth 5 avec StandardScaler
adssPipeline = make_pipeline(StandardScaler(), ad)
adssPipeline.fit(X_train, y_train)
y_pred = adssPipeline.predict(X_test)
print("Arbre de décision, maxdepth : 5 + Standardisation ", r2_score(y_test, y_pred))    

print("Le résultat pour AD max depth 5 avec Normalisation ou Standardisation ou sans prétraiment sont exactement les même et est moins bien que AD max depth 4")
print("--------------------")

#Troisième modèle : N plus proches voisins

    #4 Voisin 
knn = KNeighborsRegressor(n_neighbors=4)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print("KNN, n_neighbors : 4 : ", r2_score(y_test, y_pred))
    #4 Voisin  avec Normalisation
knnmmPipeline = make_pipeline(MinMaxScaler(), knn)
knnmmPipeline.fit(X_train, y_train)
y_pred = knnmmPipeline.predict(X_test)
print("KNN, n_neighbors : 4 + Normalisation ", r2_score(y_test, y_pred))
    #4 Voisin  avec Normalisation
knnssPipeline = make_pipeline(StandardScaler(), knn)
knnssPipeline.fit(X_train, y_train)
y_pred = knnssPipeline.predict(X_test)
print("KNN, n_neighbors : 4 + Standardisation  ", r2_score(y_test, y_pred))

print("On peut voir que KNN n_neighbors 4 sans prétraitement est moins bien que KNN n_neighbors 4 + Normalisation et Standardisation. KNN n_neighbors 4 + Normalisation est meilleur.")
print("--------------------")

    #5 Voisin 
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print("KNN, n_neighbors : 5 ", r2_score(y_test, y_pred))
    #5 Voisin  avec Normalisation
knnmmPipeline = make_pipeline(MinMaxScaler(), knn)
knnmmPipeline.fit(X_train, y_train)
y_pred = knnmmPipeline.predict(X_test)
print("KNN, n_neighbors : 5 avec Normalisation ", r2_score(y_test, y_pred))
    #5 Voisin  avec Normalisation
knnssPipeline = make_pipeline(StandardScaler(), knn)
knnssPipeline.fit(X_train, y_train)
y_pred = knnssPipeline.predict(X_test)
print("KNN, n_neighbors : 5 avec Standardisation ", r2_score(y_test, y_pred))

print("On peut constater la même chose que KNN n_neighbors 4 mais le résultats est meilleur que KNN n_neighbors 4.")
print("--------------------")

#Discussions sur le jeu de données

print("LR : 0.29559470502250307")
print("AD : 0.16354831034646378")
print(" KNN : 0.47017287901767346")

    #Meilleur y_pred :
y_pred_meilleur = knnmmPipeline.predict(X_test)

    #PCA
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train, y_train)
X_test_pca = pca.transform(X_test)
knnmmPipeline.fit(X_train_pca, y_train)
y_pred_pca = knnmmPipeline.predict(X_test_pca)
print("Résultat après PCA, n_components=2 : ", r2_score(y_test, y_pred_pca))
#La modélisation avec 2 composantes principales n'est pas satisfaisante pour ce jeu de données
#Le résultat est moins bien que quand on applique juste knn 5 + Normalisation

    #5 attribut
X_5attribut = annonces.drop(columns=["Prix", "Type_Appartement", "Type_Maison", "NbPieces", "Type_Appartement", "Type_Maison", "DPE_A", "DPE_B", "DPE_C", "DPE_E", "DPE_F", "latitude", "longitude"])
X_train_attribut, X_test_attribut, y_train_attribut, y_test_attribut = train_test_split(X_5attribut, Y, train_size=0.75, test_size=0.25, random_state=49)
knn5 = KNeighborsRegressor(n_neighbors=5)
knnmmPipeline_attribut5 = make_pipeline(MinMaxScaler(),knn5)
knnmmPipeline_attribut5.fit(X_train_attribut, y_train_attribut)
y_pred_attribut = knnmmPipeline_attribut5.predict(X_test_attribut)
print("Score quand on garde juste les meilleurs 5 plus grosses corrélation : ", r2_score(y_test_attribut, y_pred_attribut))
print("le score est moins bien que quand on applique juste KNN 5 avec Normalisation")


    #Graphique
plt.figure(figsize=(8, 8))
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--')
plt.scatter(y_test, y_pred, color='green')
plt.xlabel('y_test')
plt.ylabel('estimation')
plt.show()

    #Corrélation
corr_annonces = annonces.corr()
plt.figure(figsize=(10, 10))
sns.heatmap(corr_annonces, annot=True)
plt.show()

#L’attribut dont la connaissance nous renseigne le plus sur le prix est la surface
#5 attribut les plus corrélés : Surface NbChambres, NbSDB,  DPE_D, DPE_Vierge
