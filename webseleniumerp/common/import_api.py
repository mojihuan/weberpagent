# coding: utf-8
import importlib

# lazy import: api.api_purse.PurseWalletCenterApi
# lazy import: api.api_purse.PurseWalletOrderListApi
# lazy import: api.api_quotation.QuotationBaseListApi
# lazy import: api.api_quotation.QuotationConfigurationApi
# lazy import: api.api_quotation.QuotationMyListApi
# lazy import: api.api_quotation.QuotationRecordsListApi
# lazy import: api.api_camera.CameraAfterSalesOrderApi
# lazy import: api.api_camera.CameraListOfAirportVisitsApi
# lazy import: api.api_finance.FinanceAccountListApi
# lazy import: api.api_finance.FinanceAnalyzeApi
# lazy import: api.api_finance.FinanceBillReviewApi
# lazy import: api.api_finance.FinanceCollectionAndSettlementApi
# lazy import: api.api_finance.FinanceCommissionPaySettingApi
# lazy import: api.api_finance.FinanceCommissionSettingApi
# lazy import: api.api_finance.FinanceCopingWithEachOtherApi
# lazy import: api.api_finance.FinanceCostIncomeAdjustmentApi
# lazy import: api.api_finance.FinanceCustomerPaySettingApi
# lazy import: api.api_finance.FinanceDailyExpenditureApi
# lazy import: api.api_finance.FinanceDailyIncomeApi
# lazy import: api.api_finance.FinanceExchangesAndReceivablesApi
# lazy import: api.api_finance.FinanceFeeSettingApi
# lazy import: api.api_finance.FinancePaymentSettlementApi
# lazy import: api.api_finance.FinancePrepayReceiveListApi
# lazy import: api.api_finance.FinanceSupplierSettingApi
# lazy import: api.api_finance.FinanceTransactionDetailsApi
# lazy import: api.api_fulfillment.FulfillmentItemsToBeQuotedApi
# lazy import: api.api_fulfillment.FulfillmentOrderManageApi
# lazy import: api.api_fulfillment.FulfillmentQualityManageApi
# lazy import: api.api_fulfillment.FulfillmentReturnsManageApi
# lazy import: api.api_fulfillment.FulfillmentSignIntoTheLibraryApi
# lazy import: api.api_fulfillment.FulfillmentSellGoodsTransactionsApi
# lazy import: api.api_fulfillment.FulfillmentBotOrderApi
# lazy import: api.api_fulfillment.FulfillmentVirtualListApi
# lazy import: api.api_fulfillment.FulfillmentSalesAndShipmentManageApi
# lazy import: api.api_fulfillment.FulfillmentItemsAreOutOfStorageApi
# lazy import: api.api_fulfillment.FulfillmentCameraAfterSalesOrderApi
# lazy import: api.api_fulfillment.FulfillmentAfterSalesReturnManageApi
# lazy import: api.api_guarantee.GuaranteeOrderManageApi
# lazy import: api.api_guarantee.GuaranteeReturnsManageApi
# lazy import: api.api_guarantee.GuaranteeGoodsManageApi
# lazy import: api.api_index.IndexStaticsApi
# lazy import: api.api_index.UserInfoApi
# lazy import: api.api_trafficker.TraffickerIndexApi
# lazy import: api.api_trafficker.TraffickerStaticsApi
# lazy import: api.api_message.MessageCenterApi
# lazy import: api.api_message.MessageReleaseListApi
# lazy import: api.api_sell.SellAfterSalesListApi
# lazy import: api.api_sell.SellCustomersManageApi
# lazy import: api.api_sell.SellGoodsReceivedApi
# lazy import: api.api_sell.SellItemsForSaleApi
# lazy import: api.api_sell.SellListOfItemsForSaleApi
# lazy import: api.api_sell.SellOrderListForSaleApi
# lazy import: api.api_sell.SellSaleItemListApi
# lazy import: api.api_sell.SellSoldOrderApi
# lazy import: api.api_sell.SellStaticsApi
# lazy import: api.api_platform.PlatformVirtualInventoryListApi
# lazy import: api.api_platform.PlatformAuctionProductManageApi
# lazy import: api.api_platform.PlatformAuctionBusinessSettingsApi
# lazy import: api.api_platform.PlatformExpenseConfigApi
# lazy import: api.api_platform.PlatformMarginAllocationApi
# lazy import: api.api_platform.PlatformYzAuctionApi
# lazy import: api.api_platform.PlatformGrievanceManageApi
# lazy import: api.api_platform.PlatformAfterSalesReturnManageApi
# lazy import: api.api_platform.PlatformAftermarketAttributesApi
# lazy import: api.api_platform.PlatformDistributionApi
# lazy import: api.api_platform.PlatformDistributionOrdersApi
# lazy import: api.api_platform.PlatformDistributionRolesApi
# lazy import: api.api_platform.PlatformHelpSellConfigApi
# lazy import: api.api_platform.PlatformHelpSellListApi
# lazy import: api.api_platform.PlatformItemsOrdersManagementApi
# lazy import: api.api_platform.PlatformItemsReturnsManagementApi
# lazy import: api.api_platform.PlatformItemsToBeSpecifiedApi
# lazy import: api.api_platform.PlatformItemsRuleManagementApi
# lazy import: api.api_platform.PlatformListOfDarkAuctionHousesApi
# lazy import: api.api_platform.PlatformListOfDirectAuctionHousesApi
# lazy import: api.api_platform.PlatformSalesLookBoardDataApi
# lazy import: api.api_platform.PlatformLogisticsConfigApi
# lazy import: api.api_platform.PlatformLogisticsOrdersListApi
# lazy import: api.api_platform.PlatformMessageReleaseListApi
# lazy import: api.api_platform.PlatformIntensityFiveGoodsApi
# lazy import: api.api_platform.PlatformOrderReviewApi
# lazy import: api.api_platform.PlatformOrderListApi
# lazy import: api.api_platform.PlatformProductManageApi
# lazy import: api.api_platform.PlatformProductReviewApi
# lazy import: api.api_platform.PlatformPurchaseManageApi
# lazy import: api.api_platform.PlatformQuotationApi
# lazy import: api.api_platform.PlatformQuotationCalculateApi
# lazy import: api.api_platform.PlatformQuotationDeductionApi
# lazy import: api.api_platform.PlatformQuotationLevelApi
# lazy import: api.api_platform.PlatformQuotationQualityApi
# lazy import: api.api_platform.PlatformQuotationMenuApi
# lazy import: api.api_platform.PlatformQuotationRecordsApi
# lazy import: api.api_platform.PlatformQuotationRecycleApi
# lazy import: api.api_platform.PlatformSoldAccountsApi
# lazy import: api.api_platform.PlatformSoldDwGoodsApi
# lazy import: api.api_platform.PlatformSoldDwOrdersApi
# lazy import: api.api_platform.PlatformSoldDwRebackApi
# lazy import: api.api_platform.PlatformSoldDwSalesApi
# lazy import: api.api_platform.PlatformSoldFeeApi
# lazy import: api.api_platform.PlatformSoldLogisticsApi
# lazy import: api.api_platform.PlatformSoldMerchantFeeApi
# lazy import: api.api_platform.PlatformSoldNinetyFiveOrdersApi
# lazy import: api.api_platform.PlatformSoldNinetyFiveSalesApi
# lazy import: api.api_platform.PlatformSoldPayoutOrdersApi
# lazy import: api.api_platform.PlatformSoldQualityRecordsApi
# lazy import: api.api_platform.PlatformSoldSendAddressApi
# lazy import: api.api_platform.PlatformSoldSmsListApi
# lazy import: api.api_platform.PlatformSoldXianYuOrdersApi
# lazy import: api.api_platform.PlatformWalletConfigApi
# lazy import: api.api_platform.PlatformXianYuGoodsApi
# lazy import: api.api_platform.PlatformXianYuOrdersApi
# lazy import: api.api_platform.PlatformXianYuSalesApi
# lazy import: api.api_platform.PlatformYzAppApi
# lazy import: api.api_platform.PlatformsBannerConfigApi
# lazy import: api.api_platform.PlatformsImListApi
# lazy import: api.api_platform.PlatformsMerchantApi
# lazy import: api.api_platform.PlatformsOrdersApi
# lazy import: api.api_platform.PlatformRecycleMerchantsApi
# lazy import: api.api_platform.PlatformServiceFeeApi
# lazy import: api.api_platform.PlatformSignReceiveApi
# lazy import: api.api_platform.PlatformInspectionCenterManageApi
# lazy import: api.api_platform.PlatformGuaranteedSalePriceListApi
# lazy import: api.api_platform.PlatformSuShouSalePriceListApi
# lazy import: api.api_platform.PlatformModelPriceTemplateApi
# lazy import: api.api_platform.PlatformFranchiseesReleaseRecordsApi
# lazy import: api.api_platform.PlatformPlatformReleaseRecordApi
# lazy import: api.api_platform.PlatformGuaranteeSaleCalculationRulesApi
# lazy import: api.api_platform.PlatformGuaranteeSalesAndDeductionManageApi
# lazy import: api.api_platform.PlatformTradingGoodsCenterManageApi
# lazy import: api.api_detect.DetectCustomDetectionApi
# lazy import: api.api_detect.DetectListOfModelsApi
# lazy import: api.api_detect.DetectInspectionManageApi
# lazy import: api.api_detect.DetectQualityOrdersListApi
# lazy import: api.api_detect.DetectQualityReportExportedApi
# lazy import: api.api_help.HelpGenerateOrderApi
# lazy import: api.api_help.HelpSellTheListOfGoodsApi
# lazy import: api.api_help.HelpServiceConfigurationApi
# lazy import: api.api_bidding.BiddingCameraApi
# lazy import: api.api_bidding.BiddingMyApi
# lazy import: api.api_repair.RepairItemsApi
# lazy import: api.api_repair.RepairListApi
# lazy import: api.api_repair.RepairPartsManageApi
# lazy import: api.api_repair.RepairProjectListApi
# lazy import: api.api_repair.RepairReceiveApi
# lazy import: api.api_repair.RepairReviewListApi
# lazy import: api.api_repair.RepairStaticsListApi
# lazy import: api.api_system.SystemMessageReceptionManageApi
# lazy import: api.api_system.SystemApiLogManageApi
# lazy import: api.api_system.SystemDeptManageApi
# lazy import: api.api_system.SystemBaseImportManageApi
# lazy import: api.api_system.SystemDictManageApi
# lazy import: api.api_system.SystemDispositionListApi
# lazy import: api.api_system.SystemExportListApi
# lazy import: api.api_system.SystemGeneralConfigApi
# lazy import: api.api_system.SystemInterfaceLogApi
# lazy import: api.api_system.SystemInterfaceManageApi
# lazy import: api.api_system.SystemInternationalConfigManageApi
# lazy import: api.api_system.SystemKeyConfigManageApi
# lazy import: api.api_system.SystemLogManageApi
# lazy import: api.api_system.SystemMenuManageApi
# lazy import: api.api_system.SystemNoticeManageApi
# lazy import: api.api_system.SystemParametersSettingManageApi
# lazy import: api.api_system.SystemPostManageApi
# lazy import: api.api_system.SystemPrintTemplateConfigApi
# lazy import: api.api_system.SystemQualityBarcodeConfigApi
# lazy import: api.api_system.SystemQualityPrintConfigApi
# lazy import: api.api_system.SystemQueryManageApi
# lazy import: api.api_system.SystemRoleManageApi
# lazy import: api.api_system.SystemThirdPartyAccountsManageApi
# lazy import: api.api_system.SystemUserManageApi
# lazy import: api.api_system.SystemWarehouseManageApi
# lazy import: api.api_system.SystemWorkOrderSettingApi
# lazy import: api.api_system.SystemPriceCalculationLogApi
# lazy import: api.api_system.SystemPermissionListApi
# lazy import: api.api_mall.MallAftermarketListApi
# lazy import: api.api_mall.MallBranchManageApi
# lazy import: api.api_mall.MallCommodityManageApi
# lazy import: api.api_purchase.PurchaseAfterSalesListApi
# lazy import: api.api_purchase.PurchaseArrivalNoticesApi
# lazy import: api.api_purchase.PurchaseItemsToBeReceivedApi
# lazy import: api.api_purchase.PurchaseLyArrivalApi
# lazy import: api.api_purchase.PurchaseOrderListApi
# lazy import: api.api_purchase.PurchasePostSaleListApi
# lazy import: api.api_purchase.PurchaseSupplierManageApi
# lazy import: api.api_purchase.PurchaseTaskListApi
# lazy import: api.api_purchase.PurchaseUnShippedOrderListApi
# lazy import: api.api_purchase.PurchaseWorkOrderApi
# lazy import: api.api_sold.SoldListOfXianYuOrdersApi
# lazy import: api.api_sold.SoldListOfXianYuProductsApi
# lazy import: api.api_sold.SoldListOfXianYuSalesApi
# lazy import: api.api_sold.SoldNinetyFiveItemListApi
# lazy import: api.api_sold.SoldNinetyFiveOrdersListApi
# lazy import: api.api_sold.SoldNinetyFiveRebackListApi
# lazy import: api.api_sold.SoldNinetyFiveSalesListApi
# lazy import: api.api_attachment.AttachmentAfterSalesListApi
# lazy import: api.api_attachment.AttachmentGiftDetailsApi
# lazy import: api.api_attachment.AttachmentGoodsReceivedApi
# lazy import: api.api_attachment.AttachmentHandoverRecordsApi
# lazy import: api.api_attachment.AttachmentInventoryDetailsApi
# lazy import: api.api_attachment.AttachmentInventoryListApi
# lazy import: api.api_attachment.AttachmentMaintenanceApi
# lazy import: api.api_attachment.AttachmentNewArrivalApi
# lazy import: api.api_attachment.AttachmentOldWarehouseApi
# lazy import: api.api_attachment.AttachmentPurchaseListApi
# lazy import: api.api_attachment.AttachmentPurchaseSalesListApi
# lazy import: api.api_attachment.AttachmentReceiveItemsApi
# lazy import: api.api_attachment.AttachmentHandOverTheListOfItemsApi
# lazy import: api.api_attachment.AttachmentSalesDetailsApi
# lazy import: api.api_attachment.AttachmentSalesListApi
# lazy import: api.api_attachment.AttachmentSortingListApi
# lazy import: api.api_attachment.AttachmentStaticsDetailApi
# lazy import: api.api_attachment.AttachmentWarehouseAllocationApi
# lazy import: api.api_auction.AuctionIndexApi
# lazy import: api.api_auction.AuctionMyApi
# lazy import: api.api_distribution.DistributionListApi
# lazy import: api.api_distribution.DistributionOrdersApi
# lazy import: api.api_quality.QualityCentreItemApi
# lazy import: api.api_quality.QualityContentTemplateApi
# lazy import: api.api_quality.QualityCountApi
# lazy import: api.api_quality.QualityRecordListApi
# lazy import: api.api_quality.QualityStaticsApi
# lazy import: api.api_quality.QualityStoreApi
# lazy import: api.api_quality.QualityTemplatesApi
# lazy import: api.api_quality.QualityWaitReceiveApi
# lazy import: api.api_quality.QualityWaitTurnOverApi
# lazy import: api.api_recycler.RecyclerBidSuccessOrderApi
# lazy import: api.api_recycler.RecyclerJoinMachineApi
# lazy import: api.api_recycler.RecyclerManualBiddingApi
# lazy import: api.api_inventory.InventoryAddressManageApi
# lazy import: api.api_inventory.InventoryCountApi
# lazy import: api.api_inventory.InventoryListApi
# lazy import: api.api_inventory.InventoryLogisticsChangeRecordApi
# lazy import: api.api_inventory.InventoryLogisticsIntoWarehouseApi
# lazy import: api.api_inventory.InventoryLogisticsListApi
# lazy import: api.api_inventory.InventoryModelDistributionApi
# lazy import: api.api_inventory.InventoryOutStockLogisticsListApi
# lazy import: api.api_inventory.InventoryOutboundOrdersListApi
# lazy import: api.api_inventory.InventoryPeopleDistributionApi
# lazy import: api.api_inventory.InventoryReceiveItemsApi
# lazy import: api.api_inventory.InventorySendOutRepairApi
# lazy import: api.api_inventory.InventoryTransferRecordsApi
# lazy import: api.api_inventory.InventoryWaitReceiveApi
# lazy import: api.api_inventory.InventoryWarehouseAllocationApi
# lazy import: api.api_inventory.InventoryWarningListApi
# lazy import: api.api_send.SendBeenSentRepairApi
# lazy import: api.api_send.SendListOfRepairOrdersApi
# lazy import: api.api_send.SendStayRepairApi
# lazy import: api.api_send.SendWaitReceiveApi

