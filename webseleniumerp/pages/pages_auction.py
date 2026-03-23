# coding: utf-8
from common.mini_base_minium import BaseMinium
from common.import_desc import *


class AuctionIndexPages(BaseMinium):
    """首页"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loc = self.mg_locator('index')

    @doc(a_fast_submit_new_order)
    def fast_submit_new_order(self):
        self.elem(**self.loc['fast_shipping'], desc='快速发货')
        self.input(**self.loc['selling_price'], text='8888', desc='卖出总价')
        self.elem(**self.loc['committed'], desc='提交')
        return self

    @doc(a_auto_submit_new_order)
    def auto_submit_new_order(self):
        self.elem(**self.loc['precise_shipping'], desc='精准发货')
        self.elem(**self.loc['model'], desc='机型')
        self.elem(**self.loc['small_model'], desc='小型号')
        self.elem(**self.loc['purchase_channels'], desc='购买渠道')
        self.elem(**self.loc['color'], desc='颜色')
        self.elem(**self.loc['rom_capacity'], desc='rom容量')
        self.elem(**self.loc['next_step'], desc='下一步')
        self.elem(**self.loc['boot_situation'], desc='开机情况')
        self.elem(**self.loc['account_lock'], desc='账户锁')
        self.elem(**self.loc['color'], desc='保修情况')
        self.elem(**self.loc['rom_capacity'], desc='边框背板')
        self.elem(**self.loc['screen_appearance'], desc='屏幕外观')
        self.elem(**self.loc['lcd_display'], desc='液晶显示')
        self.elem(**self.loc['body_appearance'], desc='机身外观')
        self.elem(**self.loc['next_step'], desc='下一步')
        self.elem(**self.loc['battery_health'], desc='电池健康度')
        self.elem(**self.loc['front_facing_shooting_function'], desc='前摄拍摄功能')
        self.elem(**self.loc['get_an_instant_estimate'], desc='立即估价')
        self.elem(**self.loc['confirm_submission'], desc='确认提交')
        self.wait()
        return self
