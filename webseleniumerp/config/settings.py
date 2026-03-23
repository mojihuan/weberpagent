DATA_PATHS = {
    'excel': r'C:\\Users\\99479\\Downloads\\excel\\',  # 公共数据文件路径，比如导入excel、img
    'chrome_driver': r'C:\Program Files\Google\Chrome\Application\chromedriver.exe',  # 谷歌浏览器驱动
    'testcase_numbers': True,  # True: 清除测试用例编号; False: 只生成缺失的测试用例编号
    # ui自动化
    'retry_enabled': False,  # True开启重跑用例，False禁止重跑用例
    'time_wait': False,  # 是否每个步骤增加强制等待时间
    'wait_time': 1,  # 显示等待时间
    'tries': 3,  # 重跑最大尝试次数
    'delay': 2,  # 重跑每次重试间隔秒数
    'force_wait': 1.5,  # 小程序强制等待时间
    'screenshot_enabled': False,  # True 开启截图功能，False 关闭截图功能
    # 接口自动化
    'print_request': False,  # 接口请求信息，True打印，False不打印
    'log_open': False,  # 是否开启日志
    # 性能测试
    'performance': 'close',  # close 关闭性能测试；open 打开性能测试
    'performance_user': 10,  # 并发用户数
    'performance_spawn_rate': 2,  # 每秒启动用户数
    'performance_run_time': '30s',  # 运行时间 s秒 m分 h时
    'performance_pkl_del': True,  # pkl文件并重新生成 True删除，False不删除
    'perform_report_api_build': True,  # api模块生成测试报告 True生成，False不生成
    # ui与接口自动化配置
    'auto_type': 'ui',  # ui，执行UI自动化 api，执行接口自动化
    'api_only_mode': False,  # False，执行UI自动化 True，执行接口自动化
    'sk-6c924d128cc24fa09acf281ccf5670d3': '',
}
