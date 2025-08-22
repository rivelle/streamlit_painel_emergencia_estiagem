import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
import folium
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mapclassify

from utils import mapa_bahia


st.set_page_config(layout="wide")

st.title("Panorama Geral Bahia")
st.divider()

mun_estiagem = gpd.read_file('dados/dados.gpkg', leayer='mun_estiagem')
mun_estiagem = mun_estiagem[mun_estiagem['Situaçăo'] == 'Situaçăo de Emergęncia']
mun_estiagem['cod_situacao'] = 1

mun_ope_pipa = gpd.read_file('dados/dados.gpkg', layer='mun_operacaopipa')
mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['Situacao'].notna()]

pocos_agua = gpd.read_file('dados/csv/pocos_agua_potavel_cerb.csv')
pocos_agua = pocos_agua.rename(columns={'município': 'mun'})

pocos_agua_animal = gpd.read_file('dados/csv/pocos_dessend_animal_cerb.csv')
pocos_agua_animal = pocos_agua_animal.rename(columns={'MUNICÍPIO': 'mun'})

col01, col02 = st.columns([5.5, 6], gap='small')

bioma = st.sidebar.selectbox(
    'Selecione um Bioma',
    options=mun_estiagem['bioma'].unique(),
    index=None,
    placeholder='Selecione um bioma',
    help='Selecione um bioma para filtrar os municípios.')

territorio = st.sidebar.selectbox(
    'Selecione um Território',
    options=mun_estiagem['territorio'].unique(),
    index=None,
    placeholder='Selecione um território',
    help='Selecione um território para filtrar os municípios.')

municipio = st.sidebar.selectbox(
    'Selecione um Município',
    options=mun_estiagem['mun'].unique(),
    index=None,
    placeholder='Selecione um município',
    help='Selecione um município para visualizar os dados específicos.')

if bioma:
    mun_estiagem = mun_estiagem[mun_estiagem['bioma'] == bioma]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['bioma'] == bioma]

if territorio:
    mun_estiagem = mun_estiagem[mun_estiagem['territorio'] == territorio]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['territorio'] == territorio]

if municipio:
    mun_estiagem = mun_estiagem[mun_estiagem['mun'] == municipio]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['mun'] == municipio]
    pocos_agua = pocos_agua[pocos_agua['mun'] == municipio]
    pocos_agua_animal = pocos_agua_animal[pocos_agua_animal['mun'] == municipio]
    


with col01:
    st.subheader("Municípios em Situação de Emergência Estiagem")
    with st.container(border=True, gap='small'):
        with st.spinner('Gerando mapas e gráficos...'):
                map_container = st.empty()
                mapa = mapa_bahia(mun_estiagem, atributo='cod_situacao', zoom=7, title='Municípios em Situação de Emergência Estiagem')
                map_container.empty()  # Limpa container antes de renderizar
                st_folium(mapa, use_container_width=True, height=950)

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

    

with col02:
    st.subheader("Indicadores Gerais")
    col02a, col02b = st.columns(2, gap='small')
    with col02a:
        with st.container(border=True, gap='small'):
            with st.spinner('Gerando mapas e gráficos...'):
                    map_container = st.empty()
                    mapa = mapa_bahia(mun_estiagem, atributo='est_agricf', zoom=6, title='Estabelecimentos Familiares por Município')
                    map_container.empty()  # Limpa container antes de renderizar
                    st_folium(mapa, use_container_width=True, height=500)       
        st.metric(label="Total de Municípios em Situação de Emergência Estiagem", value=len(mun_estiagem))

        total_pipeiros = round(mun_ope_pipa['Pipeiros'].sum())
        txt_total_pipeiros = f"{total_pipeiros:,}".replace(',', '.')
        st.metric(label="Total de Pipeiros", value=txt_total_pipeiros)

        total_estab_agrico = round(mun_estiagem['est_agrico'].sum())
        txt_total_estab_agrico = f"{total_estab_agrico:,}".replace(',', '.')
        st.metric(label="Total Estabelecimentos Agropecuários", value=txt_total_estab_agrico)

        st.metric(label="Número de Poços Água Potável - CERB", value=len(pocos_agua))

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
        st.write(mun_ope_pipa)
        
        


    with col02b:
        with st.container(border=True, gap='small'):
            with st.spinner('Gerando mapas e gráficos...'):
                    map_container = st.empty()
                    mapa = mapa_bahia(mun_ope_pipa, atributo='Pipeiros', zoom=6, title='Número de Pipeiros por Município')
                    map_container.empty()  # Limpa container antes de renderizar
                    st_folium(mapa, use_container_width=True, height=500)

        st.metric(label="Total de Municípios com Operação Pipa", value=len(mun_ope_pipa))


        percent_pop_atend_pipa = round((mun_ope_pipa['Populacao'].sum() / mun_ope_pipa['pop_2022'].sum()) * 100, 2)
        txt_percent_pop_atend_pipa = f"{percent_pop_atend_pipa}%"
        total_pop_atend_pipa = round(mun_ope_pipa['Populacao'].sum())
        txt_total_pop_atend_pipa = f"{total_pop_atend_pipa:,}".replace(',', '.')
        st.metric(label="População Atendida Carros Pipa", value=txt_total_pop_atend_pipa)

        total_estab_agricf = round(mun_estiagem['est_agricf'].sum())
        txt_total_estab_agricf = f"{total_estab_agricf:,}".replace(',', '.')
        st.metric(label="Total de Estabelecimentos Familiares", value=txt_total_estab_agricf)

        st.metric(label="Número de Poços Água Dessedentação Animal - CERB", value=len(pocos_agua_animal))

        

  
       

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
        
 



# col03, col04 = st.columns(2, gap='large')

# with col03:
#     st.subheader("Municípios em Situação de Emergência Estiagem")
#     st.write(mun_estiagem)


# with col04:
   


