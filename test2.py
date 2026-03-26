import random
import os
import oracledb
from datetime import datetime, timedelta
from faker import Faker
from faker_food import FoodProvider
import csv

# ─── 1. CONFIGURATION ORACLE ─────────────────────────────────────────────────
DB_USER = "SYSTEM"
DB_PASSWORD = "653412"
NB_MEMBRE = 501
NB_REPAS = 200

# ─── 2. PARAMÈTRES ET CATALOGUES MÉTIERS ─────────────────────────────────────
fake = Faker("fr_FR")
fake.add_provider(FoodProvider)

# ─── 3. FONCTIONS UTILITAIRES ────────────────────────────────────────────────
def rand_date(start_year=2000, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")
def gambling(): 
    return random.choice([True,False])

def drop_tables():
    """Supprime les tables et recrée la structure depuis intention.sql"""
    try:
        with open("intention.sql", "r") as intention:
            intentionSQL = intention.read().split(";")
    except FileNotFoundError:
        print("⚠️ Fichier intention.sql introuvable. Ignoré.")
        return

    # CORRECTION : Utilisation des bonnes variables globales DB_USER, DB_PASSWORD, DB_DSN
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, host="127.0.0.1") as connection:
        with connection.cursor() as cursor:
            # Liste des tables à drop pour alléger le code visuellement
# Liste complète des tables à drop (de la plus dépendante à la plus indépendante)
            tables_to_drop = [
                "EFFECTUE", "PARTICIPE", "HISTORIQUE_ENTRETIEN", "EST", 
                "COMPORTE", "EST_COMPOSÉ", "EST_ORGANISÉ", "CONTIENT", 
                "APPARTIENT", "ADHÈRE", "EST_AFFILIÉ", "CLUB", 
                "ORDRE", "ENTRETIEN", "PLAT", "GROUPE", 
                "ORGANISATION", "MEMBRE", "INGRÉDIENT", "SAUCE", 
                "DATE_", "MODÈLE", "MACHINE", "LÉGUME", 
                "COMPOSANT", "RANG", "DIGNITÉ", "TITRE", 
                "GRADE", "REPAS", "TERRITOIRE", "ORGANISME"
            ]
            for table in tables_to_drop:
                try:
                    cursor.execute(f"drop table {table} cascade constraints")
                except oracledb.DatabaseError:
                    pass 
            for query in intentionSQL:
                if query.strip(): # Évite d'exécuter des requêtes vides
                    cursor.execute(query)
                    
        print("✓ Drop all tables & recreate succeed")

