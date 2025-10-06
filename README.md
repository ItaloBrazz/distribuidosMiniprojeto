# Mini Projeto de Sistemas Distribuídos

Este é um mini projeto de sistemas distribuídos que processa imagens usando uma arquitetura de microserviços com Docker.

## Descrição

O projeto utiliza Docker para orquestrar contêineres que executam diferentes serviços da aplicação. Um script em Python é usado para enviar imagens para processamento, e os resultados são salvos em uma pasta `output`. As notificações do sistema podem ser consultadas através de um endpoint específico.

## Começando

Siga as instruções abaixo para rodar o projeto em sua máquina local.

### Pré-requisitos

  * **Docker:**
      * No **Windows** ou **macOS**, instale o [Docker Desktop](https://www.docker.com/products/docker-desktop).
      * No **Linux**, instale o [Docker Engine e o Docker Compose](https://docs.docker.com/engine/install/).
  * **Python 3:**
      * Verifique se o [Python](https://www.python.org/downloads/) está instalado.

### Instalação

1.  **Clone o repositório:**
    ```sh
    git clone https://github.com/ItaloBrazz/distribuidosMiniprojeto.git
    ```
2.  **Navegue até o diretório do projeto:**
    ```sh
    cd distribuidosMiniprojeto
    ```
3.  **Instale as dependências Python** (necessário apenas no primeiro uso):
    ```sh
    python3 -m pip install requests
    ```
    *Observação: Dependendo da sua configuração, você pode precisar usar `python` em vez de `python3`.*

## Como Usar

1.  **Construa e inicie os contêineres do Docker:**

    Abra um terminal no diretório do projeto e execute os seguintes comandos. Certifique-se de que o serviço do Docker esteja em execução antes de começar.

    ```sh
    docker-compose build
    ```

    ```sh
    docker-compose up
    ```

    Mantenha esta janela do terminal aberta para monitorar os serviços.

2.  **Envie imagens para processamento:**

    Abra um **novo** terminal no mesmo diretório do projeto.

      * Coloque as imagens que você deseja processar na raiz do diretório do projeto.
      * Execute o script `enviar.py`:
        ```sh
        python3 enviar.py
        ```

3.  **Verifique os resultados:**

      * As imagens processadas serão salvas na pasta `output`. Para listar os arquivos nesta pasta, use o comando:
        ```sh
        ls output
        ```
      * Para verificar as notificações do sistema, use o seguinte comando `curl`:
        ```sh
        curl http://localhost:5001/poll
        ```

## Monitorando os Logs dos Serviços

Você pode visualizar os logs dos contêineres em execução para depurar ou monitorar o comportamento da aplicação. Execute estes comandos no terminal onde os serviços estão rodando ou em um novo terminal na pasta do projeto.

  * **Ver logs de todos os serviços em tempo real:**

    ```sh
    docker compose logs -f
    ```

  * **Ver logs de um serviço específico em tempo real:**

    ```sh
    # Substitua "estoque" pelo nome do serviço desejado
    docker compose logs -f estoque
    ```

  * **Ver as últimas linhas de log de um serviço:**

    ```sh
    # Exibe as últimas 20 linhas do serviço "servidor"
    docker compose logs --tail=20 servidor
    ```

## Resumo dos Comandos

#### 1\. Navegar para a pasta do projeto

  * **Windows (PowerShell/CMD):**
    ```sh
    cd C:\caminho\para\distribuidosMiniprojeto
    ```
  * **Linux/macOS (Terminal):**
    ```sh
    cd /caminho/para/distribuidosMiniprojeto
    ```

#### 2\. No primeiro terminal

Certifique-se de que o Docker está rodando.

```sh
# Constrói as imagens dos contêineres
docker compose build

# Inicia os serviços
docker compose up
```

#### 3\. No segundo terminal

```sh
# Instala a dependência (apenas na primeira vez)
python3 -m pip install requests

# Adicione suas imagens na pasta do projeto e execute o script
python3 enviar.py
```

#### 4\. Verificar saída e logs

```sh
# Listar as imagens geradas
ls output

# Mostrar as notificações
curl http://localhost:5001/poll

# Acompanhar logs (exemplo)
docker compose logs -f
```
