# Phase 7: 动态数据支持 - Research

**Researched:** 2026-03-17
**Status:** Complete

---

## Research Summary

通过 gitnexus 分析 webseleniumerp-master 项目，发现动态数据支持的核心实现集中在 `BaseRandomMixin` 和 `BaseApi` 类中。

---

## 1. 随机数生成器 (BaseRandomMixin)

**源文件:** `common/base_random_mixin.py`

### 核心设计模式

1. **类级别存储 + 线程锁确保唯一性**
   ```python
   _generated_sf = set()      # 已生成的 SF 单号
   _sf_lock = threading.Lock()  # 线程锁
   _sf_counter = 0            # 计数器
   ```

2. **通用唯一 ID 生成器**
   ```python
   def _generate_unique_id(self, prefix, timestamp_len, random_len, counter_name, suffix="", max_attempts=1000):
       # 时间戳部分 + 随机部分 + 计数器部分
       timestamp_part = str(int(time.time() * 1000000))[-timestamp_len:]
       random_part = str(self.random_numbers(random_len))
       counter_part = str(counter_value % 10000).zfill(4)
       new_id = prefix + timestamp_part + random_part + counter_part + suffix
   ```

### 支持的随机数据类型

| 方法 | 格式 | 说明 |
|------|------|------|
| `sf` | SF + 14位 | 顺丰物流单号，使用时间戳+UUID+线程ID+计数器 |
| `phone` | 13 + 9位 | 11位手机号（13开头） |
| `imei` | I + 14位 | 15位 IMEI 设备识别码 |
| `jd` | JD + 12位 | JD 开头编号 |
| `serial` | 8位数字 | 纯数字序列号 |
| `serial_number` | SN + 时间戳 + UUID + 线程ID + 随机数 + 计数器 | 完整序列号 |
| `mixed_random` | 6位数字+字母 | 混合随机字符串 |
| `number` | 2位数字 | 短数字 |
| `four_digits` | 4位数字 | 4位数字 |
| `random_numbers(n)` | N位数字 | 指定长度随机数字 |

### SF 物流单号详细实现

```python
@property
def sf(self):
    """
    动态生成SF开头的14位编号，确保唯一性，兼容高并发
    格式：SF + 时间戳部分 + UUID部分 + 线程ID后四位 + 计数器
    """
    timestamp_part = str(int(time.time() * 1000000))[-4:]  # 取时间戳的后4位
    uuid_part = str(uuid.uuid4())[:4].upper()  # 使用UUID的前4位
    thread_id = str(threading.current_thread().ident)[-4:]  # 使用线程ID后四位
    base_sf = f"SF{timestamp_part}{uuid_part}{thread_id}"

    with self._sf_lock:
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
```

---

## 2. 时间计算工具 (BaseApi)

**源文件:** `common/base_api.py`

**继承关系:** `class BaseApi(BaseRandomMixin)` - BaseApi 继承了 BaseRandomMixin 的所有功能

### 时间计算方法

| 方法 | 参数 | 返回格式 | 说明 |
|------|------|----------|------|
| `get_time_stamp_by_minute(minute)` | minute: int | `%Y-%m-%d %H:%M:%S` | 当前时间 ±N 分钟 |
| `get_formatted_datetime(...)` | years, months, days, hours, minutes, seconds | `%Y-%m-%d %H:%M:%S` | 灵活时间偏移 |
| `get_current_time(hours, minutes, seconds)` | hours, minutes, seconds | `%H:%M:%S` | 时分秒 |
| `get_the_date(days)` | days | `%Y-%m-%d` | 日期 |

### get_time_stamp_by_minute 实现

```python
def get_time_stamp_by_minute(self, minute: int) -> str:
    """
    输入指定的分钟数，生成对应分钟数后的时间戳
    :param minute: 分钟数（可为负数）
    :return: 时间戳字符串
    """
    formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S") +
            timedelta(minutes=int(minute))).strftime("%Y-%m-%d %H:%M:%S")
```

### get_formatted_datetime 实现

```python
def get_formatted_datetime(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
    """
    获取当前时间，并支持增加指定年、月、日、时、分、秒数
    """
    from dateutil.relativedelta import relativedelta
    current_time = datetime.now()
    adjusted_time = current_time + relativedelta(
        years=years,
        months=months,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )
    return adjusted_time.strftime("%Y-%m-%d %H:%M:%S")
```

---

## 3. 数据缓存机制

### 现有实现 (webseleniumerp-master)

使用 pickle 文件存储：
- `get_list_data(file_name, key)` - 从 pkl 文件获取列表数据
- `make_pkl_file(content, filename)` - 将数据序列化保存到 pkl 文件

### aiDriveUITest 设计决策

根据 CONTEXT.md：
- **缓存范围:** 单次运行（Run），数据存储在内存 context 中
- **生命周期:** 仅在当前 Run 执行期间有效，不持久化到数据库
- **跨步骤传递:** 顺序传递 context（前置条件 → UI 测试 → 接口断言）
- **变量引用:** 使用 `{{变量名}}` 语法（Jinja2）

