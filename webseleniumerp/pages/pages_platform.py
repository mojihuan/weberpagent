# coding: utf-8
from common.base_page import BasePage, reset_after_execution
from common.import_desc import *


class CommonPages(BasePage):

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


class G9Xb1VIa3XI(CommonPages):
    """平台管理|运营中心|待指定物品"""


class ZbWaTtRLQPH(CommonPages):
    """平台管理|卖场管理|暗拍卖场列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='EIhiiqWjacBoO', desc='平台管理')
         .scroll(key='HcXWTRkRg7Dfh', desc='卖场管理')
         .step(key='CLap64pGtN64R', desc='卖场管理')
         .step(key='yEdADAZd2nqHT', desc='暗拍卖场列表')
         .wait())
        return self

    @reset_after_execution
    @doc(oQ4T86fmEaH8KwhBSxP3)
    def oQ4T86fmEaH8KwhBSxP3(self, ):
        self.menu_manage()
        (self.step(key='dQ5pwTnwtUWVt', desc='创建卖场')
         .step(key='T1kbBIc1li7jC', value='直拍卖场' + self.serial, action='input', desc='卖场名称')
         .step(key='CF8oYFIsheUAC', value='卖场描述' + self.serial, action='input', desc='卖场描述')
         .step(key='z4BqMcjUu9T2P', value='1', action='input', desc='广告位优先级')
         .step(key='VFtT5SfsHJtuR', value=self.get_the_date(days=-2), action='input', desc='活动开始时间')
         .step(key='zsnXUgRImjq9R', value=self.get_the_date(days=-1), action='input', desc='活动结束时间')
         .custom(lambda: self.wait_time())
         .step(key='snLkjNDTW4WpA', value='场次标题' + self.serial, action='input', desc='场次1标题')
         .step(key='HTBWvhlJRP8o5', value=f"00:10:00", action='input', desc='场次开始时间')
         .step(key='W4U38t7clJeys', value=f"22:00:00", action='input', desc='场次结束时间')
         .step(key='sieo9Ij7hncxu', desc='确定时间')
         .step(key='QzoJCatNABdbJ', value=f"20:00", action='input', desc='展示排名时间')
         .step(key='gaIoL5JUxLvlg', desc='商品中标规则')
         .custom(lambda: self.down_enter(2))
         .step(key='DiRUq8TRZ8n4n', desc='请选择场次流拍规则')
         .custom(lambda: self.down_enter(2))
         .step(key='Vft7K2tNzBGH6', value='1', action='input', desc='场次保底数量')
         .step(key='egDpvVnDIyVBc', value='1000', action='input', desc='场次封顶数量')
         .step(key='j2i8klzQmGluP', desc='所有条件(and)')
         .step(key='ecsrhEKFVeHlh', desc='品类')
         .custom(lambda: self.down_enter())
         .step(key='nzEtNyGUlgVkt', desc='品牌')
         .custom(lambda: self.down_enter())
         .step(key='c0fpTKAJvqGZi', desc='型号')
         .custom(lambda: self.down_enter())
         .step(key='WIV1nm0m9hCs5', desc='成色要求')
         .step(key='dMxC1aRiOoAy2', desc='选择靓机')
         .step(key='zWNej7CqEIvX5', desc='关闭选项')
         .step(key='RLisHPJyinEe5', value='100', action='input', desc='最小起拍价')
         .step(key='l4OTOBjd8iPGz', desc='点击一下其他位置【成色要求】')
         .step(key='mX2j3hvpRHQsB', value='100000', action='input', desc='最大起拍价')
         .step(key='qp5tYh5GaAIRh', desc='保存并上架')
         .step(key='qWltUPJxD57yU', desc='确定')
         .step(key='NMDhJABRf8n9X', desc='我知道了')
         .wait())

    @reset_after_execution
    @doc(Bkz45n2kH6kLSep0tdDB)
    def Bkz45n2kH6kLSep0tdDB(self):
        self.menu_manage()
        (self.step(key='VMMkZewTltG7h', desc='已下架')
         .custom(lambda: self.wait_time())
         .step(key='RZBvuAUXaUjC8', desc='编辑')
         .step(key='bkIW7g3lJAsvW', desc='清空原来的日期')
         .step(key='SP2QRHEH6UEUg', value=self.get_the_date(), action='input', desc='活动开始时间')
         .step(key='i98kWAV8ypuOF', value=self.get_the_date(days=7), action='input', desc='活动结束时间')
         .custom(lambda: self.wait_time())
         .scroll('save_only', desc='仅保存')
         .step(key='cG4hPG2FC46qJ', desc='保存并上架')
         .step(key='SmkgGgubqWQgd', desc='确定')
         .step(key='lQ0J9V59bdODb', desc='我知道了')
         .wait())
        return

    @reset_after_execution
    @doc(SML4kMf2uJffhQbwtUx6)
    def SML4kMf2uJffhQbwtUx6(self):
        self.menu_manage()
        (self.step(key='PYOfRtOQ7LUn9', desc='已上架')
         .step(key='IhKHbAIsTscZz', desc='下架')
         .step(key='FvkDtoVSnYqXG', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(gnlGXVVK4aiBrYlOX6oB)
    def gnlGXVVK4aiBrYlOX6oB(self):
        self.menu_manage()
        (self.step(key='XoSK9IZiJ0JBS', desc='已上架')
         .step(key='bYjFTW5l8qB5F', desc='查看场次')
         .step(key='FrCt35PNySWYK', desc='添加商品')
         .step(key='E5QJ1Upgwtsk9', desc='选择品类-手机')
         .custom(lambda: self.down_enter())
         .step(key='M7qdEyVDx7ZYJ', desc='搜索')
         .custom(lambda: self.down_enter(3))
         .step(key='bkuu3hjYR2c43', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(rWYreYEUUn6guCfMIcjL)
    def rWYreYEUUn6guCfMIcjL(self):
        self.menu_manage()
        (self.step(key='xnFUZXf4uRkJi', desc='已上架')
         .step(key='k5PSDV8j0F1H3', desc='查看场次')
         .step(key='n009VTuccEqCm', desc='关闭查看商品')
         .wait())
        return

    @reset_after_execution
    @doc(ZAkeZYaFKKXvRIOgPLOU)
    def ZAkeZYaFKKXvRIOgPLOU(self):
        self.menu_manage()
        (self.step(key='gdtQZnKPd4nO0', desc='待上架')
         .step(key='MXiVDNEMdEvP5', desc='上架')
         .step(key='PWHKMjTyAtbDb', desc='确定')
         .step(key='eab2xANS6YrhZ', desc='我知道了')
         .wait())
        return

    @reset_after_execution
    @doc(pf1dNwfGdkEBsdL4SZfG)
    def pf1dNwfGdkEBsdL4SZfG(self):
        self.menu_manage()
        (self.step(key='zNxB1IuONeNsJ', desc='待上架')
         .step(key='G3z6WhrUIzsZV', desc='删除')
         .scroll('tip_determine', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(jinaFo1BfuHnHIiDdZPE)
    def jinaFo1BfuHnHIiDdZPE(self):
        self.menu_manage()
        (self.step(key='XwwAprrJeoQog', desc='调整广告位')
         .step(key='LCvBnrr40U96G', desc='显示待上架')
         .step(key='C9EmmtyjMypIT', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(iArGbfUX5RsDKrB8KgZN)
    def iArGbfUX5RsDKrB8KgZN(self):
        self.menu_manage()
        (self.step(key='Mz1v8czCKWCBa', desc='调整广告位')
         .step(key='lon1NKWWXCjvC', desc='显示待上架')
         .step(key='zgyRKEsuLS6Ah', desc='显示已下架')
         .step(key='hzJX6pbXmB8fk', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(KPvNzeTk3NvDtpqKWlVb)
    def KPvNzeTk3NvDtpqKWlVb(self):
        self.menu_manage()
        (self.step(key='Ap9k8vkByMGRN', desc='查看日志')
         .wait())
        return

    @reset_after_execution
    @doc(I1S9lui6I0jHXse8gVcc)
    def I1S9lui6I0jHXse8gVcc(self):
        self.menu_manage()
        (self.step(key='sypCgxenHZhs0', desc='导出')
         .wait())


class YAKR9LJejV2(CommonPages):
    """平台管理|卖场管理|直拍卖场列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='tjaXcObHChu2p', desc='平台管理')
         .scroll(key='mwN0DUQBbMXFc', desc='卖场管理')
         .step(key='SrADXNdPxE2WF', desc='卖场管理')
         .step(key='NhcII1erf39F5', desc='直拍卖场列表')
         .wait())
        return self

    @reset_after_execution
    @doc(dkzcGVBC4f0eOkX7psWu)
    def dkzcGVBC4f0eOkX7psWu(self):
        """创建直拍卖场"""
        self.menu_manage()
        (self.step(key='FRO6e212wPWwz', desc='创建卖场')
         .step(key='jacWDgr0A7qWS', value='直拍卖场' + self.serial, action='input', desc='卖场名称')
         .step(key='k2qWL5OLCW4ky', value='卖场描述' + self.serial, action='input', desc='卖场描述')
         .step(key='AI8lueef8eFc8', value='1', action='input', desc='广告位优先级')
         .step(key='UEi3uCJX8RIVW', value=self.get_formatted_datetime(), action='input', desc='活动开始时间')
         .step(key='KX8YGNKdpt7cB', value=self.get_formatted_datetime(days=1), action='input', desc='活动开结束时间')
         .step(key='ylNDsuUHFrRLW', value='场次标题' + self.serial, action='input', desc='场次1标题')
         .step(key='fPGze9bHCYZX4', desc='场次1标题')
         .step(key='yCADNfBwlQkpJ', value="09:00", action='input', desc='场次开始时间')
         .step(key='IhabMxZ1Xc3YQ', value="09:55", action='input', desc='场次结束时间')
         .step(key='djou30lY8trrW', value='1', action='input', desc='商品倒计时分钟')
         .step(key='drzMRCH1EM3cz', value='1', action='input', desc='场次保底数量')
         .step(key='F3wO9WUMubo6v', value='10000', action='input', desc='场次封顶数量')
         .step(key='r8HRgD9RTtvh8', desc='品类')
         .custom(lambda: self.down_enter())
         .step(key='Nb8jcpAgX7pN2', desc='品牌')
         .custom(lambda: self.down_enter())
         .step(key='QZuXxn7fksiS8', desc='型号')
         .custom(lambda: self.down_enter())
         .step(key='lT1VOCvyLHMUC', desc='成色要求')
         .custom(lambda: self.down_enter())
         .step(key='oD2g6hueW1byH', value='1', action='input', desc='最小起拍价')
         .step(key='JLZn6y2dNQWbn', desc='条件组配置')
         .step(key='VFxDsQRtL4SES', value='100000', action='input', desc='最大起拍价')
         .step(key='OOw001Zl8gysI', desc='保存并上架')
         .step(key='IPIHGbvtKBD7A', desc='确定')
         .step(key='BL79hAZwyUh6p', desc='我知道了')
         .wait())
        return

    @reset_after_execution
    @doc(S9rWKvQ89U7Uknx1aXeR)
    def S9rWKvQ89U7Uknx1aXeR(self):
        self.menu_manage()
        (self.step(key='NOf71adwYp5Gc', desc='下架')
         .step(key='ooqJ93tlCT4gI', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(i2PADX8AIUDmt1eH6XmL)
    def i2PADX8AIUDmt1eH6XmL(self):
        self.menu_manage()
        (self.step(key='LU8I4eOKX9WhU', desc='已上架')
         .step(key='jTlDRsWssa5Vd', desc='查看场次')
         .step(key='wuD9O2xCM0DBt', desc='添加商品')
         .step(key='gCXBlOjkKxRVh', desc='选择品类')
         .custom(lambda: self.down_enter())
         .step(key='jOb0ijnSxqlVY', desc='搜索')
         .custom(lambda: self.down_enter(3))
         .step(key='CvAFZvXA2j4Fl', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(icBZPN1P562alvUYw9qv)
    def icBZPN1P562alvUYw9qv(self):
        self.menu_manage()
        (self.step(key='ww6AU3OHCVoIG', desc='已上架')
         .step(key='Mx1UTuyqh4WNd', desc='查看场次')
         .step(key='I8slktMyHVtw9', desc='关闭开发查看商品')
         .wait())
        return

    @reset_after_execution
    @doc(w7Q9iTIZZFL6IeAt7EDA)
    def w7Q9iTIZZFL6IeAt7EDA(self):
        self.menu_manage()
        (self.step(key='W52dBvCUd6V9Z', desc='调整广告位')
         .step(key='p46mh1OsQdOBc', desc='显示待上架')
         .scroll('save_and_update', desc='保存并更新')
         .step(key='PiuWaExPpYwU5', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(E9V5GboJRLQOhqmn6ZP0)
    def E9V5GboJRLQOhqmn6ZP0(self):
        self.menu_manage()
        (self.step(key='CSaNVJP5si8zj', desc='调整广告位')
         .step(key='qNZOWnioJZfjj', desc='显示待上架')
         .step(key='wOeohbohvdwe3', desc='显示已下架')
         .scroll('save_and_update', desc='保存并更新')
         .step(key='vwC8nuoco8tXJ', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(VCvQ9C6taFx1IE4yFXlK)
    def VCvQ9C6taFx1IE4yFXlK(self):
        self.menu_manage()
        (self.step(key='f7AsuhzjoNXcx', desc='查看日志')
         .wait())
        return

    @reset_after_execution
    @doc(xGvapPmmNaRHIGh8Hi7I)
    def xGvapPmmNaRHIGh8Hi7I(self):
        self.menu_manage()
        (self.step(key='N8EVplCsVwr82', desc='导出')
         .wait())
        return


class Ga3L1J6IKxy(CommonPages):
    """平台管理|商户管理"""


class QE6VcNFjGEj(CommonPages):
    """平台管理|消息管理|消息发布列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='ovrJsvms0v7ln', desc='平台管理')
         .scroll(key='nqlzPoqrm6Uxo', desc='消息管理')
         .step(key='g2OEsBR9848bD', desc='消息管理')
         .step(key='cf6w9Jnx4OVZU', desc='消息发布列表')
         .wait())
        return self

    @reset_after_execution
    @doc(G9C97BkpOngHG41cgA0L)
    def G9C97BkpOngHG41cgA0L(self):
        self.menu_manage()
        (self.step(key='PdA4Y0lFzRyj8', desc='回收商发布')
         .step(key='G5DfrBsibv4cp', desc='搜索')
         .step(key='lLTB4jKb2ahhh', desc='平台审核')
         .step(key='wPcPPrpJKxsKs', desc='通过')
         .step(key='eklfJ6u5VDNj8', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(pj4bj85GPh759JlXB1ir)
    def pj4bj85GPh759JlXB1ir(self):
        self.menu_manage()
        (self.step(key='Y8ZTupe7pUn7g', desc='回收商发布')
         .step(key='R3fS4fLdSDUP0', desc='搜索')
         .step(key='C3eEzQA2anMgO', desc='平台审核')
         .step(key='oKw69yb9qLhoP', desc='拒绝')
         .step(key='WqFLzzqvrvB5p', value=self.serial, action='input', desc='拒绝原因')
         .step(key='IqRvrqE84Rr6T', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(pdEsg1lHJfR191fcMim5)
    def platform_bpdEsg1lHJfR191fcMim5ack(self):
        self.menu_manage()
        (self.step(key='KdKJzMVcyPk20', desc='回收商发布')
         .step(key='y3g1ZmUC8B7WR', desc='搜索')
         .step(key='UNwNIIPwFctLr', desc='平台撤回')
         .custom(self.wait_time)
         .step(key='G1lIluS73oZCX', desc='确定')
         .wait())
        return self


class TvMioJovFR2(CommonPages):
    """平台管理|同售管理|商品审核"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='VAFCLuHyFhIQN', desc='平台管理')
         .scroll(key='jjrvSXW1kg5j9', desc='同售管理')
         .step(key='mr4MZmJZzrcED', desc='同售管理')
         .step(key='GdAiVGvde32FM', desc='商品审核')
         .wait())
        return self


class AjSkA6klpCA(CommonPages):
    """平台管理|订单管理|订单审核"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='SFHGFeQ0VJZFy', desc='平台管理')
         .scroll(key='WeWRC4QST5Xv8', desc='订单管理')
         .step(key='Ss8IzijhFTL7W', desc='订单管理')
         .step(key='w5GmeF7QkdZww', desc='订单审核')
         .wait())
        return self

    @reset_after_execution
    @doc(BBiltLX4GA5cpSCyECIP)
    def BBiltLX4GA5cpSCyECIP(self):
        self.menu_manage()
        (self.step(key='OLRk3NwGh858Y', desc='审核')
         .step(key='OHHR9UoJLD3Du', value=self.serial, action='input', desc='审核说明')
         .step(key='sIGE9QEkiVNtQ', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(FMRI6lTSPPbGRqorxtkt)
    def FMRI6lTSPPbGRqorxtkt(self):
        self.menu_manage()
        (self.step(key='gitr7gA84FBjc', desc='审核')
         .step(key='jOq5RFkQbJFUJ', desc='未通过')
         .step(key='lTsOnZ4AEATPS', value=self.serial, action='input', desc='审核说明')
         .step(key='E06LRT4TQi6bd', desc='确认')
         .wait())
        return self