class ImportApi:
    """
    ImportApi 是一个聚合类，用于统一管理多个模块的 API 断言类。
    通过延迟加载方式按需实例化各个模块的断言类，提高性能并避免重复初始化。
    """

    # ===== 模块与API类映射表 =====
    _module_map = {
        'purse_wallet_center': ('api.api_purse', 'PurseWalletCenterApi'),
        'purse_wallet_order_list': ('api.api_purse', 'PurseWalletOrderListApi'),
        'quotation_base_list': ('api.api_quotation', 'QuotationBaseListApi'),
        'quotation_configuration': ('api.api_quotation', 'QuotationConfigurationApi'),
        'quotation_my_list': ('api.api_quotation', 'QuotationMyListApi'),
        'quotation_records_list': ('api.api_quotation', 'QuotationRecordsListApi'),
        'camera_after_sales_order': ('api.api_camera', 'CameraAfterSalesOrderApi'),
        'camera_list_of_airport_visits': ('api.api_camera', 'CameraListOfAirportVisitsApi'),
        'finance_account_list': ('api.api_finance', 'FinanceAccountListApi'),
        'finance_analyze': ('api.api_finance', 'FinanceAnalyzeApi'),
        'finance_bill_review': ('api.api_finance', 'FinanceBillReviewApi'),
        'finance_collection_and_settlement': ('api.api_finance', 'FinanceCollectionAndSettlementApi'),
        'finance_commission_pay_setting': ('api.api_finance', 'FinanceCommissionPaySettingApi'),
        'finance_commission_setting': ('api.api_finance', 'FinanceCommissionSettingApi'),
        'finance_coping_with_each_other': ('api.api_finance', 'FinanceCopingWithEachOtherApi'),
        'finance_cost_income_adjustment': ('api.api_finance', 'FinanceCostIncomeAdjustmentApi'),
        'finance_customer_pay_setting': ('api.api_finance', 'FinanceCustomerPaySettingApi'),
        'finance_daily_expenditure': ('api.api_finance', 'FinanceDailyExpenditureApi'),
        'finance_daily_income': ('api.api_finance', 'FinanceDailyIncomeApi'),
        'finance_exchanges_and_receivables': ('api.api_finance', 'FinanceExchangesAndReceivablesApi'),
        'finance_fee_setting': ('api.api_finance', 'FinanceFeeSettingApi'),
        'finance_payment_settlement': ('api.api_finance', 'FinancePaymentSettlementApi'),
        'finance_prepay_receive_list': ('api.api_finance', 'FinancePrepayReceiveListApi'),
        'finance_supplier_setting': ('api.api_finance', 'FinanceSupplierSettingApi'),
        'finance_transaction_details': ('api.api_finance', 'FinanceTransactionDetailsApi'),
        'fulfillment_items_to_be_quoted': ('api.api_fulfillment', 'FulfillmentItemsToBeQuotedApi'),
        'fulfillment_order_manage': ('api.api_fulfillment', 'FulfillmentOrderManageApi'),
        'fulfillment_quality_manage': ('api.api_fulfillment', 'FulfillmentQualityManageApi'),
        'fulfillment_returns_manage': ('api.api_fulfillment', 'FulfillmentReturnsManageApi'),
        'fulfillment_sign_into_the_library': ('api.api_fulfillment', 'FulfillmentSignIntoTheLibraryApi'),
        'fulfillment_sell_goods_transactions': ('api.api_fulfillment', 'FulfillmentSellGoodsTransactionsApi'),
        'fulfillment_bot_order': ('api.api_fulfillment', 'FulfillmentBotOrderApi'),
        'fulfillment_virtual_list': ('api.api_fulfillment', 'FulfillmentVirtualListApi'),
        'fulfillment_sales_and_shipment_manage': ('api.api_fulfillment', 'FulfillmentSalesAndShipmentManageApi'),
        'fulfillment_items_are_out_of_storage': ('api.api_fulfillment', 'FulfillmentItemsAreOutOfStorageApi'),
        'fulfillment_camera_after_sales_order': ('api.api_fulfillment', 'FulfillmentCameraAfterSalesOrderApi'),
        'fulfillment_after_sales_return_manage': ('api.api_fulfillment', 'FulfillmentAfterSalesReturnManageApi'),
        'guarantee_order_manage': ('api.api_guarantee', 'GuaranteeOrderManageApi'),
        'guarantee_returns_manage': ('api.api_guarantee', 'GuaranteeReturnsManageApi'),
        'guarantee_goods_manage': ('api.api_guarantee', 'GuaranteeGoodsManageApi'),
        'index_statics': ('api.api_index', 'IndexStaticsApi'),
        'user_info': ('api.api_index', 'UserInfoApi'),
        'trafficker_index': ('api.api_trafficker', 'TraffickerIndexApi'),
        'trafficker_statics': ('api.api_trafficker', 'TraffickerStaticsApi'),
        'message_center': ('api.api_message', 'MessageCenterApi'),
        'message_release_list': ('api.api_message', 'MessageReleaseListApi'),
        'sell_after_sales_list': ('api.api_sell', 'SellAfterSalesListApi'),
        'sell_customers_manage': ('api.api_sell', 'SellCustomersManageApi'),
        'sell_goods_received': ('api.api_sell', 'SellGoodsReceivedApi'),
        'sell_items_for_sale': ('api.api_sell', 'SellItemsForSaleApi'),
        'sell_list_of_items_for_sale': ('api.api_sell', 'SellListOfItemsForSaleApi'),
        'sell_order_list_for_sale': ('api.api_sell', 'SellOrderListForSaleApi'),
        'sell_sale_item_list': ('api.api_sell', 'SellSaleItemListApi'),
        'sell_sold_order': ('api.api_sell', 'SellSoldOrderApi'),
        'sell_statics': ('api.api_sell', 'SellStaticsApi'),
        'platform_virtual_inventory_list': ('api.api_platform', 'PlatformVirtualInventoryListApi'),
        'platform_auction_product_manage': ('api.api_platform', 'PlatformAuctionProductManageApi'),
        'platform_auction_business_settings': ('api.api_platform', 'PlatformAuctionBusinessSettingsApi'),
        'platform_expense_config': ('api.api_platform', 'PlatformExpenseConfigApi'),
        'platform_margin_allocation': ('api.api_platform', 'PlatformMarginAllocationApi'),
        'platform_yz_auction': ('api.api_platform', 'PlatformYzAuctionApi'),
        'platform_grievance_manage': ('api.api_platform', 'PlatformGrievanceManageApi'),
        'platform_after_sales_return_manage': ('api.api_platform', 'PlatformAfterSalesReturnManageApi'),
        'platform_aftermarket_attributes': ('api.api_platform', 'PlatformAftermarketAttributesApi'),
        'platform_distribution': ('api.api_platform', 'PlatformDistributionApi'),
        'platform_distribution_orders': ('api.api_platform', 'PlatformDistributionOrdersApi'),
        'platform_distribution_roles': ('api.api_platform', 'PlatformDistributionRolesApi'),
        'platform_help_sell_config': ('api.api_platform', 'PlatformHelpSellConfigApi'),
        'platform_help_sell_list': ('api.api_platform', 'PlatformHelpSellListApi'),
        'platform_items_orders_management': ('api.api_platform', 'PlatformItemsOrdersManagementApi'),
        'platform_items_returns_management': ('api.api_platform', 'PlatformItemsReturnsManagementApi'),
        'platform_items_to_be_specified': ('api.api_platform', 'PlatformItemsToBeSpecifiedApi'),
        'platform_items_rule_management': ('api.api_platform', 'PlatformItemsRuleManagementApi'),
        'platform_list_of_dark_auction_houses': ('api.api_platform', 'PlatformListOfDarkAuctionHousesApi'),
        'platform_list_of_direct_auction_houses': ('api.api_platform', 'PlatformListOfDirectAuctionHousesApi'),
        'platform_sales_look_board_data': ('api.api_platform', 'PlatformSalesLookBoardDataApi'),
        'platform_logistics_config': ('api.api_platform', 'PlatformLogisticsConfigApi'),
        'platform_logistics_orders_list': ('api.api_platform', 'PlatformLogisticsOrdersListApi'),
        'platform_message_release_list': ('api.api_platform', 'PlatformMessageReleaseListApi'),
        'platform_intensity_five_goods': ('api.api_platform', 'PlatformIntensityFiveGoodsApi'),
        'platform_order_review': ('api.api_platform', 'PlatformOrderReviewApi'),
        'platform_order_list': ('api.api_platform', 'PlatformOrderListApi'),
        'platform_product_manage': ('api.api_platform', 'PlatformProductManageApi'),
        'platform_product_review': ('api.api_platform', 'PlatformProductReviewApi'),
        'platform_purchase_manage': ('api.api_platform', 'PlatformPurchaseManageApi'),
        'platform_quotation': ('api.api_platform', 'PlatformQuotationApi'),
        'platform_quotation_calculate': ('api.api_platform', 'PlatformQuotationCalculateApi'),
        'platform_quotation_deduction': ('api.api_platform', 'PlatformQuotationDeductionApi'),
        'platform_quotation_level': ('api.api_platform', 'PlatformQuotationLevelApi'),
        'platform_quotation_quality': ('api.api_platform', 'PlatformQuotationQualityApi'),
        'platform_quotation_menu': ('api.api_platform', 'PlatformQuotationMenuApi'),
        'platform_quotation_records': ('api.api_platform', 'PlatformQuotationRecordsApi'),
        'platform_quotation_recycle': ('api.api_platform', 'PlatformQuotationRecycleApi'),
        'platform_sold_accounts': ('api.api_platform', 'PlatformSoldAccountsApi'),
        'platform_sold_dw_goods': ('api.api_platform', 'PlatformSoldDwGoodsApi'),
        'platform_sold_dw_orders': ('api.api_platform', 'PlatformSoldDwOrdersApi'),
        'platform_sold_dw_reback': ('api.api_platform', 'PlatformSoldDwRebackApi'),
        'platform_sold_dw_sales': ('api.api_platform', 'PlatformSoldDwSalesApi'),
        'platform_sold_fee': ('api.api_platform', 'PlatformSoldFeeApi'),
        'platform_sold_logistics': ('api.api_platform', 'PlatformSoldLogisticsApi'),
        'platform_sold_merchant_fee': ('api.api_platform', 'PlatformSoldMerchantFeeApi'),
        'platform_sold_ninety_five_orders': ('api.api_platform', 'PlatformSoldNinetyFiveOrdersApi'),
        'platform_sold_ninety_five_sales': ('api.api_platform', 'PlatformSoldNinetyFiveSalesApi'),
        'platform_sold_payout_orders': ('api.api_platform', 'PlatformSoldPayoutOrdersApi'),
        'platform_sold_quality_records': ('api.api_platform', 'PlatformSoldQualityRecordsApi'),
        'platform_sold_send_address': ('api.api_platform', 'PlatformSoldSendAddressApi'),
        'platform_sold_sms_list': ('api.api_platform', 'PlatformSoldSmsListApi'),
        'platform_sold_xian_yu_orders': ('api.api_platform', 'PlatformSoldXianYuOrdersApi'),
        'platform_wallet_config': ('api.api_platform', 'PlatformWalletConfigApi'),
        'platform_xian_yu_goods': ('api.api_platform', 'PlatformXianYuGoodsApi'),
        'platform_xian_yu_orders': ('api.api_platform', 'PlatformXianYuOrdersApi'),
        'platform_xian_yu_sales': ('api.api_platform', 'PlatformXianYuSalesApi'),
        'platform_yz_app': ('api.api_platform', 'PlatformYzAppApi'),
        'platforms_banner_config': ('api.api_platform', 'PlatformsBannerConfigApi'),
        'platforms_im_list': ('api.api_platform', 'PlatformsImListApi'),
        'platforms_merchant': ('api.api_platform', 'PlatformsMerchantApi'),
        'platforms_orders': ('api.api_platform', 'PlatformsOrdersApi'),
        'platform_recycle_merchants': ('api.api_platform', 'PlatformRecycleMerchantsApi'),
        'platform_service_fee': ('api.api_platform', 'PlatformServiceFeeApi'),
        'platform_sign_receive': ('api.api_platform', 'PlatformSignReceiveApi'),
        'platform_inspection_center_manage': ('api.api_platform', 'PlatformInspectionCenterManageApi'),
        'platform_guaranteed_sale_price_list': ('api.api_platform', 'PlatformGuaranteedSalePriceListApi'),
        'platform_su_shou_sale_price_list': ('api.api_platform', 'PlatformSuShouSalePriceListApi'),
        'platform_model_price_template': ('api.api_platform', 'PlatformModelPriceTemplateApi'),
        'platform_franchisees_release_records': ('api.api_platform', 'PlatformFranchiseesReleaseRecordsApi'),
        'platform_platform_release_record': ('api.api_platform', 'PlatformPlatformReleaseRecordApi'),
        'platform_guarantee_sale_calculation_rules': ('api.api_platform', 'PlatformGuaranteeSaleCalculationRulesApi'),
        'platform_guarantee_sales_and_deduction_manage': ('api.api_platform', 'PlatformGuaranteeSalesAndDeductionManageApi'),
        'platform_trading_goods_center_manage': ('api.api_platform', 'PlatformTradingGoodsCenterManageApi'),
        'detect_custom_detection': ('api.api_detect', 'DetectCustomDetectionApi'),
        'detect_list_of_models': ('api.api_detect', 'DetectListOfModelsApi'),
        'detect_inspection_manage': ('api.api_detect', 'DetectInspectionManageApi'),
        'detect_quality_orders_list': ('api.api_detect', 'DetectQualityOrdersListApi'),
        'detect_quality_report_exported': ('api.api_detect', 'DetectQualityReportExportedApi'),
        'help_generate_order': ('api.api_help', 'HelpGenerateOrderApi'),
        'help_sell_the_list_of_goods': ('api.api_help', 'HelpSellTheListOfGoodsApi'),
        'help_service_configuration': ('api.api_help', 'HelpServiceConfigurationApi'),
        'bidding_camera': ('api.api_bidding', 'BiddingCameraApi'),
        'bidding_my': ('api.api_bidding', 'BiddingMyApi'),
        'repair_items': ('api.api_repair', 'RepairItemsApi'),
        'repair_list': ('api.api_repair', 'RepairListApi'),
        'repair_parts_manage': ('api.api_repair', 'RepairPartsManageApi'),
        'repair_project_list': ('api.api_repair', 'RepairProjectListApi'),
        'repair_receive': ('api.api_repair', 'RepairReceiveApi'),
        'repair_review_list': ('api.api_repair', 'RepairReviewListApi'),
        'repair_statics_list': ('api.api_repair', 'RepairStaticsListApi'),
        'system_message_reception_manage': ('api.api_system', 'SystemMessageReceptionManageApi'),
        'system_api_log_manage': ('api.api_system', 'SystemApiLogManageApi'),
        'system_dept_manage': ('api.api_system', 'SystemDeptManageApi'),
        'system_base_import_manage': ('api.api_system', 'SystemBaseImportManageApi'),
        'system_dict_manage': ('api.api_system', 'SystemDictManageApi'),
        'system_disposition_list': ('api.api_system', 'SystemDispositionListApi'),
        'system_export_list': ('api.api_system', 'SystemExportListApi'),
        'system_general_config': ('api.api_system', 'SystemGeneralConfigApi'),
        'system_interface_log': ('api.api_system', 'SystemInterfaceLogApi'),
        'system_interface_manage': ('api.api_system', 'SystemInterfaceManageApi'),
        'system_international_config_manage': ('api.api_system', 'SystemInternationalConfigManageApi'),
        'system_key_config_manage': ('api.api_system', 'SystemKeyConfigManageApi'),
        'system_log_manage': ('api.api_system', 'SystemLogManageApi'),
        'system_menu_manage': ('api.api_system', 'SystemMenuManageApi'),
        'system_notice_manage': ('api.api_system', 'SystemNoticeManageApi'),
        'system_parameters_setting_manage': ('api.api_system', 'SystemParametersSettingManageApi'),
        'system_post_manage': ('api.api_system', 'SystemPostManageApi'),
        'system_print_template_config': ('api.api_system', 'SystemPrintTemplateConfigApi'),
        'system_quality_barcode_config': ('api.api_system', 'SystemQualityBarcodeConfigApi'),
        'system_quality_print_config': ('api.api_system', 'SystemQualityPrintConfigApi'),
        'system_query_manage': ('api.api_system', 'SystemQueryManageApi'),
        'system_role_manage': ('api.api_system', 'SystemRoleManageApi'),
        'system_third_party_accounts_manage': ('api.api_system', 'SystemThirdPartyAccountsManageApi'),
        'system_user_manage': ('api.api_system', 'SystemUserManageApi'),
        'system_warehouse_manage': ('api.api_system', 'SystemWarehouseManageApi'),
        'system_work_order_setting': ('api.api_system', 'SystemWorkOrderSettingApi'),
        'system_price_calculation_log': ('api.api_system', 'SystemPriceCalculationLogApi'),
        'system_permission_list': ('api.api_system', 'SystemPermissionListApi'),
        'mall_aftermarket_list': ('api.api_mall', 'MallAftermarketListApi'),
        'mall_branch_manage': ('api.api_mall', 'MallBranchManageApi'),
        'mall_commodity_manage': ('api.api_mall', 'MallCommodityManageApi'),
        'purchase_after_sales_list': ('api.api_purchase', 'PurchaseAfterSalesListApi'),
        'purchase_arrival_notices': ('api.api_purchase', 'PurchaseArrivalNoticesApi'),
        'purchase_items_to_be_received': ('api.api_purchase', 'PurchaseItemsToBeReceivedApi'),
        'purchase_ly_arrival': ('api.api_purchase', 'PurchaseLyArrivalApi'),
        'purchase_order_list': ('api.api_purchase', 'PurchaseOrderListApi'),
        'purchase_post_sale_list': ('api.api_purchase', 'PurchasePostSaleListApi'),
        'purchase_supplier_manage': ('api.api_purchase', 'PurchaseSupplierManageApi'),
        'purchase_task_list': ('api.api_purchase', 'PurchaseTaskListApi'),
        'purchase_un_shipped_order_list': ('api.api_purchase', 'PurchaseUnShippedOrderListApi'),
        'purchase_work_order': ('api.api_purchase', 'PurchaseWorkOrderApi'),
        'sold_list_of_xian_yu_orders': ('api.api_sold', 'SoldListOfXianYuOrdersApi'),
        'sold_list_of_xian_yu_products': ('api.api_sold', 'SoldListOfXianYuProductsApi'),
        'sold_list_of_xian_yu_sales': ('api.api_sold', 'SoldListOfXianYuSalesApi'),
        'sold_ninety_five_item_list': ('api.api_sold', 'SoldNinetyFiveItemListApi'),
        'sold_ninety_five_orders_list': ('api.api_sold', 'SoldNinetyFiveOrdersListApi'),
        'sold_ninety_five_reback_list': ('api.api_sold', 'SoldNinetyFiveRebackListApi'),
        'sold_ninety_five_sales_list': ('api.api_sold', 'SoldNinetyFiveSalesListApi'),
        'attachment_after_sales_list': ('api.api_attachment', 'AttachmentAfterSalesListApi'),
        'attachment_gift_details': ('api.api_attachment', 'AttachmentGiftDetailsApi'),
        'attachment_goods_received': ('api.api_attachment', 'AttachmentGoodsReceivedApi'),
        'attachment_handover_records': ('api.api_attachment', 'AttachmentHandoverRecordsApi'),
        'attachment_inventory_details': ('api.api_attachment', 'AttachmentInventoryDetailsApi'),
        'attachment_inventory_list': ('api.api_attachment', 'AttachmentInventoryListApi'),
        'attachment_maintenance': ('api.api_attachment', 'AttachmentMaintenanceApi'),
        'attachment_new_arrival': ('api.api_attachment', 'AttachmentNewArrivalApi'),
        'attachment_old_warehouse': ('api.api_attachment', 'AttachmentOldWarehouseApi'),
        'attachment_purchase_list': ('api.api_attachment', 'AttachmentPurchaseListApi'),
        'attachment_purchase_sales_list': ('api.api_attachment', 'AttachmentPurchaseSalesListApi'),
        'attachment_receive_items': ('api.api_attachment', 'AttachmentReceiveItemsApi'),
        'attachment_hand_over_the_list_of_items': ('api.api_attachment', 'AttachmentHandOverTheListOfItemsApi'),
        'attachment_sales_details': ('api.api_attachment', 'AttachmentSalesDetailsApi'),
        'attachment_sales_list': ('api.api_attachment', 'AttachmentSalesListApi'),
        'attachment_sorting_list': ('api.api_attachment', 'AttachmentSortingListApi'),
        'attachment_statics_detail': ('api.api_attachment', 'AttachmentStaticsDetailApi'),
        'attachment_warehouse_allocation': ('api.api_attachment', 'AttachmentWarehouseAllocationApi'),
        'auction_index': ('api.api_auction', 'AuctionIndexApi'),
        'auction_my': ('api.api_auction', 'AuctionMyApi'),
        'distribution_list': ('api.api_distribution', 'DistributionListApi'),
        'distribution_orders': ('api.api_distribution', 'DistributionOrdersApi'),
        'quality_centre_item': ('api.api_quality', 'QualityCentreItemApi'),
        'quality_content_template': ('api.api_quality', 'QualityContentTemplateApi'),
        'quality_count': ('api.api_quality', 'QualityCountApi'),
        'quality_record_list': ('api.api_quality', 'QualityRecordListApi'),
        'quality_statics': ('api.api_quality', 'QualityStaticsApi'),
        'quality_store': ('api.api_quality', 'QualityStoreApi'),
        'quality_templates': ('api.api_quality', 'QualityTemplatesApi'),
        'quality_wait_receive': ('api.api_quality', 'QualityWaitReceiveApi'),
        'quality_wait_turn_over': ('api.api_quality', 'QualityWaitTurnOverApi'),
        'recycler_bid_success_order': ('api.api_recycler', 'RecyclerBidSuccessOrderApi'),
        'recycler_join_machine': ('api.api_recycler', 'RecyclerJoinMachineApi'),
        'recycler_manual_bidding': ('api.api_recycler', 'RecyclerManualBiddingApi'),
        'inventory_address_manage': ('api.api_inventory', 'InventoryAddressManageApi'),
        'inventory_count': ('api.api_inventory', 'InventoryCountApi'),
        'inventory_list': ('api.api_inventory', 'InventoryListApi'),
        'inventory_logistics_change_record': ('api.api_inventory', 'InventoryLogisticsChangeRecordApi'),
        'inventory_logistics_into_warehouse': ('api.api_inventory', 'InventoryLogisticsIntoWarehouseApi'),
        'inventory_logistics_list': ('api.api_inventory', 'InventoryLogisticsListApi'),
        'inventory_model_distribution': ('api.api_inventory', 'InventoryModelDistributionApi'),
        'inventory_out_stock_logistics_list': ('api.api_inventory', 'InventoryOutStockLogisticsListApi'),
        'inventory_outbound_orders_list': ('api.api_inventory', 'InventoryOutboundOrdersListApi'),
        'inventory_people_distribution': ('api.api_inventory', 'InventoryPeopleDistributionApi'),
        'inventory_receive_items': ('api.api_inventory', 'InventoryReceiveItemsApi'),
        'inventory_send_out_repair': ('api.api_inventory', 'InventorySendOutRepairApi'),
        'inventory_transfer_records': ('api.api_inventory', 'InventoryTransferRecordsApi'),
        'inventory_wait_receive': ('api.api_inventory', 'InventoryWaitReceiveApi'),
        'inventory_warehouse_allocation': ('api.api_inventory', 'InventoryWarehouseAllocationApi'),
        'inventory_warning_list': ('api.api_inventory', 'InventoryWarningListApi'),
        'send_been_sent_repair': ('api.api_send', 'SendBeenSentRepairApi'),
        'send_list_of_repair_orders': ('api.api_send', 'SendListOfRepairOrdersApi'),
        'send_stay_repair': ('api.api_send', 'SendStayRepairApi'),
        'send_wait_receive': ('api.api_send', 'SendWaitReceiveApi'),

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
        raise AttributeError(f"'ImportApi' object has no attribute '{item}'")
