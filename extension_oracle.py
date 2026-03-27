import random
import os
import oracledb
from faker import Faker
from faker_food import FoodProvider
import csv

# ─── 1. CONFIGURATION ORACLE ─────────────────────────────────────────────────
DB_USER = "SYSTEM"
DB_PASSWORD = "653412" 
NB_MEMBRE = 10000 
NB_REPAS = 200
NB_ADRESSE = 1000
NB_ORGANISME = 200
NB_MACHINE = 21
NB_ENTRETIEN = 20000

# ─── 2. PARAMÈTRES ET CATALOGUES MÉTIERS ─────────────────────────────────────
fake = Faker("fr_FR")
fake.add_provider(FoodProvider)

# ─── 3. FONCTIONS UTILITAIRES ────────────────────────────────────────────────

def drop_tables():
    """Supprime les tables et recrée la structure depuis intention.sql"""
    try:
        with open("intention.sql", "r") as intention:
            intentionSQL = intention.read().split(";")
    except FileNotFoundError:
        print(" Fichier intention.sql introuvable. Ignoré.")
        return

    # CORRECTION : Utilisation des bonnes variables globales DB_USER, DB_PASSWORD, DB_DSN
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, host="127.0.0.1") as connection:
        with connection.cursor() as cursor:

            tables_to_drop = [
                "EFFECTUE", "PARTICIPE", "HISTORIQUE_ENTRETIEN", "EST", 
                "COMPORTE", "EST_COMPOSÉ", "EST_ORGANISÉ", "CONTIENT", 
                "APPARTIENT", "ADHÈRE", "EST_AFFILIÉ", "CLUB", 
                "ORDRE", "ENTRETIEN", "PLAT", "GROUPE", 
                "ORGANISATION", "MEMBRE",
                "MODÈLE", "MACHINE", "LÉGUME", 
                "COMPOSANT", "RANG", "DIGNITÉ", "TITRE", 
                "GRADE", "REPAS", "TERRITOIRE", "ORGANISME"
            ]
            for table in tables_to_drop:
                try:
                    cursor.execute(f"drop table {table} cascade constraints")
                except oracledb.DatabaseError:
                    pass 
            for query in intentionSQL:
                if query.strip(): 
                    cursor.execute(query)
                    
        print("✓ Drop all tables & recreate succeed")

