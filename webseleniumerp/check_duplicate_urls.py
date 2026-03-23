# check_duplicate_urls.py
from common.base_url import URL


def check_duplicate_urls():
    """
    检查 base_url.py 文件中的接口地址是否有重复
    """
    # 获取所有的API接口地址
    api_urls = {}

    if 'api' in URL:
        for key, url in URL['api'].items():
            if url in api_urls:
                api_urls[url].append(key)
            else:
                api_urls[url] = [key]

    # 查找重复的URL
    duplicates = {url: keys for url, keys in api_urls.items() if len(keys) > 1}

    if duplicates:
        print("发现重复的接口地址:")
        print("-" * 50)
        for url, keys in duplicates.items():
            print(f"重复地址: {url}")
            print(f"对应键名: {', '.join(keys)}")
            print()
        return True
    else:
        print("未发现重复的接口地址")
        return False


if __name__ == "__main__":
    check_duplicate_urls()
