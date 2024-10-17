import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Tente carregar os dados
try:
    df = pd.read_csv('C:/Users/diogo/Downloads/ecommerce_estatistica.csv')  # Carrega o arquivo CSV
    print(df.head())  # Exibe as primeiras linhas do DataFrame
    print(df.info())  # Exibe informações sobre as colunas e tipos de dados
    print(df.describe())  # Exibe estatísticas descritivas das colunas numéricas
    pd.set_option('display.max_columns', None)  # Configura o Pandas para mostrar todas as colunas
    print(df)  # Exibe o DataFrame completo
    print(df.isnull().sum())  # Verifica e exibe a contagem de valores nulos em cada coluna
except Exception as e:
    print(f"Erro ao carregar os dados: {e}")  # Mensagem de erro caso falhe ao carregar os dados

def cria_graficos(df):
    # Filtra as 15 marcas mais populares
    top_brands = df['Marca'].value_counts().nlargest(15).index
    df_filtered = df[df['Marca'].isin(top_brands)]  # Filtra o DataFrame para incluir apenas as marcas populares

    # Cria gráfico de histograma da nota dos produtos
    fig1 = px.histogram(df_filtered, x='Nota', nbins=30, title='Distribuição da Nota dos Produtos')
    fig1.update_layout(xaxis_title='Nota', yaxis_title='Contagem', legend_title='Distribuição')

    # Cria gráfico de pizza para distribuição de marcas
    fig2 = px.pie(df_filtered, names='Marca', values='N_Avaliações', title='Distribuição de Marcas', hole=0.1)
    fig2.update_layout(height=600, width=900)

    # Cria gráfico de dispersão: Nota vs Preço
    fig3 = px.scatter(df_filtered, x='Preço', y='Nota', color='Marca', hover_name='Título', size_max=20)
    fig3.update_layout(title='Nota vs. Preço dos Produtos', xaxis_title='Preço', yaxis_title='Nota', legend_title='Marca')

    # Cria gráfico de linha: Nota por Desconto
    fig4 = px.line(df_filtered, x='Desconto', y='Nota', color='Marca', title='Nota por Desconto')
    fig4.update_layout(xaxis_title='Desconto', yaxis_title='Nota', legend_title='Marca')

    # Cria gráfico de barras: Quantidade de Avaliações por Marca
    fig5 = px.bar(df_filtered, x='Título', y='N_Avaliações', title='Quantidade de Avaliações por Marca')
    fig5.update_layout(height=800, width=1200, xaxis_title='Título', yaxis_title='N_Avaliações', legend_title='Marca')

    return fig1, fig2, fig3, fig4, fig5, top_brands  # Retorna todos os gráficos e as marcas populares

def cria_grafico_3d(filtered_df):
    # Cria um gráfico 3D: Preço vs Nota vs Desconto
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=filtered_df['Preço'],
        y=filtered_df['Nota'],
        z=filtered_df['Desconto'],
        mode='markers',
        marker=dict(
            size=12,
            color=filtered_df['N_Avaliações'],  # Cor baseada no número de avaliações
            colorscale='Viridis',
            colorbar=dict(title='N_Avaliações'),
            showscale=True
        ),
        text=filtered_df['Título']  # Mostra o título do produto ao passar o mouse
    )])

    fig_3d.update_layout(title='Gráfico 3D: Preço vs. Nota vs. Desconto',
                         scene=dict(
                             xaxis_title='Preço',
                             yaxis_title='Nota',
                             zaxis_title='Desconto'
                         ))
    return fig_3d  # Retorna o gráfico 3D

def cria_app(df):
    app = Dash(__name__)  # Cria uma instância do aplicativo Dash

    # Gera os gráficos iniciais
    fig1, fig2, fig3, fig4, fig5, top_brands = cria_graficos(df)

    # Define o layout da aplicação
    app.layout = html.Div([
        html.H1("Análise de Produtos E-commerce", style={'textAlign': 'center'}),  # Título do aplicativo

        html.Div([
            dcc.Graph(figure=fig1, id='histogram-plot'),  # Gráfico de histograma
            dcc.Dropdown(
                id='histogram-dropdown',
                options=[{'label': brand, 'value': brand} for brand in top_brands],  # Opções do dropdown
                value=top_brands[0],  # Valor padrão
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(figure=fig2),  # Gráfico de pizza
            dcc.Graph(id='scatter-plot'),  # Gráfico de dispersão
            dcc.Dropdown(
                id='scatter-dropdown',
                options=[{'label': brand, 'value': brand} for brand in top_brands],  # Opções do dropdown
                value=top_brands[0],  # Valor padrão
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='line-chart'),  # Gráfico de linha
            dcc.Dropdown(
                id='line-dropdown',
                options=[{'label': brand, 'value': brand} for brand in top_brands],  # Opções do dropdown
                value=top_brands[0],  # Valor padrão
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='bar-chart'),  # Gráfico de barras
            dcc.Dropdown(
                id='bar-dropdown',
                options=[{'label': brand, 'value': brand} for brand in top_brands],  # Opções do dropdown
                value=top_brands[0],  # Valor padrão
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='3d-scatter'),  # Gráfico 3D
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})  # Estilização do layout
    ])

    # Define os callbacks para atualizar os gráficos com base na seleção do usuário
    @app.callback(
        [Output('scatter-plot', 'figure'),
         Output('line-chart', 'figure'),
         Output('bar-chart', 'figure'),
         Output('3d-scatter', 'figure'),
         Output('histogram-plot', 'figure')],
        [Input('scatter-dropdown', 'value'),
         Input('line-dropdown', 'value'),
         Input('bar-dropdown', 'value'),
         Input('histogram-dropdown', 'value')]
    )
    def update_graphs(scatter_brand, line_brand, bar_brand, histogram_brand):
        # Filtra os dados com base na marca selecionada em cada gráfico
        filtered_scatter = df[df['Marca'] == scatter_brand]
        filtered_line = df[df['Marca'] == line_brand]
        filtered_bar = df[df['Marca'] == bar_brand]
        filtered_histogram = df[df['Marca'] == histogram_brand]

        # Atualiza o gráfico de dispersão
        scatter_fig = px.scatter(
            filtered_scatter,
            x='Preço',
            y='Nota',
            color='Marca',
            hover_name='Título',
            title=f'Nota vs. Preço - {scatter_brand}'  # Título dinâmico
        )

        # Atualiza o gráfico de linha
        line_fig = px.line(
            filtered_line,
            x='Desconto',
            y='Nota',
            color='Marca',
            title=f'Nota por Desconto - {line_brand}'  # Título dinâmico
        )

        # Atualiza o gráfico de barras
        bar_fig = px.bar(
            filtered_bar,
            x='Título',
            y='N_Avaliações',
            title=f'Quantidade de Avaliações - {bar_brand}'  # Título dinâmico
        )

        # Atualiza o gráfico 3D com os dados filtrados
        fig_3d = cria_grafico_3d(filtered_bar)

        # Atualiza o gráfico de histograma
        histogram_fig = px.histogram(
            filtered_histogram,
            x='Nota',
            nbins=30,
            title=f'Distribuição da Nota - {histogram_brand}'  # Título dinâmico
        )

        return scatter_fig, line_fig, bar_fig, fig_3d, histogram_fig  # Retorna os gráficos atualizados

    return app  # Retorna a instância do aplicativo

# Cria a instância do aplicativo
app = cria_app(df)

# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Inicia o servidor do Dash
