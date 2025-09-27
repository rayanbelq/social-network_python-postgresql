import pandas as pd
from datetime import datetime, timedelta
import random


# Charger le fichier Excel
file_path = "Excel_Sae.xlsx"
df = pd.read_excel(file_path)

colonnes =list(df.columns)

nb_utilisateurs=len(df)
types = ["like", "partage", "commentaire", "participation"]
messages = ["Salut !", "Tu vas bien ?", "On se voit demain ?", "C’est top ça !"]

#Peuplement utilisateur
def insert_util(col):
    date_naissance = str(2025-int(col[" G (Âge) "]))
    insert=(
        f"INSERT INTO utilisateurs VALUES(DEFAULT, "
        f"'{col[' F (Sexe) '].strip()}',"
        f"'nom_user',"
        f"'{date_naissance}',"
        f"'{col[' I (Niveau d\'éducation) '].strip()}', "
        f"'{col[' J (Type d\'abonnement) '].strip()}');"
    )
    return insert

insert_into=df.apply(insert_util, axis=1)
with open("PeuplementBD.sql", "w", encoding='utf-8') as f:
    f.write("\n".join(insert_into))

f= open("PeuplementBD.sql","w") #On re ouvre le fichier car with open le ferme automatiquement.
#Peuplement page
for i in range(1, 100):
    titre = f"c_{i}"
    f.write(f"INSERT INTO page VALUES (DEFAULT,'{titre}');\n")
    
#Peuplement groupe
for i in range(1, 100):
    id_groupe = i
    f.write(f"INSERT INTO groupe VALUES ({id_groupe}, DEFAULT);\n")
    
#Peuplement session
for i in range(1, nb_utilisateurs + 1):
    debut = datetime(2025, 1, random.randint(1, 30), random.randint(8, 18)) #Entre le 1 et le 30 et entre 8h et 18h
    fin = debut + timedelta(hours=random.randint(1, 3)) #Ajouter la durée pour savoir quand il y a une déconnexion
    loc = f"Ville_{random.randint(1, 5)}"
    f.write(f"INSERT INTO Session VALUES (DEFAULT, '{debut}', '{fin}', '{loc}', {i});\n")

#Peuplement Publication
for i in range(1, nb_utilisateurs + 1):
    id_page = random.randint(1, 100)
    contenu = f"Contenu de l'utilisateur {i}"
    date_pub = datetime(2025, random.randint(1, 12), random.randint(1, 28)) # Entre janvier et décembre et le premier et le 31ème jour
    f.write(f"INSERT INTO publication VALUES ({id_page}, {i}, DEFAULT, '{contenu}', '{date_pub}');\n")
    
#Peuplement Reactions
for i in range(1, nb_utilisateurs + 1):
    id_page = random.randint(1, 100)
    id_publication = i
    utilisateur_react = random.randint(1, nb_utilisateurs) #quel utilisateur à réagis ? 
    type_react = random.choice(types) #choix aleatoire dans le tableau type
    contenu = f"Réaction de l'utilisateur {utilisateur_react}"
    f.write(f"""INSERT INTO reaction VALUES (
        {id_page}, {utilisateur_react}, {id_publication}, {i},
        DEFAULT, '{type_react}', '{contenu}'
    );\n""") #le i représente la publication de l'utilisateur i 
    
#Peuplement rejoint    
for groupe in range(1, 100):
    for utilisateur in range(1, nb_utilisateurs + 1):
        groupes_rejoints = random.sample(range(1, 101), random.randint(1, 5)) # Un utilisateur rejoint ici entre 1 et 5 groupes parmi les 100. Le tirage est aléatoire pour le réalisme
    
    for groupe in groupes_rejoints:
        f.write(f"INSERT INTO rejoint VALUES ({utilisateur}, {groupe}, {groupe});\n")
        
#Peuplement Notification
for i in range(1, nb_utilisateurs + 1):
    contenu = f"Notification pour utilisateur {i}"
    f.write(f"INSERT INTO Notification VALUES ({i}, DEFAULT, '{contenu}');\n")

#Peuplement Messages
for i in range(100):
    exp = random.randint(1, nb_utilisateurs) #expediteur au hasard
    dest = random.randint(1, nb_utilisateurs) #destinataire au hasard
    contenu = random.choice(messages) #Message prégeneré aléatoire
    while dest == exp: #Impossible de s'auto envoyer un message
        dest = random.randint(1, nb_utilisateurs) #si c'est le cas on retire un destinataire
    f.write(f"INSERT INTO message VALUES ({exp}, {dest}, '{contenu}');\n")   
    
#Peuplement Accede_A 
for i in range(1, 101):
    id_sess = random.randint(1, nb_utilisateurs)
    id_page = random.randint(1, 100)
    f.write(f"INSERT INTO Accede_a VALUES ({id_sess}, {id_page});\n")

#Peuplement Administre
for i in range(1, nb_utilisateurs + 1):
    id_page = random.randint(1, 100)
    f.write(f"INSERT INTO administre VALUES ({i}, {id_page});\n")

#Peuplement réponse_à
for i in range(1, 100): #Imaginons 100 publications
    if random.random() < 0.2:  # 20% de chance qu'une publication soit une réponse à une autre 
        repondue = random.randint(1, 100)
        while repondue == i:
            repondue = random.randint(1, 100)  # Impossible qu'une publication se réponde à elle même
        f.write(f"INSERT INTO reponse_a VALUES ({repondue}, {i});\n") #repondue répond à i
        
