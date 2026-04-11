import json
import os


class CacheManager:
    """
    缓存管理器，实现单例模式的缓存功能

    该类提供了一个全局的缓存机制，用于存储和获取数据，
    避免重复计算或重复查询，提高程序性能。
    """
    _instance = None
    _cache = {}

    def __new__(cls):
        """
        实现单例模式，确保整个程序中只有一个缓存管理器实例
        """
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance

    def get_or_set(self, key, compute_func, *args, **kwargs):
        """
        如果缓存中有key对应的数据就返回它，
        否则执行compute_func并将结果缓存。
        """
        if key not in self._cache:
            self._cache[key] = compute_func(*args, **kwargs)
        return self._cache[key]

    def clear_cache(self, key=None):
        """
        清除指定缓存或所有缓存
        """
        if key:
            if key in self._cache:
                del self._cache[key]
        else:
            self._cache.clear()

    def has_cache(self, key):
        """
        检查是否存在指定缓存
        """
        return key in self._cache


class ParamCache:
    @staticmethod
    def get_cache_file_path(filename='practical.json', cache_dir='cache_assert'):
        """
        获取缓存文件的绝对路径 - 统一路径管理
        Args:
            filename: 缓存文件名，默认为 practical.json
            cache_dir: 缓存目录名称，默认为 cache_assert
        Returns:
            缓存文件的绝对路径
        """
        # 获取项目的根目录 - 从当前 file_cache_manager.py 文件向上两级到达项目根目录
        current_file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cache_path = os.path.join(current_file_dir, cache_dir)
        return os.path.join(cache_path, filename)

    @staticmethod
    def cache_object(*args, filename='practical.json', cache_dir='cache_assert', copy_to_clipboard=True, clipboard_key=None):
        """
        通用缓存对象方法 - 存储到项目根目录的 cache 文件夹 (JSON 格式)
        支持以下调用方式:
        1. cache_object(obj) - 使用默认文件名
        2. cache_object(obj, filename) - 指定文件名
        3. cache_object(dict1, dict2, ..., filename) - 合并多个字典后指定文件名
        4. cache_object({"cache": value}, copy_to_clipboard=True, clipboard_key="cache") - 缓存并复制到剪贴板
        Args:
            *args: 要缓存的对象，可以是单个对象或多个字典
            filename: 缓存文件名，默认为 practical.json
            cache_dir: 缓存目录名称，默认为 cache_assert
            copy_to_clipboard: 是否将值复制到剪贴板，默认 False
            clipboard_key: 当 copy_to_clipboard=True 时，指定从 obj 中提取哪个 key 的值复制到剪贴板
                          如果为 None，则尝试从 obj 中提取 'cache' 键的值
        Returns:
            缓存的对象，如果 copy_to_clipboard=True 且提取到值，则返回该值
        """
        try:
            import pyperclip

            # 判断最后一个参数是否为字符串（即 filename）
            if len(args) > 0 and isinstance(args[-1], str):
                # 最后一个参数是文件名
                filename = args[-1]
                dicts_to_merge = args[:-1]
            else:
                # 使用默认文件名
                dicts_to_merge = args

            # 如果有多个字典，合并它们
            if len(dicts_to_merge) > 1:
                obj = {}
                for item in dicts_to_merge:
                    if isinstance(item, dict):
                        obj.update(item)
                    else:
                        # 如果不是字典，将其作为整体存储
                        obj = dicts_to_merge[0] if len(dicts_to_merge) == 1 else list(dicts_to_merge)
            elif len(dicts_to_merge) == 1:
                obj = dicts_to_merge[0]
            else:
                obj = {}

            # 使用统一的路径获取方法
            cache_file = ParamCache.get_cache_file_path(filename, cache_dir)
            cache_path = os.path.dirname(cache_file)
            os.makedirs(cache_path, exist_ok=True)

            # 直接将对象保存为 JSON 格式
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)

            print(f"缓存文件已保存到项目根目录：{cache_file}")

            # 如果需要复制到剪贴板
            if copy_to_clipboard and isinstance(obj, dict):
                # 确定从哪个 key 提取值
                key_to_copy = clipboard_key if clipboard_key else 'i'
                if key_to_copy in obj:
                    value_to_copy = str(obj[key_to_copy])
                    pyperclip.copy(value_to_copy)
                    print(f"已将 '{key_to_copy}' 的值复制到剪贴板：{value_to_copy}")
                    return obj[key_to_copy]

            return obj

        except Exception as e:
            print(f"创建缓存文件时发生错误：{e}")
            import traceback
            traceback.print_exc()
            return None

