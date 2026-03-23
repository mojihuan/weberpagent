# -*- coding: utf-8 -*-
import os
import sys
import unittest
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time
import threading
import gc
import importlib
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方框的问题

PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH)
REPORT_DIR = os.path.join(PROJECT_PATH, r'report')
HTML_REPORT_PATH = os.path.join(REPORT_DIR, 'report.html')
EXCEL_OUTPUT_PATH = os.path.join(REPORT_DIR, '原始测试报告.xlsx')


class TestSuiteManager:
    """测试套件管理类"""

    def __init__(self, target_path='testcase/test_attachment.py'):
        self.target_path = target_path

    def load_test_suite(self):
        """自动发现并加载指定目录下的所有测试用例，组成测试套件。"""
        self.reset_test_environment()

        if os.path.isfile(self.target_path):
            return self._load_single_file()
        elif os.path.isdir(self.target_path):
            return self._load_directory()
        else:
            print(f"警告：路径 {self.target_path} 不存在")
            return unittest.TestSuite()

    def _load_single_file(self):
        """加载单个测试文件"""
        test_dir = os.path.dirname(self.target_path)
        if test_dir not in sys.path:
            sys.path.insert(0, test_dir)

        module_name = os.path.basename(self.target_path).rstrip('.py')
        try:
            spec = importlib.util.spec_from_file_location(module_name, self.target_path)
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)

            loader = unittest.TestLoader()
            return loader.loadTestsFromModule(test_module)
        except Exception as e:
            print(f"加载测试文件失败: {e}")
            import traceback
            traceback.print_exc()
            return unittest.TestSuite()

    def _load_directory(self):
        """加载目录中的测试文件"""
        if not os.path.exists(self.target_path):
            print(f"警告：测试目录 {self.target_path} 不存在")
            return unittest.TestSuite()

        print(f"正在从 {self.target_path} 发现测试用例...")
        return unittest.defaultTestLoader.discover(
            self.target_path,
            pattern="test*.py",
            top_level_dir=os.path.dirname(os.path.abspath(__file__))
        )

    @staticmethod
    def reset_test_environment():
        """重置测试环境，清理可能影响测试执行的资源"""
        modules_to_remove = [name for name in sys.modules if name.startswith('testcase.')]
        for name in modules_to_remove:
            del sys.modules[name]
        gc.collect()
        importlib.invalidate_caches()


class TestRunnerManager:
    """测试运行器管理类"""

    def __init__(self, suite, report_dir, filename):
        self.suite = suite
        self.report_dir = report_dir
        self.filename = filename

    def run_tests(self):
        """执行测试并返回结果统计"""
        os.makedirs(self.report_dir, exist_ok=True)
        runner = CustomTestRunner(verbosity=2)
        test_result = runner.run(self.suite)

        # 生成HTML报告
        ReportGenerator.generate_html_report(runner.test_details, self.report_dir, self.filename)

        return {
            'all': len(runner.test_details),
            'success': len([d for d in runner.test_details if d['result'] == '通过']),
            'fail': len([d for d in runner.test_details if d['result'] == '失败']),
            'skip': len([d for d in runner.test_details if d['result'] == '跳过']),
            'error': len([d for d in runner.test_details if d['result'] == '错误'])
        }


