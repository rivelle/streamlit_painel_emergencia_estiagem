import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
import folium
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from utils import mapa_bahia


st.set_page_config(layout="wide")

st.title("Panorama Geral Bahia")
st.divider()

mun_estiagem = gpd.read_file('dados/dados.gpkg', leayer='mun_estiagem')
mun_estiagem = mun_estiagem[mun_estiagem['Situaçăo'] == 'Situaçăo de Emergęncia']

mun_ope_pipa = gpd.read_file('dados/dados.gpkg', layer='mun_operacaopipa')
mun_ope_pipa = mun_ope_pipa[mun_ope_pipa['Situacao'].notnull()]


st.write(mun_estiagem)
st.write(mun_ope_pipa)


