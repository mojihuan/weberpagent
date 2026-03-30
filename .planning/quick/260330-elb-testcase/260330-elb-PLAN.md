# Quick Task 260330-elb: 为 testcase 下所有测试生成测试步骤文档

## 目标
为 `webseleniumerp/testcase/` 下每个测试文件，参考 `docs/测试步骤.md` 的格式，生成对应的测试步骤文档。

## 参考格式
```
前置条件：'FA1', 'HC1'
imei: pc.inventory_list_data(i=2, j=13)[0]['imei']

步骤1：{点击}密码登录
步骤2：{输入}请输入账号{Y59800075}
...
断言：调用方法：pc.sell_sale_item_list_assert(...)
```

## 输出目录
`docs/test-steps/`

## 任务列表

### Task 1: 创建输出目录并生成测试步骤文档
- **files**: `docs/test-steps/*.md`
- **action**: 为每个测试文件生成对应的测试步骤文档，包含前置条件、步骤、断言
- **verify**: 确认每个测试文件都有对应的步骤文档
- **done**: 所有文档已创建

#### 需要生成的文档（19个）：
1. `登录-测试步骤.md` - test_login.py
2. `采购-测试步骤.md` - test_purchase.py
3. `销售-测试步骤.md` - test_sell.py
4. `库存-测试步骤.md` - test_inventory.py
5. `财务-测试步骤.md` - test_finance.py
6. `质检-测试步骤.md` - test_quality.py
7. `维修-测试步骤.md` - test_repair.py
8. `运营中心-测试步骤.md` - test_fulfillment.py
9. `配件-测试步骤.md` - test_attachment.py
10. `拍机堂-测试步骤.md` - test_camera.py
11. `消息-测试步骤.md` - test_message.py
12. `送修-测试步骤.md` - test_send.py
13. `竞标小程序-测试步骤.md` - test_bidding.py
14. `拍卖行小程序-测试步骤.md` - test_auction.py
15. `保卖-测试步骤.md` - test_guarantee.py
16. `平台管理-测试步骤.md` - test_platform.py
17. `帮卖-测试步骤.md` - test_help.py
18. `钱包-测试步骤.md` - test_purse.py
19. `小贩小程序-测试步骤.md` - test_trafficker.py

### Task 2: 更新 STATE.md
- **action**: 在 STATE.md 中记录 quick task 完成
- **done**: STATE.md 已更新

### Task 3: 提交
- **action**: git commit 所有测试步骤文档
- **done**: 已提交
