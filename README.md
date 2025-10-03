# Projeto aplicarFiltro_corrigido v2

## Como rodar
1. `docker compose build`
2. `docker compose up`

## Testes diretos (do host)
Agora o servidor está exposto na porta **5000**.

- Enviar imagem:
  ```bash
  curl -F "image=@sua_imagem.jpg" http://localhost:5000/process
  ```

- Consultar notificações recebidas:
  ```bash
  curl http://localhost:5001/poll
  ```

## Cliente (dentro do container)
Abra o cliente:
```bash
docker compose run --rm cliente bash
```
e dentro:
```bash
python client.py /app/sua_imagem.jpg
```

## Fluxo
- **Servidor** recebe imagem, aplica 3 filtros (bw, sepia, vintage), salva em ./output e envia:
  - Notificação síncrona via HTTP POST para serviço de notificações.
  - Mensagem assíncrona para a fila Redis (`stock_queue`).
- **Serviço de notificações** expõe:
  - `POST /notify` recebe notificações síncronas.
  - `GET /poll` retorna lista de notificações recebidas.
- **Serviço de estoque** consome fila `stock_queue` e processa cada item.
