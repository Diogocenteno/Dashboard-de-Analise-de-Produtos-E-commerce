Análise de Produtos E-commerce
Este projeto consiste em uma aplicação Dash para análise interativa de dados de produtos de e-commerce. Utilizando gráficos dinâmicos, a aplicação permite explorar a relação entre preço, nota, avaliações e descontos de produtos, além de filtrar informações por gênero e material.

Funcionalidades
Distribuição de Notas: Histograma mostrando a distribuição das notas dos produtos.
Distribuição de Marcas: Gráfico de pizza representando a participação das marcas.
Relação Preço x Nota: Gráfico de dispersão com a relação entre preço e nota, destacando diferentes marcas.
Nota por Desconto: Gráfico de linha que mostra como as notas dos produtos variam com o desconto.
Avaliações por Marca: Gráfico de barras que exibe a quantidade de avaliações por título de produto.
Gráfico 3D: Visualização interativa que representa a relação entre preço, nota e desconto.
Pré-requisitos
Python 3.x
Bibliotecas:
pandas
plotly
dash
Você pode instalar as bibliotecas necessárias usando pip:

bash
Copiar código
pip install pandas plotly dash
Como Usar
Carregar os Dados: O caminho para o arquivo CSV com os dados deve ser ajustado na variável caminho_dados na seção de inicialização do script.

python
Copiar código
caminho_dados = 'C:/Users/diogo/Downloads/ecommerce_estatistica.csv'
Executar a Aplicação: Após ajustar o caminho do arquivo CSV, execute o script. A aplicação será iniciada em http://127.0.0.1:8050/.

bash
Copiar código
python nome_do_arquivo.py
Interação: Utilize os sliders e dropdowns para filtrar os dados e explorar as visualizações geradas.

Estrutura do Código
Função carregar_dados(caminho): Carrega os dados do CSV e realiza uma análise preliminar.
Função cria_graficos(df): Gera os gráficos iniciais a partir do DataFrame.
Função cria_grafico_3d(filtered_df): Cria um gráfico 3D interativo.
Função cria_app(df): Configura a aplicação Dash e define os callbacks para interação com o usuário.
Contribuição
Sinta-se à vontade para contribuir com melhorias ou sugestões! Para contribuir, faça um fork do repositório e crie um pull request.

Licença
Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.

Contato
Para dúvidas ou sugestões, entre em contato: diogocenteno1979@gmail.com.

Divirta-se explorando os dados!
