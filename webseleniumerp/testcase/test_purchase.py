# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *
from config.constant import DICT_DATA
from config.user_info import INFO


class TestrrPjGZUY(BaseCase, unittest.TestCase):
    """商品采购|采购管理|新增采购单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.ZTKvMx4gs4()
        else:
            return purchase_p.Yum9T9OO7WP(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0LTMkAl3mr9wdiYoATjak(self):
        """[新增]-苹果手机-未付款在路上-物品创建采购单"""
        case = self.common_operations(login='main')
        case.LTMkAl3mr9wdiYoATjak()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_N4CQUFEbAhA6O3SqB3ap(self):
        """[新增]-苹果手机-未付款入库-物品创建采购单"""
        case = self.common_operations()
        case.N4CQUFEbAhA6O3SqB3ap()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UXWWtbpIHPQ9A7QMbtc9(self):
        """[新增]-苹果手机-未付款未发货-物品创建采购单"""
        case = self.common_operations()
        case.UXWWtbpIHPQ9A7QMbtc9()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='未发货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Iv2a1sAnyG1YRbkyU84V(self):
        """[新增]-苹果手机-部分已付款入库-物品创建采购单"""
        case = self.common_operations()
        case.Iv2a1sAnyG1YRbkyU84V()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_W8Tva7jFU0AkEqegXRnE(self):
        """[新增]-苹果手机-全部已付款入库-物品创建采购单"""
        case = self.common_operations()
        case.W8Tva7jFU0AkEqegXRnE()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tkqeuQNKA9C86c8AQuHz(self):
        """[导入]-采购物品导入-创建采购单"""
        case = self.common_operations()
        case.tkqeuQNKA9C86c8AQuHz()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_K2g9gJbSU76WxYKMFL1A(self):
        """[新增]-已付款入库-创建采购单-入库并移交订单原因是质检"""
        case = self.common_operations()
        case.K2g9gJbSU76WxYKMFL1A()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)


class TestgSsguYTq(BaseCase, unittest.TestCase):
    """商品采购|采购管理|新增采购单"""

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0BB4DySLMjyQ0zFNVq9sj(self):
        """[+-创建供应商]-选择供应商生成采购单"""
        case = self.common_operations(login='idle')
        case.BB4DySLMjyQ0zFNVq9sj()
        res = [lambda: self.pc.LXtfeb(headers='idle', purchaseTime='now', payStateStr='部分付款', stateStr='已收货')]
        self.assert_all(*res)


class TestGVVLVGSZ(BaseCase, unittest.TestCase):
    """商品采购|采购售后管理|采购售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.N47ymrezM8()
        else:
            return purchase_p.Sd1EWjfzgR1(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0tTRW133mzbKPeCd8m40H(self):
        """[采购售后中tab]-换货-在途"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations(login='main')
        case.tTRW133mzbKPeCd8m40H()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', saleStateStr='采购换货', id=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_J5gqPGgMCU66iUGcjVkX(self):
        """[采购售后中tab]-换货-直接入库"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.J5gqPGgMCU66iUGcjVkX()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', saleStateStr='采购换货', id=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_phfsqPqFesHVfgjiWNer(self):
        """[采购售后中tab]-退货退款-未结算"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.phfsqPqFesHVfgjiWNer()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', saleStateStr='采购退货退款', id=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_jVgd53LQsvnwXfUXRRgq(self):
        """[采购售后中tab]-退货退款-已结算"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.jVgd53LQsvnwXfUXRRgq()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', saleStateStr='采购退货退款', id=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Z4SuqHs6Y2LaV2QZa5Ir(self):
        """[采购售后中tab]-拒退退回-在途"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.Z4SuqHs6Y2LaV2QZa5Ir()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', saleStateStr='采购拒退', id=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pHj61cDnzOd8FgCqMVW5(self):
        """[采购售后中tab]-拒退退回-入库"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.pHj61cDnzOd8FgCqMVW5()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', saleStateStr='采购拒退', id=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_OrOE57gtX6xtqaXXMsPi(self):
        """[导出]"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.OrOE57gtX6xtqaXXMsPi()
        res = [lambda: self.pc.T241Se(name='采购待售后列表数据导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Bht5FveIIJwsO1nzrSou(self):
        """[搜索]全部-imei"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD', 'O09i'])
        case = self.common_operations()
        case.Bht5FveIIJwsO1nzrSou()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_CfF5rsovr6q1eXvK89E3(self):
        """[搜索]采购售后中-imei"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.CfF5rsovr6q1eXvK89E3()
        res = [lambda: self.pc.BtoGb1(i=2, createTime='now', imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_k39WRkcNXmAaALC0Vslr(self):
        """[搜索]全部-采购供应商"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD', 'O09i'])
        case = self.common_operations()
        case.k39WRkcNXmAaALC0Vslr()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', supplierId=INFO['main_supplier_id'], imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NqFHiIZhsGNUUdvC6h2P(self):
        """[搜索]采购售后中-采购供应商"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.NqFHiIZhsGNUUdvC6h2P()
        res = [lambda: self.pc.BtoGb1(i=2, createTime='now', supplierId=INFO['main_supplier_id'], imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WGIFhMXGjLDYNdHFNmZ6(self):
        """[搜索]全部-平台物品编号"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD', 'O09i'])
        case = self.common_operations()
        case.WGIFhMXGjLDYNdHFNmZ6()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', platformArticlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_nwM5r4G3gxMKFkY7vCkS(self):
        """[搜索]采购售后中-平台物品编号"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.nwM5r4G3gxMKFkY7vCkS()
        res = [lambda: self.pc.BtoGb1(i=2, createTime='now', platformArticlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SdxPSZvsxDBQFJmoq0sn(self):
        """[搜索]全部-售后订单号"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD', 'O09i'])
        case = self.common_operations()
        case.SdxPSZvsxDBQFJmoq0sn()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', billNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xKOkW569Bn2xL0RXmnEZ(self):
        """[搜索]采购售后中-售后订单号"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.xKOkW569Bn2xL0RXmnEZ()
        res = [lambda: self.pc.BtoGb1(i=2, createTime='now', saleNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_XEQ3tAQnMxJ6mC5Z3zSu(self):
        """[搜索]全部-创建时间"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD', 'O09i'])
        case = self.common_operations()
        case.XEQ3tAQnMxJ6mC5Z3zSu()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', billNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_PhchxOyoBh6ZBZxAR8B5(self):
        """[搜索]采购售后中-创建时间"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.PhchxOyoBh6ZBZxAR8B5()
        res = [lambda: self.pc.BtoGb1(i=2, createTime='now', saleNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cJyOkQvyQsMExyu5Vt45(self):
        """[搜索]全部-出库物流单号"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD', 'O09i'])
        case = self.common_operations()
        case.cJyOkQvyQsMExyu5Vt45()
        res = [lambda: self.pc.BtoGb1(i=1, createTime='now', logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_y4THlC3ekhRh4iae3DtD(self):
        """[搜索]采购售后中-出库物流单号"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD'])
        case = self.common_operations()
        case.y4THlC3ekhRh4iae3DtD()
        res = [lambda: self.pc.BtoGb1(i=2, createTime='now', logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_dhBbO6TlYXaCCyMti4Sf(self):
        """[搜索]-售后状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['ekBx', 'Fv9l', 'O09i'])
            case = self.common_operations()
            case.dhBbO6TlYXaCCyMti4Sf()
            res = [lambda: self.pc.BtoGb1(i=2, createTime='now', saleStateStr='采购退货退款', billNo=cached('i'))]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['ekBx', 'Fv9l', 'v6AD',
                                      'ekBx', 'Fv9l', 'v6AD', 'O09i',
                                      'ekBx', 'Fv9l', 'v6AD', 'LuOO',
                                      'ekBx', 'Fv9l', 'v6AD', 'gfHM',
                                      'ekBx', 'Fv9l', 'v6AD', 'vQ7r'])
            for status in DICT_DATA['j']:
                case = self.common_operations()
                case.dhBbO6TlYXaCCyMti4Sf(status)
                res = [lambda s=status: self.pc.BtoGb1(j=s, saleState=s)]
                self.assert_all(*res)


class TestiJ167dNl(BaseCase, unittest.TestCase):
    """商品采购|采购售后管理|待售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.WdU75jpBUw()
        else:
            return purchase_p.ZrnG6O3xUlf(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0AObSRgmEGYVIgbuCw6h4(self):
        """[取消售后]-确认取消"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations(login='main')
        case.AObSRgmEGYVIgbuCw6h4()
        res = [lambda: self.pc.XtWLz8(data='b', info='取消物品采购售后状态,取消原因：备注')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Zd7znz6pdWwciZ4zhv18(self):
        """[售后操作]-采购补差-未结算"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.Zd7znz6pdWwciZ4zhv18()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购退差价', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Mlllk8zWuMbryTvo07YA(self):
        """[售后操作]-采购补差-已结算"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.Mlllk8zWuMbryTvo07YA()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购退差价', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_EXJN6Kfs99I6kkD0lNX2(self):
        """[售后操作]-售后出库-普通快递-退货退款-未结算"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.EXJN6Kfs99I6kkD0lNX2()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购退货退款', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_r3no6VL2SjqT3qCMSXsF(self):
        """[售后操作]-售后出库-普通快递-退货退款-已结算"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.r3no6VL2SjqT3qCMSXsF()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购退货退款', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WCIspC62VSOcHhuvk6oH(self):
        """[售后操作]-售后出库-普通快递-拒退退回-在途"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.WCIspC62VSOcHhuvk6oH()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购拒退', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bRT8qBZ1qzcsOegIVUiL(self):
        """[售后操作]-售后出库-普通快递-拒退退回-直接入库"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.bRT8qBZ1qzcsOegIVUiL()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购拒退', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_p2NxayPBZqnmytlhtjEy(self):
        """[售后操作]-售后出库-普通快递-换货-在途"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.p2NxayPBZqnmytlhtjEy()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购换货', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HR074UMjBJ9KgEckp0hD(self):
        """[售后操作]-售后出库-普通快递-换货-直接入库"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.HR074UMjBJ9KgEckp0hD()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购换货', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iWItsJtwj5CLc0GYimGA(self):
        """[批量售后]-退差价"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'ekBx', 'Fv9l'])
        case = self.common_operations()
        case.iWItsJtwj5CLc0GYimGA()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购退差价', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uq01dOZeO9ByThGMfj4w(self):
        """[批量售后]-售后出库-普通快递-无"""
        self.pre.operations(data=['ekBx', 'Fv9l', 'ekBx', 'Fv9l'])
        case = self.common_operations()
        case.uq01dOZeO9ByThGMfj4w()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购售后中', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_mtmZ9ns5g8nanblESlTR(self):
        """[售后操作]-售后出库-普通快递-无"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.mtmZ9ns5g8nanblESlTR()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购售后中', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gXtFuS2Icw1FTTfLvWC0(self):
        """[售后操作]-售后出库-快递易-无"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.gXtFuS2Icw1FTTfLvWC0()
        res = [lambda: self.pc.BtoGb1(createTime='now', saleStateStr='采购售后中', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_nFSWCuNM4gli2yRB2dwD(self):
        """[添加物品]-"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.nFSWCuNM4gli2yRB2dwD()
        res = [lambda: self.pc.QPF5WW(purchaseTime='now', articlesState='待采购售后')]
        self.assert_all(*res)


class TestHqbVmZqx(BaseCase, unittest.TestCase):
    """商品采购|采购售后管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.LZnv9DokCX()
        else:
            return purchase_p.Am1rGtH5Djz(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0kDYL6B67bVRYqDohXGBm(self):
        """[接收]-物品接收"""
        self.pre.operations(data=['ekBx', 'nxWZ'])
        case = self.common_operations(login='special')
        case.kDYL6B67bVRYqDohXGBm()
        res = [lambda: self.pc.jbliLf(statusStr='已接收', createTime='now'),
               lambda: self.pc.jbliLf(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rf4cDB3LPxVAKj6lhBRy(self):
        """[扫码精确接收]-物品接收"""
        self.pre.operations(data=['ekBx', 'nxWZ'])
        case = self.common_operations()
        case.rf4cDB3LPxVAKj6lhBRy()
        res = [lambda: self.pc.jbliLf(statusStr='已接收', createTime='now'),
               lambda: self.pc.jbliLf(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gXbPXTa8tODEWzcuCWKK(self):
        """[搜索]-imei"""
        self.pre.operations(data=['ekBx', 'nxWZ'])
        case = self.common_operations()
        case.gXbPXTa8tODEWzcuCWKK()
        res = [lambda: self.pc.k60zWG(imei=cached('i'), deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_GK9UcuLcY440l6QirME6(self):
        """[搜索]-移交时间"""
        self.pre.operations(data=['ekBx', 'nxWZ'])
        case = self.common_operations()
        case.GK9UcuLcY440l6QirME6()
        res = [lambda: self.pc.k60zWG(imei=cached('i'), deliveryTime='now')]
        self.assert_all(*res)


class TestymybGFFL(BaseCase, unittest.TestCase):
    """商品采购|采购管理|采购订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.G4EaCouJoJ()
        else:
            return purchase_p.EDzjBdrUqTJ(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0V3OaBTTJgYrJQyoMmypY(self):
        """[采购单号]-售后处理-采购仅退款"""
        self.pre.operations(data=['XLBD'])
        case = self.common_operations(login='main')
        case.V3OaBTTJgYrJQyoMmypY()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已取消', articlesNoList_0=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FxIuRXAgm25KpkG1vYdL(self):
        """[发货]-"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.FxIuRXAgm25KpkG1vYdL()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已发货', articlesNoList_0=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_onkEdLesfyWSOGVCSZdB(self):
        """[物流发货]-添加物品-发货"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.onkEdLesfyWSOGVCSZdB()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已发货', imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IOHuxRCgSyddeY0Uw98C(self):
        """[物流发货]-导入物品-发货"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations(login='main')
        case.IOHuxRCgSyddeY0Uw98C()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已发货', imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZaJnjFDN816Yj39HvvTA(self):
        """[收货]-签收入库"""
        self.pre.operations(data=['XLBD'])
        case = self.common_operations()
        case.ZaJnjFDN816Yj39HvvTA()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_X9AzyILbQOMXUGnTTHIW(self):
        """[搜索]-编号/IMEI"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.X9AzyILbQOMXUGnTTHIW()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', articlesNoList_0=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UBQunveHStNfKk7VC1MY(self):
        """[搜索]-采购单号"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.UBQunveHStNfKk7VC1MY()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_CIlgrf4csxjqTWz7KBW8(self):
        """[搜索]-供应商"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.CIlgrf4csxjqTWz7KBW8()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', orderNo=cached('i'), supplierId=INFO['main_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SEQRfhZPQLSks8OIHSUp(self):
        """[搜索]-采购单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['MwyC'])
            case = self.common_operations()
            case.SEQRfhZPQLSks8OIHSUp()
            res = [lambda: self.pc.LXtfeb(purchaseTime='now', orderNo=cached('i'), stateStr='未发货')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['ekBx',
                                      'XLBD',
                                      'MwyC',
                                      'XLBD', 'TFma'])
            for status in DICT_DATA['f']:
                case = self.common_operations()
                case.SEQRfhZPQLSks8OIHSUp(status)
                res = [lambda s=status: self.pc.LXtfeb(i=s, state=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RHW76Y60nHIiwxzfeZNR(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.RHW76Y60nHIiwxzfeZNR()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZQ8ruPTDvW7q2hXTRV77(self):
        """[搜索]-付款状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['MwyC'])
            case = self.common_operations()
            case.ZQ8ruPTDvW7q2hXTRV77()
            res = [lambda: self.pc.LXtfeb(purchaseTime='now', orderNo=cached('i'), payStateStr='已付款')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['MwyC',
                                      'CFo3',
                                      'ciS4'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.ZQ8ruPTDvW7q2hXTRV77(status)
                res = [lambda s=status: self.pc.LXtfeb(j=s, payState=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gwoujeJsaB3onqINz3vL(self):
        """[搜索]-采购时间"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.gwoujeJsaB3onqINz3vL()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JB7S4POKRpjesx1Q32J0(self):
        """[搜索]-采购人"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.JB7S4POKRpjesx1Q32J0()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', orderNo=cached('i'), userId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FysimTUmjHi3FisKVbsM(self):
        """[搜索]-采购单详情-平台物品编号"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.FysimTUmjHi3FisKVbsM()
        res = [lambda: self.pc.LXtfeb(data='b', purchaseTime='now', platformArticlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_KjmhjLfM7YrFQNE6NiZG(self):
        """[搜索]-采购单详情-imei"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.KjmhjLfM7YrFQNE6NiZG()
        res = [lambda: self.pc.LXtfeb(data='b', purchaseTime='now', imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_D1M3VTxNoTROnlErwIkd(self):
        """[搜索]-采购单详情-平台订单号"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.D1M3VTxNoTROnlErwIkd()
        res = [lambda: self.pc.LXtfeb(data='b', purchaseTime='now', platformOrderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Nu2xob41mVQX0Uwyv77c(self):
        """[搜索]-采购单详情-序列号"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.Nu2xob41mVQX0Uwyv77c()
        res = [lambda: self.pc.LXtfeb(data='b', purchaseTime='now', serialNo=cached('i'))]
        self.assert_all(*res)


class TestXl9vwQbI(BaseCase, unittest.TestCase):
    """商品采购|供应商管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.FYDICk4EbP()
        else:
            return purchase_p.O5TxXs1xP4q(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0h0V1zMfjLKSd4odY9NU2(self):
        """[新增]-平台拍货-默认付款"""
        case = self.common_operations(login='idle')
        case.h0V1zMfjLKSd4odY9NU2()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_VUZzvXlURvWP4b43uTRg(self):
        """[新增]-同行贸易-已付款"""
        case = self.common_operations()
        case.VUZzvXlURvWP4b43uTRg()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZwXnGe8s67ZogrbVkpxf(self):
        """[编辑]-修改信息保存"""
        case = self.common_operations()
        case.ZwXnGe8s67ZogrbVkpxf()
        res = [lambda: self.pc.gsWmaV(headers='idle', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_AO2AZxYBELIUmcGqLQlG(self):
        """[搜索]-供应商名称"""
        case = self.common_operations()
        case.AO2AZxYBELIUmcGqLQlG()


class TestniU1fvak(BaseCase, unittest.TestCase):
    """商品采购|采购管理|采购工单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.EE20RTANF9()
        else:
            return purchase_p.YylKNDKVlLq(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0rfP03M51AR6P1V5a2zV9(self):
        """[新建]-采购工单-按合格数量计算"""
        case = self.common_operations(login='main')
        case.rfP03M51AR6P1V5a2zV9()
        res = [lambda: self.pc.ttqNVt(stateStr='待开始', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_plgZg761v9pgtz1l53NY(self):
        """[新建]-采购工单-按合格数量计算"""
        case = self.common_operations()
        case.plgZg761v9pgtz1l53NY()
        res = [lambda: self.pc.ttqNVt(stateStr='待开始', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pQejvS83KhwLmhztGkIZ(self):
        """[编辑]采购工单"""
        self.pre.operations(data=['IcFU'])
        case = self.common_operations()
        case.pQejvS83KhwLmhztGkIZ()
        res = [lambda: self.pc.ttqNVt(stateStr='待开始', updateTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_H7QZrgxeJPrgyVASQvUy(self):
        """[编辑]添加特殊工序-报价"""
        self.pre.operations(data=['IcFU'])
        case = self.common_operations()
        case.H7QZrgxeJPrgyVASQvUy()
        res = [lambda: self.pc.ttqNVt(stateStr='待开始', orderNo=cached('i'), taskProgressList_1_processName='报价')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hsFfIhIFCLXHb4x2J1CC(self):
        """[编辑]添加特殊工序-退货"""
        self.pre.operations(data=['IcFU', 'ZcF1'])
        case = self.common_operations()
        case.hsFfIhIFCLXHb4x2J1CC()
        res = [lambda: self.pc.ttqNVt(stateStr='待开始', orderNo=cached('i'), taskProgressList_2_processName='退货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LrMhNar9BE7bRoEWOGFt(self):
        """[编辑]添加特殊工序-付款"""
        self.pre.operations(data=['IcFU', 'ZcF1', 'uVt1'])
        case = self.common_operations()
        case.LrMhNar9BE7bRoEWOGFt()
        res = [lambda: self.pc.ttqNVt(stateStr='待开始', orderNo=cached('i'), taskProgressList_3_processName='付款')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sruAfwpM3knh3URDgVTd(self):
        """[业务报工]报价"""
        self.pre.operations(data=['IcFU', 'ZcF1', 'uVt1', 'DoNc', 'YS1c'])
        case = self.common_operations()
        case.sruAfwpM3knh3URDgVTd()
        res = [lambda: self.pc.ttqNVt(stateStr='进行中', updateTime='now', orderNo=cached('i'), taskProgressList_1_processName='报价'),
               lambda: self.pc.ttqNVt(data='a', processName='报价', payAmount=88.88)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IBx6SkNmcqoSeAqgrxkF(self):
        """[业务报工]退货"""
        self.pre.operations(data=['IcFU', 'ZcF1', 'uVt1', 'DoNc', 'YS1c'])
        case = self.common_operations()
        case.IBx6SkNmcqoSeAqgrxkF()
        res = [lambda: self.pc.ttqNVt(stateStr='进行中', updateTime='now', orderNo=cached('i'), taskProgressList_2_processName='退货'),
               lambda: self.pc.ttqNVt(data='a', processName='退货', returnNum=5)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vkKizyCO3AYcLb15f5j2(self):
        """[业务报工]付款"""
        self.pre.operations(data=['IcFU', 'ZcF1', 'uVt1', 'DoNc', 'YS1c'])
        case = self.common_operations()
        case.vkKizyCO3AYcLb15f5j2()
        res = [lambda: self.pc.ttqNVt(stateStr='进行中', updateTime='now', orderNo=cached('i'), taskProgressList_3_processName='付款'),
               lambda: self.pc.ttqNVt(data='a', processName='付款', paidAmount=23.43)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HTjf6RsIbsSIfYSwsXzv(self):
        """[业务报工]工序"""
        self.pre.operations(data=['IcFU', 'ZcF1', 'uVt1', 'DoNc', 'YS1c'])
        case = self.common_operations()
        case.HTjf6RsIbsSIfYSwsXzv()
        res = [lambda: self.pc.ttqNVt(stateStr='进行中', updateTime='now', orderNo=cached('i'), taskProgressList_0_processName='工序'),
               lambda: self.pc.ttqNVt(data='a', processName='工序', workNum=100)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_v7dp0gZaBk5c5dnae7G3(self):
        """[开始任务]"""
        self.pre.operations(data=['IcFU'])
        case = self.common_operations()
        case.v7dp0gZaBk5c5dnae7G3()
        res = [lambda: self.pc.ttqNVt(stateStr='进行中', updateTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RB3GNQ8IJqAeegDYmA32(self):
        """[结束任务]"""
        self.pre.operations(data=['IcFU', 'YS1c'])
        case = self.common_operations()
        case.RB3GNQ8IJqAeegDYmA32()
        res = [lambda: self.pc.ttqNVt(stateStr='已结束', updateTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FNyrgjsFJzK3B4902iHy(self):
        """[恢复任务]"""
        self.pre.operations(data=['IcFU', 'YS1c', 'MbiP'])
        case = self.common_operations()
        case.FNyrgjsFJzK3B4902iHy()
        res = [lambda: self.pc.ttqNVt(stateStr='进行中', updateTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_q7pI3tL3zRqZ67pGHnxf(self):
        """[删除采购工单]"""
        self.pre.operations(data=['IcFU'])
        case = self.common_operations()
        case.q7pI3tL3zRqZ67pGHnxf()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_KOF9RCucwpiZtv3KYptu(self):
        """[搜索]工单编号"""
        self.pre.operations(data=['IcFU', 'YS1c'])
        case = self.common_operations()
        case.KOF9RCucwpiZtv3KYptu()
        res = [lambda: self.pc.ttqNVt(createTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_D198Z7vIR4WbkTl36hHI(self):
        """[搜索]计划时间"""
        self.pre.operations(data=['IcFU', 'YS1c'])
        case = self.common_operations()
        case.D198Z7vIR4WbkTl36hHI()
        res = [lambda: self.pc.ttqNVt(createTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_GlZThKYcHMLtYtD6WFjf(self):
        """[搜索]供应商"""
        self.pre.operations(data=['IcFU', 'YS1c'])
        case = self.common_operations()
        case.GlZThKYcHMLtYtD6WFjf()
        res = [lambda: self.pc.ttqNVt(createTime='now', orderNo=cached('i'), supplierId=INFO['main_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZfNPiUkcpGxXUTMsfG0n(self):
        """[搜索]-状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['IcFU', 'YS1c'])
            case = self.common_operations()
            case.ZfNPiUkcpGxXUTMsfG0n()
            res = [lambda: self.pc.ttqNVt(createTime='now', orderNo=cached('i'), stateStr='待开始')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['IcFU', 'YS1c',
                                      'IcFU', 'MbiP',
                                      'IcFU', 'YS1c', 'mybg'])
            for state in DICT_DATA['b']:
                case = self.common_operations()
                case.ZfNPiUkcpGxXUTMsfG0n(state)
                res = [lambda s=state: self.pc.ttqNVt(i=s, state=s)]
                self.assert_all(*res)


class TestcwtXrPcU(BaseCase, unittest.TestCase):
    """商品采购|采购管理|未发货订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.GVdV4FYYC3()
        else:
            return purchase_p.TsxUzXRsZ5y(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0Ol6cW1DJGyj0f1eaoFJB(self):
        """[导出]"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations(login='main')
        case.Ol6cW1DJGyj0f1eaoFJB()
        res = [lambda: self.pc.T241Se(name='未发货物品列表导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uXCn7JV8wWVKBqpjkPz1(self):
        """[搜索]供应商"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.uXCn7JV8wWVKBqpjkPz1()
        res = [lambda: self.pc.p1kRiO(createTime='now', supplierName=INFO['main_supplier_name'], purchaseNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NApBGCWJXaD8TCr8oG0O(self):
        """[搜索]平台订单号"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.NApBGCWJXaD8TCr8oG0O()
        res = [lambda: self.pc.p1kRiO(createTime='now', platformOrderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gEvHUJODc2blQ0T3B8vs(self):
        """[搜索]平台物品编号"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.gEvHUJODc2blQ0T3B8vs()
        res = [lambda: self.pc.p1kRiO(createTime='now', platformArticlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tg0itP0B1fKeUwbew3bL(self):
        """[搜索]imei"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.tg0itP0B1fKeUwbew3bL()
        res = [lambda: self.pc.p1kRiO(createTime='now', imei=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DntxwTAfuSnkVqrNwSV9(self):
        """[搜索]采购时间"""
        self.pre.operations(data=['MwyC'])
        case = self.common_operations()
        case.DntxwTAfuSnkVqrNwSV9()
        res = [lambda: self.pc.p1kRiO(createTime='now', imei=cached('i'))]
        self.assert_all(*res)


class Testx8u6DwMG(BaseCase, unittest.TestCase):
    """商品采购|采购管理|到货通知单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.HMBSFfGhqc()
        else:
            return purchase_p.UyQmHapMXQU(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0KbYnHWYarqIZt0JaCFuZ(self):
        """[搜索]采购供应商"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.KbYnHWYarqIZt0JaCFuZ()
        res = [lambda: self.pc.uhvTi6(purchaseTime='now', orderNo=cached('i'), supplierId=INFO['main_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yUfJVOWNNm8e1oZ0AOli(self):
        """[搜索]物流单号"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.yUfJVOWNNm8e1oZ0AOli()
        res = [lambda: self.pc.LXtfeb(createTime='now'),
               lambda: self.pc.LXtfeb(data='c', logisticsNoList=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_EY8ajeO8hDESQhWV9p4d(self):
        """[搜索]采购单号"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.EY8ajeO8hDESQhWV9p4d()
        res = [lambda: self.pc.uhvTi6(purchaseTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_W62QpkNGF7aGdL8UtHlh(self):
        """[搜索]采购日期"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.W62QpkNGF7aGdL8UtHlh()
        res = [lambda: self.pc.uhvTi6(purchaseTime='now', orderNo=cached('i'))]
        self.assert_all(*res)


class TestGotV9LOz(BaseCase, unittest.TestCase):
    """商品采购|采购任务"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return purchase_r.SDhYvjpFxu()
        else:
            return purchase_p.JlYj7UfDcRG(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0tuGormTpYPA2aELsOzkM(self):
        """[新建任务]手机"""
        case = self.common_operations(login='main')
        case.tuGormTpYPA2aELsOzkM()
        res = [lambda: self.pc.HMd55z5LcuW(createTime='now', statusStr='未完成')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Vax4XBiddBZJvUZ7eKdV(self):
        """[新建任务]平板电脑"""
        case = self.common_operations()
        case.Vax4XBiddBZJvUZ7eKdV()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='未完成')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_XBHUgvj186aUw4Sixsaa(self):
        """[新建任务]笔记本电脑"""
        case = self.common_operations()
        case.XBHUgvj186aUw4Sixsaa()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='未完成')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IlyTw4WbHlrGhJIXjQNt(self):
        """[新建任务]智能手表"""
        case = self.common_operations()
        case.IlyTw4WbHlrGhJIXjQNt()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='未完成')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Jo3v4QXhq0GyXeDDjAG8(self):
        """[更新到货初验]"""
        self.pre.operations(data=['odNU'])
        case = self.common_operations()
        case.Jo3v4QXhq0GyXeDDjAG8()
        res = [lambda: self.pc.HMLcuW(createTime='now', orderNo=cached('i'), deliveryNum=30, qualifiedNum=10)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_e65OsVYsAZfUdtju3ktx(self):
        """[采购录入]"""
        self.pre.operations(data=['odNU'])
        case = self.common_operations()
        case.e65OsVYsAZfUdtju3ktx()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已完成', successNum=1, orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_QlWxSfpR4xrTDauwyHLD(self):
        """[退货]"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(orderNo=cached('i')),
               lambda: self.pc.HMLcuW(data='a', returnNum='1', returnTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WYBiBGE7VdR3njn7NPom(self):
        """[取消]"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.WYBiBGE7VdR3njn7NPom()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SB3L2MTy6Akwg7s7DxMi(self):
        """[编辑]"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_taK4q6mJhM6CWjnVVCPs(self):
        """[导出]"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_f3N2dDqRmAtCrRFZDaTc(self):
        """[搜索]采购任务单号"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Nrafk2EPWIAnq3GrKVH2(self):
        """[搜索]采购人"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WDlG1CIIdGDh9T4unA3R(self):
        """[搜索]供应商"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ocWEDpiVUd5hyHZiVeuT(self):
        """[搜索]-任务状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['ekBx', 'Fv9l', 'O09i'])
            case = self.common_operations()
            case.dhBbO6TlYXaCCyMti4Sf()
            res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['odNU', 'D6bk'])
            for status in DICT_DATA['j']:
                case = self.common_operations()
                case.dhBbO6TlYXaCCyMti4Sf(status)
                res = [lambda s=status: self.pc.HMLcuW(j=s, saleState=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_US2rQK6F5ZHHgmuHPHYa(self):
        """[搜索]任务开始时间"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_QZzPyowzxFc8Gfa4rWH5(self):
        """[搜索]任务结束时间"""
        self.pre.operations(data=['odNU', 'D6bk'])
        case = self.common_operations()
        case.QlWxSfpR4xrTDauwyHLD()
        res = [lambda: self.pc.HMLcuW(createTime='now', statusStr='已取消', orderNo=cached('i'))]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
