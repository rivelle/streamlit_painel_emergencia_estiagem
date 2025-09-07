import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
import branca
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mapclassify

from utils import mapa_geral, mapa_op_carropipa

st.set_page_config(layout="wide")

st.title("Mapa Geral Bahia")
st.divider()



## Dados ============================================================================
df_municipios = gpd.read_file('dados/dados.gpkg', layer = 'ba_municipios')
df_municipios = df_municipios.rename(columns = {
    'cd_mun': 'cod_ibge',
    'nm_mun': 'mun'
})

df_municipios['est_agrico'] = df_municipios['est_agrico'].astype('Int64')
df_municipios['est_agricf'] = df_municipios['est_agricf'].astype('Int64')

df_municipios['percent_fam'] = (df_municipios['est_agricf']*100)/df_municipios['est_agrico']

mun_estiagem = gpd.read_file('dados/dados.gpkg', leayer='mun_estiagem')
mun_estiagem = mun_estiagem[mun_estiagem['Situaçăo'] == 'Situaçăo de Emergęncia']
mun_estiagem['cod_situacao'] = 1

mun_ope_pipa = gpd.read_file('dados/dados.gpkg', layer='mun_operacaopipa')
mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['Situacao'].notna()]

pocos_agua = gpd.read_file('dados/csv/pocos_agua_potavel_cerb.csv')
pocos_agua = pocos_agua.rename(columns={'município': 'mun'})

pocos_agua_animal = gpd.read_file('dados/csv/pocos_dessend_animal_cerb.csv')
pocos_agua_animal = pocos_agua_animal.rename(columns={'MUNICÍPIO': 'mun'})


# Filtros ========================================================================

# bioma = st.sidebar.selectbox(
#     'Selecione um Bioma',
#     options=mun_estiagem['bioma'].unique(),
#     index=None,
#     placeholder='Selecione um bioma',
#     help='Selecione um bioma para filtrar os municípios.')

territorio = st.sidebar.selectbox(
    'Selecione um Território',
    options=sorted(df_municipios['territorio'].unique()),
    index=None,
    placeholder='Selecione um território',
    help='Selecione um território para filtrar os municípios.')





# if bioma:
#     mun_estiagem = mun_estiagem[mun_estiagem['bioma'] == bioma]
#     mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['bioma'] == bioma]
#     df_municipios = df_municipios[df_municipios['mun'] == bioma]

if territorio:
    mun_estiagem = mun_estiagem[mun_estiagem['territorio'] == territorio]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['territorio'] == territorio]
    df_municipios = df_municipios[df_municipios['territorio'] == territorio]

    # mun_estiagem_territorio = mun_estiagem
    # mun_ope_pipa_territorio = mun_ope_pipa
    # df_municipios_territorio = df_municipios

    municipio = st.sidebar.selectbox(
    'Selecione um Município do Território',
    options=sorted(df_municipios['mun'].unique()),
    index=None,
    placeholder='Selecione um município do território',
    help='Selecione um município pertencente ao território para visualizar os dados específicos.')  

    # if municipio_territorio:
    #     mun_estiagem_territorio = mun_estiagem[mun_estiagem['mun'] == municipio_territorio]
    #     mun_ope_pipa_territorio = mun_ope_pipa[mun_ope_pipa['mun'] == municipio_territorio]
    #     pocos_agua = pocos_agua[pocos_agua['mun'] == municipio_territorio]
    #     pocos_agua_animal = pocos_agua_animal[pocos_agua_animal['mun'] == municipio_territorio]
    #     df_municipios_territorio = df_municipios[df_municipios['mun'] == municipio_territorio]

    if municipio:
        mun_estiagem = mun_estiagem[mun_estiagem['mun'] == municipio]
        mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['mun'] == municipio]
        pocos_agua = pocos_agua[pocos_agua['mun'] == municipio]
        pocos_agua_animal = pocos_agua_animal[pocos_agua_animal['mun'] == municipio]
        df_municipios = df_municipios[df_municipios['mun'] == municipio]

    
municipio = st.sidebar.selectbox(
    'Selecione um Município',
    options=mun_estiagem['mun'].unique(),
    index=None,
    placeholder='Selecione um município',
    help='Selecione um município para visualizar os dados específicos.')    

if municipio:
    mun_estiagem = mun_estiagem[mun_estiagem['mun'] == municipio]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['mun'] == municipio]
    pocos_agua = pocos_agua[pocos_agua['mun'] == municipio]
    pocos_agua_animal = pocos_agua_animal[pocos_agua_animal['mun'] == municipio]
    df_municipios = df_municipios[df_municipios['mun'] == municipio]


## Display ==============================================================================

col01, col02 = st.columns([3, 9])