def insert(data, connection, table, sql):
    # --- 1. Insertion dans la base de données Oracle ---
    with connection.cursor() as cursor:
        cursor.executemany(sql, data)
        connection.commit() 
        print(f"  ✓ {table:<25} {len(data):>8,} lignes insérées")

    # --- Création des dossiers s'ils n'existent pas ---
    os.makedirs("csv", exist_ok=True)
    os.makedirs("sql", exist_ok=True)

    # --- 2. Exportation en CSV ---
    # Le chemin pointe maintenant vers le dossier_csv/
    chemin_csv = os.path.join("csv", f"{table}.csv")
    with open(chemin_csv, mode="w", newline="", encoding="utf-8") as f_csv:
        writer = csv.writer(f_csv, delimiter=";")
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
# ─── 4. SCRIPT PRINCIPAL ─────────────────────────────────────────────────────
def main():
    liste_grades = [(1,'Affilié'), (2,'Sympathisant'), (3,'Adhérent'),(4, 'Chevalier'), (5, 'Grand Chevalier'), (6, 'Commandeur'), (7, 'Grand Croix')]
    liste_rangs = [(1,'Novice'),(2,'Compagnon')]
    liste_titres = [(1, 'Philanthrope'), (2, 'Protecteur'), (3, 'Honorable'),(4,'Chevalier')]
    liste_dignites = [(1, 'Maître'), (2, 'Grand Chancelier'), (3, 'Grand Maître')]
    liste_machines = [(1, 'Tefal 6 personnes'), (2, 'Bron Coucke Traditionnelle'), (3, 'Klarstein Appenzell'), (4, 'Lagrange Transparence'), (5, 'Moulinex Principio'), (6, 'Severin Gril'), (7, 'Louis Tellier Brézière'), (8, 'Tristar Compacte'), (9, 'EssentielB Multi-raclette'), (10, 'Tefal Pierrade')]
    
    adresses = [(i,fake.address().replace('\n',' ')) for i in range(1,100)]
    organismes = [(fake.siret(),fake.company()) for i in range (1,500)]
    
    # --- 1. Génération préliminaire pour éviter les erreurs de dépendances ---
    repas_temporaire = [(i, fake.word()) for i in range(1, NB_REPAS)]
    

    repas_pour_groupes = random.sample(repas_temporaire, 50)
    legume = [(i,fake.boolean(),fake.vegetable())for i in range(1,20)]




    groupe = [(i, repas_pour_groupes[i-1][0]) for i in range(1, 51)]
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
        # On construit le repas COMPLET avec ses 5 paramètres (ID, nom, date, adresse, id_chevalier)
        repas.append((i, fake.word(), fake.date_time_between(start_date='-2y', end_date='now'), random.choice(adresses)[1], random.choice(ids_chevaliers)))
        
    est_organise_unique = {(random.choice(repas)[0])}     
    plat = []
    for i in range(len(repas)):
        if random.random() > 0.5:
            plat.append((i,random.choice(legume)[0]))
        else :
            plat.append((i,None))
    # --- 4. Le reste des tables ---
    membres_aleatoires = random.sample(membre, 500)
    entretien = [(i, fake.date_this_year(), membres_aleatoires[i-1][0]) for i in range(1, 501)]    
    
    machine = [(i,fake.word()) for i in range (1,200)]
    effectue_uniques = {(random.choice(machine)[0], random.choice(entretien)[0]) for _ in range(2000)}
    effectue = list(effectue_uniques)[:1000]    
    
    participe_uniques = {(random.choice(repas)[0], random.choice(machine)[0]) for _ in range(2000)}    
    participe = list(participe_uniques)[:1000]    
    modele = [(i,random.choice(liste_machines)[1]) for i in range(1,101)]
    territoire = [(i,fake.region()) for i in range (1,101)]
    
    est_unique = {(random.choice(machine)[0],random.choice(modele)[0])for i in range(1,1000)}
    est = list(est_unique)[:1000]
    drop_tables()
    est_affilie_unique = {(random.choice(membre)[0],random.choice(organismes)[0])for i in range(1,1000)}
    est_affilie = list(est_affilie_unique)[:1000]

    # --- 5. Insertions (Attention à l'ordre des parents/enfants !) ---
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, host="127.0.0.1") as connection:
        insert(organismes, connection, "Organismes", "insert into Organisme values (:1, :2)")        
        insert(machine, connection, "Machine", "insert into machine values (:1, :2)")
        insert(liste_titres, connection, "Titre", "insert into Titre values (:1, :2)")
        insert(liste_grades, connection, "Grade", "insert into grade values (:1, :2)")
        insert(liste_dignites, connection, "Dignites", "insert into Dignité values (:1, :2)")
        insert(liste_rangs, connection, "Rang", "insert into rang values (:1, :2)")
        
        insert(repas, connection, "Repas", "insert into Repas values (:1, :2, :3, :4, :5)")
        insert(legume, connection, "Légume", "insert into Légume values (:1, :2, :3)")
        insert(plat, connection, "Plat", "insert into plat values (:1, :2)")
        insert(groupe, connection, "Groupe", "insert into Groupe values (:1, :2)")
        insert(membre, connection, "Membre", "insert into Membre values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)")
        insert(est_affilie, connection, "Est afflié", "insert into est_affilié values (:1, :2)")                
        insert(participe, connection, "Participe", "insert into Participe values (:1, :2)")

        insert(territoire, connection, "Territoire", "insert into territoire values (:1, :2)")
        insert(modele, connection, "Modèle", "insert into modèle values (:1, :2)")
        insert(entretien, connection, "Entretien", "insert into Entretien values (:1, :2, :3)")
        insert(effectue, connection, "Effectue",  "insert into Effectue values (:1, :2)")
        insert(est, connection, "Est", "insert into est values (:1, :2)")
        
if __name__ == "__main__":
    main()