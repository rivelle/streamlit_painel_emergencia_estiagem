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
        zoom_start=3,
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


def mapa_bahia(df, atributo, zoom, title):
    geojson = load_geojson_ba()
    m = folium.Map(
        location=[-13.325673, -42.063333],
        tiles='cartodbpositron',
        position='relative',
        prefer_canvas=False,
        control_scale=True,
        zoom_control=False,
        zoom_start=zoom,
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
        line_weight=0.1,
        line_color='black',
        legend_name=f'{title}',
        smooth_factor=0.1,
        nan_fill_color='white',
    ).add_to(m)  

    estilo = lambda x: {
        'fillColor': 'white',
        'color': 'black',
        'fillOpacity': 0.001,
        'weight': 0.5
    }
    estilo_destaque = lambda x: {
        'fillColor': 'yellow',
        'color': 'black',
        'fillOpacity': 0.5,
        'weight': 1.5
    }

    highlight = folium.features.GeoJson(data=geojson,
                                        style_function=estilo,
                                        highlight_function=estilo_destaque,
    )

    folium.features.GeoJsonTooltip(
        fields=['mun', 'TER_IDENT'],
        aliases=['Município:', 'Território:'],
        localize=True,
    ).add_to(highlight)

    m.add_child(highlight)

    return m


def mapa_geral(df1, df2):
    geojson = load_geojson_ba()
    mun_estiagem = gpd.read_file('dados/dados.gpkg', leayer='mun_estiagem')
    mun_estiagem = mun_estiagem[mun_estiagem['Situaçăo'] == 'Situaçăo de Emergęncia']
    mun_estiagem['cod_situacao'] = 1

    m = folium.Map(
        location=[-13.325673, -42.063333],
        tiles='openstreetmap',
        position='relative',        
        control_scale=True,
        zoom_control='bottomleft',
        zoom_start=7,
        zoom_delta=0.5,
        max_bounds=True,
        max_bounds_style='circle',
        dragging=True,
        scrollWheelZoom=True,
        attribution_control=True)
    
    base_mun = folium.Choropleth(
         geo_data=geojson,
         fill_color='white',
         fill_opacity=0.1,
         line_color='gray',
         line_weight=0.5,
         nan_fill_color='white',
         nan_fill_opacity=0,
         control=False,
         legend_name='Limites Municipais'
    )
    m.add_child(base_mun)
    
    mun_estiagem = folium.Choropleth(
        geo_data=geojson,
        data=df1,
        columns=['mun', 'cod_situacao'],
        key_on='feature.properties.mun',
        fill_color='Reds',
        fill_opacity=1,
        line_weight=0.3,
        line_color='black',
        name='Municípios em Emergência Estiagem',
        smooth_factor=0.1,
        nan_fill_color='white',
        nan_fill_opacity=0,
        show=True,
    ).add_to(m)

    est_fam = folium.Choropleth(
        geo_data=geojson,
        data=df2,
        columns=['mun', 'est_agricf'],
        key_on='feature.properties.mun',
        fill_color='OrRd',
        fill_opacity=1,
        line_weight=0.3,
        line_color='black',
        name='Estabelecimentos Familiares por Município',
        legend_name=f'Estabelecimentos Familiares por Município',
        smooth_factor=0.1,
        nan_fill_color='white',
        nan_fill_opacity=0,
        show=False,
    ).add_to(m)


    percent_est_fam = folium.Choropleth(
        geo_data=geojson,
        data=df2,
        columns=['mun', 'percent_fam'],
        key_on='feature.properties.mun',
        fill_color='YlOrBr',
        fill_opacity=1,
        line_weight=0.3,
        line_color='black',
        name='Percentual de Estabelecimentos Familiares por Município',
        legend_name='Percentual de Estabelecimentos Familiares por Município',
        smooth_factor=0.1,
        nan_fill_color='white',
        nan_fill_opacity=0,
        show=False,        
    ).add_to(m)

    folium.LayerControl(
        position='topleft',
        collapsed=False,
        draggable=True,
    ).add_to(m)

    # legenda_mapa = """
    # {% macro html(this,kwargs) %}
    #     <div style = "position: fixed;
    #     bottom: 20px;
    #     left: 1600px;
    #     width: 300px;
    #     height: 500px;
    #     font-size: 14px;
    #     z-index: 9999;        
    #     ">

    #     <h6><a style = "color: black; margin-left: 10px"><b>Legenda</b></a></h6>

    #     <p><a style = "color: OrRd; margin-left: 10px">&FilledSmallSquare;Estabelecimentos Familiares</a></p>
    #     </div>

    #     <div style = "position: fixed;
    #     bottom: 20px;
    #     left: 1600px;
    #     width: 300px;
    #     height: 500px;
    #     font-size: 14px;
    #     background-color: white;
    #     z-index: 9998;
    #     opacity: 0.6;
    #     border: 2px solid gray;
    #     border-radius: 10px;
    #     ">
    #     </div>

    # {% endmacro %}
    # """
    # legenda = branca.element.MacroElement()
    # legenda._template = branca.element.Template(legenda_mapa)

    # m.add_child(legenda)

    return m


def mapa_op_carropipa(df):
    geojson = load_geojson_ba()
    m = folium.Map(
        location=[-13.325673, -42.063333],
        tiles='openstreetmap',
        position='relative',        
        control_scale=True,
        zoom_control='bottomleft',
        zoom_start=7,
        zoom_delta=0.5,
        max_bounds=True,
        max_bounds_style='circle',
        dragging=True,
        scrollWheelZoom=True,
        attribution_control=True)
    
    base_mun = folium.Choropleth(
         geo_data=geojson,
         fill_color='white',
         fill_opacity=0.1,
         line_color='gray',
         line_weight=0.5,
         nan_fill_color='white',
         nan_fill_opacity=0,
         control=False,
         legend_name='Limites Municipais'
    )
    m.add_child(base_mun)
    
    
    op_carropipa = folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=['mun', 'Populacao'],
        key_on='feature.properties.mun',
        fill_color='RdYlBu',
        fill_opacity=1,
        line_weight=0.3,
        line_color='black',
        name='Status Operação Carro Pipa nos Municípios',
        legend_name='Status Operação Carro Pipa nos Municípios',
        smooth_factor=0.1,
        nan_fill_color='white',
        nan_fill_opacity=0,
        show=True,
    ).add_to(m)


    folium.LayerControl(
        position='topleft',
        collapsed=False,
        draggable=False,
    ).add_to(m)

    return m