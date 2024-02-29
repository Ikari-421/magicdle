import streamlit as st
import pandas as pd
import numpy as np

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

#   ---------------------------------------
#
#          AFFICHAGE DE STREAMLIT
#
#   ---------------------------------------

url_img = "https://media.wizards.com/images/magic/daily/wallpapers/Rakdos_Wallpaper_1920x1080.jpg?_gl=1*irug3u*_ga*MjA1NDMyNTExOS4xNzA5MTMyNzEw*_ga_X145Z177LS*MTcwOTEzMjcxMC4xLjEuMTcwOTEzMjcyMi40OC4wLjA."

style_css = '''
<style>
[data-testid="stAppViewContainer"] {
background-color:#fff;
opacity: 0.6;
background-image: url("https://media.wizards.com/images/magic/daily/wallpapers/Rakdos_Wallpaper_1920x1080.jpg?_gl=1*irug3u*_ga*MjA1NDMyNTExOS4xNzA5MTMyNzEw*_ga_X145Z177LS*MTcwOTEzMjcxMC4xLjEuMTcwOTEzMjcyMi40OC4wLjA.");
background-size: cover;
}
</style>
'''

st.markdown(style_css, unsafe_allow_html=True)

header_html = '''
<div class="main" >
    <div class=logo_img>
        <img src=""/>
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

if 'df_result' in st.session_state:
    df_result = st.session_state['df_result']
else:
    df_result = pd.DataFrame(columns = df_game.columns)



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

if submitted:
    if  attempt_legend:
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

                if info1 < info2 :
                    new_row.append("LESS")
                else :
                    new_row.append("MORE")
            else:
                new_row.append("FALSE")


        # CONVERTIR LISTE EN DF
        df_features = pd.DataFrame(new_row)
        df_features = df_features.T
        df_features.columns = df_game.columns

        if todays_legend != attempt_legend :

            # AJOUT LIGNE DE NOTRE ATTEMPT
            df_result = pd.concat([df_result, attempt_creature], ignore_index=True)

            # AJOUT LIGNE DE RESULTAT
            df_result = pd.concat([df_result, df_features], ignore_index=True)

        else :
            st.success('FELICITATION TU AS TROUVE', icon="✅")

    else:
        st.warning('ENTRER UN LEGENDAIRE', icon="⚠️")

st.session_state['df_result'] = df_result
st.dataframe(df_result, use_container_width=True)

if len(df_result) > 6 :
    if st.button('Découvrir le légendaire'):
        st.warning(f'Le legendaire est : {todays_legend} ', icon="⚠️") 

# # df_result.iloc[0]
attempt_name = 'df_result["name"].iloc[0]'
attr_val_1 = 'df_result["cmc"].iloc[0]'
attr_val_2 = 'df_result["colors"].iloc[0]'
attr_val_3 ='df_result["subtypes"].iloc[0]'
attr_val_4 = 'df_result["rarity"].iloc[0]'
attr_val_5 = 'df_result["power"].iloc[0]'
attr_val_6 = 'df_result["toughness"].iloc[0]'

src_img = ""
bg_color_attr_1 = ""
bg_color_attr_2 = ""
bg_color_attr_3 = ""
bg_color_attr_4 = ""
bg_color_attr_5 = ""
bg_color_attr_6 = ""

style_css = '''
<style>
.game_display{
    display:flex;
    width:100%;
    border: darkred solid 1px;
}
.item_img{
    height:100px;
    width:100px;
}
.item_attr{
    height:100px;
    width:100px;
    border: silver solid 1px;
}
</style>
'''

st.markdown(style_css, unsafe_allow_html=True)

# footer_html = f'''
# <div class="game_display">
#     <div class="item_img"><img src="{src_img}"/></div>
#     <div class="item_attr">{attempt_name}</div>
#     <div class="item_attr {bg_color_attr_1}">{attr_val_1}</div>
#     <div class="item_attr {bg_color_attr_2}">{attr_val_2}</div>
#     <div class="item_attr {bg_color_attr_3}">{attr_val_3}</div>
#     <div class="item_attr {bg_color_attr_4}">{attr_val_4}</div>
#     <div class="item_attr {bg_color_attr_5}">{attr_val_5}</div>
#     <div class="item_attr {bg_color_attr_6}">{attr_val_6}</div>
# </div> <!-- close game display -->
# '''
# st.markdown(footer_html, unsafe_allow_html=True)


footer_html = '''
</div> <!-- close main -->
'''
st.markdown(footer_html, unsafe_allow_html=True)

