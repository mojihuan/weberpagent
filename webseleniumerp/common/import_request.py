# coding: utf-8
import importlib

# lazy import: request.request_quality.QualityCentreItemRequest
# lazy import: request.request_quality.QualityContentTemplateRequest
# lazy import: request.request_quality.QualityGoodsReceivedRequest
# lazy import: request.request_quality.QualityStoreRequest
# lazy import: request.request_quality.QualityWaitTurnOverRequest
# lazy import: request.request_auction.AuctionIndexRequest
# lazy import: request.request_auction.AuctionMyRequest
# lazy import: request.request_purchase.PurchaseAddRequest
# lazy import: request.request_purchase.PurchaseUnsendListRequest
# lazy import: request.request_purchase.PurchaseArrivalListRequest
# lazy import: request.request_purchase.PurchaseAfterSaleListRequest
# lazy import: request.request_purchase.PurchaseAwaitAfterSaleListRequest
# lazy import: request.request_purchase.PurchaseGoodsReceivedRequest
# lazy import: request.request_purchase.PurchaseOrderListRequest
# lazy import: request.request_purchase.PurchaseSupplierManageRequest
# lazy import: request.request_purchase.PurchaseWorkOrderRequest
# lazy import: request.request_guarantee.GuaranteeReturnsManageRequest
# lazy import: request.request_guarantee.GuaranteeOrderManageRequest
# lazy import: request.request_guarantee.GuaranteeGoodsManageRequest
# lazy import: request.request_send.SendBeenSentRepairRequest
# lazy import: request.request_send.SendRepairListRequest
# lazy import: request.request_send.SendStayRepairRequest
# lazy import: request.request_bidding.BiddingCameraRequest
# lazy import: request.request_bidding.BiddingMyRequest
# lazy import: request.request_repair.RepairAuditListRequest
# lazy import: request.request_repair.RepairCentreItemRequest
# lazy import: request.request_repair.RepairProjectListRequest
# lazy import: request.request_login.LoginRequest
# lazy import: request.request_attachment.AttachmentGoodsReceivedRequest
# lazy import: request.request_attachment.AttachmentHandOverItemsRequest
# lazy import: request.request_attachment.AttachmentHandOverRecordsRequest
# lazy import: request.request_attachment.AttachmentInventoryListRequest
# lazy import: request.request_attachment.AttachmentMaintenanceRequest
# lazy import: request.request_attachment.AttachmentOldWarehouseRequest
# lazy import: request.request_attachment.AttachmentPickListsRequest
# lazy import: request.request_attachment.AttachmentPurchaseAddRequest
# lazy import: request.request_attachment.AttachmentPurchaseListRequest
# lazy import: request.request_attachment.AttachmentReceiveItemsRequest
# lazy import: request.request_attachment.AttachmentSalesListRequest
# lazy import: request.request_attachment.AttachmentSortingListRequest
# lazy import: request.request_attachment.AttachmentStockTransferRequest
# lazy import: request.request_fulfillment.FulfillmentItemItemToBeQuotedRequest
# lazy import: request.request_fulfillment.FulfillmentQualityManageRequest
# lazy import: request.request_fulfillment.FulfillmentReturnsManageRequest
# lazy import: request.request_fulfillment.FulfillmentSignIntoTheLibraryRequest
# lazy import: request.request_fulfillment.FulfillmentOrderManageRequest
# lazy import: request.request_fulfillment.FulfillmentItemsAreOutOfStorageRequest
# lazy import: request.request_fulfillment.FulfillmentAQuasiCameraRequest
# lazy import: request.request_fulfillment.FulfillmentAfterSalesReturnManageRequest
# lazy import: request.request_inventory.InventoryAddressManageRequest
# lazy import: request.request_inventory.InventoryHandOverGoodsRecordsRequest
# lazy import: request.request_inventory.InventoryHandOverGoodsRequest
# lazy import: request.request_inventory.InventoryItemSignWarehousingRequest
# lazy import: request.request_inventory.InventoryListRequest
# lazy import: request.request_inventory.InventoryLogisticsListRequest
# lazy import: request.request_inventory.InventoryNewItemRequest
# lazy import: request.request_inventory.InventoryOutboundOrdersListRequest
# lazy import: request.request_inventory.InventoryPurchaseAndSellOutRequest
# lazy import: request.request_inventory.InventoryReceiveItemRequest
# lazy import: request.request_inventory.InventorySaleOutWarehouseRequest
# lazy import: request.request_inventory.InventorySellAfterSaleDeliveryRequest
# lazy import: request.request_inventory.InventorySendOutRepairRequest
# lazy import: request.request_inventory.InventoryStockCountRequest
# lazy import: request.request_inventory.InventoryStoreTransferRequest
# lazy import: request.request_platform.PlatformAuctionProductManageRequest
# lazy import: request.request_platform.PlatformItemsToBeSpecifiedRequest
# lazy import: request.request_platform.PlatformListOfDarkAuctionHousesRequest
# lazy import: request.request_platform.PlatformListOfDirectAuctionHousesRequest
# lazy import: request.request_platform.PlatformMerchantManageRequest
# lazy import: request.request_platform.PlatformProductReviewRequest
# lazy import: request.request_platform.PlatformPurseCenterRequest
# lazy import: request.request_platform.PlatformMessageReleaseListRequest
# lazy import: request.request_platform.PlatformGrievanceManageRequest
# lazy import: request.request_message.MessageReleaseListRequest
# lazy import: request.request_help.HelpGenerateOrderRequest
# lazy import: request.request_help.HelpSellTheListOfGoodsRequest
# lazy import: request.request_help.HelpServiceConfigurationRequest
# lazy import: request.request_camera.CameraAfterSalesOrdersRequest
# lazy import: request.request_camera.AListOfAirportVisitsRequest
# lazy import: request.request_purse.PurseCenterRequest
# lazy import: request.request_sell.SellAfterSalesHandlingRequest
# lazy import: request.request_sell.SellGoodsListingRequest
# lazy import: request.request_sell.SellMiddleItemListRequest
# lazy import: request.request_sell.SellSaleItemRequest
# lazy import: request.request_sell.SellSaleOrderListRequest
# lazy import: request.request_sell.SellSaleItemListRequest
# lazy import: request.request_sell.SellCustomManageRequest
# lazy import: request.request_sell.SellStaticsRequest
# lazy import: request.request_sell.SellSalesListRequest
# lazy import: request.request_sell.SellWaitReceivedRequest
# lazy import: request.request_sell.SellingOrderListRequest
# lazy import: request.request_trafficker.TraffickerHelpRequest
# lazy import: request.request_trafficker.TraffickerInventoryRequest
# lazy import: request.request_trafficker.TraffickerPurchaseRequest
# lazy import: request.request_trafficker.TraffickerQualityRequest
# lazy import: request.request_trafficker.TraffickerRepairRequest
# lazy import: request.request_trafficker.TraffickerSellRequest
# lazy import: request.request_finance.FinanceAccountListRequest
# lazy import: request.request_finance.FinanceBillReviewRequest
# lazy import: request.request_finance.FinanceCopingWithEachOtherRequest
# lazy import: request.request_finance.FinanceCostIncomeAdjustmentRequest
# lazy import: request.request_finance.FinanceDailyDisburseRequest
# lazy import: request.request_finance.FinanceDailyIncomeRequest
# lazy import: request.request_finance.FinanceExchangesAndReceivablesRequest
# lazy import: request.request_finance.FinancePrePayReceivedRequest

