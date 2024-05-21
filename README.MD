# TestNotification


[![PyPI version](https://badge.fury.io/py/test-notification-library.svg)](https://badge.fury.io/py/test-notification-library)

A biblioteca TestNotification pode ser utilizada para enviar notificações para diferentes plataformas durante ou após a execução dos testes com o Robot Framework.

## Utilização

### Instalação

Instale a biblioteca utilizando o comando:

```pip install test-notification-library```

### Exemplo de Uso

Importe a biblioteca no início do seu arquivo de teste Robot Framework:

```
Library    TestNotification    url/webhook    plataforma    end_suite
```
Argumentos:
#### - url/webhook: 
   De acordo com a plataforma desejada, informe a URL. Caso utilize Google, Slack ou Telegram, envie um webhook; para uso em e-mails, utilize a URL do servidor SMTP.
#### - plataforma: 
   Google, Slack, Telegram ou Email. Informe a plataforma para a qual deseja receber as notificações.
#### - end_suite: 
Envia notificação ao final de cada suite com o resumo da execução da suíte.

### Exemplos de Plataformas e Parâmetros

- Google Chat:
  ```
  Library TestNotification         https://chat.googleapis.com/v1/spaces/ASASssapasmc.com.br     google      end_suite
  ```
- Slack:
  ```
  Library TestNotification https://hooks.slack.com/services/EQE23EWQ12/dsaSDAD/VgS06iIiwmL slack end_suite
  ```
- Telegram:
  ```
  Library TestNotification https://api.telegram.org/bot TOKEN CHAT_ID telegram end_suite
  ```
- Email:
  ```
  Library TestNotification smtp.gmail.com USERNAME PASSWORD 587 receiver@example.com email end_suite
  ```
## Contribuindo

Sinta-se à vontade para contribuir para este projeto! Abra uma issue ou envie um pull request com suas sugestões.

## Licença

Este projeto está licenciado sob a Licença MIT.
