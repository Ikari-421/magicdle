import streamlit as st
import pandas as pd
import numpy as np

dataset = "all_mtg_cards.zip"
df_magic = pd.read_csv(dataset, compression='zip', low_memory=False)

# Filtre sur Legendary Creatures + Legendary Artifact Creatures + PlanesWalker ??
df_legend = df_magic.loc[df_magic['type'].str.contains(r'Legendary (Artifact )?Creature', regex = True),:]

# Colonnes de caracteristiques
col_to_keep = ('name', 'cmc', 'colors', 'subtypes', 'rarity', 'power', 'toughness')

df_game = df_legend.drop(df_legend.columns.difference(col_to_keep), axis=1)
df_game.reset_index(drop = True, inplace = True)

# remplacer colors NaN par 'Uncolor'
df_game['colors'] = df_game['colors'].fillna("UC")

# Supprimer les doublons
df_game.drop_duplicates(subset = ['name'], inplace = True)

# Enlever les , dans la colonne 'name'
df_game['name'] = df_game['name'].str.replace(',', '')


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
# attempt_legend = input('Créature Légendaire : ') # Le choix du joueur

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
    <h1>
        MAGICDLE
    </h1>
'''
st.markdown(header_html, unsafe_allow_html=True)

with st.container(border=True):
    legend_list = np.insert(df_game['name'].unique(), 0, '')
    attempt_legend = st.selectbox("Devine le légendaire de \"Magic the Gatering\" du jour !",
            key="placeholder", options=legend_list)
    btn_status = st.button("Envoi ton légendaire")

#   ---------------------------------------
#           TEST DE COMPATIBILITE
#   ---------------------------------------
st.write(attempt_legend)
# Creation df
df_result = df_game.loc[(df_game['name'] == todays_legend) | (df_game['name'] == attempt_legend)]
df_result.reset_index(drop = True, inplace = True)

# Fonction pour bien évaluer les données de ces colonnes = liste
from ast import literal_eval
df_result['subtypes'] = df_result['subtypes'].apply(literal_eval)
df_result['colors'] = df_result['colors'].apply(literal_eval)

# Comparaison pour chaque colonne

new_row = []

for colonne in df_result.columns :
    info1 = df_result.loc[0, colonne]
    info2 = df_result.loc[1, colonne]

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
        new_row.append("FALSE")

    else:
        new_row.append("FALSE")

# Ajout des résultats à une nouvelle ligne dans df_game
df_result.loc[2] = pd.Series(new_row)



st.dataframe(df_result.iloc[0], use_container_width=True)


# df_result.iloc[0]
attempt_name = df_result["name"].iloc[0]
attr_val_1 = df_result["cmc"].iloc[0]
attr_val_2 = df_result["colors"].iloc[0]
attr_val_3 = df_result["subtypes"].iloc[0]
attr_val_4 = df_result["rarity"].iloc[0]
attr_val_5 = df_result["power"].iloc[0]
attr_val_6 = df_result["toughness"].iloc[0]

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

footer_html = f'''
<div class="game_display">
    <div class="item_img"><img src="{src_img}"/></div>
    <div class="item_attr">{attempt_name}</div>
    <div class="item_attr {bg_color_attr_1}">{attr_val_1}</div>
    <div class="item_attr {bg_color_attr_2}">{attr_val_2}</div>
    <div class="item_attr {bg_color_attr_3}">{attr_val_3}</div>
    <div class="item_attr {bg_color_attr_4}">{attr_val_4}</div>
    <div class="item_attr {bg_color_attr_5}">{attr_val_5}</div>
    <div class="item_attr {bg_color_attr_6}">{attr_val_6}</div>
</div> <!-- close game display -->
'''
st.markdown(footer_html, unsafe_allow_html=True)


footer_html = '''
</div> <!-- close main -->
'''
st.markdown(footer_html, unsafe_allow_html=True)

