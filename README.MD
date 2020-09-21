# Visualizador de dependências
Este script utiliza o Graphviz para montar um gráfico de dependências de pacotes para um determinado projeto

## Observações
- vértices que só possuem arestas para o mesmo package são prunados
- vértices que contem as strings para ignorar são prunados junto com suas arestas
- vértices sem conexões são prunados


## Requerimentos
- requirements.txt
- graphviz


## Como executar
- Rodar python -m plot_system_graph -t {target_path} -r {string_list}
- o argumento "r" recebe strings para remover nos vértices e arestas. Ele é opcional e seus valores padrão estão configurados para um projeto Django (test, apps, admin, urls, settings, migrations)
