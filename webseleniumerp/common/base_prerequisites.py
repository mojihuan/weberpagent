# coding: utf-8
from common.base_api import BaseApi
from common.import_api import ImportApi
from common.import_request import ImportRequest


class CommonFront(BaseApi):
    """前置条件"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = ImportRequest()
        self.api = ImportApi()

    def execute_operations(self, operations_dict, data):
        """通用操作执行方法"""
        actions = operations_dict.get(data)
        if not actions:
            raise ValueError(f"无效的操作参数 '{data}'")
        for action in actions:
            action()


class PreFront(CommonFront):

    def login_operations(self):
        """登录"""
        pass

    def operations(self, data=None):
        # 定义各个模块的操作字典
        attachment = {
            # 配件管理|配件采购|新增采购单
            'AA1': [self.request.attachment_purchase_add.new_purchase_order_warehousing],  # 手机-新增采购单未付款已到货
            'AA2': [self.request.attachment_purchase_add.added_purchase_order_unpaid_in_transit],  # 笔记本电脑-新增采购单未付款在路上
            'AA3': [self.request.attachment_purchase_add.new_purchase_order_route],  # 平板电脑-新增采购单已付款在路上
            'AA4': [self.request.attachment_purchase_add.attachment_new_purchase_order_payment],  # 智能手表-新增采购单已付款已到货
            # 配件管理|配件销售|销售列表
            'AB1': [self.request.attachment_sales_list.uncollected_partial_sales_amount],  # 销售出库-未收款
            'AB2': [self.request.attachment_sales_list.accessories_sales_express_received_payment],  # 销售出库-已收款
            # 配件管理|配件库存|库存调拨
            'AC1': [self.request.attachment_stock_transfer.new_allocation],  # 新增调拨
            # 配件管理|配件库存|库存列表
            'AD1': [self.request.attachment_inventory_list.transfer_items_special],  # 库存移交给库存配件
            # 配件管理|入库管理|待接收物品
            'AE1': [self.request.attachment_goods_received.goods_received],  # 接收物品
            # 配件管理|移交接收管理|移交记录
            'AF1': [self.request.attachment_hand_over_records.bulk_cancel_handovers],  # 批量移交取消
            # 配件管理|入库管理|旧配件入库
            'AG1': [self.request.attachment_old_warehouse.phone_old_attachment_warehouse],  # 手机-新增采购单
            # 配件管理|配件维护
            'AH1': [self.request.attachment_maintenance.added_a_button_category_external_category],  # 新增配件维护-停用
            'AH2': [self.request.attachment_maintenance.added_a_button_category_matching],  # 新增配件维护-启用
            # 配件管理|入库管理|新到货入库
            'AI1': [self.request.attachment_sorting_list.search_for_tracking_number_inbound_and_handover],  # 新到货入库
        }
        finance = {
            # 财务管理|业务记账|预付预收
            'BA1': [self.request.finance_pre_pay_received.add_prepay],  # 新增预付单
            'BA2': [self.request.finance_pre_pay_received.add_received],  # 新增预收单
        }
        fulfillment = {
            # 运营中心|收货入库
            'CA1': [self.request.fulfillment_sign_into_the_library.quality_inspection_upload_videos_for_storage],  # 收货入库
            'CA2': [self.request.fulfillment_sign_into_the_library.unpacking_and_receiving_goods_into_storage],  # 收货入库-X
            # 运营中心|质检管理
            'CB1': [self.request.fulfillment_quality_manage.quality_receive_items_in_bulk],  # 批量接收
            'CB2': [self.request.fulfillment_quality_manage.quality_submit_the_quality_inspection_results, self.wait_default],  # 提交质检结果
            'CB3': [self.request.fulfillment_quality_manage.receive_items_in_bulk],  # 批量接收-X
            'CB4': [self.request.fulfillment_quality_manage.not_quality],  # 无需质检
            'CB5': [self.request.fulfillment_quality_manage.submit_the_quality_inspection_results_no, self.wait_default],  # 提交质检结果不传图
            'CB6': [self.request.fulfillment_quality_manage.submit_the_quality_inspection_results, self.wait_default],  # 提交质检结果-X
            'CB7': [self.request.fulfillment_quality_manage.direct_shot_physical_re_inspection_received],  # 批量接收
            'CB8': [self.request.fulfillment_quality_manage.direct_shot_of_the_real_thing_submit_quality, self.wait_default],  # 提交质检结果
            'CB9': [self.request.fulfillment_quality_manage.direct_platform_review_receive_in_batches],  # 批量接收
            'CB10': [self.request.fulfillment_quality_manage.direct_platform_review_submit_quality],  # 提交质检结果
            # 运营中心|退货管理
            'CC1': [self.request.fulfillment_returns_manage.return_to_the_warehouse],  # 邮寄退货出库
            'CC2': [self.request.fulfillment_returns_manage.self_submitted_library],  # 自提退货出库
            # 运营中心|待报价物品
            'CD1': [self.request.platform_items_to_be_specified.designated_recyclers],  # 指定供应商
            # 运营中心|物品出库
            'CE1': [self.request.fulfillment_items_are_out_of_storage.direct_shot_express_sales_out_of_the_warehouse],  # 销售出库
            # 运营中心|壹准拍机|售后管理|售后订单
            'CF1': [self.request.fulfillment_a_quasi_camera.the_direct_auction_price_difference_was_approved],  # 审核优先补差-X
            'CF2': [self.request.fulfillment_a_quasi_camera.direct_shot_return_refund_approved],  # 审核退货退款
            'CF3': [self.request.fulfillment_a_quasi_camera.to_be_received_signature_into_the_library],  # 签收入库-X
            'CF4': [self.request.fulfillment_a_quasi_camera.direct_shot_review_priority_spread],  # 审核优先补差
            'CF5': [self.request.fulfillment_a_quasi_camera.direct_shot_review_rejection],  # 复检审核拒绝
            'CF6': [self.request.fulfillment_a_quasi_camera.direct_platform_review_sign_into_the_library],  # 签收入库
            'CF7': [self.request.fulfillment_a_quasi_camera.online_review_direct_shooting_passed],  # 审核仅退差
        }
        platform = {
            # 平台管理|运营中心|待指定物品
            'DA1': [self.request.fulfillment_item_item_to_be_quoted.commodity_quotes],  # 商品报价
            # 平台管理|卖场管理|直拍卖场列表
            'DB1': [self.request.platform_list_of_direct_auction_houses.zhi_every_day_on_a_specified_date_phone, self.wait_until_next_five_minute],  # 创建指定5分钟卖场
            'DB2': [self.request.platform_list_of_direct_auction_houses.zhi_add_goods_mobile_phones],  # 添加商品上架
            'DB3': [self.request.platform_list_of_direct_auction_houses.zhi_price_priority_for_close_proximity, ],  # 创建卖场仅保存
            'DB4': [self.request.platform_list_of_direct_auction_houses.zhi_listed_status_removed_from_the_store],  # 下架
            # 平台管理|壹准拍机|售后管理|申诉管理
            'DC1': [self.request.platform_grievance_manage.direct_approved_refund],  # 审核退货退款
            'DC2': [self.request.platform_grievance_manage.direct_shooting_through_priority_supplementation],  # 审核优先补差
            # 平台管理|卖场管理|直拍卖场列表
            'DD1': [self.request.platform_list_of_dark_auction_houses.every_day_on_a_expired_phone, self.wait_until_next_five_minute],  # 创建卖场
            'DD2': [self.request.platform_list_of_dark_auction_houses.create_five_minute_auction_session, self.wait_until_next_five_minute],  # 创建指定5分钟卖场
            'DD3': [self.request.platform_list_of_dark_auction_houses.listed_status_removed_from_the_store],  # 下架
            'DD4': [self.request.platform_list_of_dark_auction_houses.add_goods_mobile_phones],  # 添加商品上架
            'DD5': [self.request.platform_list_of_dark_auction_houses.price_priority_for_close_proximity],  # 创建卖场仅保存
            # 平台管理|消息管理|消息发布列表
            'DE1': [self.request.platform_message_release_list.platform_approved],  # 平台审核通过
            # 平台管理|虚拟库存|上拍商品管理
            'DF1': [self.request.platform_auction_product_manage.select_the_session_to_add_product_confirm],  # 添加商品上架
        }
        guarantee = {
            # 保卖管理|订单列表
            'EA1': [self.request.guarantee_order_manage.quick_guarantee_item_submission],  # 快速保卖
            'EA2': [self.request.guarantee_order_manage.ship_now_by_express_sf],  # 提交发货
        }
        purchase = {
            # 商品采购|采购管理|新增采购单
            'FA1': [self.request.purchase_add.new_purchase_order_unpaid_warehouse],  # 新增采购单未付款入库
            'FA2': [self.request.purchase_add.new_purchase_order_unpaid_journey],  # 新增采购单未付款在路上
            'FA3': [self.request.purchase_add.new_purchase_order_paid_warehouse],  # 新增采购单已付款入库
            'FA4': [self.request.purchase_add.new_purchase_order_has_not_been_shipped],  # 新增采购单未付款未发货
            # 商品采购|采购管理|采购订单列表
            'FB1': [self.request.purchase_order_list.new_purchase_order_refund],  # 采购仅退款
            # 商品采购|采购管理|采购工单
            'FC1': [self.request.purchase_work_order.work_order_add],  # 新增采购工单
            'FC2': [self.request.purchase_work_order.work_order_to_start_the_task],  # 开始任务
            'FC3': [self.request.purchase_work_order.work_order_ends_the_task],  # 结束任务
            # 商品采购|采购售后管理|待接收物品
            'FD1': [self.request.purchase_goods_received.goods_received],  # 接收物品
        }
        help = {
            # 帮卖管理|帮卖上架列表
            'GA1': [self.request.help_generate_order.add_item],  # 添加物品
            'GA2': [self.request.help_generate_order.place_an_order_to_add_items_delete_the_item],  # 删除物品
            'GA3': [self.request.help_generate_order.save_the_desired_price],  # 保存期望价格
            'GA4': [self.request.help_generate_order.new_help_order],  # 帮卖下单
            'GA5': [self.request.help_generate_order.sf_express_delivery_is_easy],  # 快递易发货
            'GA6': [self.request.help_generate_order.self_dispatch],  # 自行邮寄发货
            'GA7': [self.request.help_generate_order.send_it_yourself],  # 自己送发货
            'GA8': [self.request.help_generate_order.apply_for_cancellation],  # 申请退机
            'GA9': [self.request.help_generate_order.new_guaranteed_purchase_order],  # 保卖买断下单
            'GA10': [self.request.help_generate_order.new_profit_sharing_order],  # 保卖分润下单
            'GA11': [self.request.help_generate_order.confirmation_bond],  # 确认保卖
            'GA12': [self.request.help_generate_order.apply_for_bargaining],  # 申请议价
            # 帮卖管理|帮卖来货列表
            'GB1': [self.request.help_sell_the_list_of_goods.go_to_quality],  # 去质检
            'GB2': [self.request.help_sell_the_list_of_goods.send_it_yourself_vice],  # 去退机自己送
            'GB3': [self.request.help_sell_the_list_of_goods.mail_by_yourself],  # 去退机自行邮寄
        }
        inventory = {
            # 库存管理|入库管理|物流签收入库
            'HA1': [self.request.inventory_new_item.help_sell_logistics_signature_for_receipt],  # 来货物流签收入库
            'HA2': [self.request.inventory_new_item.logistics_signature_for_receipt],  # 物流签收入库
            # 库存管理|出库管理|销售出库
            'HB1': [self.request.inventory_sale_out_warehouse.sales_out_warehouse_help_sell],  # 销售出库-来货
            'HB2': [self.request.inventory_sale_out_warehouse.sales_out_warehouse_not_received],  # 销售出库未收款
            'HB3': [self.request.inventory_sale_out_warehouse.sales_out_warehouse_received],  # 销售出库已收款
            # 库存管理|库存列表
            'HC1': [self.request.inventory_list.inventory_transfer_sell_main],  # 库存移交销售
            'HC2': [self.request.inventory_list.inventory_transfer_quality_special],  # 库存移交质检给库管
            'HC3': [self.request.inventory_list.inventory_transfer_quality_main],  # 库存移交质检
            'HC4': [self.request.inventory_list.inventory_transfer_repair_special],  # 库存移交维修给库管
            'HC5': [self.request.inventory_list.inventory_transfer_repair_main],  # 库存移交维修
            'HC6': [self.request.inventory_list.inventory_transfer_purchase_main],  # 库存移交采购售后
            'HC7': [self.request.inventory_list.inventory_transfer_purchase_special],  # 库存移交采购售后给库管
            'HC8': [self.request.inventory_list.inventory_transfer_sell_special],  # 库存移交销售给库管
            'HC9': [self.request.inventory_list.inventory_transfer_send_main],  # 库存移交送修
            'HC10': [self.request.inventory_list.inventory_transfer_send_special],  # 库存移交送修给库管
            # 库存管理|库存调拨
            'HD1': [self.request.inventory_store_transfer.new_allocation],  # 新增仓库调拨
            # 库存管理|出库管理|仅出库订单列表
            'HE1': [self.request.inventory_outbound_orders_list.create_an_outbound_only_order],  # 仅出库订单
            # 库存管理|库存盘点
            'HF1': [self.request.inventory_stock_count.completed_inventory_count],  # 新增盘点》提交盘点》完成库存盘点
            # 库存管理|出库管理|采购售后出库
            'HG1': [self.request.inventory_purchase_and_sell_out.purchase_after_sales_warehouse],  # 采购售后出库
            # 库存管理|出库管理|地址管理
            'HH1': [self.request.inventory_address_manage.add_address],  # 新增收货地址
            # 库存管理|出库管理|送修出库
            'HI1': [self.request.inventory_send_out_repair.send_out_the_warehouse],  # 送修出库
        }
        sell = {
            # 商品销售|销售售后管理|销售售后处理
            'IA1': [self.request.sell_after_sales_handling.sales_after_sales_returns],  # 销售售后退货
            'IA2': [self.request.sell_after_sales_handling.sell_returned_spare_parts_after_sale_journey_warehouse],  # 仅退配件入库
            'IA3': [self.request.sell_after_sales_handling.sell_returned_spare_parts_after_sale_journey],  # 仅退配件在路上
            # 商品销售|销售管理|销售上架
            'IB1': [self.request.sell_goods_listing.sell_goods_listing],  # 销售上架物品
            # 商品销售|销售管理|待销售物品
            'IC1': [self.request.sell_sale_item.sell_advance_sale],  # 销售预售出库
        }
        message = {
            # 消息管理|消息发布列表
            'JA1': [self.request.message_release_list.publish_the_message],  # 消息发布新消息提交审核
            'JA2': [self.request.message_release_list.release_the_review_message],  # 消息发布新消息审核通过
        }
        purse = {
            # 钱包管理|钱包中心
            'KA1': [self.request.purse_center.recharge_the_product_wallet],  # 钱包对公转账支付充值
        }
        quality = {
            # 质检管理|先质检后入库
            'LA1': [self.request.quality_store.quality_artificial_add],  # 新增人工质检数据
            # 质检管理|质检中物品
            'LB1': [self.request.quality_centre_item.submit_quality_results_by_no_transfer],  # 质检提交质检结果不移交
            # 质检管理|质检内容模版
            'LC1': [self.request.quality_content_template.new_template_added],  # 新增质检模版
        }
        repair = {
            # 维修管理|维修中物品
            'MA1': [self.request.repair_centre_item.submit_the_maintenance_results],  # 提交维修结果
            # 维修管理|维修项目列表
            'MB1': [self.request.repair_project_list.new_model_configuration],  # 新增机型配置
            # 维修管理|维修审核列表
            'MC1': [self.request.repair_audit_list.the_maintenance_audit_passed],  # 维修审核通过
        }
        send = {
            # 送修管理|已送修物品
            'NA1': [self.request.send_been_sent_repair.repair_completed_route],  # 送修完成入库
        }
        mg_guaranteed = {
            # 保卖小程序|首页
            '@AA1': [self.request.auction_index.auto_submit_new_order],  # 精确发货创建订单
            '@AA2': [self.request.auction_index.quality_inspection_service_create_an_order],  # 质检服务创建订单
            # 保卖小程序|我的
            '@AB1': [self.request.auction_my.quality_shipped_immediately_own],  # 自行邮寄发货
            '@AB2': [self.request.auction_my.express_easy_return],  # 邮寄退货
            '@AB3': [self.request.auction_my.self_pickup_returns],  # 自提退货
            '@AB4': [self.request.auction_my.sales_out_warehouse],  # 销售物品
            '@AB5': [self.request.auction_my.shipped_immediately_own],  # 自行邮寄发货-X
            '@AB6': [self.request.auction_my.shipped_immediately_sf],  # 顺丰快递发货-X
            '@AB7': [self.request.auction_my.quality_shipped_immediately_sf],  # 顺丰快递发货
            '@AB8': [self.request.auction_my.platform_cancel_the_sale],  # 取消销售
            '@AB9': [self.request.auction_my.sales_re_inspection],  # 复检
            '@AB10': [self.request.auction_my.cancel_the_return],  # 取消退货
        }
        mc_camera = {
            # 竞拍小程序|竞拍
            '@BA1': [self.request.bidding_camera.direct_auction_bidding, self.wait_for_five_minutes],  # 直拍出价
            '@BA2': [self.request.bidding_camera.bidding_offer, self.wait_for_five_minutes],  # 暗拍出价
            # 竞拍小程序|我的
            '@BB1': [self.request.bidding_my.direct_shot_confirm_receipt],  # 确认收货
            '@BB2': [self.request.bidding_my.direct_shooting_apply_for_after_sales],  # 申请售后
            '@BB3': [self.request.bidding_my.direct_shot_to_ship_by_yourself],  # 去发货自己送-X
            '@BB4': [self.request.bidding_my.direct_shooting_to_ship_logistics],  # 去发货自叫物流
            '@BB5': [self.request.bidding_my.straight_shot_i_want_to_appeal],  # 待申诉我要申诉
            '@BB6': [self.request.bidding_my.straight_shot_change_to_self_pickup],  # 改自提
            '@BB7': [self.request.bidding_my.direct_platform_review_mail_it_yourself],  # 去发货自己送
        }

        # 合并所有操作字典为一个大字典
        operations = {
            **attachment,
            **finance,
            **fulfillment,
            **platform,
            **guarantee,
            **purchase,
            **help,
            **inventory,
            **sell,
            **message,
            **purse,
            **quality,
            **repair,
            **send,
            **mg_guaranteed,
            **mc_camera
        }
        # 如果传入的是字符串，则转换为列表
        if isinstance(data, str):
            data = [data]

        # 遍历每个 key 并执行对应的操作
        for key in data:
            self.execute_operations(operations, key)
