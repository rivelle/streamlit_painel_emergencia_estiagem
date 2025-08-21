import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import folium
import streamlit as st
from streamlit_folium import st_folium


# Mapas e Figuras ---------------------------------------------------------------------



@st.cache_data
def figura_mapa_brasil(df, nome):
    #Dados---------------------------------
    brasil = gpd.read_file('brasil.gpkg', layer='limites_estados')
    brasil = brasil.rename(columns={
        'CD_UF':'UF-id',
        'NM_UF':'Estado'
    })
    brasil['UF-id'] = brasil['UF-id'].astype('Int64')
    st.session_state['df_brasil'] = brasil
    

    brasil_freq = brasil.join(df['Frequencia'], on='UF-id', how='left')
    st.session_state['df_brasil_freq'] = brasil_freq

    #Plot------------------------------------
    fig, eixo = plt.subplots(figsize=(10,10))
    st.session_state['df_brasil'].plot(ax=eixo, color='lightgray', alpha=0.3, edgecolor='black', linewidth=0.3)
    st.session_state['df_brasil_freq'].plot(ax=eixo,
                column='Frequencia',
                cmap='YlOrRd',
                edgecolor='black',
                linewidth=0.5,
                legend=False,
                )


    fig.suptitle(f'Mapa de Frequência do nome {nome} por Estado', fontsize=10)
    fig.tight_layout()
    return fig
    
@st.cache_data
def load_geojson():
    brasil = gpd.read_file('dados/geojson/lmt_estados.geojson')
    brasil = brasil.rename(columns={
        'CD_UF':'uf',
        'NM_UF':'estado'
    })
    brasil['geometry'] = brasil['geometry'].simplify(tolerance=0.01, preserve_topology=True)
    return brasil


def mapa_brasil(df, atributo, title):
    geojson = load_geojson()
    m = folium.Map(
        location=[-14.619526, -53.662294],
        tiles='cartodbpositron',
        position='relative',
        prefer_canvas=True,
        control_scale=True,
        zoom_control=False,
        zoom_start=4,
        min_zoom=3,
        max_zoom=8,
        zoom_delta=0.5,
        max_bounds=True,
        max_bounds_style='circle',
        dragging=True,
        scrollWheelZoom=True,
        attribution_control=True,        
    )
    folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=['estado', atributo],
        key_on='feature.properties.estado',
        fill_color='OrRd',
        fill_opacity=0.8,
        legend_name=f'{title}',
        smooth_factor=0.1
    ).add_to(m)  

    return m



    
@st.cache_data
def load_geojson_ba():
    bahia = gpd.read_file('dados/geojson/lmt_municipios_ba.geojson')
    bahia = bahia.rename(columns={
        'CD_MUN':'cod_ibge',
        'NM_MUN':'mun'
    })
    bahia['geometry'] = bahia['geometry'].simplify(tolerance=0.01, preserve_topology=True)
    return bahia


def mapa_bahia(df, atributo, title):
    geojson = load_geojson_ba()
    m = folium.Map(
        location=[-13.325673, -42.063333],
        tiles='cartodbpositron',
        position='relative',
        prefer_canvas=True,
        control_scale=True,
        zoom_control=False,
        zoom_start=6,
        min_zoom=3,
        max_zoom=8,
        zoom_delta=0.5,
        max_bounds=True,
        max_bounds_style='circle',
        dragging=True,
        scrollWheelZoom=True,
        attribution_control=True,        
    )
    folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=['mun', atributo],
        key_on='feature.properties.mun',
        fill_color='OrRd',
        fill_opacity=0.8,
        legend_name=f'{title}',
        smooth_factor=0.1
    ).add_to(m)  

    return m