class ReportGenerator:
    """报告生成管理类"""

    @staticmethod
    def generate_html_report(test_details, report_dir, filename):
        """生成HTML格式的测试报告"""
        if not test_details:
            return

        chart_base64 = ReportGenerator._generate_chart_data(test_details)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>测试报告结果</title>
            <link rel="icon" href="data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50 10 L90 50 L50 90 L10 50 Z' fill='%2328a745'/%3E%3C/svg%3E" />
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    margin: 20px;
                    color: #333;
                    line-height: 1.6;
                }}
                .header {{
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }}
                .summary {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin: 20px 0;
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }}
                .summary-item {{
                    display: inline-block;
                    padding: 8px 12px;
                    background: #f8f9fa;
                    border-radius: 6px;
                    font-weight: 500;
                    min-width: 120px;
                }}
                .pass {{ color: #28a745; }}
                .fail {{ color: #dc3545; }}
                .error {{ color: #ffc107; }}
                .skip {{ color: #17a2b8; }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    border-radius: 8px;
                    overflow: hidden;
                }}
                th, td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #e0e0e0;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: 600;
                    color: #444;
                }}
                tr:hover {{
                    background-color: #f9f9f9;
                }}

                .chart-container {{
                    margin: 30px 0;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                }}
                .chart {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 6px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}

                h1, h2 {{
                    color: #2c3e50;
                    margin-top: 0;
                }}
                h2 {{
                    border-bottom: 2px solid #eee;
                    padding-bottom: 8px;
                }}

                /* 错误详情样式 */
                .detail-toggle {{
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                }}
                .detail-toggle:hover {{
                    background-color: #0056b3;
                }}
                .detail-content {{
                    margin: 10px 0;
                    padding: 10px;
                    background: #f8f9fa;
                    border: 1px dashed #ccc;
                    font-family: monospace;
                    font-size: 12px;
                    overflow: auto;
                    max-height: 200px;
                    display: none;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>测试报告结果</h1>
                <p><strong>测试人员:</strong> 壹准二手通erp</p>
                <p><strong>测试描述:</strong> 回归测试</p>
                <p><strong>生成时间:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="summary">
                <div class="summary-item"><strong>总测试数:</strong> {len(test_details)}</div>
                <div class="summary-item pass"><strong>通过:</strong> {len([d for d in test_details if d['result'] == '通过'])}</div>
                <div class="summary-item fail"><strong>失败:</strong> {len([d for d in test_details if d['result'] == '失败'])}</div>
                <div class="summary-item error"><strong>错误:</strong> {len([d for d in test_details if d['result'] == '错误'])}</div>
                <div class="summary-item skip"><strong>跳过:</strong> {len([d for d in test_details if d['result'] == '跳过'])}</div>
            </div>

            <!-- 图表区域 -->
            <div class="chart-container">
                <h2>测试结果分析图表</h2>
                <img src="data:image/png;base64,{chart_base64}" alt="测试结果分析图表" class="chart">
            </div>

            <table>
                <thead>
                    <tr>
                        <th>测试类</th>
                        <th>测试方法</th>
                        <th>描述</th>
                        <th>结果</th>
                        <th>耗时</th>
                    </tr>
                </thead>
                <tbody>
        """

        for i, detail in enumerate(test_details):
            row_bg = "#E0E0E0" if i % 2 == 0 else "#FFFFFF"
            result_color = ""
            if detail['result'] == '通过':
                result_color = "class='pass'"
            elif detail['result'] == '失败':
                result_color = "class='fail'"
            elif detail['result'] == '错误':
                result_color = "class='error'"
            elif detail['result'] == '跳过':
                result_color = "class='skip'"

            # 构建错误详情的折叠面板
            error_detail = ""
            if detail['result'] in ['失败', '错误'] and detail['full_traceback']:
                escaped_traceback = detail['full_traceback'].replace('<', '&lt;').replace('>', '&gt;')
                error_detail = f"""
                    <tr style="background-color: {row_bg};">
                        <td colspan="5" style="padding: 5px;">
                            <button onclick="toggleDetail(this)" class="detail-toggle">展开详情</button>
                            <div id="detail-{i}" class="detail-content">
                                <pre>{escaped_traceback}</pre>
                            </div>
                        </td>
                    </tr>
                """
            else:
                error_detail = ""

            html_content += f"""
                                <tr style="background-color: {row_bg};">
                                    <td>{detail['test_class']}</td>
                                    <td>{detail['test_method']}</td>
                                    <td>{detail['description']}</td>  <!-- 新增列 -->
                                    <td {result_color}>{detail['result']}</td>
                                    <td>{detail['time']}s</td>
                                </tr>
            """
            html_content += error_detail

        html_content += """
                </tbody>
            </table>

            <script>
                function toggleDetail(button) {
                    const detailDiv = button.nextElementSibling;
                    if (detailDiv.style.display === 'none' || detailDiv.style.display === '') {
                        detailDiv.style.display = 'block';
                        button.textContent = '收起详情';
                    } else {
                        detailDiv.style.display = 'none';
                        button.textContent = '展开详情';
                    }
                }
            </script>
        </body>
        </html>
        """

        report_path = os.path.join(report_dir, filename)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML报告已生成: {report_path}")

    @staticmethod
    def _generate_chart_data(test_details):
        """生成测试结果分析图表"""
        if not test_details:
            return None

        stats = {
            '通过': len([d for d in test_details if d['result'] == '通过']),
            '失败': len([d for d in test_details if d['result'] == '失败']),
            '错误': len([d for d in test_details if d['result'] == '错误']),
            '跳过': len([d for d in test_details if d['result'] == '跳过'])
        }

        total = len(test_details)
        percentages = {k: v / total * 100 for k, v in stats.items()}

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db']
        non_zero_stats = {k: v for k, v in stats.items() if v > 0}

        if not non_zero_stats:
            ax1.text(0.5, 0.5, "无有效测试结果", ha='center', va='center', transform=ax1.transAxes, fontsize=14, fontweight='bold')
            ax1.axis('off')
        else:
            wedges, texts, autotexts = ax1.pie(
                non_zero_stats.values(),
                labels=non_zero_stats.keys(),
                colors=[colors[list(stats.keys()).index(k)] for k in non_zero_stats.keys()],
                startangle=180,
                textprops={'fontsize': 12},
                autopct='%1.1f%%',
                pctdistance=0.85,
                explode=[0.05] * len(non_zero_stats),
            )
            ax1.axis('equal')
            ax1.set_title('测试结果分布', fontsize=14, fontweight='bold', pad=20)

        # 条形图 - 各类测试用例数量
        bars = ax2.bar(stats.keys(), stats.values(), color=colors, edgecolor='black', linewidth=0.5)
        ax2.set_title('各类测试用例数量', fontsize=14, fontweight='bold', pad=25)
        ax2.set_ylabel('数量', fontsize=12)
        ax2.set_xlabel('测试结果类型', fontsize=12)
        ax2.tick_params(axis='both', which='major', labelsize=11)

        # 添加数值标签
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                     f'{height}', ha='center', va='bottom', fontsize=11)

        # 调整布局
        plt.tight_layout(pad=4.0)

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
        buf.seek(0)
        chart_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        plt.close()

        return chart_base64


class ResourceManager:
    """资源管理类"""

    def __init__(self):
        self.lock_thread_running = True
        self.lock_thread = None

    def start_prevent_lock(self):
        """启动防锁屏线程"""
        try:
            self.lock_thread = threading.Thread(target=self._prevent_lock_worker)
            self.lock_thread.daemon = True
            self.lock_thread.start()
        except Exception as e:
            print(f"启动防锁屏线程失败: {e}")

    def stop_prevent_lock(self):
        """停止防锁屏线程"""
        self.lock_thread_running = False

    def _prevent_lock_worker(self):
        """防锁屏线程的实际工作逻辑"""
        try:
            import pyautogui
            pyautogui.FAILSAFE = False
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width / 2, screen_height / 2)

            while self.lock_thread_running:
                try:
                    pyautogui.press('shift')
                    time.sleep(30)
                except Exception as e:
                    print(f"防止锁屏时出错: {e}")
                    time.sleep(30)
        except ImportError:
            print("未安装 pyautogui，跳过防锁屏功能")
        except Exception as e:
            print(f"防锁屏线程异常: {e}")

    def cleanup_resources(self):
        """清理所有资源"""
        self.stop_prevent_lock()
        try:
            import gevent
            hub = gevent.get_hub()
            if hub:
                hub.destroy()
        except:
            pass


class MainController:
    """主控制器类"""

    def __init__(self):
        self.resource_manager = ResourceManager()
        self.suite_manager = TestSuiteManager()
        self.runner_manager = None

    def run(self):
        """主流程函数"""
        self.resource_manager.start_prevent_lock()
        print("当前工作目录:", os.getcwd())

        try:
            suite = self.suite_manager.load_test_suite()
            total_tests = sum(s.countTestCases() for s in suite if s is not None)
            print(f"准备执行 {total_tests} 个测试用例")

            if total_tests == 0:
                print("警告：测试套件为空，没有发现测试用例")
                return

            self.runner_manager = TestRunnerManager(suite, REPORT_DIR, 'report.html')
            result = self.runner_manager.run_tests()

            headers, data = parse_html_report(HTML_REPORT_PATH)
            export_to_excel(headers, data)

            print(f"测试执行完成，结果: {result}")
        except Exception as e:
            print(f"主程序执行异常: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.resource_manager.cleanup_resources()


class CustomTestResult(unittest.TextTestResult):
    """
    自定义测试结果类，用于收集详细的测试用例信息（包括完整 traceback）
    """

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_details = []

    def startTest(self, test):
        """在测试开始前记录时间"""
        super().startTest(test)
        test._start_time = time.time()  # 为每个测试用例记录开始时间

    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - test._start_time
        # 获取测试方法对象并提取其 docstring
        method_name = test._testMethodName
        method = getattr(test, method_name, None)
        docstring = getattr(method, '__doc__', '').strip()
        self.test_details.append({
            'test_class': test.__class__.__name__,
            'test_method': method_name,
            'result': '通过',
            'time': round(elapsed, 2),
            'error_info': None,
            'full_traceback': None,
            'description': docstring  # 正确获取方法注释
        })

    def addError(self, test, err):
        super().addError(test, err)
        try:
            if err is None:
                error_msg = "未知错误：err 为 None"
                full_traceback = "无法获取堆栈信息"
            else:
                if isinstance(err, tuple) and len(err) == 3:
                    exc_type, exc_value, exc_traceback = err
                else:
                    exc_type = type(err)
                    exc_value = err
                    exc_traceback = None

                import traceback
                error_msg = ''.join(traceback.format_exception_only(exc_type, exc_value))
                if exc_traceback is not None:
                    full_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                else:
                    full_traceback = f"无法获取堆栈信息: {str(err)}"
        except Exception as e:
            error_msg = f"获取错误信息时出错: {e}"
            full_traceback = "无法获取堆栈信息"

        elapsed = time.time() - getattr(test, '_start_time', 0)
        method_name = test._testMethodName
        method = getattr(test, method_name, None)
        docstring = getattr(method, '__doc__', '').strip()
        self.test_details.append({
            'test_class': test.__class__.__name__,
            'test_method': method_name,
            'result': '错误',
            'time': round(elapsed, 2),
            'error_info': error_msg.strip(),
            'full_traceback': full_traceback.strip(),
            'description': docstring  # 正确获取方法注释
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        try:
            if err is None:
                error_msg = "未知错误：err 为 None"
                full_traceback = "无法获取堆栈信息"
            else:
                if isinstance(err, tuple) and len(err) == 3:
                    exc_type, exc_value, exc_traceback = err
                else:
                    exc_type = type(err)
                    exc_value = err
                    exc_traceback = None

                import traceback
                error_msg = ''.join(traceback.format_exception_only(exc_type, exc_value))
                if exc_traceback is not None:
                    full_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                else:
                    full_traceback = f"无法获取堆栈信息: {str(err)}"
        except Exception as e:
            error_msg = f"获取失败信息时出错: {e}"
            full_traceback = "无法获取堆栈信息"

        elapsed = time.time() - getattr(test, '_start_time', 0)
        method_name = test._testMethodName
        method = getattr(test, method_name, None)
        docstring = getattr(method, '__doc__', '').strip()
        self.test_details.append({
            'test_class': test.__class__.__name__,
            'test_method': method_name,
            'result': '失败',
            'time': round(elapsed, 2),
            'error_info': error_msg.strip(),
            'full_traceback': full_traceback.strip(),
            'description': docstring  # 正确获取方法注释
        })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        elapsed = time.time() - test._start_time
        method_name = test._testMethodName
        method = getattr(test, method_name, None)
        docstring = getattr(method, '__doc__', '').strip()
        self.test_details.append({
            'test_class': test.__class__.__name__,
            'test_method': method_name,
            'result': '跳过',
            'time': round(elapsed, 2),
            'error_info': f"跳过原因: {reason}",
            'full_traceback': None,
            'description': docstring  # 正确获取方法注释
        })


class CustomTestRunner(unittest.TextTestRunner):
    """
    自定义测试运行器，用于收集详细的测试结果
    """

    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super().__init__(stream, descriptions, verbosity)
        self.results = []
        self.test_details = []

    def run(self, test):
        # 创建自定义的结果对象
        result = CustomTestResult(self.stream, self.descriptions, self.verbosity)

        # 执行测试
        start_time = time.time()
        test(result)
        end_time = time.time()

        # 收集测试结果
        self.test_details = result.test_details

        # 返回结果
        return result


def parse_html_report(report_path):
    """解析HTML报告"""
    try:
        if not os.path.exists(report_path):
            print(f"报告文件不存在: {report_path}")
            return [], []

        with open(report_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')

        if not table:
            print("报告中未找到表格数据")
            return [], []

        headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
        data = []
        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                while len(row_data) < len(headers):
                    row_data.append("")
                data.append(row_data)

        return headers, data
    except Exception as e:
        print(f"解析HTML报告时出错: {e}")
        return [], []


def export_to_excel(headers, data):
    """导出Excel文件"""
    try:
        if not data:
            df = pd.DataFrame(columns=headers or ["测试类", "测试方法", "描述", "结果", "耗时"])
        else:
            aligned_data = []
            for row in data:
                while len(row) < len(headers):
                    row.append("")
                aligned_data.append(row[:len(headers)])
            df = pd.DataFrame(aligned_data, columns=headers if headers else ["测试类", "测试方法", "描述", "结果", "耗时"])

        df.to_excel(EXCEL_OUTPUT_PATH, index=False)
        print(f'Excel文件已生成: {EXCEL_OUTPUT_PATH}')
    except Exception as e:
        print(f"导出Excel文件时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    controller = MainController()
    controller.run()
