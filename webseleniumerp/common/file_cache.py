# coding: utf-8
import os
import pickle
import time
import portalocker


class FileCache:
    """
    FileCache 是一个基于文件系统的缓存类，支持设置、获取、删除和清理缓存数据。
    使用 pickle 序列化对象，并支持缓存过期机制和文件锁保障并发安全。
    """

    def __init__(self, cache_dir="cache_token"):
        """
        初始化缓存目录路径，若不存在则自动创建。
        :param cache_dir: 缓存目录名称（相对于项目根目录）
        """
        self.root_dir = os.path.dirname(os.path.abspath(__file__)).replace('common', '')
        self.cache_dir = self.root_dir + cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key):
        """
        根据 key 生成对应的缓存文件路径。
        :param key: 缓存键名
        :return: 缓存文件路径字符串
        """
        return os.path.join(self.cache_dir, f"{key}.pkl")

    def set(self, key, value, expire=3600):
        """
        设置缓存并指定过期时间（秒）。
        :param key: 缓存键名
        :param value: 要缓存的对象（可为任意 Python 对象）
        :param expire: 过期时间（秒），默认为 3600 秒
        :return: None
        """
        cache_path = self._get_cache_path(key)
        with open(cache_path, "wb") as f:
            try:
                portalocker.lock(f, portalocker.LOCK_EX)  # 加排他锁
            except portalocker.exceptions.LockException:
                print('设置缓存时获取锁失败')
                return value
            try:
                data = {
                    "value": value,
                    "expire_time": time.time() + expire
                }
                pickle.dump(data, f)
            finally:
                portalocker.unlock(f)  # 解锁
                return None

    def get(self, key, default=None):
        """
        获取缓存值，若缓存不存在或已过期，则返回默认值。
        :param key: 缓存键名
        :param default: 键不存在或缓存过期时返回的默认值
        :return: 缓存值 或 default
        """
        cache_path = self._get_cache_path(key)
        if not os.path.exists(cache_path):
            return default

        with open(cache_path, "rb") as f:
            try:
                portalocker.lock(f, portalocker.LOCK_SH)  # 加共享锁
            except portalocker.exceptions.LockException:
                print('读取缓存时获取锁失败')
                return default
            try:
                data = pickle.load(f)
                if time.time() > data.get("expire_time", 0):
                    return default
                return data.get("value")
            finally:
                portalocker.unlock(f)  # 解锁

    def delete(self, key):
        """
        删除指定 key 的缓存文件。
        :param key: 缓存键名
        :return: None
        """
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)

    def clear_expired(self):
        """
        清理所有已过期的缓存文件。
        :return: None
        """
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".pkl"):
                cache_path = os.path.join(self.cache_dir, filename)
                try:
                    with open(cache_path, "rb") as f:
                        try:
                            portalocker.lock(f, portalocker.LOCK_EX)  # 加排他锁
                        except portalocker.exceptions.LockException:
                            print('清理缓存时获取锁失败')
                            return None
                        try:
                            data = pickle.load(f)
                            if time.time() > data.get("expire_time", 0):
                                os.remove(cache_path)
                        finally:
                            portalocker.unlock(f)
                            return None
                except (TimeoutError, Exception):
                    continue
            return None
        return None
