# coding: utf-8
from common.base_page import BasePage, reset_after_execution
from common.base_params import InitializeParams
from common.import_desc import *


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []

    def menu(self, menu_type, key):
        """获取元素"""
        menu_mapping = {
            'main': self.elem_positioning['positioning'],
        }
        if menu_type in menu_mapping:
            return self.exc(lambda: menu_mapping[menu_type][key])
        else:
            raise ValueError(f"menu not found: {menu_type}")


class Ssjg8hIuEBI(CommonPages):
    """维修管理|维修审核列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='cWmnf5VpyKtSx', desc='维修管理')
         .step(key='aY8bP74o3b0fs', desc='维修审核列表')
         .wait())
        return self

    @reset_after_execution
    @doc(InAnaHvFTy76b32mumFp)
    def InAnaHvFTy76b32mumFp(self):
        self.menu_manage()
        (self.step(key='IjDwJDVOYpAuP', desc='审核')
         .step(key='FG8l3xc7o429H', value=self.serial, action='input', desc='审核说明')
         .step(key='ONIJTKxrdmO58', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(oxfkjSLPMvxmooiko075)
    def oxfkjSLPMvxmooiko075(self):
        self.menu_manage()
        (self.step(key='mTMoUBxgy19KM', desc='审核')
         .step(key='Lgi1m7uie2kRb', desc='未通过')
         .step(key='yQ85S9AcXKaWS', value=self.serial, action='input', desc='审核说明')
         .step(key='TI1FejRxxrDZL', desc='确认')
         .wait())
        return self


class HDrV92hc5GF(CommonPages):
    """维修管理|维修中物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='VANBF0jIEGaD0', desc='维修管理')
         .step(key='fz5QBvaxD8GJh', desc='维修中物品')
         .wait())
        return self

    @reset_after_execution
    @doc(PYrzOPhQBEGaXo51nyaY)
    def PYrzOPhQBEGaXo51nyaY(self):
        self.menu_manage()
        (self.step(key='B73vj5XQM5tzF', desc='提交维修结果')
         .step(key='x0s7SJhF9gpV5', desc='维修项目-1')
         .step(key='P3TOQ871Nn6jV', desc='维修项目-2')
         .scroll('repair_details', desc='维修详情')
         .step(key='m56x8JbfXurcO', desc='移交库存')
         .step(key='zXFsPEXEAp293', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='HHRQ0xg6AE5gB', value=self.serial, action='input', desc='维修详情')
         .step(key='UMKPGpcvb7K4W', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(kFFewUiXptz4lRt4hmYw)
    def kFFewUiXptz4lRt4hmYw(self):
        self.menu_manage()
        (self.step(key='oIzuh0Ej1OzRc', desc='提交维修结果')
         .step(key='je14phQnAaoCD', desc='添加配件')
         .step(key='j8IhRPcNjFRev', desc='单选')
         .scroll('add_accessories_verify', desc='确定')
         .step(key='wO934NgFywfVs', desc='确定')
         .step(key='mbb7gLLPww0nI', desc='维修项目-1')
         .step(key='Hw8UiHkml45to', desc='维修项目-2')
         .scroll(key='oGL5Z05gwIiCw', desc='确认')
         .step(key='AT5V7LlgpkwCE', desc='移交库存')
         .step(key='StSqr2SkIndFb', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='sgtskaL5LPc8m', value=self.serial, action='input', desc='维修详情')
         .step(key='CO631ExirWy9U', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(Xbfhk0aSUEnYlIVthPdi)
    def Xbfhk0aSUEnYlIVthPdi(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='ZA8U64bUbkMRt', desc='提交维修结果')
         .step(key='dvmlzaef3ttaJ', desc='扫码添加配件')
         .custom(self.affix_carriage_return)
         .step(key='JOCSB6J7J25ml', desc='确认添加')
         .step(key='cw1mVckvUHFOt', desc='维修项目-1')
         .step(key='ayuE7jYf6AnCC', desc='维修项目-2')
         .scroll(key='H9c6Uu99RLZbM', desc='确认')
         .step(key='iFRqlD9LAs5Xl', desc='移交库存')
         .step(key='GNYpwPzUxk81Z', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='pZmDw6MIOZ4lI', value=self.serial, action='input', desc='维修详情')
         .step(key='c7mxZgA7smT2T', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(bmPmqA7zguunIKgYInWf)
    def bmPmqA7zguunIKgYInWf(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='kyl11u4EZDzX4', desc='点击IMEI输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='R05K6pHDqY8hD', desc='快速维修')
         .step(key='ijaJkz3wxFl4Q', desc='维修项目-1')
         .step(key='TLml5j2Oaf4Sf', desc='维修项目-2')
         .scroll(key='UoWcFIp7NwOvk', desc='确认')
         .step(key='jmDsQAwsHthxv', desc='移交库存')
         .step(key='jsj0OTt0wnn99', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='JdMqJgbgggZd7', value=self.serial, action='input', desc='维修详情')
         .step(key='vt1EyRIDoI1nx', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(TwCDg8NuDSsEnMf1GPPT)
    def TwCDg8NuDSsEnMf1GPPT(self):
        self.menu_manage()
        (self.step(key='bmzLA63c2JVCt', desc='全选')
         .step(key='kU4OigUMy0FEW', desc='批量提交维修结果')
         .step(key='YyJ4ZM2gOVSFe', desc='维修项目-1')
         .step(key='YVB8PLgL4fmOK', desc='维修项目-2')
         .scroll(key='hQmrFDIKVLupP', desc='确认')
         .step(key='aHu3JYxE8XxNy', desc='移交库存')
         .step(key='iT6jcsRvHyLeF', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='KSbcuaUmKwobV', value=self.serial, action='input', desc='维修详情')
         .step(key='D2cE1frezdx3N', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(FzCP5d1Cyk04Rg7XdXWW)
    def FzCP5d1Cyk04Rg7XdXWW(self):
        self.menu_manage()
        (self.step(key='gLf519Ev8yo7j', desc='单选')
         .step(key='tCRQdK4bFhQHi', desc='未修移交')
         .step(key='wGEYRqRtkMr7l', desc='移交库存')
         .step(key='Bou2TPSXwIIvh', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='HwvDeLoB4yVn6', value=self.serial, action='input', desc='移交说明')
         .step(key='GyH2J3bYL4iBO', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(Nk6CFDyXMFV3sMEXwPOA)
    def Nk6CFDyXMFV3sMEXwPOA(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=7)[0]['articlesNo'])
        (self.step(key='BTrRL3QfbYhSW', desc='扫描批量未修移交')
         .step(key='YbfW5GOp1BwMb', desc='物品IMEI框')
         .custom(self.affix_carriage_return)
         .step(key='gJ4xvNz16gqrE', desc='未修移交')
         .step(key='o5tiSVww3MIi1', desc='移交库存')
         .step(key='cem3lkL8hbXZM', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='nXL9b2eYxnmpn', value=self.serial, action='input', desc='移交说明')
         .step(key='WnQ0C9bb3T4JL', desc='确定')
         .step(key='qrN1nTzG7phgl', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i1XbL2CrIPwi6h2C6y1T)
    def i1XbL2CrIPwi6h2C6y1T(self):
        self.menu_manage()
        (self.step(key='FBLW0Der46lLt', desc='提交维修结果')
         .scroll(key='b5ecw1jL0RZe9', desc='确认')
         .step(key='QYTRa0nZc0Ea1', value="200", action='input', desc='输入工费200')
         .step(key='rtMCjvnc0hkHi', desc='移交维修')
         .step(key='vCUcHc0mJ4TCx', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='TZCheoueIlqLP', value=self.serial, action='input', desc='维修详情')
         .step(key='wRnpIZctjlXPG', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(XZsjWIGPtCtyCOxtxlJo)
    def XZsjWIGPtCtyCOxtxlJo(self):
        self.menu_manage()
        (self.step(key='V9IxR3K1e2Sbm', desc='提交维修结果')
         .scroll(key='tpJKILuY9pU6q', desc='确认')
         .step(key='mrVZipDjQR6ue', value="200", action='input', desc='工费')
         .step(key='qMAI0of6lUiLd', desc='移交销售')
         .step(key='k3xmCmqH8rvyT', desc='接收人')
         .custom(lambda: self.up_enter())
         .step(key='VQmm7jf9qA3nY', value=self.serial, action='input', desc='维修详情')
         .step(key='qKLLzSCDQdDmx', desc='确认')
         .wait())
        return self


class A0lyjFxl9Cw(CommonPages):
    """维修管理|维修数据统计"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='CHXNtRJCbz8hR', desc='维修管理')
         .step(key='q5KeY7YlDYXHy', desc='维修数据统计')
         .wait())
        return self

    @doc(jgkToL04qhtLIicYNjr2)
    def jgkToL04qhtLIicYNjr2(self):
        """导出按钮"""
        self.menu_manage()
        (self.step(key='dHxWnWz6uRy2S', desc='导出')
         .wait())
        return self


class ZdRLslkrxnz(CommonPages):
    """维修管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='i56A7TwUTUL2U', desc='维修管理')
         .step(key='y6nkcNizvvHVb', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(dtMnLD99xu70O75WPpZI)
    def dtMnLD99xu70O75WPpZI(self):
        self.menu_manage()
        (self.step(key='dRCcWvU42icMe', desc='全选')
         .step(key='M8QXUPM2eg405', desc='接收')
         .step(key='v5JQpAnZm2CpI', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(Do71TcM8aJhiO9BlM30Q)
    def Do71TcM8aJhiO9BlM30Q(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='JdoumpbD085fT', desc='扫码精确接收')
         .custom(self.affix_carriage_return)
         .step(key='imqZ6uheGxPOV', desc='接收')
         .step(key='dg5flh906KQLJ', desc='确定')
         .wait())
        return self


class HAJk7yhq6D2(CommonPages):
    """维修管理|维修项目列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='pLxa56NgCKbZO', desc='维修管理')
         .step(key='pCeumPU1GLToS', desc='维修项目列表')
         .wait())
        return self

    @reset_after_execution
    @doc(otRpL7YRWiPq6A7gGbBE)
    def otRpL7YRWiPq6A7gGbBE(self):
        self.menu_manage()
        (self.step(key='akIfJwpPmrYur', desc='新增维修项目')
         .step(key='U46ghFNGEz4fR', desc='维修类目')
         .custom(lambda: self.up_enter())
         .step(key='hy10kExbUtDxB', value=self.serial, action='input', desc='维修项目')
         .step(key='k28mlnvYS8Jbg', value='21', action='input', desc='维修工费')
         .step(key='iTJjyX6U0wftl', desc='适用品类')
         .custom(lambda: self.down_enter())
         .step(key='TS25FXqsbQXJ4', desc='弹窗标题')
         .step(key='hvhW0Es9MjmXM', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(jCLIGsFOwpQqsIwpnxNc)
    def jCLIGsFOwpQqsIwpnxNc(self):
        self.menu_manage()
        (self.step(key='MZBV2QFJDS2Pp', desc='新增维修项目')
         .step(key='xIY4oumAKXksH', desc='维修类目')
         .custom(lambda: self.up_enter())
         .step(key='PLAUlMaWg6v2E', value=self.serial, action='input', desc='维修项目名称')
         .step(key='OuOaEZhEAnYp4', value='34', action='input', desc='维修工费')
         .step(key='Qi3zQG7QngsWv', desc='适用品类')
         .custom(lambda: self.down_enter())
         .custom(lambda: self.down_enter())
         .step(key='Nh8T42RBqdFAZ', desc='弹窗标题')
         .step(key='jAnbV56Gunr5d', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(A3huxJD5Z6IGUspl0I6d)
    def A3huxJD5Z6IGUspl0I6d(self):
        self.menu_manage()
        (self.step(key='Y19IooouHvDUW', desc='编辑')
         .step(key='IO0aHiV7aQu3d', desc='点击维修类目')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='R5HmKQNrfUApb', value=self.serial, action='input', desc='维修项目名称')
         .step(key='gaRyeu9DvHHFv', value='22', action='input', desc='维修工费')
         .step(key='NFgdzAOViA3E6', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(z6Fij1duyB9APTQsy7SW)
    def z6Fij1duyB9APTQsy7SW(self):
        self.menu_manage()
        (self.step(key='gCM9erctCsEmY', desc='删除')
         .step(key='tOt78MfaUwJDp', desc='确认删除')
         .wait())
        return self

    @reset_after_execution
    @doc(V0LveJcsirDBPkbnoy5r)
    def V0LveJcsirDBPkbnoy5r(self):
        self.menu_manage()
        (self.step(key='yDT8CXw5lPCms', desc='机型配置')
         .step(key='tAB7Rhh3eMAET', desc='新增')
         .step(key='pS8KantwTVKPN', desc='品牌')
         .custom(lambda: self.down_enter(2))
         .step(key='izrbycVAQw0El', desc='型号')
         .custom(lambda: self.down_enter(3))
         .step(key='f29ICi0oj6Nnj', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(Q8t9eC7T5nzs0GLMTihp)
    def Q8t9eC7T5nzs0GLMTihp(self):
        self.menu_manage()
        (self.step(key='nvEs2NwwYafNd', desc='机型配置')
         .step(key='rywlvAAOMpVxb', desc='删除')
         .step(key='vzaptd21RAedB', desc='确认删除')
         .wait())
        return self
