# scrapy-notices

Repositório destinado a uma prova de conceito para exemplificar o uso do scrapy para percorrer sites como G1 e CNN em busca de links de notícias com suas respectivas datas de publicações.

## Modo de usar

Instalar os requerimentos.

```shell
$ pip install -r requirements.txt
```

Para executar o exemplo do G1:

```python
$ scrapy runspider globo_spider.py -o globo_items.json
```

Para executar o exemplo da CNN:

```python
$ scrapy runspider cnn_spider.py -o cnn_items.json
```

## Limitações

Por se tratar de um projeto para prova de conceito, algumas funcionalidades não foram implementadas como a recursividade no links e a passagem de parâmetros para início de busca dos links.