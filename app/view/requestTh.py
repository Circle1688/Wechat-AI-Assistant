from PySide6.QtCore import QThread, Signal
import requests

class RequestTh(QThread):
    """获取用户信息的后台线程"""
    finish = Signal(bool, str)
    def __init__(self, url, json_data, request_type):
        super().__init__()
        self.payload = json_data
        self.url = url
        self.request_type = request_type

    def run(self):
        try:
            # Make the POST request
            if self.request_type == 'post':
                response = requests.post(self.url, json=self.payload)
            elif self.request_type == 'get':
                response = requests.get(self.url)

            self.finish.emit(True, response.text)
        except Exception as e:
            self.finish.emit(False, e)