class ImportRequest:
    """
    ImportApi 是一个聚合类，用于统一管理多个模块的 API 断言类。
    通过延迟加载方式按需实例化各个模块的断言类，提高性能并避免重复初始化。
    """

    # ===== 模块与API类映射表 =====
    _module_map = {
        'quality_centre_item': ('request.request_quality', 'QualityCentreItemRequest'),
        'quality_content_template': ('request.request_quality', 'QualityContentTemplateRequest'),
        'quality_goods_received': ('request.request_quality', 'QualityGoodsReceivedRequest'),
        'quality_store': ('request.request_quality', 'QualityStoreRequest'),
        'quality_wait_turn_over': ('request.request_quality', 'QualityWaitTurnOverRequest'),
        'auction_index': ('request.request_auction', 'AuctionIndexRequest'),
        'auction_my': ('request.request_auction', 'AuctionMyRequest'),
        'purchase_add': ('request.request_purchase', 'PurchaseAddRequest'),
        'purchase_unsend_list': ('request.request_purchase', 'PurchaseUnsendListRequest'),
        'purchase_arrival_list': ('request.request_purchase', 'PurchaseArrivalListRequest'),
        'purchase_after_sale_list': ('request.request_purchase', 'PurchaseAfterSaleListRequest'),
        'purchase_await_after_sale_list': ('request.request_purchase', 'PurchaseAwaitAfterSaleListRequest'),
        'purchase_goods_received': ('request.request_purchase', 'PurchaseGoodsReceivedRequest'),
        'purchase_order_list': ('request.request_purchase', 'PurchaseOrderListRequest'),
        'purchase_supplier_manage': ('request.request_purchase', 'PurchaseSupplierManageRequest'),
        'purchase_work_order': ('request.request_purchase', 'PurchaseWorkOrderRequest'),
        'guarantee_returns_manage': ('request.request_guarantee', 'GuaranteeReturnsManageRequest'),
        'guarantee_order_manage': ('request.request_guarantee', 'GuaranteeOrderManageRequest'),
        'guarantee_goods_manage': ('request.request_guarantee', 'GuaranteeGoodsManageRequest'),
        'send_been_sent_repair': ('request.request_send', 'SendBeenSentRepairRequest'),
        'send_repair_list': ('request.request_send', 'SendRepairListRequest'),
        'send_stay_repair': ('request.request_send', 'SendStayRepairRequest'),
        'bidding_camera': ('request.request_bidding', 'BiddingCameraRequest'),
        'bidding_my': ('request.request_bidding', 'BiddingMyRequest'),
        'repair_audit_list': ('request.request_repair', 'RepairAuditListRequest'),
        'repair_centre_item': ('request.request_repair', 'RepairCentreItemRequest'),
        'repair_project_list': ('request.request_repair', 'RepairProjectListRequest'),
        'login': ('request.request_login', 'LoginRequest'),
        'attachment_goods_received': ('request.request_attachment', 'AttachmentGoodsReceivedRequest'),
        'attachment_hand_over_items': ('request.request_attachment', 'AttachmentHandOverItemsRequest'),
        'attachment_hand_over_records': ('request.request_attachment', 'AttachmentHandOverRecordsRequest'),
        'attachment_inventory_list': ('request.request_attachment', 'AttachmentInventoryListRequest'),
        'attachment_maintenance': ('request.request_attachment', 'AttachmentMaintenanceRequest'),
        'attachment_old_warehouse': ('request.request_attachment', 'AttachmentOldWarehouseRequest'),
        'attachment_pick_lists': ('request.request_attachment', 'AttachmentPickListsRequest'),
        'attachment_purchase_add': ('request.request_attachment', 'AttachmentPurchaseAddRequest'),
        'attachment_purchase_list': ('request.request_attachment', 'AttachmentPurchaseListRequest'),
        'attachment_receive_items': ('request.request_attachment', 'AttachmentReceiveItemsRequest'),
        'attachment_sales_list': ('request.request_attachment', 'AttachmentSalesListRequest'),
        'attachment_sorting_list': ('request.request_attachment', 'AttachmentSortingListRequest'),
        'attachment_stock_transfer': ('request.request_attachment', 'AttachmentStockTransferRequest'),
        'fulfillment_item_item_to_be_quoted': ('request.request_fulfillment', 'FulfillmentItemItemToBeQuotedRequest'),
        'fulfillment_quality_manage': ('request.request_fulfillment', 'FulfillmentQualityManageRequest'),
        'fulfillment_returns_manage': ('request.request_fulfillment', 'FulfillmentReturnsManageRequest'),
        'fulfillment_sign_into_the_library': ('request.request_fulfillment', 'FulfillmentSignIntoTheLibraryRequest'),
        'fulfillment_order_manage': ('request.request_fulfillment', 'FulfillmentOrderManageRequest'),
        'fulfillment_items_are_out_of_storage': ('request.request_fulfillment', 'FulfillmentItemsAreOutOfStorageRequest'),
        'fulfillment_a_quasi_camera': ('request.request_fulfillment', 'FulfillmentAQuasiCameraRequest'),
        'fulfillment_after_sales_return_manage': ('request.request_fulfillment', 'FulfillmentAfterSalesReturnManageRequest'),
        'inventory_address_manage': ('request.request_inventory', 'InventoryAddressManageRequest'),
        'inventory_hand_over_goods_records': ('request.request_inventory', 'InventoryHandOverGoodsRecordsRequest'),
        'inventory_hand_over_goods': ('request.request_inventory', 'InventoryHandOverGoodsRequest'),
        'inventory_item_sign_warehousing': ('request.request_inventory', 'InventoryItemSignWarehousingRequest'),
        'inventory_list': ('request.request_inventory', 'InventoryListRequest'),
        'inventory_logistics_list': ('request.request_inventory', 'InventoryLogisticsListRequest'),
        'inventory_new_item': ('request.request_inventory', 'InventoryNewItemRequest'),
        'inventory_outbound_orders_list': ('request.request_inventory', 'InventoryOutboundOrdersListRequest'),
        'inventory_purchase_and_sell_out': ('request.request_inventory', 'InventoryPurchaseAndSellOutRequest'),
        'inventory_receive_item': ('request.request_inventory', 'InventoryReceiveItemRequest'),
        'inventory_sale_out_warehouse': ('request.request_inventory', 'InventorySaleOutWarehouseRequest'),
        'inventory_sell_after_sale_delivery': ('request.request_inventory', 'InventorySellAfterSaleDeliveryRequest'),
        'inventory_send_out_repair': ('request.request_inventory', 'InventorySendOutRepairRequest'),
        'inventory_stock_count': ('request.request_inventory', 'InventoryStockCountRequest'),
        'inventory_store_transfer': ('request.request_inventory', 'InventoryStoreTransferRequest'),
        'platform_auction_product_manage': ('request.request_platform', 'PlatformAuctionProductManageRequest'),
        'platform_items_to_be_specified': ('request.request_platform', 'PlatformItemsToBeSpecifiedRequest'),
        'platform_list_of_dark_auction_houses': ('request.request_platform', 'PlatformListOfDarkAuctionHousesRequest'),
        'platform_list_of_direct_auction_houses': ('request.request_platform', 'PlatformListOfDirectAuctionHousesRequest'),
        'platform_merchant_manage': ('request.request_platform', 'PlatformMerchantManageRequest'),
        'platform_product_review': ('request.request_platform', 'PlatformProductReviewRequest'),
        'platform_purse_center': ('request.request_platform', 'PlatformPurseCenterRequest'),
        'platform_message_release_list': ('request.request_platform', 'PlatformMessageReleaseListRequest'),
        'platform_grievance_manage': ('request.request_platform', 'PlatformGrievanceManageRequest'),
        'message_release_list': ('request.request_message', 'MessageReleaseListRequest'),
        'help_generate_order': ('request.request_help', 'HelpGenerateOrderRequest'),
        'help_sell_the_list_of_goods': ('request.request_help', 'HelpSellTheListOfGoodsRequest'),
        'help_service_configuration': ('request.request_help', 'HelpServiceConfigurationRequest'),
        'camera_after_sales_orders': ('request.request_camera', 'CameraAfterSalesOrdersRequest'),
        'a_list_of_airport_visits': ('request.request_camera', 'AListOfAirportVisitsRequest'),
        'purse_center': ('request.request_purse', 'PurseCenterRequest'),
        'sell_after_sales_handling': ('request.request_sell', 'SellAfterSalesHandlingRequest'),
        'sell_goods_listing': ('request.request_sell', 'SellGoodsListingRequest'),
        'sell_middle_item_list': ('request.request_sell', 'SellMiddleItemListRequest'),
        'sell_sale_item': ('request.request_sell', 'SellSaleItemRequest'),
        'sell_sale_order_list': ('request.request_sell', 'SellSaleOrderListRequest'),
        'sell_sale_item_list': ('request.request_sell', 'SellSaleItemListRequest'),
        'sell_custom_manage': ('request.request_sell', 'SellCustomManageRequest'),
        'sell_statics': ('request.request_sell', 'SellStaticsRequest'),
        'sell_sales_list': ('request.request_sell', 'SellSalesListRequest'),
        'sell_wait_received': ('request.request_sell', 'SellWaitReceivedRequest'),
        'selling_order_list': ('request.request_sell', 'SellingOrderListRequest'),
        'trafficker_help': ('request.request_trafficker', 'TraffickerHelpRequest'),
        'trafficker_inventory': ('request.request_trafficker', 'TraffickerInventoryRequest'),
        'trafficker_purchase': ('request.request_trafficker', 'TraffickerPurchaseRequest'),
        'trafficker_quality': ('request.request_trafficker', 'TraffickerQualityRequest'),
        'trafficker_repair': ('request.request_trafficker', 'TraffickerRepairRequest'),
        'trafficker_sell': ('request.request_trafficker', 'TraffickerSellRequest'),
        'finance_account_list': ('request.request_finance', 'FinanceAccountListRequest'),
        'finance_bill_review': ('request.request_finance', 'FinanceBillReviewRequest'),
        'finance_coping_with_each_other': ('request.request_finance', 'FinanceCopingWithEachOtherRequest'),
        'finance_cost_income_adjustment': ('request.request_finance', 'FinanceCostIncomeAdjustmentRequest'),
        'finance_daily_disburse': ('request.request_finance', 'FinanceDailyDisburseRequest'),
        'finance_daily_income': ('request.request_finance', 'FinanceDailyIncomeRequest'),
        'finance_exchanges_and_receivables': ('request.request_finance', 'FinanceExchangesAndReceivablesRequest'),
        'finance_pre_pay_received': ('request.request_finance', 'FinancePrePayReceivedRequest'),

    }

    def __init__(self):
        # 不使用 __slots__ 以避免兼容性问题
        self._initialized = {}

    def __getattr__(self, item):
        """
        动态获取模块对应的 API 实例
        :param item: 模块名
        :return: 对应的 API 实例
        """
        if item in self._module_map:
            # 检查是否已经初始化过该模块
            if item in self._initialized:
                # 如果已经初始化，则直接返回缓存的实例
                return self._initialized[item]

            module_path, class_name = self._module_map[item]
            module = importlib.import_module(module_path)
            instance_class = getattr(module, class_name)
            # 创建实例
            instance = instance_class()
            # 缓存实例，避免重复创建
            self._initialized[item] = instance
            return instance
        raise AttributeError(f"'ImportRequest' object has no attribute '{item}'")
