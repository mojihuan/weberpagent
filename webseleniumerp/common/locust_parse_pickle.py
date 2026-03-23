import pickle


def count_pkl_items(file_path):
    """
    解析pickle文件并返回数据条目总数
    """
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)

        if isinstance(data, list):
            total_count = len(data)
            print(f"总数据条目数量: {total_count}")
            return total_count
        else:
            print(f"数据类型不是列表，而是: {type(data)}")
            print(f"数据条目数量: 1")  # 如果不是列表，作为一个整体计算
            return 1

    except Exception as e:
        print(f"解析文件时出错: {e}")
        return 0


# 使用示例
if __name__ == "__main__":
    pkl_file_path = r"D:\project\python\web_selenium_erp\common\params\pkl\inventory_list_result.pkl"
    count = count_pkl_items(pkl_file_path)
