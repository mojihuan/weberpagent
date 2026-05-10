# Excel 模版动态数据填充设计

## 背景

webseleniumerp 项目中 `ImportDataEdit` 类支持从 ERP API 获取数据后写入 Excel 模版，
再由 Selenium 上传到 ERP 系统完成业务操作。weberpagent 项目需要复用这一能力，
但用 AI agent（browser-use）替代 Selenium 执行上传操作。

## 目标

在前置条件阶段，支持从 ERP API 获取真实数据并写入 Excel 模版文件，
生成填充后的文件路径供 agent 在任务执行阶段上传。

## 设计

### 架构

```
data/templates/              ← Excel 模版目录（.xlsx 文件，git 管理）
    ├── new_purchase_order.xlsx
    ├── attachment_receive.xlsx
    └── inventory_transfer.xlsx

data/filled/                 ← 运行时填充文件（每次 run 一个子目录）
    {run_id}/
        new_purchase_order.xlsx

前置条件执行流：
  context.get_data()         ← 复用现有 API 获取数据
  context.fill_excel()       ← [新增] 复制模版 → 填充单元格 → 保存副本
  context.get_excel_path()   ← [新增] 获取填充后文件路径

变量替换：
  任务描述中 {{excel_file}}  ← Jinja2 替换为实际文件路径

Agent 执行：
  看到路径后自动上传文件
```

### ContextWrapper 新增方法

在 `backend/core/precondition_service.py` 的 `ContextWrapper` 类中新增：

#### `fill_excel(template_name, sheet='Sheet1', row=2, col=1, value)`

- 从 `data/templates/{template_name}.xlsx` 复制到 `data/filled/{run_id}/`
- 用 openpyxl 打开副本，写入 `(sheet, row, col, value)`
- 同一 run 内多次调用同一模版名，操作同一个副本（不重复复制）
- 返回 self，支持链式调用
- 模版不存在时抛出 `FileNotFoundError`

#### `get_excel_path(template_name)`

- 返回 `data/filled/{run_id}/{template_name}.xlsx` 的绝对路径
- 如果尚未 fill 过，返回原始模版路径（只读场景）

### 文件目录结构

```
weberpagent/
  data/
    templates/          ← 模版文件（git 管理）
      new_purchase_order.xlsx
      attachment_receive.xlsx
    filled/             ← 运行时填充文件（gitignore）
      {run_id}/
        new_purchase_order.xlsx
    test-files/         ← 已有的测试文件目录
```

### 前置条件写法

#### 手动创建任务（UI）

前置条件文本框中逐行写 Python 代码：

```python
items = context.get_data('PcImport', '库存管理|库存列表', i=2, j=13)
context.fill_excel('new_purchase_order', row=2, col=1, value=items[0]['imei'])
context['excel_file'] = context.get_excel_path('new_purchase_order')
```

#### Excel 导入测试用例

preconditions 列写 JSON 数组，每条是一条 Python 代码：

```json
[
  "items = context.get_data('PcImport', '库存管理|库存列表', i=2, j=13)",
  "context.fill_excel('new_purchase_order', row=2, col=1, value=items[0]['imei'])",
  "context['excel_file'] = context.get_excel_path('new_purchase_order')"
]
```

### 任务描述写法

```
请上传文件 {{excel_file}} 到采购入库页面的文件上传区域
```

pipeline 执行时 Jinja2 将 `{{excel_file}}` 替换为实际路径，agent 看到的是：

```
请上传文件 /path/to/weberpagent/data/filled/abc12345/new_purchase_order.xlsx 到采购入库页面的文件上传区域
```

### 多模版场景

同一 Task 中使用多个模版，给变量取不同名字：

```python
context.fill_excel('template_a', row=2, col=1, value=data_a)
context['file_a'] = context.get_excel_path('template_a')

context.fill_excel('template_b', row=2, col=1, value=data_b)
context['file_b'] = context.get_excel_path('template_b')
```

任务描述：`先上传 {{file_a}} 到页面A，再上传 {{file_b}} 到页面B`

### 错误处理

- 模版不存在 → `fill_excel` 抛出 `FileNotFoundError`，前置条件标记为 failed
- 单元格坐标越界 → openpyxl 自动扩展（不报错）
- run_id 未传入 → 使用默认临时目录

### 代码生成适配

生成的 Playwright 测试代码中，需要将 `context.fill_excel()` 调用转换为对应代码。
在代码生成阶段提取 `fill_excel` 相关操作，生成等效的 openpyxl 调用。

## 影响范围

| 文件 | 变更 |
|------|------|
| `backend/core/precondition_service.py` | ContextWrapper 新增 fill_excel / get_excel_path |
| `backend/api/routes/run_pipeline.py` | 传入 run_id 给 ContextWrapper |
| `backend/config/settings.py` | 新增 templates 目录配置 |
| `data/templates/` | 新建模版目录，放入 Excel 模版文件 |
| `.gitignore` | 忽略 data/filled/ |
