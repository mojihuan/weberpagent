# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *
from config.constant import DICT_DATA
from config.user_info import INFO


class TestVo1ZgJLf(BaseCase, unittest.TestCase):
    """配件管理|入库管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.GGZectTPpu()
        else:
            return attachment_p.Xoub7k5qm8b(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0do56fxxjyrxq3jf44spl(self):
        """[接收]接收"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations(login='special')
        case.do56fxxjyrxq3jf44spl()
        res = [lambda: self.pc.wb3p9S(statusStr='已接收', totalCount=1),
               lambda: self.pc.wb3p9S(data='b', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ttg8vtbix8yyh0zzk1l5(self):
        """[扫码精确接收]-接收"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.ttg8vtbix8yyh0zzk1l5()
        res = [lambda: self.pc.wb3p9S(statusStr='已接收', totalCount=1),
               lambda: self.pc.wb3p9S(data='b', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wkocqx1u2ihsf32i7co1(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.wkocqx1u2ihsf32i7co1()
        res = [lambda: self.pc.oCiIiV(articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_a33hoz47yc05hmc4n7jw(self):
        """[搜索]-移交时间"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.a33hoz47yc05hmc4n7jw()
        res = [lambda: self.pc.oCiIiV(articlesNo=cached('i'))]
        self.assert_all(*res)


class TestSEahDjID(BaseCase, unittest.TestCase):
    """配件管理|移交接收管理|移交物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.O7NTx8CXpa()
        else:
            return attachment_p.QWfXHzt4fYt(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0pxx47rbom8j1ul0o5otk(self):
        """[移交]移交库存配件"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations(login='main')
        case.pxx47rbom8j1ul0o5otk()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='待接收'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bq9jhuudug0bycyitdho(self):
        """[移交]-移交采购售后"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.bq9jhuudug0bycyitdho()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qnig8uaqhu0cma5jwmjd(self):
        """[移交]-移交销售"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.qnig8uaqhu0cma5jwmjd()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_p0su9g9hxgnbgmkfhw8b(self):
        """[移交]-移交送修"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.p0su9g9hxgnbgmkfhw8b()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vicvey7gwzlidkxk2756(self):
        """[移交]-移交维修"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.vicvey7gwzlidkxk2756()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tvl7rnnvwpmaivcnflho(self):
        """[移交]-移交质检"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.tvl7rnnvwpmaivcnflho()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_y1f0go3apyd2gpjhtp6e(self):
        """[移交]-移交不同接收人"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.y1f0go3apyd2gpjhtp6e()
        res = [lambda: self.pc.yTiuCZ(createTime='now', statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cwwg81c7fuxew6ohcyna(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.cwwg81c7fuxew6ohcyna()
        res = [lambda: self.pc.xl40Pj(articlesNo=cached('i'))]
        self.assert_all(*res)


class TestGdEv5r5i(BaseCase, unittest.TestCase):
    """配件管理|移交接收管理|移交记录"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.BVA8mmtbcT()
        else:
            return attachment_p.H2VfJncOV57(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0bs0gqufrf2alobu8ypuc(self):
        """[导出]"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations(login='main')
        case.bs0gqufrf2alobu8ypuc()
        res = [lambda: self.pc.T241Se(state=2, createTime='now', name='导出配件移交单列表')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_z36rbt8nuevvk5zw0ev1(self):
        """[批量取消移交]"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.z36rbt8nuevvk5zw0ev1()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_dk81rtdv2rvc2fjer6m8(self):
        """[取消移交]"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.dk81rtdv2rvc2fjer6m8()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sdl1o9ghd61tojp5ap48(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.sdl1o9ghd61tojp5ap48()
        res = [lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_evbb4ktxeipdare0ybrf(self):
        """[搜索]-移交单号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.evbb4ktxeipdare0ybrf()
        res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hpjacvh5iwz7rzgwap4(self):
        """[搜索]-移交单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym', 'KDsB'])
            case = self.common_operations()
            case.hpjacvh5iwz7rzgwap4()
            res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'))]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym', 'KDsB'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.hpjacvh5iwz7rzgwap4(status)
                res = [lambda s=status: self.pc.yTiuCZ(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_v3j4micfjps17busi402(self):
        """[搜索]-移交人"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.v3j4micfjps17busi402()
        res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'), distributorName=INFO['customer_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pudb09khr1ozo3wwci4a(self):
        """[搜索]-接收人"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.pudb09khr1ozo3wwci4a()
        res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'), receiveName=INFO['special_account_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rf7nygh1xebifff8bl22(self):
        """[搜索]-移交时间"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.rf7nygh1xebifff8bl22()
        res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'), createTime='now')]
        self.assert_all(*res)


class TestVvKDYonu(BaseCase, unittest.TestCase):
    """配件管理|配件库存|库存列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.NccuqXjU5C()
        else:
            return attachment_p.Ze2iqsn6eIM(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0abuhabsmqfhq1ut9qc3c(self):
        """[物品信息编辑]"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations(login='main')
        case.abuhabsmqfhq1ut9qc3c()
        res = [lambda: self.pc.H13p6B(brandName='华为', articlesTypeName='手机', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oohakdwo34k03yybh9s8(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.oohakdwo34k03yybh9s8()
        res = [lambda: self.pc.H13p6B(articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pn81zph6ujrzvf8p5qxw(self):
        """[搜索]-供应商"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.pn81zph6ujrzvf8p5qxw()
        res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), supplierName=INFO['main_supplier_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fiy75muh6gz6nsyhyah6(self):
        """[搜索]-所属人"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.fiy75muh6gz6nsyhyah6()
        res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), userName=INFO['customer_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_lqdftflzdi25uvz52b4z(self):
        """[搜索]-采购单号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.lqdftflzdi25uvz52b4z()
        res = [lambda: self.pc.H13p6B(purchaseNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_j4r6o9x82lrhfgn7houk(self):
        """[搜索]-采购人员"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.j4r6o9x82lrhfgn7houk()
        res = [lambda: self.pc.H13p6B(purchaseNo=cached('i'), purchaseName=INFO['customer_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_awfdfgrvu5yt8ocg4om9(self):
        """[搜索]-采购时间"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.awfdfgrvu5yt8ocg4om9()
        res = [lambda: self.pc.H13p6B(purchaseNo=cached('i'), purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ie8fsxmabji7a7q54r1w(self):
        """[搜索]-配件分类"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.ie8fsxmabji7a7q54r1w()
        res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), accessoryTypeStr='内配类')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tje23q2s5q19u1i0r264(self):
        """[搜索]-库存状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym'])
            case = self.common_operations()
            case.tje23q2s5q19u1i0r264()
            res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), inventoryStatus='2')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.tje23q2s5q19u1i0r264(status)
                res = [lambda s=status: self.pc.H13p6B(i=s, inventoryStatus=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_utqrzheihgso0dngmplj(self):
        """[搜索]-品类"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym'])
            case = self.common_operations()
            case.utqrzheihgso0dngmplj()
            res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), articlesTypeId='1')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym'])
            for type_id in DICT_DATA['f']:
                case = self.common_operations()
                case.utqrzheihgso0dngmplj(type_id)
                res = [lambda s=type_id: self.pc.H13p6B(j=s, articlesTypeId=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vfi204ksnbxzyybqadvh(self):
        """[搜索]-品牌型号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.vfi204ksnbxzyybqadvh()
        res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), articlesTypeId='1', brandId='8', modelId='18111')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_x1coaubd9r45peqs8hua(self):
        """[搜索]-流转仓库"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.x1coaubd9r45peqs8hua()
        res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), warehouseName=INFO['main_warehouse_name'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tlfu0zq3fcj6qj4k4v02(self):
        """[搜索]-配件名称"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.tlfu0zq3fcj6qj4k4v02()
        res = [lambda: self.pc.H13p6B(accessoryName=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_je9vs9v7ryk65bgnpnrt(self):
        """[搜索]-配件成色"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym'])
            case = self.common_operations()
            case.je9vs9v7ryk65bgnpnrt()
            res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), accessoryQualityStr='新配件')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym'])
            for color in DICT_DATA['g']:
                case = self.common_operations()
                case.je9vs9v7ryk65bgnpnrt(color)
                res = [lambda s=color: self.pc.H13p6B(m=s, accessoryQuality=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_is3591xz3eohk67pi7h9(self):
        """[搜索]-配件编号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.is3591xz3eohk67pi7h9()
        res = [lambda: self.pc.H13p6B(accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('搜不到列表数据')
    def test_d41766ll2lal2a6qly54(self):
        """[搜索]-库存时长"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.d41766ll2lal2a6qly54()
        res = [lambda: self.pc.H13p6B(accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wuufeqpw5tq8hy6290ce(self):
        """[搜索]-配件渠道"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym'])
            case = self.common_operations()
            case.wuufeqpw5tq8hy6290ce()
            res = [lambda: self.pc.H13p6B(articlesNo=cached('i'), channelStr='原厂')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym'])
            for channel in DICT_DATA['g']:
                case = self.common_operations()
                case.wuufeqpw5tq8hy6290ce(channel)
                res = [lambda s=channel: self.pc.H13p6B(a=s, channelType=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_u6a07svx0rwzn93bn54o(self):
        """[配件销售]快递易-已收款"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.u6a07svx0rwzn93bn54o()
        res = [lambda: self.pc.nbxNKL(createTime='now', deliveryNum=1),
               lambda: self.pc.nbxNKL(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_s4ix3uhl32fhg96aeiis(self):
        """[配件销售]-普通快递-未收款"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.s4ix3uhl32fhg96aeiis()
        res = [lambda: self.pc.nbxNKL(createTime='now', deliveryNum=1),
               lambda: self.pc.nbxNKL(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oqmc5nwi0399dzltytx2(self):
        """[批量移交]-移交物品给库存配件"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.oqmc5nwi0399dzltytx2()
        res = [lambda: self.pc.yTiuCZ(statusStr='待接收'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_saaotn9359y5rsz0php1(self):
        """[批量移交]-移交物品给采购售后"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.saaotn9359y5rsz0php1()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_lrfqyoilnhzw2ejk659d(self):
        """[批量移交]-移交物品给销售"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.lrfqyoilnhzw2ejk659d()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_v60oxil51ddo2si7jl7x(self):
        """[批量移交]-移交物品给送修"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.v60oxil51ddo2si7jl7x()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_p3vluvp1sur9pfwpeyrh(self):
        """[批量移交]-移交物品给维修"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.p3vluvp1sur9pfwpeyrh()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_icdh72iujmalc7gukwol(self):
        """[批量移交]-移交物品给质检"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.icdh72iujmalc7gukwol()
        res = [lambda: self.pc.yTiuCZ(statusStr='已取消'),
               lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_r5gxaxtpflvd7qfj153k(self):
        """[物品详情]-修改物品信息"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.r5gxaxtpflvd7qfj153k()
        res = [lambda: self.pc.H13p6B(brandName='华为', articlesTypeName='手机', articlesNo=cached('i'))]
        self.assert_all(*res)


class TestTdU6oAvC(BaseCase, unittest.TestCase):
    """配件管理|配件维护"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.A3AKRuhANY()
        else:
            return attachment_p.MOknFMNUFIv(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0vnsg549qqo4e8la9pvyz(self):
        """[新增]品类外配类"""
        case = self.common_operations(login='idle')
        case.vnsg549qqo4e8la9pvyz()
        res = [lambda: self.pc.dPrUg2(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sk6ol090tlyb6qyetwl2(self):
        """[新增]品类内配类"""
        case = self.common_operations()
        case.sk6ol090tlyb6qyetwl2()
        res = [lambda: self.pc.dPrUg2(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_e8rzsfkgsktqcjm31vfu(self):
        """[编辑]修改配件名称"""
        self.pre.operations(data=['yNNo'])
        case = self.common_operations()
        case.e8rzsfkgsktqcjm31vfu()
        res = [lambda: self.pc.dPrUg2(headers='idle', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_u8m46ujx2im1noarlsmu(self):
        """[编辑]删除配件名称"""
        self.pre.operations(data=['yNNo'])
        case = self.common_operations()
        case.u8m46ujx2im1noarlsmu()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fd2dzuppjfcy0vc68osp(self):
        """[搜索]-配件编号"""
        self.pre.operations(data=['yNNo'])
        case = self.common_operations()
        case.fd2dzuppjfcy0vc68osp()
        res = [lambda: self.pc.dPrUg2(headers='idle', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oqclfc811pbxjb1ydmtf(self):
        """[搜索]-配件名称"""
        self.pre.operations(data=['yNNo'])
        case = self.common_operations()
        case.oqclfc811pbxjb1ydmtf()
        res = [lambda: self.pc.dPrUg2(headers='idle', accessoryName=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uxs5seo7otyrzfugdqsl(self):
        """[搜索]-状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['yNNo'])
            case = self.common_operations()
            case.uxs5seo7otyrzfugdqsl()
            res = [lambda: self.pc.dPrUg2(headers='idle', accessoryName=cached('i'), status='1')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['yNNo'])
            for status in DICT_DATA['h']:
                case = self.common_operations()
                case.uxs5seo7otyrzfugdqsl(status)
                res = [lambda s=status: self.pc.dPrUg2(headers='idle', i=s, status=s)]
                self.assert_all(*res)


class TestjxkIdfCW(BaseCase, unittest.TestCase):
    """配件管理|入库管理|旧配件入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.HkVg66f8Mk()
        else:
            return attachment_p.Ud4EebvDnHM(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sPBqvfYc9boVR4rGIL4w(self):
        """[新建入库]手机-确认入库"""
        case = self.common_operations(login='main')
        case.sPBqvfYc9boVR4rGIL4w()
        res = [lambda: self.pc.ZFsvTM(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zq8av7DX7E15sOdOA5na(self):
        """[新建入库]1000个数量手机-确认入库"""
        case = self.common_operations()
        case.zq8av7DX7E15sOdOA5na()
        res = [lambda: self.pc.ZFsvTM(accessoryNum=1000, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NIg8OImrULuxaaLnvprF(self):
        """[新建入库]平板电脑-确认入库"""
        case = self.common_operations()
        case.NIg8OImrULuxaaLnvprF()
        res = [lambda: self.pc.ZFsvTM(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_V7VzYOhxyeCqh4OaUKh3(self):
        """[新建入库]笔记本电脑-确认入库"""
        case = self.common_operations()
        case.V7VzYOhxyeCqh4OaUKh3()
        res = [lambda: self.pc.ZFsvTM(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_PMcmyjds8q4To8x1WYWe(self):
        """[新建入库]智能手表-确认入库"""
        case = self.common_operations()
        case.PMcmyjds8q4To8x1WYWe()
        res = [lambda: self.pc.ZFsvTM(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rXmtCESQnyljezY5hqQF(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['YqTl'])
        case = self.common_operations()
        case.rXmtCESQnyljezY5hqQF()
        res = [lambda: self.pc.ZFsvTM(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_BBRaKuLnfUAs23bBdW7L(self):
        """[搜索]-入库单号"""
        self.pre.operations(data=['YqTl'])
        case = self.common_operations()
        case.BBRaKuLnfUAs23bBdW7L()
        res = [lambda: self.pc.ZFsvTM(orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_whT4XzVC2HWmjrLwPGbu(self):
        """[搜索]-流转仓库"""
        self.pre.operations(data=['YqTl'])
        case = self.common_operations()
        case.whT4XzVC2HWmjrLwPGbu()
        res = [lambda: self.pc.ZFsvTM(orderNo=cached('i'), warehouseId=INFO['main_in_warehouse_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sJy6JWqmmKyM7r2DjLiS(self):
        """[搜索]-入库人"""
        self.pre.operations(data=['YqTl'])
        case = self.common_operations()
        case.sJy6JWqmmKyM7r2DjLiS()
        res = [lambda: self.pc.ZFsvTM(orderNo=cached('i'), userId=INFO['special_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WbSFKLvOUocIJPFJCwVb(self):
        """[搜索]-入库时间"""
        self.pre.operations(data=['YqTl'])
        case = self.common_operations()
        case.WbSFKLvOUocIJPFJCwVb()
        res = [lambda: self.pc.ZFsvTM(orderNo=cached('i'), createTime='now')]
        self.assert_all(*res)


class Testjj1YO2vM(BaseCase, unittest.TestCase):
    """配件管理|入库管理|分拣列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.ZgkiOAdiZt()
        else:
            return attachment_p.ZSRzZe4N9Tb(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0BJG1WPKutnjPESnRiaE3(self):
        """[导出全部]"""
        case = self.common_operations(login='main')
        case.BJG1WPKutnjPESnRiaE3()
        res = [lambda: self.pc.T241Se(state=2, createTime='now', name='待分拣列表数据导出')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_kieRlhO7K2AGuSdQH9b3(self):
        """[搜索]-快递单号"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.kieRlhO7K2AGuSdQH9b3()
        res = [lambda: self.pc.Dp7Ih9(logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bOxmYfGUFrevxZUW1A6G(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.bOxmYfGUFrevxZUW1A6G()
        res = [lambda: self.pc.znEgfM(articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gMjMJ10FSSvSiwf8JbsW(self):
        """[搜索]-业务单号"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.gMjMJ10FSSvSiwf8JbsW()
        res = [lambda: self.pc.znEgfM(businessNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_x2I7I6LSgnOWJ5UfzkPs(self):
        """[搜索]-分拣状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['jVML'])
            case = self.common_operations()
            case.x2I7I6LSgnOWJ5UfzkPs()
            res = [lambda: self.pc.Dp7Ih9(logisticsNo=cached('i'), status='1')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['jVML'])
            for status in DICT_DATA['g']:
                case = self.common_operations()
                case.x2I7I6LSgnOWJ5UfzkPs(status)
                res = [lambda s=status: self.pc.Dp7Ih9(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_BnQQG1HUn8tvq1ZjDMCV(self):
        """[搜索]-分拣时间"""
        self.pre.operations(data=['jVML', 'LJs9'])
        case = self.common_operations()
        case.BnQQG1HUn8tvq1ZjDMCV()
        res = [lambda: self.pc.znEgfM(logisticsNo=cached('i'), sortationTime='now')]
        self.assert_all(*res)


class TestuILxtEO4(BaseCase, unittest.TestCase):
    """配件管理|配件采购|新增采购单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.EdqL4NE5hk()
        else:
            return attachment_p.NeDm1H7FxRQ(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0rYvpUsdluGutOhIhm7af(self):
        """[新增]平板电脑-已付款在路上-确定生成采购单"""
        case = self.common_operations(login='main')
        case.rYvpUsdluGutOhIhm7af()
        res = [lambda: self.pc.HQ55MW(stateStr='已发货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_niKwILpBHogDvGt52uEB(self):
        """[新增]手机-未付款已到货-确定生成采购单"""
        case = self.common_operations()
        case.niKwILpBHogDvGt52uEB()
        res = [lambda: self.pc.HQ55MW(stateStr='已收货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_nBfEGGe1LJguXHi6aesS(self):
        """[新增]笔记本电脑-未付款在路上-确定生成采购单"""
        case = self.common_operations()
        case.nBfEGGe1LJguXHi6aesS()
        res = [lambda: self.pc.HQ55MW(stateStr='已发货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fi51E5jCFUxE1nLYPO7w(self):
        """[新增]智能手表-已付款已到货-确定生成采购单"""
        case = self.common_operations()
        case.fi51E5jCFUxE1nLYPO7w()
        res = [lambda: self.pc.HQ55MW(stateStr='已收货', purchaseTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qyeHP1UKtW02kXOihCU1(self):
        """[新增]手机1000个物品-确定生成采购单"""
        case = self.common_operations()
        case.qyeHP1UKtW02kXOihCU1()
        res = [lambda: self.pc.HQ55MW(stateStr='已收货', copeNum='1000')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Cd8pPBeDJMVuZBrTbFXN(self):
        """[新增]批量添加-确定生成采购单"""
        case = self.common_operations()
        case.Cd8pPBeDJMVuZBrTbFXN()
        res = [lambda: self.pc.HQ55MW(stateStr='已发货', copeNum='2')]
        self.assert_all(*res)


class TestpFybYoGx(BaseCase, unittest.TestCase):
    """配件管理|配件采购|采购列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.Kxg46XEPdY()
        else:
            return attachment_p.CrIo44NXokZ(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0ytFlEaPZYL2krOQHCL4y(self):
        """[采购售后]快递易-采购退货退款"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations(login='main')
        case.ytFlEaPZYL2krOQHCL4y()
        res = [lambda: self.pc.uzsnM0(saleStateStr='采购退货退款', createTime='now'),
               lambda: self.pc.uzsnM0(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DUKh4wv9QHERfWyZo08U(self):
        """[采购售后]普通快递-采购退货退款"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.DUKh4wv9QHERfWyZo08U()
        res = [lambda: self.pc.uzsnM0(saleStateStr='采购退货退款', createTime='now'),
               lambda: self.pc.uzsnM0(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_kuo3zYG5OY6r1J5GFLwS(self):
        """[采购售后]部分金额退差价"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.kuo3zYG5OY6r1J5GFLwS()
        res = [lambda: self.pc.uzsnM0(saleStateStr='采购退差价', createTime='now'),
               lambda: self.pc.uzsnM0(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_lQzjFGvhm78QmpH58t8f(self):
        """[采购售后]-添加物品退货退款"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.lQzjFGvhm78QmpH58t8f()
        res = [lambda: self.pc.uzsnM0(saleStateStr='采购退货退款', createTime='now'),
               lambda: self.pc.uzsnM0(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rNxmjG3kaLQP30Voi9tR(self):
        """[采购售后]-全部金额退差价"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.rNxmjG3kaLQP30Voi9tR()
        res = [lambda: self.pc.uzsnM0(saleStateStr='采购退差价', createTime='now'),
               lambda: self.pc.uzsnM0(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_OCChvTOX3BOwhsZ3x1Vk(self):
        """[搜索]-采购单号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.OCChvTOX3BOwhsZ3x1Vk()
        res = [lambda: self.pc.HQ55MW(orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_YHUNy8WSwZqIFfM88jqk(self):
        """[搜索]-采购供应商"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.YHUNy8WSwZqIFfM88jqk()
        res = [lambda: self.pc.HQ55MW(orderNo=cached('i'), supplierId=INFO['main_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_art1lLuMH6tdwDoJNCVF(self):
        """[搜索]-采购单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym'])
            case = self.common_operations()
            case.art1lLuMH6tdwDoJNCVF()
            res = [lambda: self.pc.HQ55MW(orderNo=cached('i'), stateStr='已收货')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym'])
            for state in DICT_DATA['i']:
                case = self.common_operations()
                case.art1lLuMH6tdwDoJNCVF(state)
                res = [lambda s=state: self.pc.HQ55MW(i=s, state=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_L2C0xDrhKPDjvib6JES4(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.L2C0xDrhKPDjvib6JES4()
        res = [lambda: self.pc.HQ55MW(logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aa4ufzsTKdxHRDOhwcsN(self):
        """[搜索]-付款状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym'])
            case = self.common_operations()
            case.aa4ufzsTKdxHRDOhwcsN()
            res = [lambda: self.pc.HQ55MW(orderNo=cached('i'), payStateStr='未付款')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym'])
            for pay in DICT_DATA['g']:
                case = self.common_operations()
                case.aa4ufzsTKdxHRDOhwcsN(pay)
                res = [lambda s=pay: self.pc.HQ55MW(j=s, payState=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uTH0rGcq6USIvzBzwnqn(self):
        """[搜索]-采购人"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.uTH0rGcq6USIvzBzwnqn()
        res = [lambda: self.pc.HQ55MW(orderNo=cached('i'), userId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Q66Jftlrzxz0MflmYaRr(self):
        """[搜索]-采购时间"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.Q66Jftlrzxz0MflmYaRr()
        res = [lambda: self.pc.HQ55MW(orderNo=cached('i'), purchaseTime='now')]
        self.assert_all(*res)


class TestOxu6qhVX(BaseCase, unittest.TestCase):
    """配件管理|移交接收管理|接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.TYqfRUwK8U()
        else:
            return attachment_p.VbLUqADcDi7(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0YGHj7l8L8BkOXk1wxK6L(self):
        """[物品接收]-移交库存配件-接收"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations(login='main')
        case.YGHj7l8L8BkOXk1wxK6L()
        res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'), statusStr='已接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NtgvclPRpONVaNJTp0yA(self):
        """[物品接收]-扫码精确接收"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.NtgvclPRpONVaNJTp0yA()
        res = [lambda: self.pc.yTiuCZ(data='a', articlesNo=cached('i'), statusStr='已接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_J8ahGmCVn2GdPlK8RMlj(self):
        """[移交单接收]-接收"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.J8ahGmCVn2GdPlK8RMlj()
        res = [lambda: self.pc.yTiuCZ(orderNo=cached('i'), statusStr='已接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ODJ550O1VM3zMxrPPETO(self):
        """[移交单接收]-导出"""
        case = self.common_operations()
        case.ODJ550O1VM3zMxrPPETO()
        res = [lambda: self.pc.T241Se(state=2, createTime='now', name='导出接收单列表')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wJXR0rLyC9FiD2Hab2GK(self):
        """[搜索]-物品接收-物品编号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.wJXR0rLyC9FiD2Hab2GK()
        res = [lambda: self.pc.wb3p9S(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vKg2HxGmBKyPPtp6kJf7(self):
        """[搜索]-物品接收-品类品牌型号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.vKg2HxGmBKyPPtp6kJf7()
        res = [lambda: self.pc.wb3p9S(data='a', articlesNo=cached('i'), brandName='华为', articlesTypeName='手机', modelName='Pocket 2 优享版')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gyC9dbIGUhd7LCpcYvDF(self):
        """[搜索]-物品接收-移交人"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.gyC9dbIGUhd7LCpcYvDF()
        res = [lambda: self.pc.wb3p9S(data='a', articlesNo=cached('i'), deliveryId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_L4sWT7EPZcuwuxZX1mLK(self):
        """[搜索]-物品接收-接收人"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.L4sWT7EPZcuwuxZX1mLK()
        res = [lambda: self.pc.wb3p9S(data='a', articlesNo=cached('i'), userId=INFO['special_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZitlblU4lMp7BYK8ANyM(self):
        """[搜索]-物品接收-移交时间"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.ZitlblU4lMp7BYK8ANyM()
        res = [lambda: self.pc.wb3p9S(data='a', articlesNo=cached('i'), deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vRCdl2fqoKNJpFGdRzRD(self):
        """[搜索]-物品接收-移交单号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.vRCdl2fqoKNJpFGdRzRD()
        res = [lambda: self.pc.wb3p9S(data='a', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Vzw0lwBx2ZAyHWSrX6RQ(self):
        """[搜索]-移交单接收-物品编号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.Vzw0lwBx2ZAyHWSrX6RQ()
        res = [lambda: self.pc.wb3p9S(data='a', articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UF6kXeN3uHtmuNDjeKwu(self):
        """[搜索]-移交单接收-移交单号"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.UF6kXeN3uHtmuNDjeKwu()
        res = [lambda: self.pc.wb3p9S(orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_un6reo9grtxgYp8gEDjc(self):
        """[搜索]-移交单接收-移交单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym', 'KDsB'])
            case = self.common_operations()
            case.un6reo9grtxgYp8gEDjc()
            res = [lambda: self.pc.wb3p9S(orderNo=cached('i'), statusStr='待接收')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym', 'KDsB'])
            for status in DICT_DATA['b']:
                case = self.common_operations()
                case.un6reo9grtxgYp8gEDjc(status)
                res = [lambda s=status: self.pc.wb3p9S(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_byg7MwSRAnzhwUDcj1Wk(self):
        """[搜索]-移交单接收-移交人"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.byg7MwSRAnzhwUDcj1Wk()
        res = [lambda: self.pc.wb3p9S(orderNo=cached('i'), distributorId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_stvghsNX2dN5itJABNYT(self):
        """[搜索]-移交单接收-接收人"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.stvghsNX2dN5itJABNYT()
        res = [lambda: self.pc.wb3p9S(orderNo=cached('i'), receiveId=INFO['special_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sn75xNW4A5LGaJtgZiQV(self):
        """[搜索]-移交单接收-移交时间"""
        self.pre.operations(data=['bAym', 'KDsB'])
        case = self.common_operations()
        case.sn75xNW4A5LGaJtgZiQV()
        res = [lambda: self.pc.wb3p9S(orderNo=cached('i'), createTime='now')]
        self.assert_all(*res)


class TestJv7ecOvs(BaseCase, unittest.TestCase):
    """配件管理|配件销售|销售列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.R3Xo25O7tV()
        else:
            return attachment_p.LrWfCZFWG8G(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0H4KdZEXetFlTiBVp1fME(self):
        """[配件销售]快递易-未收款-部分销售金额"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations(login='main')
        case.H4KdZEXetFlTiBVp1fME()
        res = [lambda: self.pc.nbxNKL(createTime='now'),
               lambda: self.pc.nbxNKL(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ye7ARAsQ9uacwEptFiSV(self):
        """[配件销售]快递易-未收款-销售金额最大值"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.ye7ARAsQ9uacwEptFiSV()
        res = [lambda: self.pc.nbxNKL(createTime='now'),
               lambda: self.pc.nbxNKL(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ivhxLmwFUYJ160MKBThl(self):
        """[配件销售]普通物流-未收款-部分销售金额"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.ivhxLmwFUYJ160MKBThl()
        res = [lambda: self.pc.nbxNKL(createTime='now'),
               lambda: self.pc.nbxNKL(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_btbwOSZldzzeYBn6qsYo(self):
        """[配件销售]-普通快递-已收款"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.btbwOSZldzzeYBn6qsYo()
        res = [lambda: self.pc.nbxNKL(createTime='now'),
               lambda: self.pc.nbxNKL(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bovLHIlzJSfrRryibqyF(self):
        """[销售售后]-退货退款-未收货"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.bovLHIlzJSfrRryibqyF()
        res = [lambda: self.pc.rmoeta(createTime='now', sellTypeName='退货退款'),
               lambda: self.pc.rmoeta(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oe82ledRfRK4B7jiOSVc(self):
        """[销售售后]-退货退款-已收货"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.oe82ledRfRK4B7jiOSVc()
        res = [lambda: self.pc.rmoeta(createTime='now', sellTypeName='退货退款'),
               lambda: self.pc.rmoeta(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hBh7ycF1AumEt4nXwMyZ(self):
        """[销售售后]-部分金额退差价"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.hBh7ycF1AumEt4nXwMyZ()
        res = [lambda: self.pc.rmoeta(createTime='now', sellTypeName='退差价'),
               lambda: self.pc.rmoeta(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_dvDaOWftNEncBuIMeo7h(self):
        """[销售售后]-全部金额退差价"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.dvDaOWftNEncBuIMeo7h()
        res = [lambda: self.pc.rmoeta(createTime='now', sellTypeName='退差价'),
               lambda: self.pc.rmoeta(data='a', accessoryNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JufIUEkkoghm3ZPziz11(self):
        """[搜索]-销售单号"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.JufIUEkkoghm3ZPziz11()
        res = [lambda: self.pc.nbxNKL(orderNo=cached('i'), createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_U9NQEB15gOzUs1kWPzHL(self):
        """[搜索]-客户"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.U9NQEB15gOzUs1kWPzHL()
        res = [lambda: self.pc.nbxNKL(orderNo=cached('i'), saleSupplierId=INFO['main_sale_supplier_id'], createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hVsGoqqW3itUAfALyFs8(self):
        """[搜索]-收款状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym', 'Ab3A'])
            case = self.common_operations()
            case.hVsGoqqW3itUAfALyFs8()
            res = [lambda: self.pc.nbxNKL(orderNo=cached('i'), statusStr='未收款', createTime='now')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym', 'Ab3A'])
            for status in DICT_DATA['g']:
                case = self.common_operations()
                case.hVsGoqqW3itUAfALyFs8(status)
                res = [lambda s=status: self.pc.nbxNKL(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aSQHqjds3CGl32QrMMgp(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.aSQHqjds3CGl32QrMMgp()
        res = [lambda: self.pc.nbxNKL(logisticsNo=cached('i'), createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Rd9OUwhBuPlpGWYEzDoo(self):
        """[搜索]-操作时间"""
        self.pre.operations(data=['bAym', 'Ab3A'])
        case = self.common_operations()
        case.Rd9OUwhBuPlpGWYEzDoo()
        res = [lambda: self.pc.nbxNKL(orderNo=cached('i'), createTime='now')]
        self.assert_all(*res)


class TestKZ6SyR4M(BaseCase, unittest.TestCase):
    """配件管理|入库管理|新到货入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.OS9qwvYXb5()
        else:
            return attachment_p.HTP9XkLGQNT(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0k75gfpU0uyhS1aEhcD2Y(self):
        """[签收入库]-搜索物流单号-暂不操作"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations(login='main')
        case.k75gfpU0uyhS1aEhcD2Y()
        res = [lambda: self.pc.Dp7Ih9(statusStr='已分拣', sortationTime='now', logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Jslqnx0TJYAcPWsTNgWG(self):
        """[签收入库]-搜索物流单号-入库并移交"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.Jslqnx0TJYAcPWsTNgWG()
        res = [lambda: self.pc.Dp7Ih9(statusStr='已分拣', sortationTime='now', logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pZnZ4E4EWsok60VOwAt0(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.pZnZ4E4EWsok60VOwAt0()
        res = [lambda: self.pc.znEgfM(logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ddwluOeEUDWfjvQcXtFf(self):
        """[搜索]-物品编号"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.ddwluOeEUDWfjvQcXtFf()
        res = [lambda: self.pc.znEgfM(articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZHplaC78vCAAs9nTV3tu(self):
        """[搜索]-业务单号"""
        self.pre.operations(data=['jVML'])
        case = self.common_operations()
        case.ZHplaC78vCAAs9nTV3tu()
        res = [lambda: self.pc.znEgfM(businessNo=cached('i'))]
        self.assert_all(*res)


class TestpRxjsNhJ(BaseCase, unittest.TestCase):
    """配件管理|配件库存|库存调拨"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.KofyeHTY2V()
        else:
            return attachment_p.P6xNXMkC4fE(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0AdqaPYO38jf7TVM9akKm(self):
        """[新增调拨]快递易-搜索添加物品"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations(login='main')
        case.AdqaPYO38jf7TVM9akKm()
        res = [lambda: self.pc.we4jOX(statusStr='待接收', createTime='now'),
               lambda: self.pc.we4jOX(data='a', itemList_articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UXuoreny4UjWmENBXQgX(self):
        """[新增调拨]-多物品调拨"""
        self.pre.operations(data=['bAym', 'bAym'])
        case = self.common_operations()
        case.UXuoreny4UjWmENBXQgX()
        res = [lambda: self.pc.we4jOX(statusStr='待接收', createTime='now', number=2)]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NvbF3ZipfMr4hBRl0nQ1(self):
        """[新增调拨]-导入添加物品"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.NvbF3ZipfMr4hBRl0nQ1()
        res = [lambda: self.pc.we4jOX(statusStr='待接收', createTime='now'),
               lambda: self.pc.we4jOX(data='a', itemList_articlesNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zwNZnOUV0fJtHzKSpk1f(self):
        """[新增调拨]-选择添加物品"""
        self.pre.operations(data=['bAym'])
        case = self.common_operations()
        case.zwNZnOUV0fJtHzKSpk1f()
        res = [lambda: self.pc.we4jOX(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vy4GQrC9c2PByhpKlKX7(self):
        """[接收]"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.vy4GQrC9c2PByhpKlKX7()
        res = [lambda: self.pc.we4jOX(statusStr='已完成', createTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HYzXRVJ2N0MDfAwPg4mA(self):
        """[扫码接收]-添加物品-接收入库"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.HYzXRVJ2N0MDfAwPg4mA()
        res = [lambda: self.pc.we4jOX(statusStr='已完成', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SfRJFEo1omEqQEMXCt1A(self):
        """[撤销]"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.SfRJFEo1omEqQEMXCt1A()
        res = [lambda: self.pc.we4jOX(statusStr='已撤销', createTime='now', orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_U2Z6NYRuai5n0iI9gc5N(self):
        """[导出]"""
        case = self.common_operations()
        case.U2Z6NYRuai5n0iI9gc5N()
        res = [lambda: self.pc.T241Se(state=2, createTime='now', name='配件调拨导出')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_irVf881IgnSudhdqrzNT(self):
        """[搜索]-调拨单号"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.irVf881IgnSudhdqrzNT()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uxleDdCbgv5xe0Yh9ihY(self):
        """[搜索]-调出仓库"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.uxleDdCbgv5xe0Yh9ihY()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'), outWarehouseId=INFO['main_warehouse_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_GEzDUNHZDHJGT31d5arP(self):
        """[搜索]-调入仓库"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.GEzDUNHZDHJGT31d5arP()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'), inWarehouseId=INFO['main_item_in_warehouse_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ykbpvOAyRCpcWTc8FTo0(self):
        """[搜索]-调拨人"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.ykbpvOAyRCpcWTc8FTo0()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'), userId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_N7hyMWrgBhZs95uhMTfo(self):
        """[搜索]-接收状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym', 'PBkr'])
            case = self.common_operations()
            case.N7hyMWrgBhZs95uhMTfo()
            res = [lambda: self.pc.we4jOX(orderNo=cached('i'), statusStr='待接收')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym', 'PBkr'])
            for status in DICT_DATA['c']:
                case = self.common_operations()
                case.N7hyMWrgBhZs95uhMTfo(status)
                res = [lambda s=status: self.pc.we4jOX(i=s, status=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gMOD5rLLkrIFYE4i7uWv(self):
        """[搜索]-最新操作人"""
        self.pre.operations(data=['bAym', 'PBkr', 'yQq9'])
        case = self.common_operations()
        case.gMOD5rLLkrIFYE4i7uWv()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'), receiveUserId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qUeEiqtgrjyltpAB3WwJ(self):
        """[搜索]-创建时间"""
        self.pre.operations(data=['bAym', 'PBkr'])
        case = self.common_operations()
        case.qUeEiqtgrjyltpAB3WwJ()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'), createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_boCbPTo0KQQbybfPC7Dp(self):
        """[搜索]-最新操作时间"""
        self.pre.operations(data=['bAym', 'PBkr', 'yQq9'])
        case = self.common_operations()
        case.boCbPTo0KQQbybfPC7Dp()
        res = [lambda: self.pc.we4jOX(orderNo=cached('i'), updateTime='now')]
        self.assert_all(*res)


class Testadmrcujl(BaseCase, unittest.TestCase):
    """配件管理|配件销售|销售售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return attachment_r.A1SFjHxpUV()
        else:
            return attachment_p.S250zQ3JaPt(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_0fQ4Cx53aMDNueSRTtdCt(self):
        """[搜索]-售后单号"""
        self.pre.operations(data=['bAym', 'Ab3A', 'GM4P'])
        case = self.common_operations(login='main')
        case.fQ4Cx53aMDNueSRTtdCt()
        res = [lambda: self.pc.rmoeta(orderNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_M2uPO43Gwj1MxRNJdmCn(self):
        """[搜索]-移交单状态"""
        if self.auto_type == 'ui':
            self.pre.operations(data=['bAym', 'Ab3A', 'GM4P'])
            case = self.common_operations()
            case.M2uPO43Gwj1MxRNJdmCn()
            res = [lambda: self.pc.rmoeta(orderNo=cached('i'), sellTypeName='退差价')]
            self.assert_all(*res)
        else:
            self.pre.operations(data=['bAym', 'Ab3A', 'GM4P'])
            for status in DICT_DATA['g']:
                case = self.common_operations()
                case.M2uPO43Gwj1MxRNJdmCn(status)
                res = [lambda s=status: self.pc.rmoeta(i=s, sellType=s)]
                self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cUNSieph0X3TfNdfkcSr(self):
        """[搜索]-售后客户"""
        self.pre.operations(data=['bAym', 'Ab3A', 'GM4P'])
        case = self.common_operations()
        case.cUNSieph0X3TfNdfkcSr()
        res = [lambda: self.pc.rmoeta(orderNo=cached('i'), sellSupplierId=INFO['main_sale_supplier_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_okQmkaKm4xMprd8BtEc3(self):
        """[搜索]-物流单号"""
        self.pre.operations(data=['bAym', 'yZMr', 'wTnl'])
        case = self.common_operations()
        case.okQmkaKm4xMprd8BtEc3()
        res = [lambda: self.pc.rmoeta(logisticsNo=cached('i'))]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_S5HIKmlK3427TT3VXmlV(self):
        """[搜索]-操作人"""
        self.pre.operations(data=['bAym', 'yZMr', 'wTnl'])
        case = self.common_operations()
        case.S5HIKmlK3427TT3VXmlV()
        res = [lambda: self.pc.rmoeta(logisticsNo=cached('i'), userId=INFO['main_user_id'])]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_XODp5acGT6jdcx10I682(self):
        """[搜索]-操作时间"""
        self.pre.operations(data=['bAym', 'yZMr', 'wTnl'])
        case = self.common_operations()
        case.XODp5acGT6jdcx10I682()
        res = [lambda: self.pc.rmoeta(logisticsNo=cached('i'), createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
