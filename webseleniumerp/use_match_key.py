from common.element_positioning import ElementPositioning


def find_duplicate_values():
    """查找并打印重复的 value 值及其对应的 key，增加间隔以提高可读性"""
    positioning_dict = ElementPositioning.positioning
    value_count = {}

    # 统计每个 value 出现的次数
    for key, value in positioning_dict.items():
        if value in value_count:
            value_count[value].append(key)
        else:
            value_count[value] = [key]

    # 打印重复的 value 及其对应的 key，增加间隔
    duplicates = {k: v for k, v in value_count.items() if len(v) > 1}
    if duplicates:
        print("发现重复的 value 值：\n")
        for i, (value, keys) in enumerate(duplicates.items()):
            print(f"Value: {value}")
            print(f"Keys: {keys}")
            if i < len(duplicates) - 1:  # 在每组之间添加分隔线
                print("-" * 50)
    else:
        print("没有发现重复的 value 值。")


if __name__ == "__main__":
    print("正在运行主函数...")
    find_duplicate_values()
