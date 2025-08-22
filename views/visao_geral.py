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

col01, col02 = st.columns([5.5, 6], gap='small')

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

if territorio:
    mun_estiagem = mun_estiagem[mun_estiagem['territorio'] == territorio]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['territorio'] == territorio]

if municipio:
    mun_estiagem = mun_estiagem[mun_estiagem['mun'] == municipio]
    mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['mun'] == municipio]


with col01:
    st.subheader("Municípios em Situação de Emergência Estiagem")
    with st.container(border=True, gap='small'):
        with st.spinner('Gerando mapas e gráficos...'):
                map_container = st.empty()
                mapa = mapa_bahia(mun_estiagem, atributo='cod_situacao', zoom=7, title='Municípios em Situação de Emergência Estiagem')
                map_container.empty()  # Limpa container antes de renderizar
                st_folium(mapa, use_container_width=True, height=950)

    st.plotly_chart(
            px.bar(
                mun_ope_pipa,
                x='mun',
                y='Pipeiros',
                orientation='v',
                title='Pipeiros por Município',
                labels={'Pipeiros': 'Número de Pipeiros', 'mun': 'Município'},
                color='Pipeiros',
                color_continuous_scale=px.colors.sequential.Plasma
            ),
            use_container_width=True
        )

    

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
        st.metric(label="Total de Pipeiros", value=mun_ope_pipa['Pipeiros'].sum())
        st.metric(label="Total Estabelecimentos Agropecuários", value=mun_estiagem['est_agrico'].sum())

        
        


    with col02b:
        with st.container(border=True, gap='small'):
            with st.spinner('Gerando mapas e gráficos...'):
                    map_container = st.empty()
                    mapa = mapa_bahia(mun_ope_pipa, atributo='Pipeiros', zoom=6, title='Número de Pipeiros por Município')
                    map_container.empty()  # Limpa container antes de renderizar
                    st_folium(mapa, use_container_width=True, height=500)

        st.metric(label="Total de Municípios com Operação Pipa", value=len(mun_ope_pipa))
        st.metric(label="População Atendida Carros Pipa", value=mun_ope_pipa['Populacao'].sum())
        st.metric(label="Total de Estabelecimentos Familiares", value=mun_estiagem['est_agricf'].sum())

        

    
    st.plotly_chart(
            px.bar(
                mun_ope_pipa,
                x='mun',
                y='Populacao',
                orientation='v',
                title='População Atendida por Carros Pipa por Município',
                labels={'Populacao': 'População Atendida', 'mun': 'Município'},
                color='Populacao',
                color_continuous_scale=px.colors.sequential.Plasma
            ),
            use_container_width=True
        )
    

    style_metric_cards(
        {
            "label_font_size": "1.2rem",
            "value_font_size": "1.5rem",
            "card_background_color": "#f0f0f0",
            "card_border_radius": "10px",
            "card_padding": "20px",
            "card_margin": "10px"
        }
    )    
        

col03, col04 = st.columns(2, gap='large')

with col03:
    st.subheader("Municípios em Situação de Emergência Estiagem")
    st.write(mun_estiagem)


with col04:
    st.subheader("Municípios Operação Carro Pipa")
    if territorio and mun_ope_pipa.empty:
        st.warning("Nenhum dado de operação de carro pipa encontrado para este território.")
    if mun_ope_pipa.empty:
        st.warning("Nenhum dado de operação de carro pipa encontrado para este município.")
    else:
        st.write(mun_ope_pipa)

    


