import streamlit as st
import pandas as pd
import numpy as np

# Pour avoir le Layout en wide d'office
st.set_page_config(layout="wide")

# Mise en cache du dataframe
if 'df_game' not in st.session_state:
    dataset = "df_game.csv"
    st.session_state['df_game'] = pd.read_csv(dataset, index_col=0)
df_game = st.session_state['df_game']

#   ---------------------------------------
##            THE GAME
#   ---------------------------------------
# Legend du jour ET le choix client
# input
import random

if 'lengedary_index' not in st.session_state:
    st.session_state['lengedary_index'] = random.randint(0,1760)
index = st.session_state['lengedary_index']
todays_legend = df_game.iloc[index,0]
df_todays_legend = df_game.iloc[index]
#   ---------------------------------------
#
#          AFFICHAGE DE STREAMLIT
#
#   ---------------------------------------

url_img = "https://media.wizards.com/images/magic/daily/wallpapers/Rakdos_Wallpaper_1920x1080.jpg?_gl=1*irug3u*_ga*MjA1NDMyNTExOS4xNzA5MTMyNzEw*_ga_X145Z177LS*MTcwOTEzMjcxMC4xLjEuMTcwOTEzMjcyMi40OC4wLjA."

style_css = '''
<style>
[data-testid="stAppViewContainer"] {
background-color:#000;
background-image: url("https://github.com/Ikari-421/magicdle/blob/master/Rakdos_Wallpaper.jpg?raw=true");
background-size: cover;
background-repeat: no-repeat;
margin: 0;
padding: 0;
height: 100%;
}
.main{
    width:950px
    margin-left: auto;
    margin-right: auto;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight: bold;
    color: bisque;
}
.st-emotion-cache-1xw8zd0 e10yg2by1{
    max-width:950px
}
.logo_entry{
    display: flex;
    justify-content: center;
}
.logo_entry img{
    width: 450px;
}
.research{
    height: 300px;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    justify-content: center;
    border: silver solid 1px;
}
.header_table{
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 30px;
    gap: 5px;
    margin-bottom: 5px;
}
.row_table{
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 100px;
    gap: 5px;
    margin-bottom: 5px;
}
.row_table .item{
    border: bisque solid 1px;
    text-align:center;
}
.item{
    justify-content: center;
    display: flex;
    align-items: center;
    width: 150px;
    height: 100%;
}
.TRUE{
    background-color: green;
}
.FALSE, .LESS, .MORE, OTHER{
    background-color: darkred;
}
.ALMOST{
    background-color: orangered;
}
</style>
'''

st.markdown(style_css, unsafe_allow_html=True)

header_html = '''
<div class="main" >
    <div class="logo_entry">
        <img src="https://github.com/Ikari-421/magicdle/blob/master/magidle_logo.png?raw=true">
    </div>
'''
st.markdown(header_html, unsafe_allow_html=True)

with st.form("my_form"):
    legend_list = np.insert(df_game['name'].unique(), 0, '')
    attempt_legend = st.selectbox("Devine le légendaire de \"Magic the Gatering\" du jour !",
            key="placeholder", options=legend_list)
    submitted = st.form_submit_button("Envoi ton légendaire")

#   ---------------------------------------
#           TEST DE COMPATIBILITE
#   ---------------------------------------

# df_result vide où on incrementera nos données
df_comparaison = pd.DataFrame(columns = df_game.columns)

# Creation d'une liste pour le Df de comparaison
col_list = []
for col in df_game.columns:
    col_list.append(col)
    col_list.append(col+'_test')

# Test de l'existence dans la session
if 'df_zip_result' in st.session_state:
    df_zip_result = st.session_state['df_zip_result']
else:
    df_zip_result = pd.DataFrame(columns = col_list)

# ----------------------------------------------------
#               AFFICHAGE DES INDICES
# ----------------------------------------------------

# if len(df_zip_result) >= 1 :
#     st.write(df_todays_legend['name'])
# Indice donné a partir d'un certain nombre d'essai
if len(df_zip_result) >= 2 :
    if st.button('Découvrir le coût Mana'):
        legend_cmc = df_todays_legend['cmc']
        st.warning(f'Le coût Mana est : {legend_cmc} ', icon="⚠️")

if len(df_zip_result) >= 4 :
    if st.button('Découvrir le Terrain'):
        legend_colors = df_todays_legend['colors']
        st.warning(f'Le Terrain est : {legend_colors} ', icon="⚠️")

if len(df_zip_result) >= 6 :
    if st.button('Découvrir le Sous Type'):
        legend_subtype = df_todays_legend['subtype']
        st.warning(f'Le Sous Type est : {legend_subtype} ', icon="⚠️")

if len(df_zip_result) >= 8 :
    if st.button('Découvrir le Légendaire'):
        legend_name = df_todays_legend['name']
        st.warning(f'Le legendaire est : {legend_name} ', icon="⚠️")

