# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class LoginApi(BaseApi):
    """登录"""

    def __init__(self):
        """
        初始化方法，设置API的基础URL、token和header
        如果Redis中有缓存的token和header，则使用缓存；否则初始化token和header
        """
        super().__init__()
        self.tokens = {}  # 存储不同账号类型的token
        self.headers = {
            'basic': {'Content-Type': 'application/json'},
            'main': {},
            'vice': {},
            'special': {},
            'platform': {},
            'idle': {},
            'super': {},
            'camera': {},
            'collection': {},
        }
        # 从Redis缓存获取token
        cached_data = self.get_cached_tokens()
        if cached_data:
            if isinstance(cached_data, dict):
                self.tokens = cached_data.get('token', {})
                self.headers.update(cached_data.get('headers', {}))
            else:
                self.initialize_tokens_headers()
        else:
            self.initialize_tokens_headers()

    def _set_token_header(self, key):
        """
        根据传入的key生成对应的token，并设置对应的请求头。
        参数: key (str): 账号类型标识符。
        返回: str: 生成的token
        """
        login_methods = {
            'main': self.main_login,
            'vice': self.vice_login,
            'special': self.special_login,
            'platform': self.platform_login,
            'idle': self.idle_login,
            'super': self.super_login,
            'camera': self.camera_login,
            'collection': self.collection_login,
        }
        if key in login_methods:
            token = login_methods[key]()
            self.set_cached_tokens(token)
        else:
            raise ValueError(f"Unsupported key: {key}")

        # 检查token是否为None，如果为None则抛出异常
        if token is None:
            raise ValueError(f"Failed to get token for key: {key}. Login may have failed.")
        self.tokens[key] = token
        self.headers[key] = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        self.set_cached_tokens({
            'token': self.tokens,
            'headers': self.headers
        })

    def initialize_tokens_headers(self):
        """初始化所有预定义账号类型的token和header"""
        for key in ['main', 'vice', 'special', 'platform', 'idle', 'super', 'camera','collection']:
            self._set_token_header(key)

    def main_login(self):
        """主账号"""
        data = {'password': INFO['password'], 'username': INFO['main_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def vice_login(self):
        """帮卖来货账号"""
        data = {'password': INFO['password'], 'username': INFO['vice_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def special_login(self):
        """管理员账号"""
        data = {'password': INFO['password'], 'username': INFO['special_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def idle_login(self):
        """特殊账号"""
        data = {'password': INFO['password'], 'username': INFO['idle_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def platform_login(self):
        """平台账号"""
        data = {'password': INFO['password'], 'username': INFO['platform_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def super_login(self):
        """超级管理员账号"""
        data = {'password': INFO['super_admin_password'], 'username': INFO['super_admin_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def camera_login(self):
        """拍机账号"""
        data = {'password': INFO['password'], 'username': INFO['camera_account']}
        response = self.request_handle('post', self.urls['CDQ3XEEfT'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)

    def collection_login(self):
        """bot速收账号"""
        data = {'phone': INFO['bot_phone'], 'wechatId': INFO['bot_wechatId'], 'miniOpenid': INFO['bot_miniOpenid'], 'loginPlatform': INFO['bot_loginPlatform'], 'type': INFO['bot_type'], 'loginType': INFO['bot_loginType'], 'latitude': INFO['bot_latitude'], 'longitude': INFO['bot_longitude'], 'deviceInfo': INFO['bot_deviceInfo']}
        response = self.request_handle('post', self.urls['W51G1tkCw'], data=json.dumps(data), headers=self.headers['basic'])
        return self.get_token(response)


if __name__ == '__main__':
    api = LoginApi()
    result = api.collection_login()
    print(json.dumps(result, indent=4, ensure_ascii=False))
