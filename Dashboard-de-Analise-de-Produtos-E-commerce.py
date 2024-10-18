import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


# Função para carregar os dados de um arquivo CSV
def carregar_dados(caminho):
    """Carrega os dados de um arquivo CSV e retorna um DataFrame."""
    try:
        df = pd.read_csv(caminho)
        print(df.head())
        print(df.info())
        print(df.describe())
        pd.set_option('display.max_columns', None)  # Exibe todas as colunas
        print(df)
        print(df.isnull().sum())  # Verifica valores ausentes
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


# Função para criar gráficos a partir do DataFrame
def cria_graficos(df):
    """Cria gráficos a partir do DataFrame fornecido e retorna uma lista de figuras e marcas populares."""
    top_brands = df['Marca'].value_counts().nlargest(15).index
    df_filtered = df[df['Marca'].isin(top_brands)]  # Filtra o DataFrame para as top marcas

    # Cria os gráficos
    fig1 = px.histogram(df_filtered, x='Nota', nbins=30, title='Distribuição da Nota dos Produtos')
    fig2 = px.pie(df_filtered, names='Marca', values='N_Avaliações', title='Distribuição de Marcas', hole=0.1)
    fig3 = px.scatter(df_filtered, x='Preço', y='Nota', color='Marca', hover_name='Título', size_max=20)
    fig4 = px.line(df_filtered, x='Desconto', y='Nota', color='Marca', title='Nota por Desconto')
    fig5 = px.bar(df_filtered, x='Título', y='N_Avaliações', title='Quantidade de Avaliações por Marca')

    # Gráfico de barras por material e gênero
    fig_material_genero = px.bar(df_filtered,
                                 x='Material',
                                 color='Gênero',
                                 title='Quantidade de Produtos por Material e Gênero',
                                 barmode='group')

    # Ajusta o layout dos gráficos
    for fig in [fig1, fig2, fig3, fig4, fig5, fig_material_genero]:
        fig.update_layout(height=600, width=1455)

    return fig1, fig2, fig3, fig4, fig5, fig_material_genero, top_brands  # Retorna as figuras e marcas populares


# Função para criar um gráfico 3D
def cria_grafico_3d(filtered_df):
    """Cria um gráfico 3D a partir do DataFrame filtrado."""
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=filtered_df['Preço'],
        y=filtered_df['Nota'],
        z=filtered_df['Desconto'],
        mode='markers',
        marker=dict(
            size=12,
            color=filtered_df['N_Avaliações'],
            colorscale='Viridis',
            colorbar=dict(title='N_Avaliações'),
            showscale=True
        ),
        text=filtered_df['Título']
    )])

    fig_3d.update_layout(title='Gráfico 3D: Preço vs. Nota vs. Desconto',
                         scene=dict(
                             xaxis_title='Preço',
                             yaxis_title='Nota',
                             zaxis_title='Desconto'
                         ))
    return fig_3d


