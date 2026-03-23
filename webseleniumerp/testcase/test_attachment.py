# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *
from config.constant import DICT_DATA
from config.user_info import INFO


class TestAttachmentGoodsReceived(BaseCase, unittest.TestCase):
    """配件管理|入库管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentGoodsReceivedRequest()
        else:
            return attachment_p.AttachmentGoodsReceivedPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0goods_received(self):
        """[接收]接收"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations(login='special')
        case.goods_received()
        res = [lambda: self.pc.attachment_receive_items_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_goods_received(self):
        """[扫码精确接收]-接收"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.scan_goods_received()
        res = [lambda: self.pc.attachment_receive_items_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_goods_received_search_item(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.goods_received_search_item()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_goods_received_assert(articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_goods_received_search_time(self):
        """[搜索]-移交时间"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.goods_received_search_time()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_goods_received_assert(articlesNo=obj)]
        self.assert_all(*res)


class TestAttachmentHandOverItems(BaseCase, unittest.TestCase):
    """配件管理|移交接收管理|移交物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentHandOverItemsRequest()
        else:
            return attachment_p.AttachmentHandOverItemsPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0hand_over_items_to_inventory(self):
        """[移交]移交库存配件"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations(login='main')
        case.hand_over_items_to_inventory()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_to_purchase(self):
        """[移交]-移交采购售后"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_items_to_purchase()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_to_sell(self):
        """[移交]-移交销售"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_items_to_sell()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_to_send(self):
        """[移交]-移交送修"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_items_to_send()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_to_repair(self):
        """[移交]-移交维修"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_items_to_repair()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_to_quality(self):
        """[移交]-移交质检"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_items_to_quality()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_different_recipients(self):
        """[移交]-移交不同接收人"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_different_recipients()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_search_item(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.hand_over_items_search_item()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_hand_over_the_list_of_items_assert(articlesNo=obj)]
        self.assert_all(*res)


class TestAttachmentHandOverRecords(BaseCase, unittest.TestCase):
    """配件管理|移交接收管理|移交记录"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentHandOverRecordsRequest()
        else:
            return attachment_p.AttachmentHandOverRecordsPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0transfer_records_export(self):
        """[导出]"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations(login='main')
        case.transfer_records_export()
        res = [lambda: self.pc.system_export_list_assert(state=2, createTime='now', name='导出配件移交单列表')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_bulk_cancel_handovers(self):
        """[批量取消移交]"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.bulk_cancel_handovers()
        res = [lambda: self.pc.attachment_handover_records_assert(statusStr='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_cancel_handovers(self):
        """[取消移交]"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.cancel_handovers()
        res = [lambda: self.pc.attachment_handover_records_assert(statusStr='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_search_item_no(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.hand_over_items_search_item_no()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_handover_records_assert(data='a', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_search_order(self):
        """[搜索]-移交单号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.hand_over_items_search_order()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_search_status(self):
        """[搜索]-移交单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1', 'AD1'])
            case = self.common_operations()
            case.hand_over_items_search_status()
            obj = cached('orderNo')
            res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj)]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AD1', 'AA1', 'AD1', 'AE1', 'AA1', 'AD1', 'AF1'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.hand_over_items_search_status(status)
                res = [lambda s=status: self.pc.attachment_handover_records_assert(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_search_name(self):
        """[搜索]-移交人"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.hand_over_items_search_name()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj, distributorName=INFO['customer_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_items_search_receive(self):
        """[搜索]-接收人"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.hand_over_items_search_receive()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj, receiveName=INFO['special_account_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('接口没请求，api还没写')
    def test_hand_over_items_search_time(self):
        """[搜索]-移交时间"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.hand_over_items_search_time()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj, createTime='now')]
        self.assert_all(*res)


class TestAttachmentInventoryList(BaseCase, unittest.TestCase):
    """配件管理|配件库存|库存列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentInventoryListRequest()
        else:
            return attachment_p.AttachmentInventoryListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0list_edit_item_info(self):
        """[物品信息编辑]"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations(login='main')
        case.list_edit_item_info()
        res = [lambda: self.pc.attachment_inventory_list_assert(brandName='华为', articlesTypeName='手机')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_item(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_item()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_suppliers(self):
        """[搜索]-供应商"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_suppliers()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, supplierName=INFO['main_supplier_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_affiliation(self):
        """[搜索]-所属人"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_affiliation()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, userName=INFO['customer_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_order_no(self):
        """[搜索]-采购单号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_order_no()
        obj = cached('purchaseNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(purchaseNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_purchaser(self):
        """[搜索]-采购人员"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_purchaser()
        obj = cached('purchaseNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(purchaseNo=obj, purchaseName=INFO['customer_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_time(self):
        """[搜索]-采购时间"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_time()
        obj = cached('purchaseNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(purchaseNo=obj, purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_class(self):
        """[搜索]-配件分类"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_class()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, accessoryTypeStr='内配类')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_status(self):
        """[搜索]-库存状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1'])
            case = self.common_operations()
            case.attachment_inventory_list_search_status()
            obj = cached('articlesNo')
            res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, inventoryStatus='2')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AD1', 'AA1', 'AD1', 'AE1', 'AA1', 'AD1', 'AF1'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.attachment_inventory_list_search_status(status)
                res = [lambda s=status: self.pc.attachment_inventory_list_assert(i=s, inventoryStatus=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_category(self):
        """[搜索]-品类"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1'])
            case = self.common_operations()
            case.attachment_inventory_list_search_category()
            obj = cached('articlesNo')
            res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, articlesTypeId='1')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AA2', 'AA3', 'AA4'])
            for type_id in DICT_DATA['f']:
                case = self.common_operations()
                case.attachment_inventory_list_search_category(type_id)
                res = [lambda s=type_id: self.pc.attachment_inventory_list_assert(j=s, articlesTypeId=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_brand_model(self):
        """[搜索]-品牌型号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_brand_model()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, articlesTypeId='1', brandId='8', modelId='18111')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_warehouse(self):
        """[搜索]-流转仓库"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_warehouse()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, warehouseName=INFO['main_warehouse_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_accessory_name(self):
        """[搜索]-配件名称"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_accessory_name()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, accessoryName='铁片')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_color(self):
        """[搜索]-配件成色"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1'])
            case = self.common_operations()
            case.attachment_inventory_list_search_color()
            obj = cached('articlesNo')
            res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, accessoryQualityStr='新配件')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AG1'])
            for color in DICT_DATA['g']:
                case = self.common_operations()
                case.attachment_inventory_list_search_color(color)
                res = [lambda s=color: self.pc.attachment_inventory_list_assert(m=s, accessoryQuality=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_serial_number(self):
        """[搜索]-配件编号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_serial_number()
        obj = cached('accessoryNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(accessoryNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('搜不到列表数据')
    def test_attachment_inventory_list_search_duration(self):
        """[搜索]-库存时长"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_inventory_list_search_duration()
        obj = cached('accessoryNo')
        res = [lambda: self.pc.attachment_inventory_list_assert(accessoryNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_inventory_list_search_channel(self):
        """[搜索]-配件渠道"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1'])
            case = self.common_operations()
            case.attachment_inventory_list_search_channel()
            obj = cached('articlesNo')
            res = [lambda: self.pc.attachment_inventory_list_assert(articlesNo=obj, channelStr='原厂')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AG1'])
            for channel in DICT_DATA['g']:
                case = self.common_operations()
                case.attachment_inventory_list_search_channel(channel)
                res = [lambda s=channel: self.pc.attachment_inventory_list_assert(a=s, channelType=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_accessory_sales_express_delivery(self):
        """[配件销售]快递易-已收款"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.accessory_sales_express_delivery()
        res = [lambda: self.pc.attachment_sales_list_assert(createTime='now', deliveryNum=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_accessory_sales(self):
        """[配件销售]-普通快递-未收款"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.accessory_sales()
        res = [lambda: self.pc.attachment_sales_list_assert(createTime='now', deliveryNum=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_transfer_items_special(self):
        """[批量移交]-移交物品给库存配件"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.transfer_items_special()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_items_purchase_after_sales(self):
        """[批量移交]-移交物品给采购售后"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.handover_items_purchase_after_sales()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_items_sell_personnel(self):
        """[批量移交]-移交物品给销售"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.handover_items_sell_personnel()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_items_send_personnel(self):
        """[批量移交]-移交物品给送修"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.handover_items_send_personnel()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_items_repair_personnel(self):
        """[批量移交]-移交物品给维修"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.handover_items_repair_personnel()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_items_quality_personnel(self):
        """[批量移交]-移交物品给质检"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.handover_items_quality_personnel()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_item_details_modify_item_information(self):
        """[物品详情]-修改物品信息"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.item_details_modify_item_information()
        res = [lambda: self.pc.attachment_inventory_list_assert(brandName='华为', articlesTypeName='手机')]
        self.assert_all(*res)


class TestAttachmentMaintenance(BaseCase, unittest.TestCase):
    """配件管理|配件维护"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentMaintenanceRequest()
        else:
            return attachment_p.AttachmentMaintenancePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0added_a_button_category_external_category(self):
        """[新增]品类外配类"""
        case = self.common_operations(login='idle')
        case.added_a_button_category_external_category()
        res = [lambda: self.pc.attachment_maintenance_assert(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_added_a_button_category_matching(self):
        """[新增]品类内配类"""
        case = self.common_operations()
        case.added_a_button_category_matching()
        res = [lambda: self.pc.attachment_maintenance_assert(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_modify_the_accessory_name(self):
        """[编辑]修改配件名称"""
        case = self.common_operations()
        case.modify_the_accessory_name()
        res = [lambda: self.pc.attachment_maintenance_assert(headers='idle', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delete_the_accessory_name(self):
        """[编辑]删除配件名称"""
        self.pre.operations(data=['AH1'])
        case = self.common_operations()
        case.delete_the_accessory_name()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_maintenance_search_num(self):
        """[搜索]-配件编号"""
        self.pre.operations(data=['AH1'])
        case = self.common_operations()
        case.attachment_maintenance_search_num()
        obj = cached('accessoryNo')
        res = [lambda: self.pc.attachment_maintenance_assert(headers='idle', accessoryNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_maintenance_search_name(self):
        """[搜索]-配件名称"""
        self.pre.operations(data=['AH1'])
        case = self.common_operations()
        case.attachment_maintenance_search_name()
        obj = cached('accessoryName')
        res = [lambda: self.pc.attachment_maintenance_assert(headers='idle', accessoryName=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_maintenance_search_status(self):
        """[搜索]-状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AH1'])
            case = self.common_operations()
            case.attachment_maintenance_search_status()
            obj = cached('accessoryName')
            res = [lambda: self.pc.attachment_maintenance_assert(headers='idle', accessoryName=obj, status='1')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AH1', 'AH2'])
            for status in DICT_DATA['h']:
                case = self.common_operations()
                case.attachment_maintenance_search_status(status)
                res = [lambda s=status: self.pc.attachment_maintenance_assert(headers='idle', i=s, status=s)]
                self.assert_all(*res)


class TestAttachmentOldWarehouse(BaseCase, unittest.TestCase):
    """配件管理|入库管理|旧配件入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentOldWarehouseRequest()
        else:
            return attachment_p.AttachmentOldWarehousePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0phone_old_attachment_warehouse(self):
        """[新建入库]手机-确认入库"""
        case = self.common_operations(login='main')
        case.phone_old_attachment_warehouse()
        res = [lambda: self.pc.attachment_old_warehouse_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_thousand_phone_old_attachment_warehouse(self):
        """[新建入库]1000个数量手机-确认入库"""
        case = self.common_operations()
        case.thousand_phone_old_attachment_warehouse()
        res = [lambda: self.pc.attachment_old_warehouse_assert(accessoryNum=1000, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ipa_old_attachment_warehouse(self):
        """[新建入库]平板电脑-确认入库"""
        case = self.common_operations()
        case.ipa_old_attachment_warehouse()
        res = [lambda: self.pc.attachment_old_warehouse_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_notebook_old_attachment_warehouse(self):
        """[新建入库]笔记本电脑-确认入库"""
        case = self.common_operations()
        case.notebook_old_attachment_warehouse()
        res = [lambda: self.pc.attachment_old_warehouse_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_smartwatches_old_attachment_warehouse(self):
        """[新建入库]智能手表-确认入库"""
        case = self.common_operations()
        case.smartwatches_old_attachment_warehouse()
        res = [lambda: self.pc.attachment_old_warehouse_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_old_warehouse_search_item(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['AG1'])
        case = self.common_operations()
        case.attachment_old_warehouse_search_item()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_old_warehouse_assert(data='a', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_old_warehouse_search_order(self):
        """[搜索]-入库单号"""
        self.pre.operations(data=['AG1'])
        case = self.common_operations()
        case.attachment_old_warehouse_search_order()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_old_warehouse_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_old_warehouse_search_warehouse(self):
        """[搜索]-流转仓库"""
        self.pre.operations(data=['AG1'])
        case = self.common_operations()
        case.attachment_old_warehouse_search_warehouse()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_old_warehouse_assert(orderNo=obj, warehouseId=INFO['main_in_warehouse_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_old_warehouse_search_user(self):
        """[搜索]-入库人"""
        self.pre.operations(data=['AG1'])
        case = self.common_operations()
        case.attachment_old_warehouse_search_user()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_old_warehouse_assert(orderNo=obj, userId=INFO['special_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_old_warehouse_search_time(self):
        """[搜索]-入库时间"""
        self.pre.operations(data=['AG1'])
        case = self.common_operations()
        case.attachment_old_warehouse_search_time()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_old_warehouse_assert(orderNo=obj, createTime='now')]
        self.assert_all(*res)


class TestAttachmentPickLists(BaseCase, unittest.TestCase):
    """配件管理|入库管理|分拣列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentPickListsRequest()
        else:
            return attachment_p.AttachmentPickListsPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_attachment_pick_lists_export_all(self):
        """[导出全部]"""
        case = self.common_operations(login='main')
        case.attachment_pick_lists_export_all()
        res = [lambda: self.pc.system_export_list_assert(state=2, createTime='now', name='待分拣列表数据导出')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_pick_lists_search_logistics(self):
        """[搜索]-快递单号"""
        self.pre.operations(data=['AA2'])
        case = self.common_operations()
        case.attachment_pick_lists_search_logistics()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.attachment_sorting_list_assert(logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_pick_lists_search_item(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['AA2'])
        case = self.common_operations()
        case.attachment_pick_lists_search_item()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_new_arrival_assert(articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_pick_lists_search_business(self):
        """[搜索]-业务单号"""
        self.pre.operations(data=['AA2'])
        case = self.common_operations()
        case.attachment_pick_lists_search_business()
        obj = cached('businessNo')
        res = [lambda: self.pc.attachment_new_arrival_assert(businessNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_pick_lists_search_status(self):
        """[搜索]-分拣状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA2'])
            case = self.common_operations()
            case.attachment_pick_lists_search_status()
            obj = cached('logisticsNo')
            res = [lambda: self.pc.attachment_sorting_list_assert(logisticsNo=obj, status='1')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA2', 'AA2', 'AI1'])
            for status in DICT_DATA['g']:
                case = self.common_operations()
                case.attachment_pick_lists_search_status(status)
                res = [lambda s=status: self.pc.attachment_sorting_list_assert(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_pick_lists_search_time(self):
        """[搜索]-分拣时间"""
        self.pre.operations(data=['AA2', 'AI1'])
        case = self.common_operations()
        case.attachment_pick_lists_search_time()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.attachment_new_arrival_assert(logisticsNo=obj, sortationTime='now')]
        self.assert_all(*res)


class TestAttachmentPurchaseAdd(BaseCase, unittest.TestCase):
    """配件管理|配件采购|新增采购单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentPurchaseAddRequest()
        else:
            return attachment_p.AttachmentPurchaseAddPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_purchase_order_route(self):
        """[新增]平板电脑-已付款在路上-确定生成采购单"""
        case = self.common_operations(login='main')
        case.new_purchase_order_route()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已发货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_purchase_order_warehousing(self):
        """[新增]手机-未付款已到货-确定生成采购单"""
        case = self.common_operations()
        case.new_purchase_order_warehousing()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已收货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_added_purchase_order_unpaid_in_transit(self):
        """[新增]笔记本电脑-未付款在路上-确定生成采购单"""
        case = self.common_operations()
        case.added_purchase_order_unpaid_in_transit()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已发货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_new_purchase_order_payment(self):
        """[新增]智能手表-已付款已到货-确定生成采购单"""
        case = self.common_operations()
        case.attachment_new_purchase_order_payment()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已收货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_generate_purchase_orders_in_bulk(self):
        """[新增]手机1000个物品-确定生成采购单"""
        case = self.common_operations()
        case.generate_purchase_orders_in_bulk()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已收货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_purchase_orders_in_bulk(self):
        """[新增]批量添加-确定生成采购单"""
        case = self.common_operations()
        case.add_purchase_orders_in_bulk()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已发货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_purchase_orders_in_bulk(self):
        """[新增]批量添加-确定生成采购单"""
        case = self.common_operations()
        case.add_purchase_orders_in_bulk()
        res = [lambda: self.pc.attachment_purchase_list_assert(stateStr='已发货', purchaseTime='now')]
        self.assert_all(*res)


class TestAttachmentPurchaseList(BaseCase, unittest.TestCase):
    """配件管理|配件采购|采购列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentPurchaseListRequest()
        else:
            return attachment_p.AttachmentPurchaseListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0refund_after_purchase_express(self):
        """[采购售后]快递易-采购退货退款"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations(login='main')
        case.refund_after_purchase_express()
        res = [lambda: self.pc.attachment_purchase_sales_list_assert(saleStateStr='采购退货退款', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_refund_after_purchase(self):
        """[采购售后]普通快递-采购退货退款"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.refund_after_purchase()
        res = [lambda: self.pc.attachment_purchase_sales_list_assert(saleStateStr='采购退货退款', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_sale_refund(self):
        """[采购售后]部分金额退差价"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.purchase_sale_refund()
        res = [lambda: self.pc.attachment_purchase_sales_list_assert(saleStateStr='采购退差价', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_refund_after_purchase_add_item(self):
        """[采购售后]-添加物品退货退款"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.refund_after_purchase_add_item()
        res = [lambda: self.pc.attachment_purchase_sales_list_assert(saleStateStr='采购退货退款', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_all_amount_refund_difference(self):
        """[采购售后]-全部金额退差价"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.all_amount_refund_difference()
        res = [lambda: self.pc.attachment_purchase_sales_list_assert(saleStateStr='采购退差价', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_details_of_the_spare_parts_purchase_list(self):
        """[采购单详情]-查看"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.details_of_the_spare_parts_purchase_list()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_purchase_list_assert(data='a', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_order(self):
        """[搜索]-采购单号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_purchase_list_search_order()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_purchase_list_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_suppliers(self):
        """[搜索]-采购供应商"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_purchase_list_search_suppliers()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_purchase_list_assert(orderNo=obj, supplierId=INFO['main_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_status(self):
        """[搜索]-采购单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1'])
            case = self.common_operations()
            case.attachment_purchase_list_search_status()
            obj = cached('orderNo')
            res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj, stateStr='已发货')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AA2'])
            for state in DICT_DATA['i']:
                case = self.common_operations()
                case.attachment_purchase_list_search_status(state)
                res = [lambda s=state: self.pc.attachment_purchase_list_assert(i=s, state=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_logistics(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_purchase_list_search_logistics()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.attachment_purchase_list_assert(logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_payment(self):
        """[搜索]-付款状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1'])
            case = self.common_operations()
            case.attachment_purchase_list_search_payment()
            obj = cached('orderNo')
            res = [lambda: self.pc.attachment_handover_records_assert(orderNo=obj, payStateStr='已付款')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AA2'])
            for pay in DICT_DATA['g']:
                case = self.common_operations()
                case.attachment_purchase_list_search_payment(pay)
                res = [lambda s=pay: self.pc.attachment_purchase_list_assert(j=s, payState=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_people(self):
        """[搜索]-采购人"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_purchase_list_search_people()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_purchase_list_assert(orderNo=obj, userId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_purchase_list_search_time(self):
        """[搜索]-采购时间"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.attachment_purchase_list_search_time()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_purchase_list_assert(orderNo=obj, purchaseTime='now')]
        self.assert_all(*res)


class TestAttachmentReceiveItem(BaseCase, unittest.TestCase):
    """配件管理|移交接收管理|接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentReceiveItemsRequest()
        else:
            return attachment_p.AttachmentReceiveItemsPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0item_inventory_accessory_item_receipt(self):
        """[物品接收]-移交库存配件-接收"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations(login='main')
        case.item_inventory_accessory_item_receipt()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='已接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_the_code_to_receive_accurately(self):
        """[物品接收]-扫码精确接收"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.scan_the_code_to_receive_accurately()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='已接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_orders_received_in_batches(self):
        """[移交单接收]-接收"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.handover_orders_received_in_batches()
        res = [lambda: self.pc.attachment_handover_records_assert(createTime='now', statusStr='已接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_export(self):
        """[移交单接收]-导出"""
        case = self.common_operations()
        case.handover_export()
        res = [lambda: self.pc.system_export_list_assert(state=2, createTime='now', name='导出接收单列表')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_item(self):
        """[搜索]-物品接收-物品编号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_item()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_category(self):
        """[搜索]-物品接收-品类品牌型号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_category()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', articlesNo=obj, brandName='华为', articlesTypeName='手机', modelName='Pocket 2 优享版')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_person(self):
        """[搜索]-物品接收-移交人"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_person()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', articlesNo=obj, deliveryId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_accept(self):
        """[搜索]-物品接收-接收人"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_accept()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', articlesNo=obj, userId=INFO['special_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_time(self):
        """[搜索]-物品接收-移交时间"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_time()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', articlesNo=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_order(self):
        """[搜索]-物品接收-移交单号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_order()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_item_no(self):
        """[搜索]-移交单接收-物品编号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_item_no()
        obj = cached('articlesNo')
        res = [lambda: self.pc.attachment_receive_items_assert(data='a', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_order_no(self):
        """[搜索]-移交单接收-移交单号"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_order_no()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_receive_items_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_status(self):
        """[搜索]-移交单接收-移交单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1', 'AD1'])
            case = self.common_operations()
            case.attachment_receive_item_search_status()
            obj = cached('orderNo')
            res = [lambda: self.pc.attachment_receive_items_assert(orderNo=obj, statusStr='待接收')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AD1', 'AA1', 'AD1', 'AE1', 'AA1', 'AD1', 'AF1'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.attachment_receive_item_search_status(status)
                res = [lambda s=status: self.pc.attachment_receive_items_assert(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_transfer_person(self):
        """[搜索]-移交单接收-移交人"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_transfer_person()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_receive_items_assert(orderNo=obj, distributorId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_recipient(self):
        """[搜索]-移交单接收-接收人"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_recipient()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_receive_items_assert(orderNo=obj, userId=INFO['special_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_receive_item_search_transfer_time(self):
        """[搜索]-移交单接收-移交时间"""
        self.pre.operations(data=['AA1', 'AD1'])
        case = self.common_operations()
        case.attachment_receive_item_search_transfer_time()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_receive_items_assert(orderNo=obj, createTime='now')]
        self.assert_all(*res)


class TestAttachmentSalesList(BaseCase, unittest.TestCase):
    """配件管理|配件销售|销售列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentSalesListRequest()
        else:
            return attachment_p.AttachmentSalesListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0accessory_sales_express_easy(self):
        """[配件销售]快递易-未收款-部分销售金额"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations(login='main')
        case.accessory_sales_express_easy()
        res = [lambda: self.pc.attachment_sales_list_assert(createTime='now', status=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_accessory_sales_express_easy_maximum(self):
        """[配件销售]快递易-未收款-销售金额最大值"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.accessory_sales_express_easy_maximum()
        res = [lambda: self.pc.attachment_sales_list_assert(createTime='now', status=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uncollected_partial_sales_amount(self):
        """[配件销售]普通物流-未收款-部分销售金额"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.uncollected_partial_sales_amount()
        res = [lambda: self.pc.attachment_sales_list_assert(createTime='now', status=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_accessories_sales_express_received_payment(self):
        """[配件销售]-普通快递-已收款"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.accessories_sales_express_received_payment()
        res = [lambda: self.pc.attachment_sales_list_assert(createTime='now', status=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_after_sale_refund_not_received(self):
        """[销售售后]-退货退款-未收货"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.sales_after_sale_refund_not_received()
        res = [lambda: self.pc.attachment_after_sales_list_assert(createTime='now', status=2)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_after_sale_refund_warehouse(self):
        """[销售售后]-退货退款-已收货"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.sales_after_sale_refund_warehouse()
        res = [lambda: self.pc.attachment_after_sales_list_assert(createTime='now', status=2)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_after_refund_the_price_difference(self):
        """[销售售后]-部分金额退差价"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.sales_after_refund_the_price_difference()
        res = [lambda: self.pc.attachment_after_sales_list_assert(createTime='now', status=2)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_full_amount_will_be_refunded_the_difference(self):
        """[销售售后]-全部金额退差价"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.the_full_amount_will_be_refunded_the_difference()
        res = [lambda: self.pc.attachment_after_sales_list_assert(createTime='now', status=2)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_sales_list_search_order(self):
        """[搜索]-销售单号"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.attachment_sales_list_search_order()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_sales_list_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_sales_list_search_customer(self):
        """[搜索]-客户"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.attachment_sales_list_search_customer()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_sales_list_assert(orderNo=obj, saleSupplierId=INFO['main_sale_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_sales_list_search_status(self):
        """[搜索]-收款状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['AA1', 'AB1'])
            case = self.common_operations()
            case.attachment_sales_list_search_status()
            obj = cached('orderNo')
            res = [lambda: self.pc.attachment_sales_list_assert(orderNo=obj, statusStr='已收款')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['AA1', 'AB1', 'AA1', 'AB2'])
            for status in DICT_DATA['g']:
                case = self.common_operations()
                case.attachment_sales_list_search_status(status)
                res = [lambda s=status: self.pc.attachment_sales_list_assert(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_attachment_sales_list_search_logistics(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.attachment_sales_list_search_logistics()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.attachment_sales_list_assert(logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('没调接口，ui和接口还没写')
    def test_attachment_sales_list_search_time(self):
        """[搜索]-操作时间"""
        self.pre.operations(data=['AA1', 'AB1'])
        case = self.common_operations()
        case.attachment_sales_list_search_time()
        obj = cached('orderNo')
        res = [lambda: self.pc.attachment_sales_list_assert(orderNo=obj)]
        self.assert_all(*res)


@unittest.skip('未完成')
class TestAttachmentSortingList(BaseCase, unittest.TestCase):
    """配件管理|入库管理|新到货入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentSortingListRequest()
        else:
            return attachment_p.AttachmentSortingListPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_0search_for_express_sign_in_warehouse(self):
        """[签收入库]-搜索物流单号-暂不操作"""
        self.pre.operations(data=['AA2'])
        case = self.common_operations(login='main')
        case.search_for_express_sign_in_warehouse()
        res = [lambda: self.pc.attachment_sorting_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)  # 配件管理|入库管理|分拣列表

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_search_for_tracking_number_inbound_and_handover(self):
        """[签收入库]-搜索物流单号-入库并移交"""
        self.pre.operations(data=['AA2'])
        case = self.common_operations()
        case.search_for_tracking_number_inbound_and_handover()
        res = [lambda: self.pc.attachment_sorting_list_assert(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)  # 配件管理|入库管理|分拣列表


@unittest.skip('未完成')
class TestAttachmentStockTransfer(BaseCase, unittest.TestCase):
    """配件管理|配件库存|库存调拨"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.AttachmentStockTransferRequest()
        else:
            return attachment_p.AttachmentStockTransferPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_express_is_easy_new_allocation(self):
        """[新增调拨]快递易-搜索添加物品"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations(login='main')
        case.express_is_easy_new_allocation()
        res = [lambda: self.pc.attachment_warehouse_allocation_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)  # 配件管理|配件库存|库存调拨

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_0import_new_allocation(self):
        """[新增调拨]-导入添加物品"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.import_new_allocation()
        res = [lambda: self.pc.attachment_warehouse_allocation_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)  # 配件管理|配件库存|库存调拨

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_select_add_item_transfer(self):
        """[新增调拨]-选择添加物品"""
        self.pre.operations(data=['AA1'])
        case = self.common_operations()
        case.select_add_item_transfer()
        res = [lambda: self.pc.attachment_warehouse_allocation_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)  # 配件管理|配件库存|库存调拨

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_receive(self):
        """[接收]"""
        self.pre.operations(data=['AA1', 'AC1'])
        case = self.common_operations()
        case.receive()
        res = [lambda: self.pc.attachment_warehouse_allocation_assert(statusStr='已完成', createTime='now')]
        self.assert_all(*res)  # 配件管理|配件库存|库存调拨

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_item_receive_inbound(self):
        """[扫码接收]-添加物品-接收入库"""
        self.pre.operations(data=['AA1', 'AC1'])
        case = self.common_operations()
        case.add_item_receive_inbound()
        res = [lambda: self.pc.attachment_warehouse_allocation_assert(statusStr='已完成', createTime='now')]
        self.assert_all(*res)  # 配件管理|配件库存|库存调拨

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_revoke(self):
        """[撤销]"""
        self.pre.operations(data=['AA1', 'AC1'])
        case = self.common_operations()
        case.revoke()
        res = [lambda: self.pc.attachment_warehouse_allocation_assert(statusStr='已撤销', createTime='now')]
        self.assert_all(*res)  # 配件管理|配件库存|库存调拨

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_export_data(self):
        """[导出]"""
        case = self.common_operations()
        case.export_data()
        res = [lambda: self.pc.system_export_list_assert(state=2, createTime='now', name='配件调拨导出')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