**无需移植 pkl 文件机制** - aiDriveUITest 使用内存 context 存储。

---

## 4. 移植策略

### 方案选择

**推荐方案:** 在 `PreconditionService._setup_execution_env()` 中直接注入辅助函数

```python
def _setup_execution_env(self, context: dict) -> dict:
    """设置执行环境，注入辅助函数"""
    from datetime import datetime, timedelta
    import random
    import uuid
    import time
    import threading

    # 随机数生成函数
    def sf_waybill():
        """生成 SF 物流单号"""
        timestamp_part = str(int(time.time() * 1000000))[-4:]
        uuid_part = str(uuid.uuid4())[:4].upper()
        thread_id = str(threading.current_thread().ident or 0)[-4:]
        return f"SF{timestamp_part}{uuid_part}{thread_id}"

    def random_phone():
        """生成 11 位手机号"""
        return "13" + ''.join(random.choices('0123456789', k=9))

    def random_imei():
        """生成 15 位 IMEI"""
        return "I" + ''.join(random.choices('0123456789', k=14))

    # 时间计算函数
    def time_now(offset_minutes: int = 0):
        """获取当前时间，支持 ±N 分钟偏移"""
        current = datetime.now()
        if offset_minutes:
            current = current + timedelta(minutes=offset_minutes)
        return current.strftime("%Y-%m-%d %H:%M:%S")

    return {
        '__builtins__': __builtins__,
        'context': context,
        'sf_waybill': sf_waybill,
        'random_phone': random_phone,
        'random_imei': random_imei,
        'time_now': time_now,
    }
```

### 为什么不直接移植 BaseRandomMixin

1. **简化需求:** aiDriveUITest 不需要高并发场景下的唯一性保证（单线程执行）
2. **降低复杂度:** 去除线程锁、计数器、类级别存储等复杂机制
3. **函数式设计:** 用户在前置条件代码中直接调用函数，更直观
4. **易于扩展:** 后续可通过添加函数轻松扩展

---

## 5. 动态数据获取

### 现有机制

根据 CONTEXT.md，动态数据获取：
- **获取时机:** 仅在前置条件阶段
- **API 来源:** 复用现有项目的 API 封装层，通过 `ERP_API_MODULE_PATH` 环境变量配置
- **用户自行处理列表数据:** 如 `context['first_order'] = orders[0]`

### 实现方式

前置条件代码示例：
```python
from api.api_purchase import PurchaseOrderListApi
api = PurchaseOrderListApi()
orders = api.list_orders(status='pending')
context['order_id'] = orders[0]['id']
```

**无需额外开发** - Phase 5 已实现 `ERP_API_MODULE_PATH` 配置和 `exec()` 执行机制。

---

## 6. Integration Points

### 需要修改的文件

1. **`backend/core/precondition_service.py`**
   - 在 `_setup_execution_env()` 中添加随机数和时间计算函数

2. **无需新建文件** - 函数直接在 PreconditionService 中定义

### 与现有系统的集成

| 组件 | 集成方式 |
|------|----------|
| PreconditionService | 在执行环境中注入辅助函数 |
| ApiAssertionService | 接收前置条件的 context（已实现） |
| AgentService | 顺序传递 context（前置 → UI → 断言） |
| Jinja2 | 变量替换 `{{变量名}}`（已实现） |

---

## 7. Validation Architecture

### 测试策略

1. **单元测试**
   - 测试每个随机数生成函数
   - 测试时间计算函数（正负偏移）
   - 测试边界条件

2. **集成测试**
   - 测试前置条件中使用动态数据
   - 测试跨步骤数据传递（前置 → UI → 断言）
   - 测试 Jinja2 变量替换

3. **E2E 测试**
   - 完整流程：创建任务 → 执行 → 验证动态数据

### 验收标准

| ID | 标准 | 验证方式 |
|----|------|----------|
| DYN-01 | 支持生成 SF 物流单号、手机号等随机数据 | 单元测试 |
| DYN-02 | 支持从 API 接口获取数据并用于测试 | 集成测试 |
| DYN-03 | 支持跨步骤缓存数据供后续复用 | E2E 测试 |
| DYN-04 | 支持时间计算（now ± N 分钟） | 单元测试 |

---

## 8. Recommendations

### 实现优先级

1. **Wave 1 (基础功能)**
   - 随机数生成函数（sf_waybill, random_phone, random_imei）
   - 时间计算函数（time_now）
   - 单元测试

2. **Wave 2 (集成验证)**
   - PreconditionService 集成
   - 跨步骤数据传递验证
   - E2E 测试

### 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 随机数不够随机 | 使用 uuid + timestamp 组合 |
| 时间偏移计算错误 | 使用 timedelta 确保正确性 |
| context 数据丢失 | 顺序传递确保完整性 |

---

## RESEARCH COMPLETE
