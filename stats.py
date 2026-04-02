import pandas as pd
import matplotlib.pyplot as plt

def graphe_salmonelle():
    
    df_repas = pd.read_csv('csv/Repas.csv', names=['IdR', 'Nom_Repas', 'Date_', 'Adresse', 'IdChevalier'])
        
    df_plat = pd.read_csv('csv/plat.csv', names=['IdP', 'IdL', 'Nom_Plat'])

        
    df = pd.merge(df_repas,df_plat,left_on='IdR',right_on='IdP')
    df['Date_'] = pd.to_datetime(df['Date_'])

        
    total_plats = df.groupby(df['Date_'].dt.to_period('M')).size()
    total_plats.index = total_plats.index.to_timestamp()

    plat_raclette = df[df['Nom_Plat'] == 'Raclette']
    plat_raclette_par_mois = plat_raclette.groupby(df['Date_'].dt.to_period('M')).size()
    plat_raclette_par_mois.index = plat_raclette_par_mois.index.to_timestamp()

    plt.figure()

    plt.plot(total_plats.index,total_plats.values,label = 'Total repas')
    plt.plot(plat_raclette_par_mois.index,plat_raclette_par_mois.values,label = 'Total raclette')

    debut_crise = pd.to_datetime('2023-06-01')
    fin_crise = pd.to_datetime('2023-08-31')
    plt.axvspan(debut_crise, fin_crise, color='red', alpha=0.2, label='Crise Sanitaire (Salmonelle)')

    plt.tight_layout()
    plt.savefig('graphique_crise_raclette.png')
    plt.show

def graphe_raclette():
    df_plat = pd.read_csv('csv/plat.csv', names=['IdP', 'IdL', 'Nom_Plat'])

    nb_plats = df_plat['Nom_Plat'].value_counts()

    plt.figure(figsize=(10, 8))

    plt.pie(nb_plats.values, labels=nb_plats.index, autopct='%1.1f%%')

    plt.title("Plats mangés par les tenracs", fontweight='bold')

    plt.tight_layout()
    plt.savefig('graphique_plats_mange.png')
    print("Graphique sauvegardé sous 'graphique_plats_mange.png'")


def graphe_scandale_pierrade(): 
    df_entretien = pd.read_csv('csv/Entretien.csv', names=['IdE', 'Date_Entretien', 'CodeMembre'])

    df_entretien['Date_Entretien'] = pd.to_datetime(df_entretien['Date_Entretien'].astype(str).str[:10])

    entretiens_par_mois = df_entretien.groupby(df_entretien['Date_Entretien'].dt.to_period('M')).size()
    
    entretiens_par_mois.index = entretiens_par_mois.index.astype(str)

    plt.figure(figsize=(12, 6))
    
    couleurs = ['red' if mois == '2023-11' else '#5DADE2' for mois in entretiens_par_mois.index]
    plt.bar(entretiens_par_mois.index, entretiens_par_mois.values, color=couleurs, edgecolor='black')
    plt.title("Volume d'entretien du au rappel de machine Teffal )", fontsize=14)
    plt.xlabel("Mois", fontsize=12)
    plt.ylabel("Nombre de machines envoyées en réparation", fontsize=12)
    
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('graphique_scandale_pierrade.png')

def graphe_vegetarien():
    df_repas = pd.read_csv('csv/Repas.csv', names=['IdR', 'Nom_Repas', 'Date_', 'Adresse', 'IdChevalier'])
    df_plat = pd.read_csv('csv/plat.csv', names=['IdP', 'IdL', 'Nom_Plat'])

        
    df = pd.merge(df_repas, df_plat, left_on='IdR', right_on='IdP')
    df['Date_'] = pd.to_datetime(df['Date_'].astype(str).str[:10])

    plats_viande = ["Poulet au curry", "Saumon rôti", "Bœuf aux carottes", "Cabillaud poché", 
                    "Crevettes sautées", "Poulet cacahuète", "Pâtes au saumon", "Bœuf au poivre"]
    
    df['Type'] = df['Nom_Plat'].apply(lambda x: 'Viande/Poisson' if x in plats_viande else 'Végétarien')

    evolution = df.groupby([df['Date_'].dt.to_period('M'), 'Type']).size().unstack(fill_value=0)
    evolution.index = evolution.index.to_timestamp()

    plt.figure(figsize=(12, 6))
    
    plt.stackplot(evolution.index, evolution['Viande/Poisson'], evolution['Végétarien'], 
                  labels=['Viande & Poisson', 'Végétarien (incl. Raclette)'], 
                  colors=['#E74C3C', '#2ECC71'], alpha=0.8)


    plt.title("Évolution des régimes alimentaires après la crise de 2023", fontsize=15, fontweight='bold', pad=20)
    plt.xlabel("Mois", fontsize=12)
    plt.ylabel("Nombre de plats servis", fontsize=12)

    plt.tight_layout()
    plt.savefig('graphique_vague_vegetarienne.png')
    plt.show


if __name__ == "__main__":
    graphe_salmonelle()
    graphe_raclette()
    graphe_scandale_pierrade()
    graphe_vegetarien()
