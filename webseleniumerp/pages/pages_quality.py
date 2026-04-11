# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from config.settings import DATA_PATHS
from common.import_desc import *


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'img': os.path.join(DATA_PATHS['excel'], 'img.jpg'),
        }

    def menu(self, menu_type, key):
        """获取元素"""
        menu_mapping = {
            'main': self.elem_positioning['positioning'],
        }
        if menu_type in menu_mapping:
            return self.exc(lambda: menu_mapping[menu_type][key])
        else:
            raise ValueError(f"menu not found: {menu_type}")


class QykEu6IoOjB(CommonPages):
    """质检管理|质检中物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='p5iHsfdQcs4Mf', desc='质检管理')
         .step(key='Eix8SYXhyOSS2', desc='质检中物品')
         .wait())
        return self

    @reset_after_execution
    @doc(TyClpwIrykofhqf4laif)
    def TyClpwIrykofhqf4laif(self):
        self.menu_manage()
        (self.step(key='tD2uki43KuwCn', desc='提交质检结果')
         .scroll('remark', desc='质检备注')
         .step(key='jsfCtfWX5cEzW', value=self.serial, action='input', desc='质检备注')
         .step(key='NXvUPsTHGV1RZ', value=self.file_path('img'), action='upload', desc='上传质检图片')
         .step(key='VD5vU2WIagzdT', value='23', action='input', desc='预售保卖价')
         .scroll(key='m7wf3Fsj6vtQ7', desc='移交库存')
         .step(key='KgcSPFhszJP7g', desc='移交库存')
         .step(key='UFEJIPIy4Akkj', desc='接收人')
         .custom(lambda: self.down_enter())
         .step(key='CJmASiaSKRMX3', value=self.serial, action='input', desc='移交说明')
         .step(key='ilHW6Mtyvtfcx', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(aKblpEyB7wculAa6At1D)
    def aKblpEyB7wculAa6At1D(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=5)[0]['imei'])
        (self.step(key='b0ESL9u2I2t9i', desc='快速质检输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='s38T16i2WkLDb', desc='快速质检')
         .step(key='ow57tGyIbspNl', desc='成色')
         .scroll('remark', desc='质检备注')
         .step(key='r0wi8qdh1oUjB', value='质检备注', action='input', desc='质检备注')
         .step(key='fNRka8oRMe9pZ', value=self.file_path('img'), action='upload', desc='上传质检图片')
         .scroll(key='ea0O7anIxAGlo', desc='预售保卖价')
         .step(key='BaXGGRcF6pm7Z', value='82', action='input', desc='预售保卖价')
         .step(key='Q6hM8xlL6uWcS', desc='移交库存')
         .step(key='G6HoGTtfJ3mUr', desc='接收人')
         .custom(lambda: self.down_enter())
         .step(key='xILWyMl0vYchm', value=self.serial, action='input', desc='移交说明')
         .step(key='Nug9pMqFLw9Ih', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(DvC4kRy5eVWdWGN9cPXB)
    def DvC4kRy5eVWdWGN9cPXB(self):
        self.menu_manage()
        (self.step(key='b98VuhTSEI3LN', desc='单选')
         .step(key='Kk20aR2JyX7DS', desc='未验移交')
         .step(key='Z3CnwKOuKmoNK', desc='移交库存')
         .step(key='QbPW6oiJe9E7H', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='mQi62Dc7vwUcU', value=self.serial, action='input', desc='移交说明')
         .step(key='Pn5hw62f3utqF', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(BHQX5vbmOfBJ4z8CzdvG)
    def BHQX5vbmOfBJ4z8CzdvG(self):
        self.menu_manage()
        (self.step(key='Y9qY0g6qPhnmY', desc='单选')
         .step(key='lftu6qGROUpv0', desc='未验移交')
         .step(key='LyTTdOY7gBOcn', desc='移交采购售后')
         .step(key='OffuhD1rSjnH5', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='WRy7h88AAVrWa', value=self.serial, action='input', desc='移交说明')
         .step(key='Vfcm5kTBD46y5', desc='取消')
         .wait())
        return self


class ZykOkDKuSN0(CommonPages):
    """质检管理|质检内容模版"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='ymtNtKZL2VEfQ', desc='质检管理')
         .step(key='HQjefXC9c6yf9', desc='质检内容模版')
         .wait())
        return self

    @reset_after_execution
    @doc(GySsTzThuG7Y0qU4dr6w)
    def GySsTzThuG7Y0qU4dr6w(self):
        self.menu_manage()
        (self.step(key='bhpoIPCaRBs2a', desc='新增')
         .step(key='r04gxkJttKwKN', value='质检内容名称' + self.serial, action='input', desc='质检内容名称')
         .step(key='bOXWsHUAuySxa', value='分类名称' + self.serial, action='input', desc='分类名称')
         .step(key='XYUaaCd8F64ZT', desc='选项类型')
         .step(key='PQFsIw4eY70ZG', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(giRhsRX1en0Lx6jNhHwp)
    def giRhsRX1en0Lx6jNhHwp(self):
        self.menu_manage()
        (self.step(key='kFTCs993cdIon', desc='编辑')
         .step(key='OZYHm8UTaT7Ec', value='质检内容名称' + self.serial, action='input', desc='质检内容名称')
         .step(key='L5NQoVM4TmWc6', value='分类名称' + self.serial, action='input', desc='分类名称')
         .step(key='R4uSaMLr3mFjU', desc='选项类型')
         .step(key='erf4etE2h0eWp', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(fFy1TGBgZDGQp4384V92)
    def fFy1TGBgZDGQp4384V92(self):
        self.menu_manage()
        (self.step(key='BmB8NSIYqxSZh', desc='删除')
         .step(key='hvKYm9rAHuGNy', desc='确认删除')
         .wait())
        return self


class ImDO8pXuDcy(CommonPages):
    """质检管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='tpZj6Gj9vidTt', desc='质检管理')
         .step(key='oJRQUgKsaXXP8', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(I3DHz0up0R0FCJ93wYgX)
    def I3DHz0up0R0FCJ93wYgX(self):
        self.menu_manage()
        (self.step(key='WUfOwvfNSsnaL', desc='全选')
         .step(key='Bc7alkuUy5fQV', desc='接收')
         .step(key='k47NaYwzwnJIU', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(jWTmru3WQNlJkhaj32WL)
    def jWTmru3WQNlJkhaj32WL(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='blAE89cnLT2ro', desc='扫码精确接收')
         .custom(self.affix_carriage_return)
         .step(key='fZpcE3hBpz5Ta', desc='接收')
         .step(key='YbDjyVroiPrfn', desc='确定')
         .wait())
        return self


class Nr0ncfVwUUT(CommonPages):
    """质检管理|先质检后入库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='yBBh39MdtyxTb', desc='质检管理')
         .step(key='eIWjOvlSdrpnq', desc='先质检后入库')
         .wait())
        return self

    @reset_after_execution
    @doc(cKaXogneNjTTTmAdUTcW)
    def cKaXogneNjTTTmAdUTcW(self):
        self.menu_manage()
        (self.step(key='XtdmAFrG1n4zx', desc='人工快速质检')
         .step(key='H4MHMmgq9SvBn', desc='选择型号')
         .step(key='il2suSWU1uKYH', desc='确定')
         .step(key='YNQ4p55oQhb4D', desc='自动生成imei')
         .step(key='DRdcmO8jAALPG', desc='成色')
         .custom(lambda: self.up_enter())
         .step(key='K7PzjNoXUvYGw', desc='颜色')
         .custom(lambda: self.up_enter())
         .step(key='lYzWbjeUL17Py', desc='rom')
         .custom(lambda: self.up_enter())
         .step(key='m07mYkidesgPS', desc='购买渠道')
         .custom(lambda: self.up_enter())
         .step(key='xg5yMZIIJTdFr', desc='苹果小型号')
         .custom(lambda: self.up_enter())
         .step(key='s7EPmJZrMPzfQ', desc='商品来源')
         .custom(lambda: self.up_enter())
         .scroll('price', desc='预售保卖价')
         .step(key='QUCgIKZ59rgGH', value='52', action='input', desc='预售保卖价')
         .custom(lambda: self.wait_time())
         .step(key='BmxrieoNC336P', desc='提交质检报告')
         .wait())
        return self

    @reset_after_execution
    @doc(m1SZEHq9GOLysyiwTJhR)
    def m1SZEHq9GOLysyiwTJhR(self):
        self.menu_manage()
        (self.step(key='LpYmybYX0XrMt', desc='单选')
         .step(key='ldRUFChcM5UHV', desc='批量采购入库')
         .step(key='C87jRhVLqJ7mT', desc='提交采购入库')
         .step(key='JCmgLlHEf0Yjd', desc='采购供应商')
         .custom(lambda: self.down_enter())
         .step(key='njP5x6Bs8GTEe', desc='采购账号')
         .custom(lambda: self.down_enter())
         .step(key='lhsRNovspLmQs', desc='流转仓库')
         .custom(lambda: self.down_enter())
         .scroll(key='H0eKq1seYyagJ', desc='付款账户')
         .step(key='jNeYBHHXcqAzZ', value='6.12', action='input', desc='付款金额')
         .custom(lambda: self.enter())
         .step(key='jxkkpDKSNYzNd', desc='确定生成采购单')
         .step(key='iLagnjb0t0lg4', desc='流转仓库确定')
         .wait())
        return self

    @reset_after_execution
    @doc(QkyLf7Jg3kvDyadrrVeA)
    def QkyLf7Jg3kvDyadrrVeA(self):
        self.menu_manage()
        (self.step(key='CVH2YqoiHJMOx', desc='采购入库')
         .step(key='yEqCOwJJbrhdp', desc='前往采购入库')
         .custom(lambda: self.wait_time())
         .step(key='I2fYdHQOuoNVH', desc='采购供应商')
         .custom(lambda: self.down_enter())
         .step(key='qoyfsFhUVedS5', desc='采购账号')
         .custom(lambda: self.down_enter())
         .step(key='xxsofbHMLraYD', desc='流转仓库')
         .custom(lambda: self.down_enter())
         .scroll('payment_account', desc='付款账户')
         .step(key='AfSjlDEHAjMbu', value='5.12', action='input', desc='付款金额')
         .custom(lambda: self.enter())
         .step(key='PgJM8Kidhz2mf', desc='确定生成采购单')
         .step(key='wKSqv2DU6dhW1', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(F89aoKW4uHkSuyvilmhi)
    def F89aoKW4uHkSuyvilmhi(self):
        self.menu_manage()
        (self.step(key='pHpwyjz20yCZq', desc='采购入库')
         .step(key='ykdOkotbTeOev', desc='提交采购入库')
         .step(key='jpQ2hQc0x3WLK', desc='采购供应商')
         .custom(lambda: self.down_enter())
         .step(key='n1HYCRDNzIUod', desc='采购账号')
         .custom(lambda: self.down_enter())
         .step(key='XEGJzfeT2CJPA', desc='流转仓库')
         .custom(lambda: self.down_enter())
         .scroll('payment_account', desc='付款账号')
         .step(key='e23iPGkUwqZFA', value='5', action='input', desc='付款金额')
         .custom(lambda: self.enter())
         .step(key='dhFP5UIxvJKiu', desc='确定生成采购单')
         .step(key='GmHgu7AtnNKFQ', desc='快捷操作')
         .custom(lambda: self.up_enter())
         .step(key='p5TEVEZ2sYqw9', desc='确定')
         .scroll('product_picture', desc='商品图片')
         .step(key='Lcpu14iIGjldB', desc='成色等级')
         .custom(lambda: self.up_enter())
         .step(key='Oh3lcJPh59UTx', value=self.number, action='input', desc='销售价')
         .step(key='Pj4c6kglp5hJb', value=self.number, action='input', desc='分佣比例')
         .step(key='tjaPQrV4RITTA', desc='商品图片')
         .step(key='rvuioSFcIHd6W', value=self.file_path('img'), action='upload', desc='上传文件')
         .step(key='VrDFS6BQ8ybdI', desc='确认')
         .step(key='kiaHdexssc7ND', desc='确认上架')
         .wait())
        return self

    @reset_after_execution
    @doc(YXbGCNN4QmspmmrgyGE1)
    def YXbGCNN4QmspmmrgyGE1(self):
        self.menu_manage()
        (self.step(key='SWzy0cflFkY1H', desc='编辑报告')
         .scroll('edit_btn', desc='修改')
         .custom(lambda: self.wait_time())
         .step(key='DYmJaerEIzPmr', desc='重新生成质检报告')
         .step(key='VKBZXpQGBepN2', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(KlvURYJReV7HI5zUM2ZK)
    def KlvURYJReV7HI5zUM2ZK(self):
        self.menu_manage()
        (self.step(key='QDx93X0KnNAoe', desc='编辑报告')
         .scroll('edit_btn', desc='修改')
         .custom(lambda: self.wait_time())
         .step(key='kYiMuLkNXZS0Z', desc='修改当前报告')
         .wait())
        return self


class VJYE0rU1LOg(CommonPages):
    """质检管理|待移交物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='PLLoukxkbCiPq', desc='质检管理')
         .step(key='TflOFBxV1iQae', desc='待移交物品')
         .wait())
        return self

    @reset_after_execution
    @doc(j8LwPxK1SoYZffAVSK0E)
    def j8LwPxK1SoYZffAVSK0E(self):
        self.menu_manage()
        (self.step(key='oGNFMz5ExQ5wd', desc='复检')
         .step(key='eZfte39Hj8qoN', desc='成色')
         .custom(lambda: self.up_enter())
         .step(key='cbvGHtAw6Urq8', desc='颜色')
         .custom(lambda: self.up_enter())
         .step(key='Q8q8iixfdnJXb', desc='商品来源')
         .custom(lambda: self.up_enter())
         .scroll('guaranteed_price', desc='预售保卖价')
         .step(key='GVROVOsbSPTj2', value='23', action='input', desc='预售保卖价')
         .step(key='RSARrjwCHBPnv', desc='移交质检')
         .step(key='OA8F7p0BsRddG', desc='选择接收人')
         .step(key='UCqXC5fu5oUXD', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(cnBfO0w1V0T7Puy4uF3I)
    def cnBfO0w1V0T7Puy4uF3I(self):
        self.menu_manage()
        (self.step(key='x4In5HMXYCf0H', desc='单选')
         .step(key='HuIBY640J9k5q', desc='移交')
         .step(key='cCqdAg6VomLrt', desc='移交库存')
         .step(key='kRhPLscHflDOF', desc='选择接收人')
         .custom(lambda: self.up_enter())
         .step(key='GRwkLG8mo84n8', value=self.serial, action='input', desc='移交说明')
         .step(key='QnNlHIcKBuic5', desc='确定')
         .wait())
        return self
