# coding: utf-8
import inspect
import pickle
import random
import shutil
import threading
from datetime import datetime, timedelta
import time
import os
import uuid
import portalocker

from config.settings import DATA_PATHS


class BaseRandomMixin:
    """解决引用文件高亮提示"""

    # 用于存储已生成的各种编号，确保唯一性
    _generated_serial = set()
    _generated_imei = set()
    _generated_jd = set()
    _generated_sf = set()
    _generated_yt = set()
    _generated_phone = set()
    _generated_mixed = set()

    # 线程锁，确保并发安全
    _serial_lock = threading.Lock()
    _imei_lock = threading.Lock()
    _jd_lock = threading.Lock()
    _sf_lock = threading.Lock()
    _yt_lock = threading.Lock()
    _phone_lock = threading.Lock()
    _mixed_lock = threading.Lock()

    # 用于确保高并发下的唯一性计数器
    _serial_counter = 0
    _imei_counter = 0
    _jd_counter = 0
    _sf_counter = 0
    _yt_counter = 0
    _phone_counter = 0
    _mixed_counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为每个实例添加随机偏移量
        self._random_offset = random.randint(0, 1000000)

    def _generate_unique_id(self, prefix, timestamp_len, random_len, counter_name, suffix="", max_attempts=1000):
        """
        通用唯一ID生成器

        :param prefix: ID前缀
        :param timestamp_len: 时间戳长度
        :param random_len: 随机数长度
        :param counter_name: 计数器名称 (如 'jd', 'sf', 'imei' 等)
        :param suffix: ID后缀
        :param max_attempts: 最大尝试次数
        :return: 唯一ID
        """
        # 根据计数器名称确定对应的锁和生成集合
        counter_attr = f'_{counter_name}_counter'
        set_attr = f'_generated_{counter_name}'

        lock = getattr(self, f'_{counter_name}_lock')
        generated_set = getattr(self, set_attr)
        counter_value = getattr(self, counter_attr)

        with lock:
            for _ in range(max_attempts):
                # 构建基础部分
                timestamp_part = str(int(time.time() * 1000000))[-timestamp_len:] if timestamp_len > 0 else ""
                random_part = str(self.random_numbers(random_len)) if random_len > 0 else ""

                # 计数器部分
                setattr(self, counter_attr, counter_value + 1)
                counter_part = str(counter_value % 10000).zfill(4)

                # 组合ID
                new_id = prefix + timestamp_part + random_part + counter_part + suffix

                if new_id not in generated_set:
                    generated_set.add(new_id)
                    return new_id

            # 如果尝试次数用尽，生成一个更复杂的唯一ID
            timestamp_part = str(int(time.time() * 1000000))[-max(timestamp_len, 6):]
            fallback_id = prefix + timestamp_part + str(random.randint(100000, 999999)) + suffix
            generated_set.add(fallback_id)
            return fallback_id

    @property
    def number(self):
        """动态生成2位数字"""
        return str(self.random_numbers(2))

    @property
    def four_digits(self):
        """动态生成4位数字"""
        return str(self.random_numbers(4))

    @property
    def jd(self):
        """动态生成JD开头的14位编号，确保唯一性"""
        return self._generate_unique_id("JD", 4, 4, 'jd')

    @property
    def phone(self):
        """动态生成以13开头的11位手机号，确保唯一性"""
        return self._generate_unique_id("13", 0, 5, 'phone')

    @property
    def serial(self):
        """动态生成8位数字，确保唯一性"""
        return self._generate_unique_id("", 4, 4, 'serial')

    @property
    def sf(self):
        """
        动态生成SF开头的14位编号，确保唯一性，兼容高并发
        格式：SF + 时间戳部分 + UUID部分 + 线程ID后四位 + 计数器
        """
        # 使用更精确的时间戳和UUID确保绝对唯一性
        timestamp_part = str(int(time.time() * 1000000))[-4:]  # 取时间戳的后4位
        uuid_part = str(uuid.uuid4())[:4].upper()  # 使用UUID的前4位
        thread_id = str(threading.current_thread().ident)[-4:]  # 使用线程ID后四位

        # 组合生成基础编号
        base_sf = f"SF{timestamp_part}{uuid_part}{thread_id}"

        # 使用线程锁确保在高并发下设置唯一值
        with self._sf_lock:
            # 如果编号已存在，则增加计数器
            counter = getattr(self, '_sf_counter', 0)
            setattr(self, '_sf_counter', counter + 1)
            final_sf = f"{base_sf}{counter % 10000:04d}"  # 添加4位计数器部分

            # 确保最终的编号是唯一的
            while final_sf in self._generated_sf:
                counter = getattr(self, '_sf_counter', 0)
                setattr(self, '_sf_counter', counter + 1)
                final_sf = f"{base_sf}{counter % 10000:04d}"

            self._generated_sf.add(final_sf)
            return final_sf

    @property
    def imei(self):
        """
        动态生成15位imei，确保每次调用都不重复
        格式：I + 14位数字
        """
        with self._imei_lock:
            counter = getattr(self, '_imei_counter', 0)
            setattr(self, '_imei_counter', counter + 1)

            # 生成14位数字部分，使用时间戳+计数器+随机偏移
            timestamp_ms = int(time.time() * 1000) % 10000000000000  # 13位时间戳
            counter_with_offset = (counter + self._random_offset) % 1000000  # 6位计数器+偏移
            combined = (timestamp_ms + counter_with_offset * 12345) % 100000000000000  # 组合并限制为14位

            number_part = f"{combined:014d}"[:14]  # 确保正好14位

            base_imei = f"I{number_part}"

            # 处理冲突情况
            attempt = 0
            while base_imei in self._generated_imei and attempt < 100:
                attempt += 1
                # 发生冲突时使用随机数
                number_part = self.random_numbers(14)
                base_imei = f"I{number_part}"

            self._generated_imei.add(base_imei)
            return base_imei

    @property
    def serial_number(self):
        """
        动态生成序列号，确保每次调用都不重复，兼容高并发
        格式：SN + 时间戳 + UUID部分 + 线程ID后四位 + 随机数 + 计数器
        """
        # 使用更精确的时间戳和UUID确保绝对唯一性
        timestamp_part = str(int(time.time() * 1000000))
        uuid_part = str(uuid.uuid4())[:6].upper()  # 使用UUID的前6位
        thread_id = str(threading.current_thread().ident)[-4:]  # 使用线程ID后四位
        random_part = str(random.randint(1000, 9999))

        # 组合生成基础序列号
        base_serial = f"SN{timestamp_part}{uuid_part}{thread_id}{random_part}"

        # 使用线程锁确保在高并发下设置唯一值
        with self._serial_lock:
            # 如果序列号已存在，则增加计数器
            counter = getattr(self, '_serial_counter', 0)
            setattr(self, '_serial_counter', counter + 1)
            final_serial = f"{base_serial}{counter % 10000:04d}"  # 添加计数器部分

            # 确保最终的序列号是唯一的
            while final_serial in self._generated_serial:
                counter = getattr(self, '_serial_counter', 0)
                setattr(self, '_serial_counter', counter + 1)
                final_serial = f"SN{timestamp_part}{uuid_part}{thread_id}{random_part}{counter % 10000:04d}"

            self._generated_serial.add(final_serial)
            return final_serial

    def mixed_random(self, length=6):
        """
        动态生成指定位数的数字 + 字母的随机字符串，确保唯一性，字母开头
        :param length: 随机字符串的长度，默认为 6 位
        :return: 指定长度的随机字符串（字母开头）
        """
        # 26 个英文字母（用于首字符，确保永远是字母）
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # 数字和字母（用于后续字符）
        digits_letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        with self._mixed_lock:
            counter = getattr(self, '_mixed_counter', 0)
            setattr(self, '_mixed_counter', counter + 1)

            max_attempts = 10000  # 最大尝试次数
            for _ in range(max_attempts):
                # 【核心逻辑】第一个字符固定从 26 个字母中随机，后面的 length-1 位从数字 + 字母中随机
                first_char = random.choice(letters)
                rest_chars = ''.join(random.choices(digits_letters, k=length - 1))
                result = first_char + rest_chars

                # 检查是否已存在
                if result not in self._generated_mixed:
                    self._generated_mixed.add(result)
                    return result

            # 如果尝试次数用尽，使用 fallback 方案
            # 第一步：强制首字符为字母（只从 letters 变量获取）
            first_fallback_char = random.choice(letters)

            # 第二步：生成剩余的 length-1 个字符（从 digits_letters 中随机）
            remaining_length = length - 1

            # 使用时间戳 + 计数器 + 随机字符组合，确保唯一性
            timestamp_part = str(int(time.time() * 1000000))[-min(6, remaining_length):] if remaining_length > 0 else ""
            counter_part = str((counter + self._random_offset) % (10 ** min(5, remaining_length))).zfill(min(5, remaining_length)) if remaining_length > 0 else ""

            # 计算还需要多少个随机字符
            random_needed = remaining_length - len(timestamp_part) - len(counter_part)
            random_part = ''.join(random.choices(digits_letters, k=random_needed)) if random_needed > 0 else ""

            # 组合剩余部分并截断到正确长度
            remaining_chars = (timestamp_part + counter_part + random_part)[:remaining_length]

            # 第三步：组合最终结果（首字母 + 剩余部分）
            fallback_result = first_fallback_char + remaining_chars

            self._generated_mixed.add(fallback_result)
            return fallback_result


    @classmethod
    def clear_generated_data(cls):
        """
        清空已生成的数据集合，用于测试开始前清空历史记录
        """
        counters_and_sets = [
            ('_serial_lock', '_generated_serial', '_serial_counter'),
            ('_imei_lock', '_generated_imei', '_imei_counter'),
            ('_jd_lock', '_generated_jd', '_jd_counter'),
            ('_sf_lock', '_generated_sf', '_sf_counter'),
            ('_yt_lock', '_generated_yt', '_yt_counter'),
            ('_phone_lock', '_generated_phone', '_phone_counter'),
            ('_mixed_lock', '_generated_mixed', '_mixed_counter')  # 新增：混合字符随机数相关清理
        ]

        for lock_attr, set_attr, counter_attr in counters_and_sets:
            lock = getattr(cls, lock_attr)
            generated_set = getattr(cls, set_attr)
            with lock:
                generated_set.clear()
                setattr(cls, counter_attr, 0)

    def random_numbers(self, n: int) -> str:
        """
        生成指定长度的随机数字字符串（允许重复）
        :param n: 要生成的随机数位数
        :return: 字符串形式的随机数字
        """
        # 使用 choices 允许重复，增加随机性
        digits = random.choices('0123456789', k=n)
        return ''.join(digits)

    def get_time_stamp_by_minute(self, minute: int) -> str:
        """
        输入指定的分钟数，生成对应分钟数后的时间戳
        :param minute: 分钟数
        :return: 时间戳字符串
        """
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S") +
                timedelta(minutes=int(minute))).strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def clear_generated_data(cls):
        """
        清空已生成的数据集合，用于测试开始前清空历史记录
        """
        counters_and_sets = [
            ('_serial_lock', '_generated_serial', '_serial_counter'),
            ('_imei_lock', '_generated_imei', '_imei_counter'),
            ('_jd_lock', '_generated_jd', '_jd_counter'),
            ('_sf_lock', '_generated_sf', '_sf_counter'),
            ('_yt_lock', '_generated_yt', '_yt_counter'),
            ('_phone_lock', '_generated_phone', '_phone_counter')
        ]

        for lock_attr, set_attr, counter_attr in counters_and_sets:
            lock = getattr(cls, lock_attr)
            generated_set = getattr(cls, set_attr)
            with lock:
                generated_set.clear()
                setattr(cls, counter_attr, 0)

    def get_list_data(self, file_name, key=''):
        """
        获取列表数据，支持Locust并发环境下的唯一性
        """
        fpath = os.path.join(os.path.dirname(__file__), r'params\pkl')
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        filename_key = os.path.join(fpath, file_name + '_key.pkl')
        filename = os.path.join(fpath, file_name + '_result.pkl')
        key_res = {}
        list_res = {}
        data_key = 0
        # 确保线程安全
        with self._serial_lock:
            # 读取当前键值
            if os.path.exists(filename_key):
                with open(filename_key, 'rb') as f:
                    key_res = pickle.load(f)
                    data_key = key_res['key']
                    if file_name == 'phone_project_list':
                        print('---data_key1:', data_key)

        # 加载数据
        try:
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    list_res = pickle.load(f)
                print(f"文件数据已加载:{filename}")
            else:
                print(f"文件不存在:{filename}")
                if key != '':
                    pkl_data = list_res[data_key][key]
                else:
                    pkl_data = [list_res[data_key]]

                # 增加键值并保存
                data_key = data_key + 1
                with open(filename_key, 'wb') as f:
                    pickle.dump({"key": data_key, "page": 1}, f)

                return pkl_data

        except Exception as e:
            print(f"从 {filename} 加载数据失败: {e}")
            return None
        print('--len_data:', len(list_res), '--use_no:', data_key, '--get:', key, '--check:', data_key >= len(list_res))
        # 检查数据是否存在
        if data_key >= len(list_res) or (key not in list_res[data_key] and key != ''):
            print(f"数据索引 {data_key} 或键 {key} 不存在,开始获取下一页数据并更新索引")

        if key != '':
            pkl_data = list_res[data_key][key]
        else:
            pkl_data = [list_res[data_key]]
        # 增加键值并保存
        data_key = data_key + 1
        with open(filename_key, 'wb') as f:
            pickle.dump({"key": data_key, "page": 1}, f)
        return pkl_data

    def get_more_data(self, list_data, data, key):
        # print('---in-get_more_data----------', len(list_data))
        new_list_data = list_data
        if isinstance(list_data, list):
            new_list_data = list_data[data]
        pkl_data = new_list_data[key]
        return pkl_data

    def write_file_safe(self, file_path, content, encoding='utf-8'):
        """
        安全地写入文件，支持加锁防止并发写冲突。
        文件不存在则创建，存在则覆盖写入。

        :param file_path: 文件路径
        :param content: 要写入的内容
        :param encoding: 编码格式
        """
        # 自动创建父目录
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 使用 portalocker 加锁写入
        with portalocker.Lock(file_path, mode='w', encoding=encoding) as f:
            f.write(content)
        print(f"✅ 已安全写入文件：{file_path}")

    def make_pkl_file(self, content, filename=None):
        """
        将数据内容序列化保存为pkl文件，用于性能测试数据缓存
        该方法会创建两个pkl文件：
        1. {filename}_result.pkl - 存储实际数据内容
        2. {filename}_key.pkl - 存储索引信息，初始键值为{"key": 0, "page": 1}
        注意：仅在性能测试开启时(DATA_PATHS['performance'] == 'open')才会执行保存操作
        :param content: 要序列化保存的数据内容
        :param filename: 文件名前缀，将生成 {filename}_result.pkl 和 {filename}_key.pkl 两个文件
        :return: 空字符串
        """
        if filename is None:
            # filename = 'api_list'  # 与request文件get_list_data方法文件名保持一致
            filename = inspect.currentframe().f_back.f_code.co_name
        if DATA_PATHS['performance'] == 'close':
            return ''
        if DATA_PATHS['performance_pkl_del'] is True:
            self.clear_pkl_files()
        # 将结果保存到当前目录下的pkl文件中
        root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'params\pkl')
        pkl_file_path = os.path.join(root_dir, filename + '_result.pkl')
        pkl_file_key_path = os.path.join(root_dir, filename + '_key.pkl')
        print('--r', root_dir, pkl_file_path, pkl_file_key_path)
        # 如果不存在则生成文件pkl_file_path
        if not os.path.exists(root_dir):
            # 创建pkl目录
            os.makedirs(root_dir)
            self.write_file_safe(pkl_file_path, '')
            self.write_file_safe(pkl_file_key_path, '')
        try:
            with open(pkl_file_path, 'wb') as f:
                pickle.dump(content, f)
            print(f"库存列表结果已保存到 {pkl_file_path}")
            with open(pkl_file_key_path, 'wb') as f:
                pickle.dump({"key": 0, "page": 1}, f)
            print(f"库存列表索引已保存到 {pkl_file_key_path}")
        except Exception as e:
            print(f"保存库存列表结果到pkl文件时出错: {e}")
        return ''

    def clear_pkl_files(self):
        """
        清除common\params\pkl目录下的所有文件
        """
        pkl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'params', 'pkl')
        # 检查目录是否存在
        if os.path.exists(pkl_dir):
            # 删除目录中的所有文件
            for filename in os.listdir(pkl_dir):
                file_path = os.path.join(pkl_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"清除文件 {file_path} 时出错: {e}")
            print(f"已清除 {pkl_dir} 目录下的所有文件")
        else:
            print(f"目录 {pkl_dir} 不存在")

    def tuple_to_dict_list(self, tuple_data, field_names):
        """
        将元组数据转换为字典列表
        Args:
            tuple_data: 元组数据
            field_names: 字段名称列表
        Returns:
            list: 字典列表
        """
        if not tuple_data:
            return []
        # 处理单个元组
        if isinstance(tuple_data, tuple) and not isinstance(tuple_data[0], tuple):
            return [dict(zip(field_names, tuple_data))]

        # 处理元组列表
        return [dict(zip(field_names, item)) for item in tuple_data]
