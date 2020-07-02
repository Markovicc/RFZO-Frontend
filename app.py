import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import requests


external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css', 'https://fonts.googleapis.com/icon?family=Material+Icons']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

dfl = pd.DataFrame(requests.get('https://trfzoapi.herokuapp.com/api/rfzo-lista').json())
df_lat_lon = pd.read_csv('list_lat_lon.csv')
df = dfl.merge(df_lat_lon)

in_dfc =df[df['Intervencija']=='Kateterizacija srca'][['Ustanova', 'Čekanje']]
in_dfb =df[df['Intervencija']=='Kateterizacija srca'][['Ustanova', 'Broj']]
dfsort = df.sort_values('Intervencija')

mapbox_access_token = 'pk.eyJ1IjoibWljY29tYXJrb3ZpYyIsImEiOiJjanRpd3kxa2cwMnUwM3lxanNxZW40aTZzIn0.hrRcDMWYmDMgkisNGQwssQ'



color_list = ['#546e7a', '#ce93d8', '#00b0ff', '#a1887f','#f57c00','#00796b','#7986cb','#ff5252','#66bb6a', '#ff7043', '#f9a825','#546e7a', '#ce93d8', '#00b0ff', '#a1887f','#f57c00','#00796b']


app.layout = html.Div([


    #html.Nav(className='row card-panel teal lighten-2'),


        html.Div([

        html.Header([

                #html.Div([html.I('accessible',  style={'fontSize': '8rem'}, className='material-icons blue-accent-3-text center')], className='row center'),
                html.Div([html.H1('Liste čekanja',style={'fontSize': '8rem'},className='lime-text text-darken-2 center')], className='col l6 s6')],
                style={'backgroundImage':'url(assets/health2.jpg)', 'backgroundSize': 'cover', 'backgroundPosition': 'center', 'minWidth':'100%', 'minHeighth':'100%'}, className='card large light-grey row'),


        html.Section([

         html.Div([


            html.Div([
             html.Div([
              html.I('accessible', className='material-icons small prefix lime-text text-darken-2'),
              html.Span('Izaberite vrstu intervencije/pregleda', style={'fontSize':'1.1rem'}, className='lime-text text-darken-2')]),
            html.Div(dcc.Dropdown(
            id='my-dropdown1',
            options=[
               {'label': i, 'value': i} for i in dfsort['Intervencija'].unique().tolist()],
             value=dfsort['Intervencija'].unique().tolist()[0]), className='row')
             ], className='col l6 s12'),

          html.Div([
            html.Div([
            html.I('local_hospital', className='material-icons small prefix lime-text text-darken-2'),
            html.Span('Izaberite zdravstvenu ustanovu', style={'fontSize':'1.1rem'}, className='lime-text text-darken-2')]),
            html.Div(dcc.Dropdown(
            id='my-dropdown2',
            options=[
             {'label': i, 'value': i} for i in dfsort['Ustanova'].unique().tolist()],
            value=dfsort['Ustanova'].unique().tolist()[0]), className='row')
            ], className='col l6 s12'),


           ], className='row'),

           html.Div([

           html.Div([html.H5(id='inter_ust', style={'fontSize':'1.4rem'}, className='lime-text text-darken-2'),
           html.Div(className='divider teal'),
           html.Div(html.P('Stanje za izabranu intervenciju i ustanovu',style={'fontSize':'0.7rem'},
           className='row lime-text text-darken-2'))],
           className='col l3 s12 card-panel indigo lighten-1'),


           html.Div([

            html.Div([
            html.Ul([
            html.Li([
            html.P('Prosečno čekanje u danima', style={'fontSize': '0.65rem'}, className='red-text text-darken-2 btn')]),
            html.Li([
            html.I('event_note', style={'fontSize': '5rem'}, className='material-icons teal-text text-lighten-1'),
            html.Span('', style={'fontSize': '3.5rem'}, id='days', className='red-text right text-darken-3')]),
            html.Div(className='divider teal'),
             ])], className='card-panel indigo lighten-1 col l3 s12'),

           html.Div([
            html.Ul([
            html.Li([
            html.P('Broj pacijenata na listi', style={'fontSize': '0.65rem'}, className='red-text text-darken-2 btn')]),
            html.Li([
            html.I('people', style={'fontSize': '5rem'}, className='material-icons teal-text text-lighten-1'),
            html.Span('', id='pac', style={'fontSize': '3.5rem'}, className='red-text right text-darken-3')]),
            html.Div(className='divider teal'),
             ])], className='card-panel indigo lighten-1 col l3 s12'),

            html.Div([
            html.Ul([
            html.Li([
            html.P('Probijen zakonski rok', style={'fontSize': '0.65rem'}, className='red-text text-darken-2 btn')]),
            html.Li([
            html.I('timelapse', style={'fontSize': '5rem'}, className='material-icons teal-text text-lighten-1'),
            html.Span('', id='warn', style={'fontSize': '3.5rem'}, className='red-text right text-darken-3')]),
            html.Div(className='divider teal'),
             ])], className='card-panel indigo lighten-1 col l3 s12')

              ], className='row'),

       html.Div(className='divider'),



          html.Div([

          html.Div([
          html.P('Poređenje s drugim ustanovama | Broj pacijenata', style={'fontSize':'1.5rem'}, className='teal-text text-lighten-2 card-panel indigo lighten-1'),
          dcc.Graph(id='map-graph', config={'displayModeBar':False})],
          className='col l6 s12'),

          html.Div([
          html.P('Čekanje na intervenciju, u danima', style={'fontSize':'1.5rem'}, className='teal-text text-lighten-2 card-panel indigo lighten-1'),
          #html.P('Na grafici je izraženo prosečno čekanje u danima za izabranu intervenciju, a izabrana ustanova je markirana crvenom bojom',
          #className='lime-text text-darken-2'),
          dcc.Graph(id='graph1', config={'displayModeBar':False}),


           ], className='col l6 s12')

          ], className='row'),




          ], className='row')],
           className='card-panel indigo lighten-4'),



       html.Section([
       html.H4('Profili zdravstvenih ustanova', className='teal-text text-lighten-2 center card-panel indigo lighten-1'),
       html.Div([
        html.I('pin_drop', className='material-icons small prefix lime-text text-darken-2'),
        html.Span('Izaberite zdravstvenu ustanovu', style={'fontSize':'1.1rem'}, className='lime-text text-darken-2')]),

       dcc.Dropdown(
        id='my-dropdown3',
        options=[
          {'label': i, 'value': i} for i in df['Ustanova'].unique().tolist()],
        value=df['Ustanova'].unique().tolist()[0]),


        html.Div([

        html.Div([
          html.P('Naziv zdravstvene ustanove', style={'fontSize': '0.7rem'}, className='lime-text text-darken-2 btn'),
          html.Div([

          html.I('local_hospital', style={'fontSize': '6rem'}, className='material-icons prefix left teal-text text-lighten-2'),
          html.Span(id='ust', style={'fontSize': '2rem'}, className='light-green-text text-darkenn-2')], className='row')
          ], className='col l8 s12 card panel indigo lighten-1'),


         html.Div([
           html.P('Broj pacijenata na listama čekanja', style={'fontSize': '0.7rem'}, className='lime-text text-darken-2 btn'),
           html.Div([
           html.I('people', style={'fontSize': '6rem'}, className='material-icons prefix left teal-text text-lighten-2'),
           html.Span('', id='pac-number2', style={'fontSize': '4em'}, className='teal-text text-lighten-2')], className='row')
           ], className='col l4 s12 card panel indigo lighten-1'),

         ], className='row align'),



        html.H6(id='pac-number', style = {'textAlign': 'center'}),


       html.Div([

        html.Div([
        html.P('Čekanje na intervenciju, u danima', style={'fontSize':'1.5rem'}, className='teal-text text-lighten-2 card-panel indigo lighten-1'),
        dcc.Graph(id='graph3', config={'displayModeBar':False})],className='col l6 s12'),

        html.Div([
        html.P('Broj pacijenata po intervenciji', style={'fontSize':'1.5rem'},className='teal-text text-lighten-2 card-panel indigo lighten-1'),
        dcc.Graph(id='graph4', config={'displayModeBar':False})],className='col l6 s12')

        ], className='row')

        ], className='card-panel indigo lighten-4'),

        html.Footer([

          html.Div([
           html.P('© 2019 Copyright javno.rs')

        ], className='footer-copyright')

        ], className='page-footer indigo lighten-4')






        ], className='container')
        ])