def insert(data, connection, table, sql):
    with connection.cursor() as cursor:
        cursor.executemany(sql, data)
        connection.commit() 
        print(f"  ✓ {table:<25} {len(data):>8,} lignes insérées")

    os.makedirs("csv", exist_ok=True)
    os.makedirs("sql", exist_ok=True)


    chemin_csv = os.path.join("csv", f"{table}.csv")
    with open(chemin_csv, mode="w", newline="", encoding="utf-8") as f_csv:
        writer = csv.writer(f_csv, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(data)


    chemin_sql = os.path.join("sql", f"{table}.sql")
    with open(chemin_sql, mode="w", encoding="utf-8") as f_sql:
        for row in data:
            formatted_values = []
            for val in row:
                if val is None:
                    formatted_values.append("NULL")
                elif isinstance(val, bool):
                    formatted_values.append("1" if val else "0")
                elif isinstance(val, (int, float)):
                    formatted_values.append(str(val))
                else:
                    clean_str = str(val).replace("'", "''") 
                    formatted_values.append(f"'{clean_str}'")
            
            values_str = ", ".join(formatted_values)
            f_sql.write(f"INSERT INTO {table} VALUES ({values_str});\n")

def main():
    liste_grades = [(1,'Affilié'), (2,'Sympathisant'), (3,'Adhérent'),(4, 'Chevalier'), (5, 'Grand Chevalier'), (6, 'Commandeur'), (7, 'Grand Croix')]
    liste_rangs = [(1,'Novice'),(2,'Compagnon')]
    liste_titres = [(1, 'Philanthrope'), (2, 'Protecteur'), (3, 'Honorable'),(4,'Chevalier')]
    liste_dignites = [(1, 'Maître'), (2, 'Grand Chancelier'), (3, 'Grand Maître')]
    liste_machines = [(1, 'Tefal 6 personnes'), (2, 'Bron Coucke Traditionnelle'), (3, 'Klarstein Appenzell'), (4, 'Lagrange Transparence'), (5, 'Moulinex Principio'), (6, 'Severin Gril'), (7, 'Louis Tellier Brézière'), (8, 'Tristar Compacte'), (9, 'EssentielB Multi-raclette'), (10, 'Tefal Pierrade')]
    liste_composants = [
        ('Viande', 'Blanc de Poulet', None),
        ('Viande', 'Bœuf haché', None),
        ('Laitier', 'Crème fraîche', 'Lactose'),
        ('Laitier', 'Beurre doux', 'Lactose'),
        ('Laitier', 'Fromage râpé', 'Lactose'),
        ('Céréale', 'Farine de Blé', 'Gluten'),
        ('Céréale', 'Pâtes', 'Gluten'),
        ('Céréale', 'Riz basmati', None),
        ('Légume', 'Carotte', None),
        ('Légume', 'Oignon', None),
        ('Légume', 'Tomate', None),
        ('Fruit à coque', 'Amande effilée', 'Fruits à coque'),
        ('Fruit à coque', 'Noix de pécan', 'Fruits à coque'),
        ('Fruit à coque', 'Cacahuète', 'Arachide'),
        ('Poisson', 'Pavé de Saumon', 'Poisson'),
        ('Poisson', 'Cabillaud', 'Poisson'),
        ('Crustacé', 'Crevette rose', 'Crustacés'),
        ('Épice', 'Poivre Noir', None),
        ('Épice', 'Curry en poudre', None),
        ('Condiment', 'Moutarde de Dijon', 'Moutarde'),
        ('Condiment', 'Sauce Soja', 'Soja et Gluten'),
        ('Œuf', 'Œuf entier', 'Œuf'),
        ('Légumineuse', 'Lentilles corail', None),
        ('Légumineuse', 'Pois chiches', None),
        ('Matière grasse', 'Huile d\'olive', None),
        ('Matière grasse', 'Huile de sésame', 'Sésame'),
        ('Herbe', 'Basilic frais', None),
        ('Herbe', 'Ciboulette', None),
        ('Sucrerie', 'Chocolat noir', 'Traces de fruits à coque'),
        ('Sucrerie', 'Miel', None)
    ]
    listes_plat = [
        "Poulet au curry",      # Blanc de Poulet + Curry
        "Saumon rôti",          # Pavé de Saumon
        "Pâtes au fromage",     # Pâtes + Fromage râpé
        "Bœuf aux carottes",    # Bœuf haché + Carotte
        "Riz sauté soja",       # Riz basmati + Sauce Soja
        "Cabillaud poché",      # Cabillaud
        "Crevettes sautées",    # Crevette rose
        "Omelette herbes",      # Œuf entier + Ciboulette
        "Dahl de lentilles",    # Lentilles corail
        "Poulet cacahuète",     # Blanc de Poulet + Cacahuète
        "Pâtes au saumon",      # Pâtes + Pavé de Saumon
        "Bœuf au poivre"        # Bœuf haché + Poivre Noir
    ]
    # On transforme cette base en une liste de tuples avec un ID incrémenté (1, 2, 3...)
    composant = []
    for i, (type_alim, nom, allergene) in enumerate(liste_composants, start=1):
        composant.append((i, type_alim, nom, allergene))
    adresses = [(i,fake.address().replace('\n',' ')) for i in range(NB_ADRESSE)]
    organismes = [(fake.siret(),fake.company()) for i in range (NB_ORGANISME)]
    repas_temporaire = [(i, fake.word()) for i in range(1, NB_REPAS)]
    territoire = [(i,fake.region()) for i in range (51)]
    organisations = []
    ordres = []
    clubs = []

    for i in range(1, 11):
        organisations.append((i, fake.fruit(), 'Ordre', random.choice(territoire)[0]))
        ordres.append((i,)) 

    # 2. On crée 50 Clubs
    for i in range(11, 61):
        organisations.append((i, fake.fruit(), 'Club', random.choice(territoire)[0]))
        id_ordre_parent = random.choice(ordres)[0]
        clubs.append((i, id_ordre_parent))

    legume = [(i,fake.boolean(),fake.vegetable())for i in range(1,20)]



    repas_pour_groupes = random.sample(repas_temporaire, 50)
    groupe = [(i, repas_pour_groupes[i-1][0]) for i in range(1, 11)]

    # --- 2. Génération des Membres ---
    membre = []
    for i in range (1, NB_MEMBRE):
        grade = random.choice(liste_grades)[0]
        rang = random.choice(liste_rangs)[0]
        titre = random.choice(liste_titres)[0]
        dignite = random.choice(liste_dignites)[0]
        
        membre.append((i, fake.last_name(), fake.street_address(), fake.email(), fake.phone_number(), dignite, titre, rang, grade, random.choice(groupe)[0]))
    
    ids_chevaliers = [m[0] for m in membre if m[6] == 4]
    if not ids_chevaliers: ids_chevaliers.append(1)
    repas = []
    for i in range(1, NB_REPAS): 
        repas.append((i, fake.word(), fake.date_time_between(start_date='-2y', end_date='now'), random.choice(adresses)[1], random.choice(ids_chevaliers)))
        
    plat = []
    for i in range(1, len(repas) + 1): 
        nom_plat = random.choice(listes_plat)
        
        if random.random() > 0.5:
            plat.append((i,random.choice(legume)[0],nom_plat))
        else :
            plat.append((i,None,nom_plat))

# --- 1. Génération des Entretiens (Garanti SANS doublons) ---
    nb_entretiens = min(NB_ENTRETIEN, len(membre))    
    membres_uniques_pour_entretien = random.sample(membre, nb_entretiens)
    
    entretien = []
    for i in range(1, nb_entretiens + 1):
        id_membre = membres_uniques_pour_entretien[i-1][0]
        entretien.append((i, fake.date_this_year(), id_membre))

    machine = [(i, fake.word()) for i in range(1, NB_MACHINE + 1)]
    modele = [(i, random.choice(liste_machines)[1]) for i in range(1, NB_MACHINE + 101)]
    modele = [(i,random.choice(liste_machines)[1]) for i in range(NB_MACHINE + 100)]
    

   
   
    drop_tables()

    historique_entretien_unique = [(random.choice(ordres)[0],random.choice(machine)[0],random.choice(entretien)[0],fake.date_this_decade())for _ in range(1,1500)]
    historique_entretien = list(historique_entretien_unique)[:1000]
    

    effectue_uniques = {(random.choice(machine)[0], random.choice(entretien)[0]) for _ in range(2000)}
    effectue = list(effectue_uniques)[:1000]   

    participe_uniques = {(random.choice(repas)[0], random.choice(machine)[0]) for _ in range(2000)}    
    participe = list(participe_uniques)[:1000]   

    adhère_unique = {(random.choice(membre)[0],random.choice(organisations)[0])for i in range(1000)}
    adhère = list(adhère_unique)[:1000]

    est_unique = {(random.choice(machine)[0],random.choice(modele)[0])for i in range(1000)}
    est = list(est_unique)[:1000]

    est_affilie_unique = {(random.choice(membre)[0],random.choice(organismes)[0])for i in range(1000)}
    est_affilie = list(est_affilie_unique)[:1000]
    
    appartient_unique = {(random.choice(membre)[0],random.choice(groupe)[0])for i in range(1,1000)}
    appartient = list(appartient_unique)[:1000]
    
    contient_unique = {(random.choice(repas)[0],random.choice(plat)[0])for i in range (1000)}
    contient = list(contient_unique)[:1000]
    
    est_organise_unique = {(random.choice(membre)[0],random.choice(repas)[0])for i in range(1000)}
    est_organise = list(est_organise_unique)[:1000]
    
    est_compose_unique = {(random.choice(plat)[0],random.choice(composant)[0])for i in range(1,21)}
    est_compose = list(est_compose_unique)[:1000]

    # --- 5. Insertions (Attention à l'ordre des parents/enfants !) ---
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, host="127.0.0.1") as connection:
        insert(organismes, connection, "Organismes", "insert into Organisme values (:1, :2)")        
        insert(machine, connection, "Machine", "insert into machine values (:1, :2)")
        insert(liste_titres, connection, "Titre", "insert into Titre values (:1, :2)")
        insert(liste_grades, connection, "Grade", "insert into grade values (:1, :2)")
        insert(liste_dignites, connection, "Dignites", "insert into Dignité values (:1, :2)")
        insert(liste_rangs, connection, "Rang", "insert into rang values (:1, :2)")
        insert(composant,connection,"Composant","insert into composant values (:1, :2, :3, :4)")

        insert(repas, connection, "Repas", "insert into Repas values (:1, :2, :3, :4, :5)")
        insert(legume, connection, "Légume", "insert into Légume values (:1, :2, :3)")
        insert(plat, connection, "Plat", "insert into plat values (:1, :2, :3)")
        insert(groupe, connection, "Groupe", "insert into Groupe values (:1, :2)")
        insert(membre, connection, "Membre", "insert into Membre values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)")
        insert(est_affilie, connection, "Est afflié", "insert into est_affilié values (:1, :2)")                
        insert(participe, connection, "Participe", "insert into Participe values (:1, :2)")

        insert(territoire, connection, "Territoire", "insert into territoire values (:1, :2)")
        insert(organisations, connection, "Organisation", "insert into organisation values (:1, :2, :3, :4)")    
        insert(ordres, connection, "Ordre", "insert into Ordre values (:1)")    
        insert(clubs, connection, "Club", "insert into Club values (:1, :2)")
        
        insert(modele, connection, "Modèle", "insert into modèle values (:1, :2)")
        insert(entretien, connection, "Entretien", "insert into Entretien values (:1, :2, :3)")
        insert(historique_entretien, connection, "Historique entretien", "insert into Historique_entretien values (:1, :2, :3, :4)")

        insert(effectue, connection, "Effectue",  "insert into Effectue values (:1, :2)")
        insert(est, connection, "Est", "insert into est values (:1, :2)")
        insert(adhère,connection,"Adhère","insert into adhère values (:1, :2)")
        insert(appartient,connection,"Appartient","insert into Appartient values (:1, :2)")
        insert(contient,connection,"Contient","insert into contient values (:1, :2)")
        insert(est_organise,connection,"Est Organise","insert into Est_organisé values (:1, :2)")
        insert(est_compose,connection,"Est composé","insert into est_composé values (:1, :2)")




if __name__ == "__main__":
    main()