with col01:
    st.metric(label="Total de Municípios em Situação de Emergência Estiagem", value=len(mun_estiagem))

    total_estab_agrico = round(df_municipios['est_agrico'].sum())
    txt_total_estab_agrico = f"{total_estab_agrico:,}".replace(',', '.')
    st.metric(label="Total Estabelecimentos Agropecuários", value=txt_total_estab_agrico)

    total_estab_agricf = round(df_municipios['est_agricf'].sum())
    txt_total_estab_agricf = f"{total_estab_agricf:,}".replace(',', '.')
    st.metric(label="Total de Estabelecimentos Familiares", value=txt_total_estab_agricf)

    df_municipios['reb_total'] = df_municipios['reb_total'].astype('Int64')
    total_reb_agricf = round(df_municipios['reb_total'].sum())
    txt_total_reb_agricf = f"{total_reb_agricf:,}".replace(',', '.')
    st.metric(label="Total do Rebanho Agricultura Familiar", value=txt_total_reb_agricf)

    st.metric(label="Total de Municípios com Operação Pipa", value=len(mun_ope_pipa))

    total_pipeiros = round(mun_ope_pipa['Pipeiros'].sum())
    txt_total_pipeiros = f"{total_pipeiros:,}".replace(',', '.')
    st.metric(label="Total de Pipeiros", value=txt_total_pipeiros)

    percent_pop_atend_pipa = round((mun_ope_pipa['Populacao'].sum() / mun_ope_pipa['pop_2022'].sum()) * 100, 2)
    txt_percent_pop_atend_pipa = f"{percent_pop_atend_pipa}%"
    total_pop_atend_pipa = round(mun_ope_pipa['Populacao'].sum())
    txt_total_pop_atend_pipa = f"{total_pop_atend_pipa:,}".replace(',', '.')
    st.metric(label="População Atendida Carros Pipa", value=txt_total_pop_atend_pipa)    

    st.metric(label="Número de Poços Água Potável - CERB", value=len(pocos_agua))    

    st.metric(label="Número de Poços Água Dessedentação Animal - CERB", value=len(pocos_agua_animal))


    

with col02:
    with st.container(border=True, gap='small'):
        with st.spinner('Gerando mapas...'):
            map_container = st.empty()
            mapa = mapa_geral(mun_estiagem, df_municipios)
            map_container.empty()  # Limpa container antes de renderizar
            st_folium(mapa, use_container_width=True, height=950)   
    
    df_municipios_display = df_municipios.copy()
    df_municipios_display = df_municipios_display[['mun', 'territorio', 'est_agrico', 'est_agricf', 'percent_fam', 'reb_total']]
    df_municipios_display = df_municipios_display.rename(columns={
        'mun':'Município',
        'territorio':'Território Identidade',
        'est_agrico':'Estab. Agropecuários',
        'est_agricf':'Estab. Familiares',
        'percent_fam':f'% Familiar',
        'reb_total':'Rebanho (Nº Animais)'
    })

    st.write(df_municipios_display) 

    
st.divider()
st.subheader("Municípios Operação Carro Pipa")

if territorio and mun_ope_pipa.empty:
    st.warning("Nenhum dado de operação de carro pipa encontrado para este território.")
elif mun_ope_pipa.empty:
    st.warning("Nenhum dado de operação de carro pipa encontrado para este município.")
elif pocos_agua.empty:
    st.warning("Nenhum dado de poços de água encontrado para este município.")
elif pocos_agua_animal.empty:
    st.warning("Nenhum dado de poços de água animal encontrado para este município.")
else:
    col03, col04 = st.columns(2, gap='large')

    with col03:
        with st.container(border=True, gap='small'):
            with st.spinner('Gerando mapas...'):
                map_container = st.empty()
                mapa = mapa_op_carropipa(mun_ope_pipa)
                map_container.empty()  # Limpa container antes de renderizar
                st_folium(mapa, use_container_width=True, height=950)    

    with col04:
        fig = go.Figure()
        fig.add_trace(go.Bar(
                    x = mun_ope_pipa['mun'],
                    y = mun_ope_pipa['Populacao'],
                    name = 'População Atendida',
                    marker_color = '#FC8D47'
                ))
        fig.add_trace(go.Bar(
                    x = mun_ope_pipa['mun'],
                    y = mun_ope_pipa['pop_2022'],
                    name = 'População do Município (2022)',
                    marker_color = '#7F0327'
                ))
        fig.update_layout(barmode = 'group', title = f'População Atendida por Carros Pipa por Município ({municipio})')
        st.plotly_chart(fig)

        st.write(mun_ope_pipa)

    

# st.write(df_municipios)
# st.write(df_municipios.shape)

# st.write(mun_estiagem)


style_metric_cards(
        {
            "label_font_size": "1.5rem",
            "value_font_size": "1.5rem",
            "card_background_color": "#ccbfbf",
            "card_border_radius": "10px",
            "card_padding": "20px",
            "card_margin": "10px",
        }
    ) 