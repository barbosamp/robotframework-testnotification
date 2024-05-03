import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json
import requests
from requests.exceptions import HTTPError
from robot.api import logger
from robot.api.deco import keyword
import telegram


class TestNotification():
    '''Test Notification pode ser utilizada para enviar notificações para diferentes plataformas durante ou após execução dos testes com RobotFramework.
        Originalmente essa biblioteca é um ouvinte e deve ser utilizado em linha de comando como exemplo abaixo:
        Exemplo:
            | robot --listener "TestNotification;url;plataforma;tipo  |
            | robot --listener "TestNotification;https://chat.googleapis.com/v1/spaces/ASASssapasmc.com.br;google;summary  |

        Arguments:
            - url: De acordo com a plataforma desejada, informe a URL. Caso Utilize Google, Slack ou Telegram envie um WEBHOOK e para uso em e-mails utilize a url do servidor smtp.
            - plataforma: Google, Slack, Telegram ou Email. Informe a plataforma que deseja receber as notificações.
            - end_test: Envia notificações após cada teste executado com status = FAIL ou SKIP
            - end_test_all: Envia notificações ao final de cada teste, independente do status.
            - end_suite: Envia notificação ao final de cada suite com o resumo da execução da suíte.
            - summary: Envia notificação ao completar a execução de todos os testes com um resumo informando a quantidade de testes em cada status.

        Para utilizar dentro de cada suíte, deve ser acionado no momento da importação da library.
        Examples:
        | Library   |  TestNotification    | url/webhook | plataforma | end_suite |
        | Library   |  TestNotification    | https://chat.googleapis.com/v1/spaces/ASASssapasmc.com.br | google | end_suite |

        | = plataforma =  | = parâmetros =                                            |         = Example =                |
        | ``google``      | webhook                                                   | ``Library     TestNotification    https://chat.googleapis.com/v1/spaces/ASASssapasmc.com.br         google  end_test_all/end_test/end_suite/summary``      |
        | ``slack``       | webhook                                                   | ``Library     TestNotification    https://hooks.slack.com/services/EQE23EWQ12/dsaSDAD/VgS06iIiwmL   slack   end_test_all/end_test/end_suite/summary`` |
        | ``telegram``    | webhhok, api_token, chat_id                               | ``Library     TestNotification    https://api.telegram.org/bot   google  end_test_all/end_test/end_suite/summary``                     |
        | ``email``       | url_server, username, password, porta, destinatário.      | ``id=login_btn``                   |
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.2.0'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, url, plataforma, *args):
        self.webhook = url
        self.platform = plataforma.lower()
        self.telegram_token = None
        if plataforma.lower() == 'telegram' and args:
            self.telegram_token = args[0]  # Se o platform for 'telegram', o primeiro argumento é o token da API do bot
            self.telegram_chat_id = args[1]
        elif plataforma.lower() == 'email' and args:
            self.email_username = args[0]
            self.email_password = args[1]
            self.email_server = url
            self.email_port = args[2]
            self.email_receiver = args[3]
        self.args = args
        self.ROBOT_LIBRARY_LISTENER = self

    def _return_statistics(self, statistics):
        '''Returns the base path where the summary statistics are stored
        This path is different between robotframework versions'''
        try:
            if statistics.total:
                return statistics  # robotframework < 4.0.0
        except:
            return statistics.all  # robotframework > 4.0.0

    @keyword('Post Message To Channel')
    def post_message_to_channel(self, message):
        '''POST a custom message to the specified platform (Google Chat, Slack, Telegram, Email).'''
        if self.platform == 'google' or self.platform == 'slack':
            self._post_to_chat(message)
        elif self.platform == 'telegram':
            self._post_to_telegram(message)
        elif self.platform == 'email':
            self._send_email(message)
        else:
            raise ValueError(f'Unsupported platform: {self.platform}')

    def _post_to_chat(self, message):
        '''POST a custom message to a Google Chat channel.'''
        data = {"text": message}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                url=self.webhook,
                data=json.dumps(data),
                headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            raise HTTPError(http_err)
        except Exception as err:
            raise Exception(err)
        else:
            logger.info(response.text)

    async def _post_to_telegram(self, message):
        '''POST a message to Telegram.'''
        if self.telegram_token and self.telegram_chat_id:
            # Se um token do Telegram foi fornecido, use-o para enviar a mensagem
            token = self.telegram_token
            tel_chat_id = self.telegram_chat_id
            bot = telegram.Bot(token=token)
            async with bot:
                await bot.send_message(chat_id=tel_chat_id, text=message)
        else:
            raise ValueError('Token Inválido/inexistente.')
            pass

    def _send_email(self, message):
        '''Send an email.'''
        try:
            server = smtplib.SMTP(self.email_server, self.email_port)
            server.starttls()
            server.login(self.email_username, self.email_password)

            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = self.email_receiver
            msg['Subject'] = 'QA - Status da execução dos testes'

            body = message
            msg.attach(MIMEText(body, 'plain'))

            server.sendmail(self.email_username, self.email_receiver, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def end_suite(self, suite, result):

        statistics = self._return_statistics(result.statistics)

        if 'end_suite' in self.args:
            if suite:
                attachment_text = (
                    f'*Resumo dos testes: {suite.name}*\n'
                    f'✅ Sucesso : {statistics.passed}\n'
                    f'❌ Falha : {statistics.failed}\n'
                    f'➡️ Pulados: {statistics.skipped}\n'
                    f'Total : {statistics.total}'
                )
                self.post_message_to_channel(attachment_text)

        if 'summary' in self.args:
            if not result.parent:
                attachment_text = (
                    f'*Resumo dos testes: {suite.longname}*\n'
                    f'✅ Sucesso : {statistics.passed}\n'
                    f'❌ Falha : {statistics.failed}\n'
                    f'➡️ Pulados: {statistics.skipped}\n'
                    f'Total : {statistics.total}'
                )
                if statistics.failed == 0:
                    attachments_data = f'{attachment_text}'
                elif statistics.failed > 0:
                    attachments_data = f'{attachment_text}'
                self.post_message_to_channel(attachments_data)

    def end_test(self, test, result):
        '''Enviar o status dos testes individualmente.
        '''
        if result.status == 'PASS':
            attachment_text = (
                f'Status: ✅\n'
                f'Test Name: *{test.name}*'
            )
        elif result.status == 'FAIL':
            attachment_text = (
                f'Status: ❌\n'
                f'Caso de Teste: *{test.name}*\n'
                f'Mensagem: {result.message}'
            )
        elif result.status == 'SKIP':
            attachment_text = (
                f'Status: ➡️\n'
                f'Caso de Teste: *{test.name}*\n'
                f'Mensagem: {result.message}'
            )
        else:
            attachment_text = (
                f'Status: ❓\n'
                f'Caso de Teste: *{test.name}*\n'
                f'Mensagem: {result.message}'
            )

        attachments_data = f'{attachment_text}'

        if 'end_test' in self.args and result.status != 'PASS':
            self.post_message_to_channel(attachments_data)

        if 'end_test_all' in self.args:
            self.post_message_to_channel(attachments_data)