import folium
import os
import random
import pandas as pd

# Lista de cores predefinidas
colors = [
    "#d6616b", "#e7ba52", "#9c9ede", "#cedb9c", "#e7969c", "#7b4173",
    "#a55194", "#637939", "#a55194", "#ff7f0e", "#2ca02c", "#d62728",
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#aec7e8", "#ffbb78",
    "#98df8a", "#ff9896", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7",
    "#dbdb8d", "#9edae5", "#ad494a", "#8c6d31", "#843c39", "#b5cf6b",
    "#17becf", "#aec7e8", "#ffbb78", "#98df8a", "#ff9896"
]

# Criar o mapa centrado em Cascavel, Paraná
cascavel_coords = (-24.9574, -53.4595)
m = folium.Map(location=cascavel_coords, zoom_start=12, tiles='CartoDB positron')

# Pasta contendo os arquivos GeoJSON
geojson_folder = "geoJsonBairros"
geojson_group = folium.FeatureGroup(name="Bairros")

# Iterar pelos arquivos GeoJSON na pasta
for filename in os.listdir(geojson_folder):
    if filename.endswith(".geojson"):
        filepath = os.path.join(geojson_folder, filename)
        if colors:
            color = colors.pop(0)
            folium.GeoJson(filepath, name=filename, style_function=lambda x, color=color: {
                "fillColor": color,
                "fillOpacity": .9,
                "color": "none"
            }).add_to(geojson_group)

# Adicionar o FeatureGroup ao mapa
geojson_group.add_to(m)

# Adicionar controle de camadas ao mapa
# Adicionar tiles diferentes ao mapa
folium.TileLayer("OpenStreetMap").add_to(m)  # Adicionar OpenStreetMap
folium.TileLayer("CartoDB positron").add_to(m)  # Adicionar CartoDB Positron
folium.TileLayer("Stamen Terrain").add_to(m)  # Adicionar Stamen Terrain
	
folium.TileLayer("cartodbdark_matter").add_to(m)


def create_colored_icon(color):
    icon = folium.Icon(color=color)
    return icon


## NOMES BAIRROS
dfNome = pd.read_csv("Dados/nomesBairros.csv", sep=';')
nomeGrupo = folium.FeatureGroup(name="Nomes Bairros")
for index, row in dfNome.iterrows():
    nome = row["Bairro"]
    lat = row["Latitude"]
    lon = row["Longitude"]

    icon_html = f"""<div style="font-family: courier new; color: black">{nome}</div>"""
    icon = folium.DivIcon(html=icon_html)
    folium.Marker(location=(lat, lon), icon=icon).add_to(nomeGrupo)

nomeGrupo.add_to(m)


## CASOS
dfCasos = pd.read_csv("Dados/geoBairrosConfirmados.csv", sep=';')
marker_group = folium.FeatureGroup(name="Casos de COVID-19")
marker_group1 = folium.FeatureGroup(name="Nº Casos de COVID-19")
for index, row in dfCasos.iterrows():
    nome = row["nomeBairro"]
    casos = row["casosBairro"]
    lat = row["Latitude"]
    lon = row["Longitude"]
    popup_text = f"Bairro: {nome}<br>Casos: {casos}"
    folium.Marker(location=(lat, lon), popup=popup_text).add_to(marker_group)
    
    icon_html = f"""<div style="font-family: courier new; color: blue">{casos}</div>"""
    icon = folium.DivIcon(html=icon_html)
    folium.Marker(location=(lat, lon), icon=icon).add_to(marker_group1)


marker_group.add_to(m)
marker_group1.add_to(m)

## OBITOS
dfObitos = pd.read_csv("Dados/geoBairrosObitos.csv", sep=';')
marker_group2 = folium.FeatureGroup(name="Óbitos COVID-19")
marker_group3 = folium.FeatureGroup(name="Nº Óbitos de COVID-19")
for index, row in dfObitos.iterrows():
    nome = row["nomeBairro"]
    obitos = row["casosBairro"]
    lat = row["Latitude"]
    lon = row["Longitude"]
    popup_text = f"Bairro: {nome}<br>Óbitos: {obitos}"
    icon_color = 'red'  # Define a cor do ícone do marcador
    icon = create_colored_icon(icon_color)
    folium.Marker(location=(lat, lon), popup=popup_text, icon=icon).add_to(marker_group2)

    icon_html = f"""<div style="font-family: courier new; color: red">{obitos}</div>"""
    icon = folium.DivIcon(html=icon_html)
    folium.Marker(location=(lat, lon), icon=icon).add_to(marker_group3)

marker_group2.add_to(m)
marker_group3.add_to(m)





# Adicionar controle de camadas ao mapa
folium.LayerControl().add_to(m)
m.save('mapa.html')


