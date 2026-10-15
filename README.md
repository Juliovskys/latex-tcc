# Template TCC FCTE-UnB

## Manuscrito e fase atual

O conteúdo em revisão está em [docs/tcc.md](docs/tcc.md), com bibliografia em [docs/referencias-tcc.bib](docs/referencias-tcc.bib). O [controle de médio prazo](docs/medio-prazo.md) registra o atendimento a todos os itens, as evidências e as avaliações futuras. A [revisão de normalização](docs/normalizacao-medio-prazo.md) discrimina a conferência editorial e a etapa de apresentação reservada ao PDF.

A branch `docs/tcc-curto-prazo` preserva a revisão anterior. Na branch `docs/tcc-medio-prazo`, Markdown, BibTeX e LaTeX foram sincronizados com a revisão de médio prazo. O Apêndice L reúne os quatro registros visuais históricos, contextualizados. O PDF compilado é gerado em `output/pdf/TCC_Avaliacao_Contextual_Medio_Prazo.pdf` e aguarda novo CopySpider. A execução local e os testes do protótipo estão documentados em [prototype-api/README.md](prototype-api/README.md).

## Origem do modelo

Template para Trabalhos de Conclusão de Cursos (TCC) na Faculdade do
Gama, atual Faculdade de Ciências e Tecnologias em Engenharia (FCTE), em Latex.

Licenciado em Creative Commons Atribuição 3.0:
http://creativecommons.org/licenses/by/3.0/

Desenvolvido e adaptado pelo professor Edson Alves <edsomjr@gmail.com>.

## Dependências
Para utilizar, certifique-se de ter instalados no seu ambiente o [Docker](https://docs.docker.com/engine/install/) e o [Docker-compose](https://docs.docker.com/compose/install/).

## Construindo imagem
Construa a imagem Docker que será utilizada com o comando:
```
docker-compose build latex
```

## Edição do template
Os arquivos para edição do template de TCC estão localizados na pasta `latex`. Depois de alterá-los utilizando um editor de texto, basta compilar os arquivos.

## Compilando o template de TCC e gerando o PDF
Execute o comando:
```
docker-compose up
```

Pronto! o PDF do seu projeto estará disponível em `latex/tcc.pdf`.


## Limpando 
Para limpar os arquivos gerados pelo latex:
```
docker-compose run latex bash -c 'make clean'
```
### FAQ

Caso você encontre algum erro na execução dos comandos acima, siga as instruções abaixo:

1. Adicione o grupo `docker` ao seu usuário com o comando
```
sudo usermod -a -G docker $USER
```

1. Altere as permissões do arquivo `/var/run/docker.sock` com o comando:
```
sudo chown $USER /var/run/docker.sock
```

1. Caso o Docker não esteja rodando, inicie o serviço (e agende o início automático no _boot_) com os comandos:
```
sudo systemctl enable docker
sudo systemctl start docker
```