# On verifie si un nom a été entré
if submitted:
    if  attempt_legend:
        # CREATION DATASET COMPARAISON
        today_creature = df_game.loc[df_game['name'] == todays_legend]
        attempt_creature = df_game.loc[df_game['name'] == attempt_legend]

        df_comparaison = pd.concat([today_creature, attempt_creature], ignore_index=True)

        # Fonction pour bien évaluer les données de ces colonnes = liste
        from ast import literal_eval
        df_comparaison['subtypes'] = df_comparaison['subtypes'].apply(literal_eval)
        df_comparaison['colors'] = df_comparaison['colors'].apply(literal_eval)

        # NOUVELLE LIGNE TRUE/ALMOST/FALSE CARACTERISTIQUES
        new_row = []

        for colonne in df_comparaison.columns :
            info1 = df_comparaison.loc[:, colonne][0]
            info2 = df_comparaison.loc[:, colonne][1]

            # Comparaison si liste d'éléments
            if colonne == 'colors' or colonne == 'subtypes' :

                # Trouver les éléments uniques
                same_data = set(info1) & set(info2)

                if len(same_data) == len(info1) and len(same_data) == len(info2):
                    new_row.append("TRUE")
                elif len(same_data) == 0 :
                    new_row.append("FALSE")
                else :
                    new_row.append("ALMOST")

            # Comparaison autres
            elif info1 == info2 :
                new_row.append("TRUE")

            elif colonne == 'cmc' or colonne == 'power' or colonne == 'toughness' :

                if info1 == '*' or info2 == '*':
                    if info1 == info2 :
                        new_row.append("TRUE")
                    else :
                        new_row.append("OTHER")
                else:
                    info1 = int(info1)
                    info2 = int(info2)

                    if info1 < info2 :
                        new_row.append("LESS")
                    else :
                        new_row.append("MORE")
            else:
                new_row.append("FALSE")

        # Intercalage des deux liste
        list_attempt = pd.Series(attempt_creature.iloc[0])
        list_attempt = list_attempt.to_list()

        zip_result = []
        for element1, element2 in zip(list_attempt, new_row):
            zip_result.append(element1)
            zip_result.append(element2)

        zip_result = pd.DataFrame(zip_result)
        zip_result = zip_result.T
        zip_result.columns = col_list

        # On concat la nouvelle ligne avec les autres lignes
        df_zip_result = pd.concat([df_zip_result, zip_result], ignore_index=True)


        if todays_legend == attempt_legend :
            st.success('FELICITATION TU AS TROUVE', icon="✅")

        # ----------------------------------------------------
        #               AFFICHAGE DU TABLEAU
        # ----------------------------------------------------

        head_table_html = f'''
            <div class="result_table">
                <div class="header_table">
                    <div class="item">Légendaire</div>
                    <div class="item">Coût Mana</div>
                    <div class="item">Terrains</div>
                    <div class="item">Sous Type</div>
                    <div class="item">Rareté</div>
                    <div class="item">Force</div>
                    <div class="item">Endurance</div>
                </div>
            </div>
        '''
        st.markdown(head_table_html, unsafe_allow_html=True)

        # ----------------------------------------------------
        #                   LES LIGNES
        # ----------------------------------------------------

        st.session_state['df_zip_result'] = df_zip_result
        
        # Boucle de récupération des infos
        for index in reversed(df_zip_result.index):

            # Liste de résultat pour affichage CSS
            name_value = df_zip_result.iloc[index]['name_test']
            cmc_value = df_zip_result.iloc[index]['cmc_test']
            colors_value = df_zip_result.iloc[index]['colors_test']
            subtypes_value = df_zip_result.iloc[index]['subtypes_test']
            rarity_value = df_zip_result.iloc[index]['rarity_test']
            power_value = df_zip_result.iloc[index]['power_test']
            toughness_value = df_zip_result.iloc[index]['toughness_test']
            # Les infos du légendaire selectionné
            name = df_zip_result.iloc[index]['name']
            cmc = df_zip_result.iloc[index]['cmc']
            colors = df_zip_result.iloc[index]['colors']
            subtypes = df_zip_result.iloc[index]['subtypes']
            rarity = df_zip_result.iloc[index]['rarity']
            power = df_zip_result.iloc[index]['power']
            toughness = df_zip_result.iloc[index]['toughness']

            result_table_html = f'''
                <div class="result_table">
                    <div class="row_table">
                        <div class="item">{name}</div>
                        <div class="item {cmc_value}">{cmc}<br>{cmc_value}</div>
                        <div class="item {colors_value}">{colors}</div>
                        <div class="item {subtypes_value}">{subtypes}</div>
                        <div class="item {rarity_value}">{rarity}</div>
                        <div class="item {power_value}">{power}<br>{power_value}</div>
                        <div class="item {toughness_value}">{toughness}<br>{toughness_value}</div>
                    </div>
                </div>
            '''
            st.markdown(result_table_html, unsafe_allow_html=True)


    else:
        st.warning('ENTRER UN LEGENDAIRE', icon="⚠️")

footer_html = '''
</div> <!-- close main -->
'''
st.markdown(footer_html, unsafe_allow_html=True)

