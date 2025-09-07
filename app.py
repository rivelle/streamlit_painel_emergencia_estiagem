import streamlit as st


st.set_page_config(layout = 'wide', page_title = 'Monitoramento Estiagem', page_icon = '🌵')


home = st.Page(
    page = 'views/home.py',
    title = 'O Monitoramento Estiagem',
    icon = '🌵',
    default=True
)

# visao_geral = st.Page(
#     page = 'views/visao_geral.py',
#     title = 'Panorama Geral',
#     icon = '📊'
# )

mapas = st.Page(
    page = 'views/mapas.py',
    title = 'Mapa Geral',
    icon = '🌐'
)


pg = st.navigation(
    {
        "Principal":[home, mapas]
    }
)


pg.run()