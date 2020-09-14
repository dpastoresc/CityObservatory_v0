import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import getRootPath
from preprocess.bike import preprocessBikeTravelsEveryHour, preprocessBikeTravelsSankeyZip, \
    preprocessBikeTravelsSankeyDistritos


def paintBikeTravelsEveryHour(year, month):
    if not (os.path.exists(os.path.join(getRootPath(), 'data/bike/' + year + month + '_movements_hour.csv'))):
        preprocessBikeTravelsEveryHour(year, month)

    groupedby_hour = pd.read_csv(os.path.join(getRootPath(), 'data/bike/' + year + month + '_movements_hour.csv'))

    fig = px.bar(x=groupedby_hour.index, y=groupedby_hour['travels'])

    return fig


def paintBikeTravelsSankey(year, month):
    if not (os.path.exists(os.path.join(getRootPath(), 'data/bike/' + year + str(month) + '_movements_Distritos.csv'))):
        preprocessBikeTravelsSankeyDistritos(year, month)

    grouped_byDistrito_count = pd.read_csv(
        os.path.join(getRootPath(), 'data/bike/' + year + str(month) + '_movements_Distritos.csv'))

    barrios = list(set(list(grouped_byDistrito_count['unplug_stationDistrito'])))
    s = [barrios.index(zip) for zip in list(grouped_byDistrito_count['unplug_stationDistrito'])]
    t = [barrios.index(zip) for zip in list(grouped_byDistrito_count['plug_stationDistrito'])]
    v = list(grouped_byDistrito_count['travels'])

    # Creating colors dics
    dic_colors_barrios = {}
    colors = [

        'rgba(31, 119, 180, 0.8)',
        'rgba(255, 127, 14, 0.8)',
        'rgba(44, 160, 44, 0.8)',
        'rgba(214, 39, 40, 0.8)',
        'rgba(148, 103, 189, 0.8)',
        'rgba(140, 86, 75, 0.8)',
        'rgba(227, 119, 194, 0.8)',
        'rgba(127, 127, 127, 0.8)',
        'rgba(188, 189, 34, 0.8)',
        'rgba(23, 190, 207, 0.8)'
    ]
    for barrio in barrios:
        index = barrios.index(barrio)
        dic_colors_barrios[barrios.index(barrio)] = colors[index]
    dic_colors_links = []
    for element in s:
        dic_colors_links.append(dic_colors_barrios[element])

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=barrios,
            customdata=barrios,
            color=colors,
            hovertemplate='El barrio %{customdata} ha tenido un total de viajes de: %{value}<extra></extra>',
        ),
        link=dict(
            source=s,
            target=t,
            value=v,
            color=dic_colors_links,
            customdata = barrios,
            hovertemplate='Desde %{source.customdata}<br />' +
                          'hasta %{target.customdata}<br />ha habido %{value} viajes<extra></extra>'
        ))])

    fig.update_layout(title_text="Viajes entre los barrios de Madrid", font_size=10)
    return fig

# Example
# fig = paintBikeTravelsEveryHour('2020', '02')
# fig.show()
# fig = paintBikeTravelsSankey('2020', '02')
# fig.show()