@app.callback(
    Output('my-dropdown2', 'options'),
    [Input('my-dropdown1', 'value')])
def set_cities_options(selected_int):
    return [{'label': i, 'value': i} for i in dfsort[dfsort['Intervencija']==selected_int]['Ustanova']]

@app.callback(
    Output('days', 'children'),
    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value')])
def set_cities_options(sel_int, sel_ust):
    num_days = df.loc[(df['Intervencija']==sel_int)&(df['Ustanova']==sel_ust),'Čekanje'].iloc[0]
    return '{}'.format(num_days)

@app.callback(
    Output('pac', 'children'),
    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value')])
def set_pac_options(sel_int, sel_ust):
    num_pac = df.loc[(df['Intervencija']==sel_int)&(df['Ustanova']==sel_ust),'Broj'].iloc[0]
    return '{}'.format(num_pac)

@app.callback(
    Output('warn', 'children'),
    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value')])
def set_pac_options(sel_int, sel_ust):
    num_pac = df.loc[(df['Intervencija']==sel_int)&(df['Ustanova']==sel_ust),'Rok'].iloc[0]
    return '{}'.format(num_pac)



@app.callback(
    Output('graph1', 'figure'),
    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value')])
def make_bar_graph_1(sel_int, sel_ust):
    gf = df[df['Intervencija']==sel_int][['Ustanova', 'Čekanje']].sort_values('Čekanje', ascending=False)
    figure = {
    'data': [{'y':gf['Ustanova'], 'x': gf['Čekanje'], 'type': 'bar', 'orientation': 'h',
    'marker': {'color':['#ff5252' if i == sel_ust else '#00695c' for i in gf['Ustanova'].tolist()], 'opacity':0.7}}],
    'layout': {#'title': 'Prosečno čekanje na intervenciju, po gradovima',
              'yaxis':{'showticklabels':False}, 'paper_bgcolor':'rgba(0,0,0,0)', 'hovermode':'closest','margin':{'l':5, 'r':0, 't':0, 'b':15},
              'plot_bgcolor':'rgba(0,0,0,0)'}


    }

    return figure

#@app.callback(
#    Output('graph2', 'figure'),
#    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value')])
#def make_bar_graph_2(sel_int, sel_ust):
#    gf = df[df['Intervencija']==sel_int][['Ustanova', 'Broj']].sort_values('Broj', ascending=False)
#    figure = {
#    'data': [{'x':gf['Ustanova'], 'y': gf['Broj'], 'type': 'bar',
#    'marker': {'color':['#ff5252' if i == sel_ust else '#00695c' for i in gf['Ustanova'].tolist()], 'opacity':0.9}}],
#    'layout': {'title': 'Broj pacijenata koji čekaju na intervenciju, po gradovima',
#              'xaxis':{'showticklabels':False}, 'paper_bgcolor':'rgba(0,0,0,0)','plot_bgcolor':'rgba(0,0,0,0)'}
#    }
#    return figure

@app.callback(
    Output('map-graph', 'figure'),
    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value') ])
def gen_map(sel_int, sel_ust):
    dfmap = df[df['Intervencija']==sel_int][['Ustanova', 'Lat', 'Long', 'Broj']]

    return {
        "data": [
                {
                    "type": "scattermapbox",
                    "lat": dfmap['Lat'],
                    "lon": dfmap['Long'],
                    "mode": "markers",
                    'ust': dfmap['Ustanova'],
                    "name": dfmap['Ustanova'],
                    'text': dfmap['Ustanova'],
                    'hoverinfo': 'text',
                    "marker": {
                        "size": [int(i)/100+35 for i in dfmap['Broj'].tolist()],
                        "opacity": 0.7,
                        "color": ['#ff5252' if i == sel_ust else '#00695c' for i in dfmap['Ustanova'].tolist()]

                    }
                }
            ],
        "layout": dict(
            height = 440,
            autosize=True,
            margin=dict(
                l=1,
                r=1,
                b=1,
                t=1
            ),
            hovermode="closest",
            #plot_bgcolor="#191A1A",
            #paper_bgcolor="indianred",
            #legend=dict(font=dict(size=10), orientation='h'),
            #title='Pređi mišem preko mape za više informacija',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style='light',
                center=dict(
                    lon=20.90,
                    lat=44.42
                ),
                zoom=5.9,
            )
        )

       }
@app.callback(
    Output('inter_ust', 'children'),
    [Input('my-dropdown1', 'value'), Input('my-dropdown2', 'value')])
def set_pac_options(sel_int, sel_ust):
    return '{}, {}'.format(sel_int, sel_ust)

@app.callback(
    Output('pac-number2', 'children'),
    [Input('my-dropdown3', 'value')])
def set_pac_number(sel_ust):
    df_ust = df[df['Ustanova']==sel_ust]
    numpac = df_ust['Broj'].sum()
    return '{}'.format(numpac)


@app.callback(
    Output('ust', 'children'),
    [Input('my-dropdown3', 'value')])
def set_pac_options(sel_ust):
    return '{}'.format(sel_ust)

@app.callback(
    Output('graph3', 'figure'),
    [Input('my-dropdown3', 'value')])
def make_bar_graph_3(sel_ust):
    df_ust = df[df['Ustanova']==sel_ust].sort_values('Čekanje')
    clr = color_list[:len(df_ust)]
    figure = {
    'data': [{'y':df_ust['Intervencija'], 'x': df_ust['Čekanje'], 'type': 'bar', 'orientation': 'h',
    'marker': {'color':clr}, 'opacity':0.95}],
    'layout': {#'title': 'Čekanje na intervenciju, u danima',
     'hovermode':'closest', 'margin':{'l':5, 'r':0, 't':0, 'b':15},
              'yaxis':{'showticklabels':False}, 'paper_bgcolor':'rgba(0,0,0,0)','plot_bgcolor':'rgba(0,0,0,0)'}
    }
    return figure

@app.callback(
    Output('graph4', 'figure'),
    [Input('my-dropdown3', 'value')])
def make_bar_graph_4(sel_ust):
    df_ust = df[df['Ustanova']==sel_ust].sort_values('Čekanje')
    clr = color_list[:len(df_ust)]
    figure = {
    'data': [{'y':df_ust['Intervencija'], 'x': df_ust['Broj'], 'type': 'bar', 'orientation': 'h',
    'marker': {'color':clr}, 'opacity':0.95}],
    'layout': {#'title': 'Broj pacijenata po intervenciji',
     'hovermode':'closest', 'margin':{'l':5, 'r':0, 't':0, 'b':15},
              'yaxis':{'showticklabels':False}, 'paper_bgcolor':'rgba(0,0,0,0)','plot_bgcolor':'rgba(0,0,0,0)'}
    }
    return figure



if __name__ == '__main__':
    app.run_server(debug=True)
