import json

import requests
from requests import HTTPError
from robot.api.deco import keyword


class TestNotification:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.2.0'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, webhook, *args):
        self.webhook = webhook
        self.args = args
        self.ROBOT_LIBRARY_LISTENER = self

    def _clean_data(self):
        '''Validates the given arguments and creates a JSON string'''
        allowed_params = ('channel', 'username', 'icon_url', 'icon_emoji', 'props', 'attachments')
        json_data = {}
        json_data['text'] = text
        for key, value in data.items():
            if key in allowed_params:
                json_data[key] = value
            else:
                raise ValueError('Invalid Parameter')
        return json.dumps(json_data)

    def _return_statistics(self, statistics):
        '''Returns the base path where the summary statistics are stored
        This path is different between robotframework versions'''
        try:
            if statistics.total:
                return statistics  # robotframework < 4.0.0
        except:
            return statistics.all  # robotframework > 4.0.0

    @keyword("Post Slack Message")
    def post_message_to_channel(self, text, **kwargs):
        '''POST a custom message to a Slack or Mattermost channel.'''
        json_data = self._clean_data(text, kwargs)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                url=self.webhook,
                data=json_data,
                headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            raise HTTPError(http_err)
        except Exception as err:
            raise Exception(err)
        else:
            print(response.text)

    def _get_attachments(self, status, text):
        '''Return a formatted attachment list'''
        attachments = {
            "color": '#dcdcdc',
            "text": '',
            "footer": 'RobotNotifications'
        }
        if status == 'GREEN':
            attachments['color'] = '#36a64f'
        elif status == 'RED':
            attachments['color'] = '#dc143c'
        attachments['text'] = text
        attachment_list = [attachments]
        return attachment_list

    def end_suite(self, data, result):
        '''Post the suite results to Slack or Mattermost'''

        statistics = self._return_statistics(result.statistics)

        if 'end_suite' in self.args:
            if result.parent:
                text = f'*{result.longname}*\n'
                if result.status == 'PASS':
                    attachments_data = self._get_attachments('GREEN', result.full_message)
                else:
                    attachments_data = self._get_attachments('RED', result.full_message)
                self.post_message_to_channel(text, attachments=attachments_data)

        if 'summary' in self.args:
            if not result.parent:
                text = f'*Report Summary - {result.longname}*'
                attachment_text = (
                    f'Total Tests : {statistics.total}\n'
                    f'Total Passed : {statistics.passed}\n'
                    f'Total Failed : {statistics.failed}'
                )
                if statistics.failed == 0:
                    attachments_data = self._get_attachments('GREEN', attachment_text)
                elif statistics.failed > 0:
                    attachments_data = self._get_attachments('RED', attachment_text)
                self.post_message_to_channel(text, attachments=attachments_data)

    def end_test(self, data, result):
        '''Post individual test results to Slack or Mattermost'''
        if result.passed:
            attachment_text = (
                f'*{result.name}*\n'
                f'{result.message}'
            )
            attachments_data = self._get_attachments('GREEN', attachment_text)

        if not result.passed:
            attachment_text = (
                f'*{result.name}*\n'
                f'{result.message}'
            )
            attachments_data = self._get_attachments('RED', attachment_text)

        if 'end_test' in self.args and not result.passed:
            self.post_message_to_channel('', attachments=attachments_data)

        if 'end_test_all' in self.args:
            self.post_message_to_channel('', attachments=attachments_data)