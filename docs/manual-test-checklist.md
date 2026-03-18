# 手动测试检查清单：前置条件集成

本检查清单用于验证与真实 webseleniumerp 项目的前置条件完整集成。

## 前置条件

- [x] 已克隆 webseleniumerp 项目到本地
- [x] 已在 webseleniumerp 中创建 `config/settings.py`（参见 README.md 模板）
- [x] 后端服务运行中：`uv run uvicorn backend.api.main:app --reload --port 8080`
- [x] 前端服务运行中：`cd frontend && npm run dev`

## 环境配置

1. 在 `.env` 中添加：
   ```
   WEBSERP_PATH=/path/to/your/webseleniumerp
   ```
2. 重启后端服务以加载新配置

---

## 测试 1：完整流程（VAL-01）

**目的：** 验证从操作码选择到前置条件执行的完整流程

### 测试步骤：

1. - [x] 打开前端页面 http://localhost:5173
2. - [x] 进入任务创建页面
3. - [x] 点击前置条件文本框上方的"选择操作码"按钮
4. - [x] 验证：弹窗显示按模块分组的操作码列表
5. - [x] 选择操作码：FA1, HC1
6. - [x] 点击"确认"按钮
7. - [x] 验证：前置条件文本框包含生成的代码：
   
   - `sys.path.insert(0, '/path/to/webseleniumerp')`
   - `from common.base_prerequisites import PreFront`
   - `pre_front.operations(['FA1', 'HC1'])`
8. - [ ] 创建并运行任务
9. - [ ] 验证：任务执行包含前置条件步骤
10. - [ ] 验证：前置条件执行显示成功状态

### 预期结果：

- [ ] 操作码从真实 webseleniumerp 成功加载
- [ ] 生成的代码是有效的 Python 代码
- [ ] 前置条件执行无错误
- [ ] 上下文变量 `precondition_result` 设置为 'success'

---

## 测试 2：错误处理 - 路径未配置（VAL-02）

**目的：** 验证 WEBSERP_PATH 未设置时的错误处理

### 测试步骤：

1. [ ] 在 `.env` 中删除或注释 WEBSERP_PATH
2. [ ] 重启后端服务
3. [ ] 尝试在前端打开操作码选择器
4. [ ] 验证：按钮显示错误提示或处于禁用状态

### 预期结果：

- [ ] API 返回 503 Service Unavailable
- [ ] 前端显示适当的错误消息
- [ ] 错误消息提及 WEBSERP_PATH 配置

---

## 测试 3：错误处理 - 路径不存在（VAL-02）

**目的：** 验证 WEBSERP_PATH 指向无效位置时的错误处理

### 测试步骤：

1. [ ] 设置 WEBSERP_PATH 为不存在的路径：`WEBSERP_PATH=/nonexistent/path`
2. [ ] 重启后端服务
3. [ ] 检查启动日志中的验证错误

### 预期结果：

- [ ] 后端启动显示错误消息："WEBSERP_PATH 目录不存在"
- [ ] 错误包含解决方案提示

---

## 测试 4：错误处理 - 缺少 config/settings.py（VAL-02）

**目的：** 验证 webseleniumerp 配置文件缺失时的错误处理

### 测试步骤：

1. [ ] 正确设置 WEBSERP_PATH
2. [ ] 重命名或删除 `webseleniumerp/config/settings.py`
3. [ ] 重启后端服务
4. [ ] 检查启动日志中的验证错误

### 预期结果：

- [ ] 后端启动显示错误消息："config/settings.py 未找到"
- [ ] 错误包含创建该文件的模板

---

## 测试 5：错误处理 - 执行异常（VAL-02）

**目的：** 验证 PreFront.operations() 抛出异常时的错误处理

### 测试步骤：

1. [ ] 配置有效的 WEBSERP_PATH
2. [ ] 创建包含会抛出异常代码的前置条件：
   ```python
   raise ValueError("测试异常")
   ```
3. [ ] 运行任务
4. [ ] 检查执行结果

### 预期结果：

- [ ] 前置条件执行显示失败状态
- [ ] 错误消息包含异常详情
- [ ] 任务不会继续执行主步骤

---

## 签署确认

- [ ] 所有测试已完成
- [ ] 所有预期结果已验证
- [ ] 问题记录：_______________

**测试人员：** _______________
**测试日期：** _______________
**测试环境：** _______________
