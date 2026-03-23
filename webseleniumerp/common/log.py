# coding: utf-8
import os
from datetime import datetime
import time
from config.settings import DATA_PATHS


class Log:

    def log_save(log_content, type='info'):
        if DATA_PATHS['log_open'] is True:
            # 文件存在则在原本的内容后追加log_content，否则新建并写入log_content
            log_file_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs'),
                                         time.strftime("%Y-%m-%d", time.localtime()) + '.log')
            # 确保目录存在
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            if os.path.exists(log_file_path):
                with open(log_file_path, 'a', encoding='utf-8') as f:
                    if type == 'error':
                        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [error]:{log_content}\r")
                    else:
                        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {log_content}\r")
                return
            else:
                with open(log_file_path, 'w', encoding='utf-8') as f:
                    if type == 'error':
                        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [error]:{log_content}\r")
                    else:
                        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {log_content}\r")
            return
