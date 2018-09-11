# scrapy-notices

Repositório destinado a uma prova de conceito para exemplificar o uso do scrapy para percorrer sites como G1 e CNN em busca de links de notícias com suas respectivas datas de publicações.

## Modo de usar

Instalar os requerimentos.

```bash
$ pip install -r requirements.txt
```

Para executar o exemplo do G1:

```bash
$ scrapy runspider globo_crawler.py -o globo_items.json
```

Para executar o exemplo da CNN:

```bash
$ scrapy runspider cnn_crawler.py -o cnn_items.json
```

## Retornos

Os itens retornados seguirão a seguinte estrutura.

```json
  {
    "title": "Bolsonaro segue na UTI e tem boas condições clínicas, diz boletim médico",
    "url": "https://g1.globo.com/sp/sao-paulo/noticia/2018/09/08/bolsonaro-segue-na-uti-e-em-boas-condicoes-clinicas-diz-boletim-medico.ghtml",
    "publish_date": "2018-09-08T13:42:15.277Z"
  }
```

## Limitações

Por se tratar de um projeto para prova de conceito, algumas funcionalidades não foram implementadas como a passagem de parâmetros para início de busca dos links.