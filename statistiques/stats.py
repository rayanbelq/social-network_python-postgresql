import pandas as pd
import matplotlib.pyplot as plt
import statistics
import math



# pour calculer les corrélations
def cor(df,c, d) :
    col1 = df[c]
    col2 = df[d]
    #    Statistiques : Moyennes
    moy_col1 = statistics.mean(col1)
    moy_col2 = statistics.mean(col2)
    #    Variances
    var_col1 = statistics.variance(col1)
    var_col2 = statistics.variance(col2)
    #    Covariance
    covariance = sum((x - moy_col1) * (y - moy_col2) for x, y in zip(col1, col2)) / (len(col1) - 1)
    #    Corrélation (Pearson)
    ecart_type_col1 = math.sqrt(var_col1)
    ecart_type_col2 = math.sqrt(var_col2)
    correlation = covariance / (ecart_type_col1 * ecart_type_col2)
    
    return correlation
#on lit le excel
df = pd.read_excel("Excel_Sae.xlsx", sheet_name="Data")

#on récupère les colonnes du excel
k = [" A (Likes) "," B (Partages) "," C (Commentaires) "," D (Nouveaux utilisateurs) "," E (Temps passé) "," F (Sexe) "," G (Âge) "," H (Localisation) "," I (Niveau d'éducation) "," J (Type d'abonnement) ","Likes en fonction des partages"," K (Messages privés) "," L (Notifications) "," M (Publications) "," N (Réactions) "," O (Vues de vidéos) "," P (Clics publicités) "," Q (Suivis) "," R (Mentions J'aime) "," S (Partages de liens) "," T (Téléchargements) "," U (Participations événements) "," V (Créations de groupes) "," W (Membres dans groupes) "," X (Publications dans groupes) "," Y (Réactions dans groupes) "," Z (Messages dans groupes) "," AA (Partages dans groupes) "," AB (Commentaires dans groupes) "," AC (Vues de vidéos dans groupes) "," AD (Clics publicités dans groupes) ","Vues de vidéos"," AE (Suivis dans groupes) "," AF (Mentions J'aime dans groupes) "," AG (Partages de liens dans groupes) "," AH (Téléchargements dans groupes) "," AI (Participations événements dans groupes) "," AJ (Créations de pages) "," AK (Membres sur pages) "," AL (Publications sur pages) "," AM (Réactions sur pages) "," AN (Messages sur pages) "," AO (Partages sur pages) "," AP (Commentaires sur pages) "," AQ (Vues de vidéos sur pages) ","Commentaires","Nouveaux utilisateurs ","Engagement estimé"]
#on a dégagé le Id pcq il sert à rien mtn on dégage les colonnes sans valeurs numériques
i=0
while i < len(k) :
    if isinstance(df[k[i]][0],str) :
        k.pop(i)
        i-=1
    i+=1
    
#mtn on récupère les noms et le coef de pearson pour les colonnes dont ce dernier est > 0.4
val =[]
noms = []
for i in range (len((k))) :
    for j in range (len(k)) :
        if j!=i and not ((k[j],k[i]) in noms):
            r = cor(df,k[i],k[j])
            if r > 0.4 :
                val.append(r)
                noms.append((k[i],k[j]))
#Mtn pour chacun des couples de colonnes on fait un nuage de points et on montre ses statistiques précises
def stt(df,c, d) :
    ages = df[c]
    temps_passe = df[d]
    #    Statistiques : Moyennes

    moy_age = statistics.mean(ages)
    moy_temps = statistics.mean(temps_passe)

    #    Variances

    var_age = statistics.variance(ages)
    var_temps = statistics.variance(temps_passe)

    #    Covariance

    covariance = sum((x - moy_age) * (y - moy_temps) for x, y in zip(ages, temps_passe)) / (len(ages) - 1)

    #    Corrélation (Pearson)

    ecart_type_age = math.sqrt(var_age)
    ecart_type_temps = math.sqrt(var_temps)
    correlation = covariance / (ecart_type_age * ecart_type_temps)

    #    Affichage des résultats

    print("Statistiques entre ",c," et ",d," sur le réseau ")
    print(f"- Moyenne " ,c," : ",moy_age)
    print(f"- Moyenne ",d," : ",moy_temps )
    print(f"- Variance ",c," : ",var_age)
    print(f"- Variance ",d," : ",var_temps)
    print(f"- Covariance : {covariance:.2f}")
    print(f"- Corrélation de Pearson : {correlation:.2f}")
    return None


def nuagepts(df, d, c):
    # Extraire les colonnes nécessaires
    data = df[[d, c]].dropna()
    x = data[d].tolist()
    y = data[c].tolist()

    # Calcul des coefficients de régression linéaire y = ax + b
    moy_x = statistics.mean(x)
    moy_y = statistics.mean(y)
    var_x = statistics.variance(x)
    cov_xy = sum((xi - moy_x) * (yi - moy_y) for xi, yi in zip(x, y)) / (len(x) - 1)
    
    a = cov_xy / var_x
    b = moy_y - a * moy_x

    # Génération des points pour la droite
    x_line = sorted(x)
    y_line = [a * xi + b for xi in x_line]

    # Tracer le nuage de points
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.6, label="Publications")
    plt.plot(x_line, y_line, color='red', linewidth=2, label="Régression linéaire")

    plt.xlabel(d)
    plt.ylabel(c)
    plt.title(f"Relation entre {d} et {c} sur le réseau")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
#le graphe et stat pour chaque couple de noms
for x,y in noms :
    stt(df,x,y)
    nuagepts(df,x,y)