# Função para criar e configurar a aplicação Dash
def cria_app(df):
    """Cria e configura a aplicação Dash."""
    app = Dash(__name__)

    fig1, fig2, fig3, fig4, fig5, fig_material_genero, top_brands = cria_graficos(df)

    app.layout = html.Div(style={'backgroundColor': '#f0f0f0', 'padding': '20px'}, children=[
        html.H1("Análise de Produtos E-commerce", style={'textAlign': 'center', 'color': '#333'}),

        # Sliders para filtrar dados
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                html.Label("Faixa de Preço"),
                dcc.RangeSlider(
                    id='preco-slider',
                    min=df['Preço'].min(),
                    max=df['Preço'].max(),
                    value=[df['Preço'].min(), df['Preço'].max()],
                    marks={i: f'R${i}' for i in range(int(df['Preço'].min()), int(df['Preço'].max()) + 1, 50)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Div(id='preco-output', style={'textAlign': 'center'})
            ]),
            html.Div(className='four columns', children=[
                html.Label("Faixa de Nota"),
                dcc.RangeSlider(
                    id='nota-slider',
                    min=df['Nota'].min(),
                    max=df['Nota'].max(),
                    value=[df['Nota'].min(), df['Nota'].max()],
                    marks={i: str(i) for i in range(int(df['Nota'].min()), int(df['Nota'].max()) + 1)},
                    step=0.1,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Div(id='nota-output', style={'textAlign': 'center'})
            ]),
            html.Div(className='four columns', children=[
                html.Label("Faixa de Desconto"),
                dcc.RangeSlider(
                    id='desconto-slider',
                    min=df['Desconto'].min(),
                    max=df['Desconto'].max(),
                    value=[df['Desconto'].min(), df['Desconto'].max()],
                    marks={i: str(i) for i in range(int(df['Desconto'].min()), int(df['Desconto'].max()) + 1)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Div(id='desconto-output', style={'textAlign': 'center'})
            ]),
        ]),

        # Dropdowns para filtrar por gênero e material
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                html.Label("Gênero"),
                dcc.Dropdown(
                    id='genero-dropdown',
                    options=[{'label': genero, 'value': genero} for genero in df['Gênero'].unique()],
                    multi=True,
                    placeholder='Selecione um ou mais gêneros'
                )
            ]),
            html.Div(className='four columns', children=[
                html.Label("Material"),
                dcc.Dropdown(
                    id='material-dropdown',
                    options=[{'label': material, 'value': material} for material in df['Material'].unique()],
                    multi=True,
                    placeholder='Selecione um ou mais materiais'
                )
            ]),
        ]),

        # Gráficos abaixo dos filtros
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                dcc.Dropdown(id='histogram-dropdown',
                             options=[{'label': brand, 'value': brand} for brand in top_brands],
                             value=top_brands[0],
                             clearable=False,
                             style={'margin-top': '10px'}),
                dcc.Graph(figure=fig1, id='histogram-plot')
            ]),
            html.Div(className='four columns', children=[
                dcc.Graph(figure=fig2),
            ]),
            html.Div(className='four columns', children=[
                dcc.Dropdown(id='scatter-dropdown',
                             options=[{'label': brand, 'value': brand} for brand in top_brands],
                             value=top_brands[0],
                             clearable=False,
                             style={'margin-top': '10px'}),
                dcc.Graph(id='scatter-plot'),
            ]),
        ]),

        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                dcc.Dropdown(id='line-dropdown',
                             options=[{'label': brand, 'value': brand} for brand in top_brands],
                             value=top_brands[0],
                             clearable=False,
                             style={'margin-top': '10px'}),
                dcc.Graph(id='line-chart'),
            ]),
            html.Div(className='four columns', children=[
                dcc.Dropdown(id='bar-dropdown',
                             options=[{'label': brand, 'value': brand} for brand in top_brands],
                             value=top_brands[0],
                             clearable=False,
                             style={'margin-top': '10px'}),
                dcc.Graph(id='bar-chart'),
            ]),
            html.Div(className='four columns', children=[
                dcc.Graph(id='3d-scatter'),
            ]),
        ]),

        # Gráfico de barras por material e gênero
        html.Div(className='row', children=[
            html.Div(className='twelve columns', children=[
                dcc.Graph(figure=fig_material_genero)
            ])
        ]),
    ])

    # Define os callbacks para atualizar os gráficos e os valores dos sliders
    @app.callback(
        [Output('scatter-plot', 'figure'),
         Output('line-chart', 'figure'),
         Output('bar-chart', 'figure'),
         Output('3d-scatter', 'figure'),
         Output('histogram-plot', 'figure'),
         Output('preco-output', 'children'),
         Output('nota-output', 'children'),
         Output('desconto-output', 'children')],
        [Input('scatter-dropdown', 'value'),
         Input('line-dropdown', 'value'),
         Input('bar-dropdown', 'value'),
         Input('histogram-dropdown', 'value'),
         Input('preco-slider', 'value'),
         Input('nota-slider', 'value'),
         Input('desconto-slider', 'value'),
         Input('genero-dropdown', 'value'),
         Input('material-dropdown', 'value')]
    )
    def update_graphs(scatter_brand, line_brand, bar_brand, histogram_brand, preco_range, nota_range, desconto_range,
                      generos_selecionados, materiais_selecionados):
        # Filtra os dados com base na marca selecionada e nos sliders
        filtered_df = df[
            (df['Marca'] == scatter_brand) &
            (df['Preço'] >= preco_range[0]) & (df['Preço'] <= preco_range[1]) &
            (df['Nota'] >= nota_range[0]) & (df['Nota'] <= nota_range[1]) &
            (df['Desconto'] >= desconto_range[0]) & (df['Desconto'] <= desconto_range[1])
            ]

        # Aplica filtros de gênero e material
        if generos_selecionados:
            filtered_df = filtered_df[filtered_df['Gênero'].isin(generos_selecionados)]
        if materiais_selecionados:
            filtered_df = filtered_df[filtered_df['Material'].isin(materiais_selecionados)]

        # Filtra o DataFrame para o histograma
        filtered_histogram = df[
            (df['Marca'] == histogram_brand) &
            (df['Preço'] >= preco_range[0]) & (df['Preço'] <= preco_range[1]) &
            (df['Nota'] >= nota_range[0]) & (df['Nota'] <= nota_range[1]) &
            (df['Desconto'] >= desconto_range[0]) & (df['Desconto'] <= desconto_range[1])
            ]

        # Aplica filtros de gênero e material ao histograma
        filtered_histogram = filtered_histogram[
            (filtered_histogram['Gênero'].isin(generos_selecionados)) &
            (filtered_histogram['Material'].isin(materiais_selecionados))
            ] if generos_selecionados and materiais_selecionados else filtered_histogram

        # Filtra o DataFrame para o gráfico de linha
        filtered_line = df[df['Marca'] == line_brand]

        # Cria os gráficos atualizados
        scatter_fig = px.scatter(filtered_df, x='Preço', y='Nota', color='Marca', hover_name='Título',
                                 title=f'Nota vs. Preço - {scatter_brand}')
        line_fig = px.line(filtered_line, x='Desconto', y='Nota', color='Marca',
                           title=f'Nota por Desconto - {line_brand}')
        bar_fig = px.bar(filtered_df, x='Título', y='N_Avaliações', title=f'Quantidade de Avaliações - {bar_brand}')
        fig_3d = cria_grafico_3d(filtered_df)
        histogram_fig = px.histogram(filtered_histogram, x='Nota', nbins=30,
                                     title=f'Distribuição da Nota - {histogram_brand}')

        # Atualiza os rótulos dos sliders
        preco_label = f'Faixa de Preço: R${preco_range[0]} - R${preco_range[1]}'
        nota_label = f'Faixa de Nota: {nota_range[0]} - {nota_range[1]}'
        desconto_label = f'Faixa de Desconto: {desconto_range[0]}% - {desconto_range[1]}%'

        return scatter_fig, line_fig, bar_fig, fig_3d, histogram_fig, preco_label, nota_label, desconto_label

    return app  # Retorna a aplicação Dash


# Carrega os dados e cria a instância do aplicativo
caminho_dados = 'C:/Users/diogo/Downloads/ecommerce_estatistica.csv'
df = carregar_dados(caminho_dados)  # Carrega os dados
app = cria_app(df)  # Cria a aplicação

# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Inicia o servidor
