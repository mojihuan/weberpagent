# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.settings import DATA_PATHS


class CommonPages(BasePage, InitializeParams):
    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'attachment_allocation': os.path.join(DATA_PATHS['excel'], 'attachment_allocation_import.xlsx')
        }


class Xoub7k5qm8b(CommonPages):
    """配件管理|入库管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='fJme9jdZaj7qz', desc='配件管理', tag='span')
        self.click(key='uZGHrJ19UvRIv', desc='入库管理', index=2, tag='span')
        self.click(key='A71OfbRC2mfBZ', desc='待接收物品', index=6, tag='span')
        return self

    @reset_after_execution
    @doc(do56fxxjyrxq3jf44spl)
    def do56fxxjyrxq3jf44spl(self):
        obj = self.pc.BF3x3lYIzbEHMnrvr80JO()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='XlxbLmDkFm1kH', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='wwMxJaPAxOiQS', desc='接收', tag='span')
        self.click(key='YrNPhYV3LZvdK', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['Sm7yLloyr'])
        return self

    @reset_after_execution
    @doc(ttg8vtbix8yyh0zzk1l5)
    def ttg8vtbix8yyh0zzk1l5(self):
        self.menu_manage()
        obj = self.pc.BF3x3lYIzbEHMnrvr80JO()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='C0EFN7X4KhZ5D', desc='扫码精准接收', tag='span')
        self.ctrl_v_enter()
        self.tab_space(2)
        self.click(key='v7gSdyJGZpBjw', desc='接收', tag='span', p_tag='div', p_name='el-dialog__body')
        return self

    @reset_after_execution
    @doc(wkocqx1u2ihsf32i7co1)
    def wkocqx1u2ihsf32i7co1(self):
        self.menu_manage()
        obj = self.pc.BF3x3lYIzbEHMnrvr80JO()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='AvDv2a6Wv36ho', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='XagRntnND9pOR', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(a33hoz47yc05hmc4n7jw)
    def a33hoz47yc05hmc4n7jw(self):
        self.menu_manage()
        obj = self.pc.BF3x3lYIzbEHMnrvr80JO()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.input(key='f9DmlWml7Edln', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='pRphPUQHD39lw', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='YgXcqYtzNV4c8', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self


class QWfXHzt4fYt(CommonPages):
    """配件管理|移交接收管理|移交物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='GLHpSOQazpNfH', desc='配件管理', tag='span')
        self.click(key='XcdkCseiVjkQp', desc='移交接收管理', tag='span', index=2)
        self.click(key='GfZ5yA3FYrqzK', desc='移交物品', tag='span', index=2)
        return self

    @reset_after_execution
    @doc(pxx47rbom8j1ul0o5otk)
    def pxx47rbom8j1ul0o5otk(self):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='ULZy5afvzHeiC', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='IfvfpIcsNo73Y', desc='搜索', tag='span')
        self.click(key='plz1LWweIxLgB', desc='移交', tag='span')
        self.click(key='VYj7NhtA8wqFz', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='pv46d0kYSfzVj', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='GkoDqLWLglrv5', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(bq9jhuudug0bycyitdho)
    def bq9jhuudug0bycyitdho(self):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='c1urEjknBlmq5', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='MCCB6CL3IOKJe', desc='搜索', tag='span')
        self.click(key='pCHlVFUG7lB8z', desc='移交', tag='span')
        self.click(key='JxpvzfuG5CVqb', desc='采购售后', tag='span')
        self.click(key='swpu8hTbQjrZA', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='pFQRMXshiGjMi', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='OSaP1f8gsZCoU', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(qnig8uaqhu0cma5jwmjd)
    def qnig8uaqhu0cma5jwmjd(self):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='dBRvqxFIz3zGe', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='RVO82miguQo28', desc='搜索', tag='span')
        self.click(key='gUCoLaoLpVZZc', desc='移交', tag='span')
        self.click(key='gUQgrMzw46vKA', desc='销售', tag='span')
        self.click(key='FeOUO4wWFYwcT', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='Eclb4c3k7VGBK', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='QrfDUIxiJp8yw', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(p0su9g9hxgnbgmkfhw8b)
    def p0su9g9hxgnbgmkfhw8b(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='BU2epqEbw24oq', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='FDl2cFkYZ8HQt', desc='搜索', tag='span')
        self.click(key='zwNhTR4hFxUdL', desc='移交', tag='span')
        self.click(key='Ntrh3nZG5hxKH', desc='送修', tag='span')
        self.click(key='jLs1KVOjCNj7d', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='xz1cVBlpzxrKL', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='x7QJPDDnekdaM', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(vicvey7gwzlidkxk2756)
    def vicvey7gwzlidkxk2756(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='X7EeXT3RhIrZz', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='N4AgTdGOyJ74n', desc='搜索', tag='span')
        self.click(key='Vl9lKCuarBnMh', desc='移交', tag='span')
        self.click(key='c9EKR7N3W4HcW', desc='维修', tag='span')
        self.click(key='AEeR7IPsIewY3', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='U8odda0OGa9de', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='rXMwUpmYs6A1w', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(tvl7rnnvwpmaivcnflho)
    def tvl7rnnvwpmaivcnflho(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='n9LklmzXAN6ia', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='DW9iWKJEdLsGT', desc='搜索', tag='span')
        self.click(key='zDl5CLi44Rhii', desc='移交', tag='span')
        self.click(key='yvtfpRsz3pbsr', desc='质检', tag='span')
        self.click(key='Urr34SswCAqC2', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='OMrORFjDMuiPQ', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='fbCMz3eCKzIpB', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(y1f0go3apyd2gpjhtp6e)
    def y1f0go3apyd2gpjhtp6e(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='mFZyZzpGcx9fy', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='G0EF91aSXa8Kv', desc='搜索', tag='span')
        self.click(key='NB0wg09EvVFA2', desc='移交', tag='span')
        self.click(key='dhwG7XjEb2Kic', desc='质检', tag='span')
        self.click(key='QWzGWlC01n6b2', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='A6Bx5K4Mr2Ya1', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='MhXolDLPnyeZC', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(cwwg81c7fuxew6ohcyna)
    def cwwg81c7fuxew6ohcyna(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='XrcEubwap1a7q', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='lPh19St9RQH1f', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['WfRN4FHg5'])
        return self


class H2VfJncOV57(CommonPages):
    """配件管理|移交接收管理|移交记录"""

    def menu_manage(self):
        """菜单"""
        self.click(key='HlZOUrJIZ4dBR', desc='配件管理', tag='span')
        self.click(key='ArEEFIjUPQQrA', desc='移交接收管理', tag='span', index=2)
        self.click(key='VELwNAdIsW1ol', desc='移交记录', tag='span', index=2)
        return self

    @reset_after_execution
    @doc(bs0gqufrf2alobu8ypuc)
    def bs0gqufrf2alobu8ypuc(self):
        self.menu_manage()
        self.click(key='SLO3afwiMIsoN', desc='导出', tag='span')
        return self

    @reset_after_execution
    @doc(z36rbt8nuevvk5zw0ev1)
    def z36rbt8nuevvk5zw0ev1(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='JJXoIvJENLwgQ', desc='1', d='移交物品数量链接', tag='span', p_tag='button', p_name='el-button el-button--text el-button--medium')
        self.click(key='qugy2CqrbYs1v', desc='搜索', tag='span', p_tag='div', p_name='el-dialog__body')
        self.tab_space(4)
        self.click(key='JnBo9qEgqOgZe', desc='批量取消移交', tag='span')
        self.click(key='vQV8hfK3DN8zv', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['qaZzLXfvX'])
        return self

    @reset_after_execution
    @doc(dk81rtdv2rvc2fjer6m8)
    def dk81rtdv2rvc2fjer6m8(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='n94jxvxLyU0hC', desc='1', d='移交物品数量链接', tag='span', p_tag='button', p_name='el-button el-button--text el-button--medium')
        self.click(key='Qdh8ayT7wrBeK', desc='搜索', tag='span', p_tag='div', p_name='el-dialog__body')
        self.tab_space(4)
        self.click(key='CoftiTQHRHabO', desc='取消移交', tag='span', p_tag='tr', p_name='el-table__row')
        self.click(key='IIOoiDraHeExL', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        return self

    @reset_after_execution
    @doc(sdl1o9ghd61tojp5ap48)
    def sdl1o9ghd61tojp5ap48(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='VyL9hWljdoh0Z', desc='请输入编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='DLElPmvseazfv', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zbE7yOZvu'])
        return self

    @reset_after_execution
    @doc(evbb4ktxeipdare0ybrf)
    def evbb4ktxeipdare0ybrf(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='it1yEfsq3UIsg', desc='请输入移交单号', tag='input')
        self.ctrl_v()
        self.click(key='V870XRtLP6hxT', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zbE7yOZvu'])
        return self

    @reset_after_execution
    @doc(hpjacvh5iwz7rzgwap4)
    def hpjacvh5iwz7rzgwap4(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='vfR3JCGgElCwd', desc='请选择移交单状态', tag='input')
        self.down_enter()
        self.click(key='sM2Nc1JEobutz', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zbE7yOZvu'])
        return self

    @reset_after_execution
    @doc(v3j4micfjps17busi402)
    def v3j4micfjps17busi402(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='d5P3Fk8t1WhRb', desc='请选择移交人', tag='input')
        self.down_enter()
        self.click(key='tXmpNoUoJkZGp', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zbE7yOZvu'])
        return self

    @reset_after_execution
    @doc(pudb09khr1ozo3wwci4a)
    def pudb09khr1ozo3wwci4a(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='I6Jqe76JBDUOT', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='HL4q0HSLR3ot4', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zbE7yOZvu'])
        return self

    @reset_after_execution
    @doc(rf7nygh1xebifff8bl22)
    def rf7nygh1xebifff8bl22(self):
        self.menu_manage()
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.input(key='jbRnM9wLmEh4T', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='mbcrOqB19Up6T', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='jsLgfCQVo1cD0', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zbE7yOZvu'])
        return self


class Ze2iqsn6eIM(CommonPages):
    """配件管理|配件库存|库存列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='kkK78LcVwWCvo', desc='配件管理', tag='span')
        self.scroll(element='cPYjFthySgGqS')
        self.click(key='cPYjFthySgGqS', desc='配件库存', tag='span')
        self.click(key='oc4x6zBktwXQt', desc='库存列表', tag='span', index=2)
        return self

    @reset_after_execution
    @doc(oqmc5nwi0399dzltytx2)
    def oqmc5nwi0399dzltytx2(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='cNrXt6y07POZl', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='ejvu4tHT3jq6H', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='O9tBkBd7fGlZO', desc='批量移交', tag='span')
        self.click(key='uiP52hRk60zLu', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.input(key='mqSZ71NFuQGNZ', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='NR5t2vTXmL3Ar', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(saaotn9359y5rsz0php1)
    def saaotn9359y5rsz0php1(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='pSBJb19Pq2HCz', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='ZBQ0dGPpXJwcG', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='YZDWKm8LDrXZD', desc='批量移交', tag='span')
        self.click(key='hx74OaWv1lNwZ', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='o4eyHLNqPTfMD', desc='采购售后', tag='span', index=2)
        self.input(key='tjlbbZdIHnQMA', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='LgFBXG0Fejs9D', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(lrfqyoilnhzw2ejk659d)
    def lrfqyoilnhzw2ejk659d(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='dEvZVcJSsMfe6', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='u04mJ9EnnLp55', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='EVzqFd6MR97MV', desc='批量移交', tag='span')
        self.click(key='HfEtrq7HUzZXj', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='zcia94zImSQJX', desc='销售', tag='span')
        self.input(key='TICT6iiavUZrB', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='VcmTkwHkESMd1', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(v60oxil51ddo2si7jl7x)
    def v60oxil51ddo2si7jl7x(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='JpsyR1HP2qS1T', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='E88kBu0B9zmeG', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='OW67oHrLir79y', desc='批量移交', tag='span')
        self.click(key='xeaKxoSTqIzfa', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='XapymMYdrBjwN', desc='送修', tag='span')
        self.input(key='vaWARZqAg04I0', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='jaVwhpA4Rj3N2', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(p3vluvp1sur9pfwpeyrh)
    def p3vluvp1sur9pfwpeyrh(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Hh1VN4byM597z', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='KLcNG598Xykd0', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='W9BV9b62ixH50', desc='批量移交', tag='span')
        self.click(key='vtiQQNeCpexcf', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='nTdLtpxcaSesQ', desc='维修', tag='span')
        self.input(key='kMXnMBt8qzQmm', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='vnGpjbxku7XcU', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(icdh72iujmalc7gukwol)
    def icdh72iujmalc7gukwol(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='KTph3kVAoUZ6p', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='WlZlR8y06AiSN', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='wiZDYXzc0ohbi', desc='批量移交', tag='span')
        self.click(key='QnibzOF1dMNyz', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='n10SuJIxIPklJ', desc='质检', tag='span')
        self.input(key='HWdUOgu9aGDpm', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='Ko8PjuXasQbav', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['EgcsFMe1T'])
        return self

    @reset_after_execution
    @doc(u6a07svx0rwzn93bn54o)
    def u6a07svx0rwzn93bn54o(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Fhir1O7GX9Bcc', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='OKDQiI5WugoV3', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='o7qolnHvTdgXp', desc='配件销售', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='h6U90I1g7HgMq', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.click(key='rvezAOcU5awRe', desc='已收款', tag='span')
        self.click(key='bRAR7F1d06DmM', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.click(key='eoXMpc7L0Eo0l', desc='@快递易图标开关', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='pD32KDA5tWXO3', desc='计算运费', tag='span')
        self.input(key='bB0SQQi6MaNSr', text='备注', desc='请填写备注', tag='input')
        self.input(key='jL9WnfLtQLoxe', text='120', desc='请输入销售金额', tag='input')
        self.scroll(element='g2V21ltvZLp6L')
        self.click(key='g2V21ltvZLp6L', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='配件销售')
        self.capture_api_request(url_keyword=self.URL['kyVzUMNcM'])
        return self

    @reset_after_execution
    @doc(s4ix3uhl32fhg96aeiis)
    def s4ix3uhl32fhg96aeiis(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='dqNtLSZ2z4KHd', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='V3fidO7FuTxun', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='G3v92pKgJ63UV', desc='配件销售', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='DxlU9msNYUqtQ', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.click(key='NInCPYIMyiaXU', desc='未收款', tag='span')
        self.click(key='ubEnXsxAfp9VC', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.input(key='pJMfstm9lx9JO', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='FF5CWQZPgHacR', text='12', desc='请填写物流费用', tag='input')
        self.input(key='cP0C7VfWjKw7X', text='备注', desc='请填写备注', tag='input')
        self.input(key='ZMLtw6FXTiPI0', text='120', desc='请输入销售金额', tag='input')
        self.scroll(element='dtLnjGpFuWX7J')
        self.click(key='dtLnjGpFuWX7J', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='配件销售')
        self.capture_api_request(url_keyword=self.URL['kyVzUMNcM'])
        return self

    @reset_after_execution
    @doc(r5gxaxtpflvd7qfj153k)
    def r5gxaxtpflvd7qfj153k(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='FK4i97nRBTrFX', desc='@物品编号链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='P3w3xAKrqC1bJ', desc='@修改图标', tag='div', index=2, p_tag='div', p_name='top-detail flex flex-col-center')
        self.click(key='HiMiPRLMgG43i', desc='请选择品牌', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='sjl7I6HBPR1e8', desc='请选择型号', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='nNhQDc73AIZGR', desc='请选择配件名称', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='YSh7YG9WvHZOT', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['PSwyXMyag'])
        return self

    @reset_after_execution
    @doc(abuhabsmqfhq1ut9qc3c)
    def abuhabsmqfhq1ut9qc3c(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='U5fQ8QqZufr0l', desc='@修改图标', tag='i', p_tag='td', p_name='el-table_1_column_9   el-table__cell')
        self.click(key='ATsj7bOrEPoCs', desc='请选择品牌', index=2, tag='input')
        self.down_enter(2)
        self.click(key='cDLwoadytKJxw', desc='请选择型号', index=2, tag='input')
        self.down_enter(2)
        self.click(key='aB2e2NaK32zyH', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='n5O4f0EifY9oE', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['PSwyXMyag'])
        return self

    @reset_after_execution
    @doc(oohakdwo34k03yybh9s8)
    def oohakdwo34k03yybh9s8(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='BNA75V0OdQ97V', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='RcomZEgaO5rf1', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(pn81zph6ujrzvf8p5qxw)
    def pn81zph6ujrzvf8p5qxw(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='rjlbXYNebpGNT', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='xOdFzj6LpbHLo', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(fiy75muh6gz6nsyhyah6)
    def fiy75muh6gz6nsyhyah6(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='sEOFrdgqeJQKy', desc='请选择所属人', tag='input')
        self.down_enter()
        self.click(key='UPtoUJdXzFot0', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(lqdftflzdi25uvz52b4z)
    def lqdftflzdi25uvz52b4z(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['purchaseNo']})
        self.click(key='RmFaemelH03WR', desc='请输入采购单号', tag='input')
        self.down_enter()
        self.click(key='XUSobxsSM7NH6', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(j4r6o9x82lrhfgn7houk)
    def j4r6o9x82lrhfgn7houk(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['purchaseNo']})
        self.click(key='yOjh3A6fCPxX2', desc='请选择采购人员', tag='input')
        self.down_enter()
        self.click(key='gC6JxaPM4jHP7', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(awfdfgrvu5yt8ocg4om9)
    def awfdfgrvu5yt8ocg4om9(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['purchaseNo']})
        self.input(key='kibunym3xItJW', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='G9YkZJNowQKkn', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.esc()
        self.click(key='UO2RhIfxgWorC', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(ie8fsxmabji7a7q54r1w)
    def ie8fsxmabji7a7q54r1w(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='nzYNqk6HpwckC', desc='请选择配件分类', tag='input')
        self.down_enter(2)
        self.click(key='JI4CEnNvXCG8v', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(tje23q2s5q19u1i0r264)
    def tje23q2s5q19u1i0r264(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Ln3o0LEWp1hxy', desc='请选择库存状态', tag='input')
        self.down_enter(2)
        self.click(key='jfhsQjOgLaQaD', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(utqrzheihgso0dngmplj)
    def utqrzheihgso0dngmplj(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='xEeATCbv2QzK4', desc='请选择品类', tag='input')
        self.down_enter()
        self.click(key='DBHnd3KuLQJsG', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(vfi204ksnbxzyybqadvh)
    def vfi204ksnbxzyybqadvh(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='TBnedOglh1TbV', desc='请选择品类', tag='input')
        self.down_enter()
        self.click(key='tUxjopZl76ucW', desc='请选择品牌', tag='input')
        self.down_enter(2)
        self.click(key='pwvgKM0eaZymH', desc='请选择型号', tag='input')
        self.down_enter()
        self.click(key='uB4bVvzX922at', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(x1coaubd9r45peqs8hua)
    def x1coaubd9r45peqs8hua(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='p4tGJ6AyPRDkX', desc='请选择仓库', tag='input')
        self.down_enter()
        self.click(key='ff82jQfu1Rilw', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(tlfu0zq3fcj6qj4k4v02)
    def tlfu0zq3fcj6qj4k4v02(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['accessoryName']})
        self.click(key='r7WTvNR4a8u3Y', desc='展开筛选', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.click(key='GcK3TNmN0GqA9', desc='请输入配件名称', tag='input')
        self.ctrl_v()
        self.click(key='LlHXg6abnTejc', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(je9vs9v7ryk65bgnpnrt)
    def je9vs9v7ryk65bgnpnrt(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='oznaMjYZq4Zwn', desc='展开筛选', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.click(key='r1ZvEQ00ZOmmV', desc='请选择配件成色', tag='input')
        self.down_enter()
        self.click(key='TJKHhRsSstM3O', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(is3591xz3eohk67pi7h9)
    def is3591xz3eohk67pi7h9(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        self.click(key='Wf5qhNGJs9E23', desc='展开筛选', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.click(key='R70bYRVEbqXO4', desc='请输入配件编号', tag='input')
        self.ctrl_v()
        self.click(key='ZQnckwyk8HtyA', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(d41766ll2lal2a6qly54)
    def d41766ll2lal2a6qly54(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='RAubUqj7749iK', desc='展开筛选', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.click(key='KS6fZMMxWj3GI', desc='请选择天数', tag='input')
        self.down_enter()
        self.click(key='G0y3sFq77O7hD', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self

    @reset_after_execution
    @doc(wuufeqpw5tq8hy6290ce)
    def wuufeqpw5tq8hy6290ce(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='ZYYuYST6dRtGQ', desc='展开筛选', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.click(key='SJxyB6QT3tnTN', desc='请选择配件渠道', tag='input')
        self.down_enter()
        self.click(key='cOxOQUXWaqXWi', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QARwOTuPY'])
        return self


class MOknFMNUFIv(CommonPages):
    """配件管理|配件维护"""

    def menu_manage(self):
        """菜单"""
        self.click(key='POSzQmxApydJW', desc='配件管理', tag='span')
        self.scroll(element='U9Cg2iA7hY0RF')
        self.click(key='U9Cg2iA7hY0RF', desc='配件维护', tag='span')
        return self

    @reset_after_execution
    @doc(vnsg549qqo4e8la9pvyz)
    def vnsg549qqo4e8la9pvyz(self):
        self.menu_manage()
        self.click(key='iW04M0VwM80VM', desc='新增', tag='span')
        self.click(key='Opxc8nyh5kXZu', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.input(key='ILwbzhIwhTltq', text='名称' + self.imei, desc='请输入配件名称', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='s8NvFL1gHShcR', desc='@状态开关', tag='span', p_tag='div', p_name='el-switch is-checked')
        self.click(key='zeXVBLPivQcHw', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['KbfOfrq4k'])
        return self

    @reset_after_execution
    @doc(sk6ol090tlyb6qyetwl2)
    def sk6ol090tlyb6qyetwl2(self):
        self.menu_manage()
        self.click(key='v5Rns3Di46RVC', desc='新增', tag='span')
        self.click(key='OLiGgQHPTFur8', desc='请选择配件品类', tag='input')
        self.down_enter(2)
        self.input(key='CGH7eXrrtlX0c', text='名称' + self.imei, desc='请输入配件名称', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='X9gAaOiUea1I6', desc='@状态开关', tag='span', p_tag='div', p_name='el-switch is-checked')
        self.click(key='HFCAQcDDL9Ztd', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['KbfOfrq4k'])
        return self

    @reset_after_execution
    @doc(e8rzsfkgsktqcjm31vfu)
    def e8rzsfkgsktqcjm31vfu(self):
        self.menu_manage()
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()[0]['accessoryNo']
        ParamCache.cache_object({"i": obj})
        self.click(key='DA2hLv4zygFZ4', desc='编辑', tag='span', p_tag='td', p_name='el-table_1_column_6   el-table__cell')
        self.input(key='Lj8VZoWPMQbkt', text='摄像头', desc='请输入配件名称', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='PQadgXgAFm8gm', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['VFgNtfVfH'])
        return self

    @reset_after_execution
    @doc(u8m46ujx2im1noarlsmu)
    def u8m46ujx2im1noarlsmu(self):
        self.menu_manage()
        self.click(key='hfaDC4zz1TZQN', desc='删除', tag='span', p_tag='td', p_name='el-table_1_column_6   el-table__cell')
        self.click(key='S6r1DijTnkprm', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['M3mcL0BDw'])
        return self

    @reset_after_execution
    @doc(fd2dzuppjfcy0vc68osp)
    def fd2dzuppjfcy0vc68osp(self):
        self.menu_manage()
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        self.click(key='hy4jyqfKfZtyM', desc='请输入配件编号', tag='input')
        self.ctrl_v()
        self.click(key='RdG7V7mi7yeWU', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['GTZ0UOiDK'])
        return self

    @reset_after_execution
    @doc(oqclfc811pbxjb1ydmtf)
    def oqclfc811pbxjb1ydmtf(self):
        self.menu_manage()
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        ParamCache.cache_object({"i": obj[0]['accessoryName']})
        self.click(key='MgJ4krYLgX4UO', desc='请输入配件名称', tag='input')
        self.ctrl_v()
        self.click(key='hCODLrwOmkK8y', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['GTZ0UOiDK'])
        return self

    @reset_after_execution
    @doc(uxs5seo7otyrzfugdqsl)
    def uxs5seo7otyrzfugdqsl(self):
        self.menu_manage()
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        ParamCache.cache_object({"i": obj[0]['accessoryName']})
        self.click(key='IpyFC2bphVHNm', desc='请选择配件状态', tag='input')
        self.down_enter()
        self.click(key='wTMVKsMY2WjfD', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['GTZ0UOiDK'])
        return self


class Ud4EebvDnHM(CommonPages):
    """配件管理|入库管理|旧配件入库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='jhKISs8QHnJvF', desc='配件管理', tag='span')
        self.click(key='yDYs83JuO2ANm', desc='入库管理', tag='span', index=2)
        self.click(key='S4jehaq9lgbfs', desc='旧配件入库', tag='span')
        return self

    @reset_after_execution
    @doc(sPBqvfYc9boVR4rGIL4w)
    def sPBqvfYc9boVR4rGIL4w(self):
        self.menu_manage()
        self.click(key='nv1qHla9eokRg', desc='新建入库', tag='span')
        self.click(key='qZ5kpZl02GjhA', desc='请选择仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='hMdmnY4jFKWA8', desc='请选择入库人', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='ThomKjfdiBCYf', text='备注', desc='请输入备注', tag='input')
        self.click(key='Oc2Cs4782wGGO', desc='添加物品', tag='span')
        self.click(key='JueXL4Xisw5jl', desc='请选择品类', tag='input')
        self.down_enter()
        self.click(key='KFUxiP3LntKBB', desc='请选择适用品牌', tag='input')
        self.down_enter()
        self.click(key='NrJ4LGdzuCXPD', desc='请选择适用型号', tag='input')
        self.down_enter()
        self.click(key='lQFoGQTX07Nkf', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='zzftsxyrrLsO7', desc='请选择配件名称', tag='input')
        self.down_enter()
        self.click(key='i94I0xhLCgyuG', desc='请选择渠道', tag='input')
        self.down_enter()
        self.input(key='IvAZoEoTE0G6b', text='1', desc='请输入具体数量', tag='input')
        self.input(key='AtST8l3wLVa8y', text='15', desc='请输入采购价格', tag='input')
        self.click(key='QWrWhzz5GDYEy', desc='添加并关闭', tag='span')
        self.click(key='W9fUF6c0IYuvL', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['AowpSZBva'])
        return self

    @reset_after_execution
    @doc(zq8av7DX7E15sOdOA5na)
    def zq8av7DX7E15sOdOA5na(self):
        self.menu_manage()
        self.click(key='VbPBkeW6RNpzG', desc='新建入库', tag='span')
        self.click(key='RFBVxrGYj0Oso', desc='请选择仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='srfjv6enFcyxv', desc='请选择入库人', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='KAbjndplDEN3s', text='备注', desc='请输入备注', tag='input')
        self.click(key='GrtSq8UQoZxmV', desc='添加物品', tag='span')
        self.click(key='r2RX9ybOVopdB', desc='请选择品类', tag='input')
        self.down_enter()
        self.click(key='ACTxFVgb0HV40', desc='请选择适用品牌', tag='input')
        self.down_enter()
        self.click(key='fkQH116gAW7rn', desc='请选择适用型号', tag='input')
        self.down_enter()
        self.click(key='I5xmUzu0nbnCb', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='O1G8TqwdoqrI7', desc='请选择配件名称', tag='input')
        self.down_enter()
        self.click(key='chfhT62HNPNlX', desc='请选择渠道', tag='input')
        self.down_enter()
        self.input(key='KJek023loQppT', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='TqLtHWpKNxtPV', text='15', desc='请输入采购价格', tag='input')
        self.click(key='Q99MHofOSsPib', desc='添加并关闭', tag='span')
        self.click(key='DHdNamFX3UWw0', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['AowpSZBva'])
        return self

    @reset_after_execution
    @doc(NIg8OImrULuxaaLnvprF)
    def NIg8OImrULuxaaLnvprF(self):
        self.menu_manage()
        self.click(key='aPXw7fxckyHwk', desc='新建入库', tag='span')
        self.click(key='DlS7MOLu3kiWu', desc='请选择仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='RifQyaaGtopyV', desc='请选择入库人', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='tnjSUoFC3nAjG', text='备注', desc='请输入备注', tag='input')
        self.click(key='Uf165rBAaoQBj', desc='添加物品', tag='span')
        self.click(key='O0mdzu43l0DJR', desc='请选择品类', tag='input')
        self.down_enter(2)
        self.click(key='ncSrtalmlETVO', desc='请选择适用品牌', tag='input')
        self.down_enter(2)
        self.click(key='ZSorQBPzwHz7v', desc='请选择适用型号', tag='input')
        self.down_enter(2)
        self.click(key='HPp67f6tZqueV', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='CQEuAf6618dGb', desc='请选择配件名称', tag='input')
        self.down_enter()
        self.click(key='jFndswvRT7RfW', desc='请选择渠道', tag='input')
        self.down_enter()
        self.input(key='GWaXvUJcR4DOC', text='1', desc='请输入具体数量', tag='input')
        self.input(key='Avo7rcSIJ1dk2', text='15', desc='请输入采购价格', tag='input')
        self.click(key='VpTHzWXFqYJjI', desc='添加并关闭', tag='span')
        self.click(key='ZOxyittZhfI9M', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['AowpSZBva'])
        return self

    @reset_after_execution
    @doc(V7VzYOhxyeCqh4OaUKh3)
    def V7VzYOhxyeCqh4OaUKh3(self):
        self.menu_manage()
        self.click(key='zMWpqQOk5GicJ', desc='新建入库', tag='span')
        self.click(key='nCS1C3IpPCYAy', desc='请选择仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='WYAxokd0dwveU', desc='请选择入库人', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='sNHI8iU6rtsxh', text='备注', desc='请输入备注', tag='input')
        self.click(key='ekUsQz40YQEei', desc='添加物品', tag='span')
        self.click(key='yiinwxkNa3FdQ', desc='请选择品类', tag='input')
        self.down_enter(3)
        self.click(key='rFeGZamWVDTXX', desc='请选择适用品牌', tag='input')
        self.down_enter(3)
        self.click(key='iEYJ9hHNli6og', desc='请选择适用型号', tag='input')
        self.down_enter(3)
        self.click(key='rA5VXTRgNvKjY', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='RE3dKVaAwIrvV', desc='请选择配件名称', tag='input')
        self.down_enter()
        self.click(key='u5G2CVbmVkjzO', desc='请选择渠道', tag='input')
        self.down_enter()
        self.input(key='hAhipFvTx6qvs', text='1', desc='请输入具体数量', tag='input')
        self.input(key='Hg0ufbrYVbNR5', text='15', desc='请输入采购价格', tag='input')
        self.click(key='fR1p7mCP8bSwj', desc='添加并关闭', tag='span')
        self.click(key='XPlaek1L4ATR2', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['AowpSZBva'])
        return self

    @reset_after_execution
    @doc(PMcmyjds8q4To8x1WYWe)
    def PMcmyjds8q4To8x1WYWe(self):
        self.menu_manage()
        self.click(key='liZuiAJLBdpsg', desc='新建入库', tag='span')
        self.click(key='FtodmKqvQLY5O', desc='请选择仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='QCfbPC2ZddbSK', desc='请选择入库人', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='pv5WADPub5h75', text='备注', desc='请输入备注', tag='input')
        self.click(key='MiUppEQFN5VRp', desc='添加物品', tag='span')
        self.click(key='C3vENqkyFJTXt', desc='请选择品类', tag='input')
        self.down_enter(4)
        self.click(key='ZBntddsbaEsUv', desc='请选择适用品牌', tag='input')
        self.down_enter(4)
        self.click(key='ESSMFOx5jVdaY', desc='请选择适用型号', tag='input')
        self.down_enter(4)
        self.click(key='yVOr5qyKCe90U', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='wgQ5sOTWah5IU', desc='请选择配件名称', tag='input')
        self.down_enter()
        self.click(key='aR2OXX8jPYe0b', desc='请选择渠道', tag='input')
        self.down_enter()
        self.input(key='Gjq7ErT9s0JP6', text='1', desc='请输入具体数量', tag='input')
        self.input(key='T1IKi7yemFLzR', text='15', desc='请输入采购价格', tag='input')
        self.click(key='EJo6amMRf71JN', desc='添加并关闭', tag='span')
        self.click(key='YYYeYVj21G4Fg', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['AowpSZBva'])
        return self

    @reset_after_execution
    @doc(rXmtCESQnyljezY5hqQF)
    def rXmtCESQnyljezY5hqQF(self):
        self.menu_manage()
        obj = self.pc.RjB1dOTFUrlGReUmemgQr(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='ay6CxwShw2Jb3', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='b3dLd4j5HFciZ', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['icqD4B9Rk'])
        return self

    @reset_after_execution
    @doc(BBRaKuLnfUAs23bBdW7L)
    def BBRaKuLnfUAs23bBdW7L(self):
        self.menu_manage()
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='XuWTHTb5MgMCF', desc='请输入入库单号', tag='input')
        self.ctrl_v()
        self.click(key='McHqstNPiCh2a', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['icqD4B9Rk'])
        return self

    @reset_after_execution
    @doc(whT4XzVC2HWmjrLwPGbu)
    def whT4XzVC2HWmjrLwPGbu(self):
        self.menu_manage()
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='R2ZvMFEgEJ6wg', desc='请选择仓库', tag='input')
        self.down_enter(2)
        self.click(key='Yub3BvpcuEwVr', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['icqD4B9Rk'])
        return self

    @reset_after_execution
    @doc(sJy6JWqmmKyM7r2DjLiS)
    def sJy6JWqmmKyM7r2DjLiS(self):
        self.menu_manage()
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='ouKkWQqgx89Qn', desc='请选择入库人', tag='input')
        self.down_enter()
        self.click(key='E6GfbmhoaUWW2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['icqD4B9Rk'])
        return self

    @reset_after_execution
    @doc(WbSFKLvOUocIJPFJCwVb)
    def WbSFKLvOUocIJPFJCwVb(self):
        self.menu_manage()
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.input(key='UCjF2ep1r9b9W', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='zyW0zXbhvtdgI', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.esc()
        self.click(key='gkAT6kqE40erR', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['icqD4B9Rk'])
        return self


class ZSRzZe4N9Tb(CommonPages):
    """配件管理|入库管理|分拣列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='Ut6tyPASHTCVw', desc='配件管理')
        self.click(key='EYfL5BzEjdBHI', desc='入库管理', index=2, tag='span')
        self.click(key='yK5gQoL34vpOB', desc='分拣列表', tag='span')
        return self

    @reset_after_execution
    @doc(BJG1WPKutnjPESnRiaE3)
    def BJG1WPKutnjPESnRiaE3(self):
        self.menu_manage()
        self.click(key='LoKxv8B8eO2J7', desc='导出全部', tag='span')
        return self

    @reset_after_execution
    @doc(kieRlhO7K2AGuSdQH9b3)
    def kieRlhO7K2AGuSdQH9b3(self):
        self.menu_manage()
        obj = self.pc.LnfQBDqBvleaE2O0412qk()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.click(key='Kikae4Yu9PFFv', desc='请输入快递单号', tag='input')
        self.ctrl_v()
        self.click(key='Lbmhx39BSbNk2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QTembQdXx'])
        return self

    @reset_after_execution
    @doc(bOxmYfGUFrevxZUW1A6G)
    def bOxmYfGUFrevxZUW1A6G(self):
        self.menu_manage()
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='VyBvE5DIZm1UI', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='o3bvwO35zZvF1', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QTembQdXx'])
        return self

    @reset_after_execution
    @doc(gMjMJ10FSSvSiwf8JbsW)
    def gMjMJ10FSSvSiwf8JbsW(self):
        self.menu_manage()
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['businessNo']})
        self.click(key='Ry0iLzOdedmIK', desc='请输入业务单号', tag='input')
        self.ctrl_v()
        self.click(key='G9Hgn3zafJ0Oj', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QTembQdXx'])
        return self

    @reset_after_execution
    @doc(x2I7I6LSgnOWJ5UfzkPs)
    def x2I7I6LSgnOWJ5UfzkPs(self):
        self.menu_manage()
        obj = self.pc.LnfQBDqBvleaE2O0412qk()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.click(key='LHZejXb08JKZP', desc='请选择分拣状态', tag='input')
        self.down_enter()
        self.click(key='deYDJjVi7fEFs', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QTembQdXx'])
        return self

    @reset_after_execution
    @doc(BnQQG1HUn8tvq1ZjDMCV)
    def BnQQG1HUn8tvq1ZjDMCV(self):
        self.menu_manage()
        obj = self.pc.LnfQBDqBvleaE2O0412qk()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.input(key='qL1RFIcZyaxVY', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='USSHpJHHMrW30', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='MvUmGBOsfjCzc', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['QTembQdXx'])
        return self


class NeDm1H7FxRQ(CommonPages):
    """配件管理|配件采购|新增采购单"""

    def menu_manage(self):
        """菜单"""
        self.click(key='f8AOGv7QJMgqG', desc='配件管理', tag='span')
        self.scroll(element='J7RNY5tdILpCW')
        self.click(key='J7RNY5tdILpCW', desc='配件采购', tag='span')
        self.click(key='UbgeX1eZOhraj', desc='新增采购单', tag='span', index=2)
        return self

    @reset_after_execution
    @doc(rYvpUsdluGutOhIhm7af)
    def rYvpUsdluGutOhIhm7af(self):
        self.menu_manage()
        self.click(key='Hrc3Dh0wlagpf', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='gjJYSTJrRTpUy', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='GaMrEv7e9QXhw', desc='请选择付款状态', tag='input')
        self.down_enter()
        self.input(key='IwZ4WBSwJDhAB', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='henzHJIbjrzGz', text='12', desc='请输入物流费用', tag='input')
        self.input(key='bnQaNzll2WvVx', text='备注', desc='请输入备注', tag='input')
        self.click(key='JCvQ4mtqNkVsh', desc='新增', tag='span')
        self.click(key='kpwPe7AScEs9f', desc='请选择品类', tag='input')
        self.down_enter(2)
        self.click(key='IRPmfrRADZNLd', desc='请选择品牌', tag='input')
        self.down_enter(2)
        self.click(key='AUKk4Hc0RNJcn', desc='请选择', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='d8cBZnl0BdO2q', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='bxotaU4thYFG9', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='idiqeZfe3dlos', desc='请选择成色', tag='input')
        self.down_enter(2)
        self.click(key='YPnMcPP3teG7X', desc='请选择渠道', tag='input')
        self.down_enter(2)
        self.input(key='CwhKQdz6bIXer', text='1', desc='请输入具体数量', tag='input')
        self.input(key='cP6BFp2AmBEzB', text='123', desc='请输入采购价格', tag='input')
        self.click(key='zQG6UYxG8TKFg', desc='添加并关闭', tag='span')
        self.click(key='Tv1kXUcWzfRwZ', desc='选择日期时间', tag='input')
        self.input(key='IurB7y8Lc0NLp', text=self.get_current_time_hms(), desc='选择时间', tag='input')
        self.click(key='iPIcK9RhLmhIG', desc='确定', tag='span', p_tag='div', p_name='el-picker-panel el-date-picker el-popper has-time')
        self.click(key='V2cGV7CedtfnX', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['qg5Cp2gXr'])
        return self

    @reset_after_execution
    @doc(niKwILpBHogDvGt52uEB)
    def niKwILpBHogDvGt52uEB(self):
        self.menu_manage()
        self.click(key='iPVWRPzdDNlXp', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='SXPloJ26VEqgO', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='wXYT7G54ExqHH', desc='请选择付款状态', tag='input')
        self.down_enter(2)
        self.click(key='H5Tph7yx57H5c', desc='请选择付款账户', tag='input')
        self.down_enter()
        self.click(key='v7XwmZxtW5Yb0', desc='请选择包裹状态', tag='input')
        self.down_enter(3)
        self.click(key='hlctgp7mgnkE3', desc='请选择仓库', tag='input')
        self.down_enter()
        self.input(key='BTiaFNpHZCpZX', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='BvlmRhCENlReh', text='12', desc='请输入物流费用', tag='input')
        self.input(key='rnvv2lCE9zIyY', text='备注', desc='请输入备注', tag='input')
        self.click(key='EpQbWZehZ8I40', desc='新增', tag='span')
        self.click(key='vo2V4UQVepFWO', desc='请选择品类', tag='input')
        self.down_enter()
        self.click(key='Xov6m38Jfr40J', desc='请选择品牌', tag='input')
        self.down_enter()
        self.click(key='VuZHpiBoPCOTt', desc='请选择', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='nIyA0ayxcCGRK', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='HMd3f9j7aVkzD', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='iRorsdS4XVqo5', desc='请选择成色', tag='input')
        self.down_enter(2)
        self.click(key='Gus3FzEwZoLdl', desc='请选择渠道', tag='input')
        self.down_enter(2)
        self.input(key='QhWaZacHJE9gc', text='1', desc='请输入具体数量', tag='input')
        self.input(key='K7XLna8cy2SFB', text='123', desc='请输入采购价格', tag='input')
        self.click(key='jVhMqBvDmaGgH', desc='添加并关闭', tag='span')
        self.click(key='KEtZL8s3sd2uo', desc='选择日期时间', tag='input')
        self.input(key='I6HtuygufpI3w', text=self.get_current_time_hms(), desc='选择时间', tag='input')
        self.click(key='k4XvmuhSbIwLD', desc='确定', tag='span', p_tag='div', p_name='el-picker-panel el-date-picker el-popper has-time')
        self.click(key='suAC0Mxbp4CAY', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['qg5Cp2gXr'])
        return self

    @reset_after_execution
    @doc(nBfEGGe1LJguXHi6aesS)
    def nBfEGGe1LJguXHi6aesS(self):
        self.menu_manage()
        self.click(key='psaBNbl5NATuK', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='crtN1WFS8GYKl', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='Czzbqa7JWvwIe', desc='请选择付款状态', tag='input')
        self.down_enter()
        self.input(key='sYvvP4VvL6yYr', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='ROJc6y58QwfvM', text='12', desc='请输入物流费用', tag='input')
        self.input(key='EqVvmk7B0EfOQ', text='备注', desc='请输入备注', tag='input')
        self.click(key='D1UOFb5KsOhAW', desc='新增', tag='span')
        self.click(key='kHb0RXN5nUdYc', desc='请选择品类', tag='input')
        self.down_enter(3)
        self.click(key='mYzZBto8PYHjx', desc='请选择品牌', tag='input')
        self.down_enter(3)
        self.click(key='rX2GWiyRgQyEy', desc='请选择', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(3)
        self.click(key='Xkve915u7gfpl', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='VPCjdS6oLtUnZ', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='xzITkNVDAybSR', desc='请选择成色', tag='input')
        self.down_enter(2)
        self.click(key='yHHdpuGayNzg0', desc='请选择渠道', tag='input')
        self.down_enter(2)
        self.input(key='nxP8qQrcREFZP', text='1', desc='请输入具体数量', tag='input')
        self.input(key='Xj97nTZR6rFgY', text='123', desc='请输入采购价格', tag='input')
        self.click(key='erQGmo0JjhFSS', desc='添加并关闭', tag='span')
        self.click(key='Nawb7EWAsm75c', desc='选择日期时间', tag='input')
        self.input(key='av8NGX0FHfpb2', text=self.get_current_time_hms(), desc='选择时间', tag='input')
        self.click(key='s8lotkMtqWD3i', desc='确定', tag='span', p_tag='div', p_name='el-picker-panel el-date-picker el-popper has-time')
        self.click(key='DkFbWFnQkM2ch', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['qg5Cp2gXr'])
        return self

    @reset_after_execution
    @doc(fi51E5jCFUxE1nLYPO7w)
    def fi51E5jCFUxE1nLYPO7w(self):
        self.menu_manage()
        self.click(key='PoQqtIDYmYmjg', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='nUbNzAnYIiZaM', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='iW0gCJ0R8heBV', desc='请选择付款状态', tag='input')
        self.down_enter(2)
        self.click(key='dwKbu6mMMiqlp', desc='请选择付款账户', tag='input')
        self.down_enter()
        self.click(key='xYabPL8I9UzGm', desc='请选择包裹状态', tag='input')
        self.down_enter(3)
        self.click(key='GskE8VcCCsQSu', desc='请选择仓库', tag='input')
        self.down_enter()
        self.input(key='s6agQIsoTinvS', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='IjYbO3X7Tqsng', text='12', desc='请输入物流费用', tag='input')
        self.input(key='UarY03BLh2DLh', text='备注', desc='请输入备注', tag='input')
        self.click(key='SJLnoDG8RloHq', desc='新增', tag='span')
        self.click(key='bMGMxmugiW6uo', desc='请选择品类', tag='input')
        self.down_enter(4)
        self.click(key='Dr8sxj782I0FV', desc='请选择品牌', tag='input')
        self.down_enter(4)
        self.click(key='C4dzOTC07Jy1f', desc='请选择', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(4)
        self.click(key='loot4SyZ0iEu5', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='ShpW1kAR2cxn8', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='uUi07jtquhGeh', desc='请选择成色', tag='input')
        self.down_enter(2)
        self.click(key='D5LPcuRtDHdsE', desc='请选择渠道', tag='input')
        self.down_enter(2)
        self.input(key='Uhrx85BNjEy76', text='1', desc='请输入具体数量', tag='input')
        self.input(key='LesxR2xvLx3xN', text='123', desc='请输入采购价格', tag='input')
        self.click(key='K25tHqi5C7GnI', desc='添加并关闭', tag='span')
        self.click(key='Ft1B11OUvtd5A', desc='选择日期时间', tag='input')
        self.input(key='aJvsTf3ce6nxJ', text=self.get_current_time_hms(), desc='选择时间', tag='input')
        self.click(key='Ptwu2HZoqqGSC', desc='确定', tag='span', p_tag='div', p_name='el-picker-panel el-date-picker el-popper has-time')
        self.click(key='Lmkg43x3fUjc7', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['qg5Cp2gXr'])
        return self

    @reset_after_execution
    @doc(qyeHP1UKtW02kXOihCU1)
    def qyeHP1UKtW02kXOihCU1(self):
        self.menu_manage()
        self.click(key='PoQqtIDYmYmjg', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='nUbNzAnYIiZaM', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='iW0gCJ0R8heBV', desc='请选择付款状态', tag='input')
        self.down_enter(2)
        self.click(key='dwKbu6mMMiqlp', desc='请选择付款账户', tag='input')
        self.down_enter()
        self.click(key='xYabPL8I9UzGm', desc='请选择包裹状态', tag='input')
        self.down_enter(3)
        self.click(key='GskE8VcCCsQSu', desc='请选择仓库', tag='input')
        self.down_enter()
        self.input(key='s6agQIsoTinvS', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='IjYbO3X7Tqsng', text='12', desc='请输入物流费用', tag='input')
        self.input(key='UarY03BLh2DLh', text='备注', desc='请输入备注', tag='input')
        self.click(key='SJLnoDG8RloHq', desc='新增', tag='span')
        self.click(key='bMGMxmugiW6uo', desc='请选择品类', tag='input')
        self.down_enter(4)
        self.click(key='Dr8sxj782I0FV', desc='请选择品牌', tag='input')
        self.down_enter(4)
        self.click(key='C4dzOTC07Jy1f', desc='请选择', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(4)
        self.click(key='loot4SyZ0iEu5', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='ShpW1kAR2cxn8', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='uUi07jtquhGeh', desc='请选择成色', tag='input')
        self.down_enter(2)
        self.click(key='D5LPcuRtDHdsE', desc='请选择渠道', tag='input')
        self.down_enter(2)
        self.input(key='Uhrx85BNjEy76', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='LesxR2xvLx3xN', text='123', desc='请输入采购价格', tag='input')
        self.click(key='K25tHqi5C7GnI', desc='添加并关闭', tag='span')
        self.click(key='Ft1B11OUvtd5A', desc='选择日期时间', tag='input')
        self.input(key='aJvsTf3ce6nxJ', text=self.get_current_time_hms(), desc='选择时间', tag='input')
        self.click(key='Ptwu2HZoqqGSC', desc='确定', tag='span', p_tag='div', p_name='el-picker-panel el-date-picker el-popper has-time')
        self.click(key='Lmkg43x3fUjc7', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['qg5Cp2gXr'])
        return self

    @reset_after_execution
    @doc(Cd8pPBeDJMVuZBrTbFXN)
    def Cd8pPBeDJMVuZBrTbFXN(self):
        self.menu_manage()
        self.click(key='pPimNHaelw7W6', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='DOyRmlsGVoQo4', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='Tfi3XbMVHhy13', desc='请选择付款状态', tag='input')
        self.down_enter()
        self.input(key='F0P4PXN7zfvfx', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='Ms1Qlsa0seDbv', text='12', desc='请输入物流费用', tag='input')
        self.input(key='kPf2GZBoZwafO', text='备注', desc='请输入备注', tag='input')
        self.click(key='DJfZRtzlt7VqO', desc='新增', tag='span')
        self.click(key='jcYOs0fS70vKd', desc='请选择品类', tag='input')
        self.down_enter(2)
        self.click(key='ZHgjf3e4XYYgd', desc='请选择品牌', tag='input')
        self.down_enter(2)
        self.click(key='QPBQmXk4KdnGF', desc='请选择', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='hW5fe1sdxSzKU', desc='请选择配件品类', tag='input')
        self.up_enter()
        self.click(key='I5VsN90iUqHFa', desc='请选择配件名称', tag='input')
        self.down_enter(2)
        self.click(key='zKrBNDUPZ8s4Z', desc='请选择成色', tag='input')
        self.down_enter(2)
        self.click(key='Cadbol40Z3jjj', desc='请选择渠道', tag='input')
        self.down_enter(2)
        self.input(key='FzAfTx6tv4XAg', text='1', desc='请输入具体数量', tag='input')
        self.input(key='D5fM9oNwN2aeV', text='12', desc='请输入采购价格', tag='input')
        self.click(key='AkZgphp63bzN3', desc='@＋图标', tag='div', p_tag='td', p_name='el-table_2_column_19   el-table__cell')
        self.click(key='lQBRks5aTupsd', desc='请选择配件品类', tag='input', index=2)
        self.up_enter()
        self.click(key='iJQYsGuACo87D', desc='请选择配件名称', tag='input', index=2)
        self.down_enter(2)
        self.click(key='GhUwovnSV0sI3', desc='请选择成色', tag='input', index=2)
        self.down_enter(2)
        self.click(key='XMwlYjbtaxBmf', desc='请选择渠道', tag='input', index=2)
        self.down_enter(2)
        self.input(key='qpeQ3jU9HzXpn', text='1', desc='请输入具体数量', index=2, tag='input')
        self.input(key='rBoWcShagh4em', text='12', desc='请输入采购价格', index=2, tag='input')
        self.click(key='Dox7PotXhrJ1H', desc='添加并关闭', tag='span')
        self.click(key='rw4PJAWyuOeAC', desc='选择日期时间', tag='input')
        self.input(key='B8gIr779zFOVU', text=self.get_current_time_hms(), desc='选择时间', tag='input')
        self.click(key='f8DQDssUbDVqQ', desc='确定', tag='span', p_tag='div', p_name='el-picker-panel el-date-picker el-popper has-time')
        self.click(key='A8ayFO9NxueBm', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['qg5Cp2gXr'])
        return self


class CrIo44NXokZ(CommonPages):
    """配件管理|配件采购|采购列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='FhevP52jQdt0o', desc='配件管理', tag='span')
        self.scroll(element='x9alRppGzRf8C')
        self.click(key='x9alRppGzRf8C', desc='配件采购', tag='span')
        self.click(key='EjcXpIVIIiV9s', desc='采购列表', tag='span')
        return self

    @reset_after_execution
    @doc(ytFlEaPZYL2krOQHCL4y)
    def ytFlEaPZYL2krOQHCL4y(self):
        self.menu_manage()
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='gF3cgCwwa476x', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='Obj37W8lSc9CU', desc='采购售后', tag='span')
        self.click(key='Ae2EE4PdO9tkp', desc='请选择售后类型', tag='input')
        self.down_enter()
        self.click(key='MJlmbWNRJfhkK', desc='@快递易图标开关', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='SGrleUy5VOpqp', desc='计算运费', tag='span')
        self.click(key='KHtPjB0klzwcz', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后')
        self.capture_api_request(url_keyword=self.URL['fed411lAJ'])
        return self

    @reset_after_execution
    @doc(DUKh4wv9QHERfWyZo08U)
    def DUKh4wv9QHERfWyZo08U(self):
        self.menu_manage()
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='dooEB87W9XWcc', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='NgHwqle7UFBre', desc='采购售后', tag='span')
        self.click(key='KthEfi5b414wk', desc='请选择售后类型', tag='input')
        self.down_enter()
        self.input(key='JzCOfgkRGPKHd', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='haRt7Hcfi87GI', text='12', desc='请填写物流费用', tag='input')
        self.input(key='w0yjz7xTWoqPj', text='备注', desc='请填写备注', tag='input')
        self.click(key='MXiuckjGqWa40', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后')
        self.capture_api_request(url_keyword=self.URL['fed411lAJ'])
        return self

    @reset_after_execution
    @doc(kuo3zYG5OY6r1J5GFLwS)
    def kuo3zYG5OY6r1J5GFLwS(self):
        self.menu_manage()
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Jldkpqw8AxUyO', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='w0QKIZvcQykNx', desc='采购售后', tag='span')
        self.click(key='ZxcsQEItI3H4W', desc='请选择售后类型', tag='input')
        self.down_enter(2)
        self.input(key='vBH6WCzrKKtd5', text='3', desc='请输入退款金额', tag='input')
        self.click(key='qlFhAvdSl3io1', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后')
        self.capture_api_request(url_keyword=self.URL['fed411lAJ'])
        return self

    @reset_after_execution
    @doc(lQzjFGvhm78QmpH58t8f)
    def lQzjFGvhm78QmpH58t8f(self):
        self.menu_manage()
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='u9pT01D0vVg64', desc='采购售后', tag='span')
        self.click(key='WtAaH6bK6LFlh', desc='请选择售后类型', tag='input')
        self.down_enter()
        self.click(key='qlDDDFKQUUbNt', desc='请选择供应商', tag='input')
        self.down_enter()
        self.input(key='uVI97ZGU5taxn', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='XQeYUfP2iYpDN', text='10', desc='请填写物流费用', tag='input')
        self.click(key='YIvqTt7oXadtM', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='i82rsXfI5fXR5', desc='添加', tag='span')
        self.click(key='IS1YQ8u4sP2qG', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后')
        self.capture_api_request(url_keyword=self.URL['fed411lAJ'])
        return self

    @reset_after_execution
    @doc(rNxmjG3kaLQP30Voi9tR)
    def rNxmjG3kaLQP30Voi9tR(self):
        self.menu_manage()
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Xh7aiL5m0RA3h', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='n5cz4D0H2UQTS', desc='采购售后', tag='span')
        self.click(key='VKaJcWUfTHOsL', desc='请选择售后类型', tag='input')
        self.down_enter(2)
        self.input(key='tNRxJaVpitFyZ', text='9999999', desc='请输入退款金额', tag='input')
        self.click(key='tuNSRtDsJxtAH', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后')
        self.capture_api_request(url_keyword=self.URL['fed411lAJ'])
        return self

    @reset_after_execution
    @doc(OCChvTOX3BOwhsZ3x1Vk)
    def OCChvTOX3BOwhsZ3x1Vk(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='VgWgnwD4DifXB', desc='请输入采购单号', tag='input')
        self.ctrl_v()
        self.click(key='PJsO9caxkxaBF', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self

    @reset_after_execution
    @doc(YHUNy8WSwZqIFfM88jqk)
    def YHUNy8WSwZqIFfM88jqk(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='kOAFGUa2hXdcs', desc='请选择采购供应商', tag='input')
        self.down_enter()
        self.click(key='lTADDSIO8cXzs', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self

    @reset_after_execution
    @doc(uTH0rGcq6USIvzBzwnqn)
    def uTH0rGcq6USIvzBzwnqn(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='Yjpf1EacEzwaq', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='zyRK8k5IHIMod', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self

    @reset_after_execution
    @doc(Q66Jftlrzxz0MflmYaRr)
    def Q66Jftlrzxz0MflmYaRr(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='UwYmZL1bCFSjf', text=self.get_the_date(), desc='开始时间', tag='input')
        self.input(key='UsVLDEsbzupzb', text=self.get_the_date(days=1), desc='结束时间', tag='input')
        self.esc()
        self.click(key='YoDjj0hsYGLCx', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self

    @reset_after_execution
    @doc(art1lLuMH6tdwDoJNCVF)
    def art1lLuMH6tdwDoJNCVF(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='hzO8EW1ymbWwZ', desc='请选择采购单状态', tag='input')
        self.down_enter()
        self.click(key='xOaPWrbVZDvTD', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self

    @reset_after_execution
    @doc(aa4ufzsTKdxHRDOhwcsN)
    def aa4ufzsTKdxHRDOhwcsN(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='qzYS4m7fHQeRs', desc='请选择付款状态', tag='input')
        self.down_enter(2)
        self.click(key='zJUJR3zqmSlLU', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self

    @reset_after_execution
    @doc(L2C0xDrhKPDjvib6JES4)
    def L2C0xDrhKPDjvib6JES4(self):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.menu_manage()
        self.click(key='fPEbDkV1TttQE', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='JgLZVaQv0o7Qg', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['fRokl0vv2'])
        return self


class VbLUqADcDi7(CommonPages):
    """配件管理|移交接收管理|接收物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='FCE30XEmKHIZv', desc='配件管理', tag='span')
        self.click(key='Ee71CHPhHLeSJ', desc='移交接收管理', tag='span', index=2)
        self.click(key='vIbTKAEmgxFt3', desc='接收物品', tag='span', index=2)
        return self

    @reset_after_execution
    @doc(YGHj7l8L8BkOXk1wxK6L)
    def YGHj7l8L8BkOXk1wxK6L(self):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='tVsVMGJPyNEAr', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='vTPgEGu0JJQbG', desc='接收', tag='span')
        self.click(key='LRGxfhdTDgMbG', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['Sm7yLloyr'])
        return self

    @reset_after_execution
    @doc(J8ahGmCVn2GdPlK8RMlj)
    def J8ahGmCVn2GdPlK8RMlj(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='eO7HintmOndO1', desc='移交单接收', tag='div')
        self.click(key='q2rbNcJnlwQWt', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='LMvBpy4WS8Yh1', desc='接收', tag='span')
        self.click(key='adtCNQDYYHUXB', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['Sm7yLloyr'])
        return self

    @reset_after_execution
    @doc(NtgvclPRpONVaNJTp0yA)
    def NtgvclPRpONVaNJTp0yA(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='c23oS57rICyd9', desc='扫码精确接收', tag='span')
        self.click(key='qIpEBHAGYIGxJ', desc='请输入物品编号', tag='input')
        self.ctrl_v_enter()
        self.tab_space(2)
        self.click(key='ejEoeh8mn2rRE', desc='接收', tag='span', p_tag='div', p_name='el-dialog__body')
        return self

    @reset_after_execution
    @doc(ODJ550O1VM3zMxrPPETO)
    def ODJ550O1VM3zMxrPPETO(self):
        self.menu_manage()
        self.click(key='sgrjJSLUuJ3Om', desc='移交单接收', tag='div')
        self.click(key='O6rSXamYMAskG', desc='导出', tag='span')
        return self

    @reset_after_execution
    @doc(wJXR0rLyC9FiD2Hab2GK)
    def wJXR0rLyC9FiD2Hab2GK(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='XCTXipWI7Zapx', desc='请输入编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='VIiJI8fa6kXFH', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(vKg2HxGmBKyPPtp6kJf7)
    def vKg2HxGmBKyPPtp6kJf7(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='BlKyVb9lXGA0g', desc='请选择品类', tag='input')
        self.down_enter()
        self.click(key='H8ywCZUdrJTvQ', desc='请选择品牌', tag='input')
        self.down_enter(2)
        self.click(key='wkOb3Gz8gxqDX', desc='请选择型号', tag='input')
        self.down_enter()
        self.click(key='Ywej9FViOv4YX', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(gyC9dbIGUhd7LCpcYvDF)
    def gyC9dbIGUhd7LCpcYvDF(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='cJd9Is4TkhCn9', desc='请选择移交人', tag='input')
        self.down_enter()
        self.click(key='sGRU08UPRJL1a', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(L4sWT7EPZcuwuxZX1mLK)
    def L4sWT7EPZcuwuxZX1mLK(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='u2gUXwL8F3Ve1', desc='请选择接收人', tag='input')
        self.down_enter(2)
        self.click(key='kt50i2W0XIE6H', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(ZitlblU4lMp7BYK8ANyM)
    def ZitlblU4lMp7BYK8ANyM(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.input(key='EVVwF4wbUbqnc', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='SUKNsfSf4rOUq', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.esc()
        self.click(key='KktUA3EJ4NNpy', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(vRCdl2fqoKNJpFGdRzRD)
    def vRCdl2fqoKNJpFGdRzRD(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='fTVS1fzxLj0Gd', desc='请输入移交单号', tag='input')
        self.ctrl_v()
        self.click(key='Z3tG6b3tvSmlq', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKjPTfATh'])
        return self

    @reset_after_execution
    @doc(Vzw0lwBx2ZAyHWSrX6RQ)
    def Vzw0lwBx2ZAyHWSrX6RQ(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Gm0f4T7HjqlRd', desc='移交单接收', tag='div')
        self.click(key='wbsJxfjBogtEF', desc='请输入编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='oFiL4JoqyIa7R', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['ZspzD8hZ0'])
        return self

    @reset_after_execution
    @doc(UF6kXeN3uHtmuNDjeKwu)
    def UF6kXeN3uHtmuNDjeKwu(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='i9XtEE0CXyFBG', desc='移交单接收', tag='div')
        self.click(key='FjLRVTaoqV2Lm', desc='请输入移交单号', tag='input')
        self.ctrl_v()
        self.click(key='ub88N004RQvjP', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['ZspzD8hZ0'])
        return self

    @reset_after_execution
    @doc(un6reo9grtxgYp8gEDjc)
    def un6reo9grtxgYp8gEDjc(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='SeW8WDN5KwStx', desc='移交单接收', tag='div')
        self.click(key='droVNQA5gbfyQ', desc='请选择移交单状态', tag='input')
        self.down_enter()
        self.click(key='Ayc4R2rmZ96HZ', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['ZspzD8hZ0'])
        return self

    @reset_after_execution
    @doc(byg7MwSRAnzhwUDcj1Wk)
    def byg7MwSRAnzhwUDcj1Wk(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='RXXwzeaJVx0JU', desc='移交单接收', tag='div')
        self.click(key='wBaptmKCUW21z', desc='请选择移交人', tag='input')
        self.down_enter()
        self.click(key='AeD2bH5d4W0Ps', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['ZspzD8hZ0'])
        return self

    @reset_after_execution
    @doc(stvghsNX2dN5itJABNYT)
    def stvghsNX2dN5itJABNYT(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='yRxZjwmgFLLMD', desc='移交单接收', tag='div')
        self.click(key='RlGG62xARr5NU', desc='请选择接收人', tag='input')
        self.down_enter()
        self.click(key='ZvNNlU2b5bRyz', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['ZspzD8hZ0'])
        return self

    @reset_after_execution
    @doc(sn75xNW4A5LGaJtgZiQV)
    def sn75xNW4A5LGaJtgZiQV(self):
        self.menu_manage()
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='xcAoH1PSj24SN', desc='移交单接收', tag='div')
        self.input(key='MGLuIMLni21r9', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='MFkM3ACw3vE9A', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.esc()
        self.click(key='XpuaPTPL7EpmS', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['ZspzD8hZ0'])
        return self


class LrWfCZFWG8G(CommonPages):
    """配件管理|配件销售|销售列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='pqzPenlNDbqKO', desc='配件管理', tag='span')
        self.click(key='xtX9KG8vO1Qww', desc='配件销售', tag='span')
        self.click(key='qAkPn1whPdvgl', desc='销售列表', tag='span')
        return self

    @reset_after_execution
    @doc(H4KdZEXetFlTiBVp1fME)
    def H4KdZEXetFlTiBVp1fME(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='ns3lfWrduAIsY', desc='配件销售', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='AZqzZkPYoHp9k', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='aZ4KIK526ya1g', desc='添加', tag='span')
        self.click(key='Mt9z1zaYN9ipb', desc='请选择客户', index=2, tag='input')
        self.down_enter(2)
        self.click(key='KotU15nz511oF', desc='未收款', index=2, tag='span')
        self.click(key='iqfq2llcQCPFB', desc='请选择收款账户', tag='input')
        self.down_enter(2)
        self.click(key='dIzG0LrDEb47z', desc='@快递易图标开关', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='bEnLi79iWxDWX', desc='计算运费', tag='span')
        self.input(key='v7jBvq2Ccs34n', text='12', desc='请输入销售金额', tag='input')
        self.scroll(element='wKxGCBoeQbY9k')
        self.click(key='wKxGCBoeQbY9k', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='配件销售')
        self.capture_api_request(url_keyword=self.URL['kyVzUMNcM'])
        return self

    @reset_after_execution
    @doc(ye7ARAsQ9uacwEptFiSV)
    def ye7ARAsQ9uacwEptFiSV(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Ln06yaogaf82J', desc='配件销售', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='ka8RFRus6ZUek', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='ycoli4i2fSeQ3', desc='添加', tag='span')
        self.click(key='JQF0fJdrSjf6X', desc='请选择客户', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='YRadAYgKYWzJ8', desc='未收款', tag='span', p_tag='div', p_name='el-dialog__body')
        self.click(key='VB4mbSafSr0GS', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.click(key='rnNBm49tkycwm', desc='@快递易图标开关', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='jPjRKFCEK0HUg', desc='计算运费', tag='span')
        self.input(key='Wc8vkUcJOqqkg', text='999999', desc='请输入销售金额', tag='input')
        self.scroll(element='B2nBmJ7fp5ubf')
        self.click(key='B2nBmJ7fp5ubf', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='配件销售')
        self.capture_api_request(url_keyword=self.URL['kyVzUMNcM'])
        return self

    @reset_after_execution
    @doc(ivhxLmwFUYJ160MKBThl)
    def ivhxLmwFUYJ160MKBThl(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='myuIXBv9YkJ3U', desc='配件销售', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='RZqLpJAv6sAmV', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='J4d6jBN7d1mPB', desc='添加', tag='span')
        self.click(key='tiphVQ7Gnjuj9', desc='请选择客户', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='ELUUr6G7gGXCu', desc='未收款', tag='span', p_tag='div', p_name='el-dialog__body')
        self.click(key='xWYro04ZnnfLn', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.input(key='Xnx7WD8jt0d0B', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='Esw6VN9ajcrHR', text='12', desc='请填写物流费用', tag='input')
        self.input(key='ZDjJtIfmciFfl', text='备注', desc='请填写备注', tag='input')
        self.input(key='OBEdWzpIyzroF', text='124', desc='请输入销售金额', tag='input')
        self.click(key='QhRCvhWNzPAn3', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='配件销售')
        self.capture_api_request(url_keyword=self.URL['kyVzUMNcM'])
        return self

    @reset_after_execution
    @doc(btbwOSZldzzeYBn6qsYo)
    def btbwOSZldzzeYBn6qsYo(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='Nx3L0IidjJn92', desc='配件销售', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='YlPhlMEUKALeK', desc='请输入物品编号', tag='input')
        self.ctrl_v()
        self.click(key='JK138msZA9CXr', desc='添加', tag='span')
        self.click(key='KoKrdpDEb9kqT', desc='请选择客户', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.click(key='L318LxIXJpyN8', desc='已收款', tag='span', p_tag='div', p_name='el-dialog__body')
        self.click(key='fYjjft28Z1g71', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.input(key='EPQdbhHYAa6Og', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='fHuSQ1lPbYwbT', text='12', desc='请填写物流费用', tag='input')
        self.input(key='sOtmzunHjqvHW', text='备注', desc='请填写备注', tag='input')
        self.input(key='Xrj0ooYLGlNT5', text='124', desc='请输入销售金额', tag='input')
        self.click(key='GHVkAt5Xnh3eH', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='配件销售')
        self.capture_api_request(url_keyword=self.URL['kyVzUMNcM'])
        return self

    @reset_after_execution
    @doc(bovLHIlzJSfrRryibqyF)
    def bovLHIlzJSfrRryibqyF(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4(data='a')
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        self.click(key='M7Gb6kGb5vwk4', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='mAvCuNraatrwd', desc='销售售后', tag='span')
        self.click(key='Fk3EzXyOejXfK', desc='请选择售后类型', tag='input')
        self.down_enter()
        self.input(key='qzqr39q2jk5GC', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='O67FLLjJho99B', text='12', desc='请填写物流费用', tag='input')
        self.click(key='ZqfbD2JU0Kcas', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['Kuc4ZIm7H'])
        return self

    @reset_after_execution
    @doc(oe82ledRfRK4B7jiOSVc)
    def oe82ledRfRK4B7jiOSVc(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4(data='a')
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        self.click(key='D6U3Gy3KmLOki', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='Zh6COns9VvtsH', desc='销售售后', tag='span')
        self.click(key='XLwDv349t3D0Y', desc='请选择售后类型', tag='input')
        self.down_enter()
        self.click(key='Tn8xY92PmBqwF', desc='已收货', tag='span')
        self.click(key='Wg7TewriJHGD9', desc='请选择仓库', tag='input')
        self.down_enter()
        self.input(key='pH14ltQrml5Nq', text='备注', desc='请填写备注', tag='input')
        self.click(key='DVc0NV4iG6Bcw', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['Kuc4ZIm7H'])
        return self

    @reset_after_execution
    @doc(hBh7ycF1AumEt4nXwMyZ)
    def hBh7ycF1AumEt4nXwMyZ(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4(data='a')
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        self.click(key='lvyEDR73NqhSx', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='nUFi67LOGBif8', desc='销售售后', tag='span')
        self.click(key='JnKOLqA4CMtDq', desc='请选择售后类型', tag='input')
        self.up_enter()
        self.input(key='mmcWpR2NSQiSX', text='5', desc='请输入退款金额', tag='input')
        self.click(key='DXwHNGb3dS2jI', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['Kuc4ZIm7H'])
        return self

    @reset_after_execution
    @doc(dvDaOWftNEncBuIMeo7h)
    def dvDaOWftNEncBuIMeo7h(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4(data='a')
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        self.click(key='hWqxfuBelQrdH', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='FBebpBBsDcQ0T', desc='销售售后', tag='span')
        self.click(key='qnIbvr0fivwol', desc='请选择售后类型', tag='input')
        self.up_enter()
        self.input(key='bCRLxetTjAcMG', text='999999', desc='请输入退款金额', tag='input')
        self.click(key='gACMDg5U1NKD9', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['Kuc4ZIm7H'])
        return self

    @reset_after_execution
    @doc(JufIUEkkoghm3ZPziz11)
    def JufIUEkkoghm3ZPziz11(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='TG6Y2Nb4ehrBa', desc='请输入销售单号', tag='input')
        self.ctrl_v()
        self.click(key='p60VCyAcuqjVP', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['m9MsjRh7V'])
        return self

    @reset_after_execution
    @doc(U9NQEB15gOzUs1kWPzHL)
    def U9NQEB15gOzUs1kWPzHL(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='Lg6fG4Ls4iAdT', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.click(key='FS5JLluB5JVi9', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['m9MsjRh7V'])
        return self

    @reset_after_execution
    @doc(hVsGoqqW3itUAfALyFs8)
    def hVsGoqqW3itUAfALyFs8(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='ti0K99YnWWoHu', desc='请选择收款状态', tag='input')
        self.down_enter()
        self.click(key='PAd2O1pKd1LTp', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['m9MsjRh7V'])
        return self

    @reset_after_execution
    @doc(aSQHqjds3CGl32QrMMgp)
    def aSQHqjds3CGl32QrMMgp(self):
        self.menu_manage()
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.click(key='lAKpt1cRY0GRs', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='hubkdtNPW30Z5', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['m9MsjRh7V'])
        return self

    @reset_after_execution
    @doc(Rd9OUwhBuPlpGWYEzDoo)
    def Rd9OUwhBuPlpGWYEzDoo(self):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='TWJ6HWMJBHWZi', desc='开始时间', text=self.get_the_date(), tag='input')
        self.input(key='p7mDELpGgNA0n', desc='结束时间', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='tVbdTk9POdKKd', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['m9MsjRh7V'])
        return self


class HTP9XkLGQNT(CommonPages):
    """配件管理|入库管理|新到货入库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='iG0bhSKhadFUr', desc='配件管理', tag='span')
        self.click(key='uGrWch5RZ7OHW', desc='入库管理', tag='span', index=2)
        self.click(key='Y9YBhKqHA8Wqu', desc='新到货入库', tag='span')
        return self

    @reset_after_execution
    @doc(k75gfpU0uyhS1aEhcD2Y)
    def k75gfpU0uyhS1aEhcD2Y(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=1)
        ParamCache.cache_object({"i": obj[0]['purchaseLogisticsNo']})
        self.click(key='uz9nFG4S0a030', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='LNVrUFpTrhMZk', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='oCUbCR1TEbTOa', desc='签收/入库', tag='span')
        self.click(key='dpYApBUrwPzgv', desc='请选择入库流转仓', tag='input')
        self.up_enter()
        self.click(key='p8HLyh7qzglrg', desc='请选择快捷操作', tag='input')
        self.down_enter()
        self.click(key='vQ6mbI1UW1wro', desc='确定', tag='span')
        self.capture_api_request(url_keyword=self.URL['Wgwpc3mTg'])
        return self

    @reset_after_execution
    @doc(Jslqnx0TJYAcPWsTNgWG)
    def Jslqnx0TJYAcPWsTNgWG(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=1)
        ParamCache.cache_object({"i": obj[0]['purchaseLogisticsNo']})
        self.click(key='r7KCmhvy3i3m2', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='S4Gqqt5czcXOh', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='M1xAQDUoU9amW', desc='签收/入库', tag='span')
        self.click(key='czpQh4MY26Cq2', desc='请选择入库流转仓', tag='input')
        self.up_enter()
        self.click(key='M78YiaWwplYef', desc='请选择快捷操作', tag='input')
        self.down_enter(2)
        self.click(key='NFP0vB4rOWKnt', desc='请选择接收人', tag='input')
        self.down_enter()
        self.input(key='drGN71q0hmwtR', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='wiYJ7PnvXbEbk', desc='确定', tag='span')
        self.capture_api_request(url_keyword=self.URL['Wgwpc3mTg'])
        return self

    @reset_after_execution
    @doc(pZnZ4E4EWsok60VOwAt0)
    def pZnZ4E4EWsok60VOwAt0(self):
        self.menu_manage()
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.click(key='OBXJVRLwUPaQL', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='MrZlzMQ8p1QbP', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['apFM5LAR2'])
        return self

    @reset_after_execution
    @doc(ddwluOeEUDWfjvQcXtFf)
    def ddwluOeEUDWfjvQcXtFf(self):
        self.menu_manage()
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='MMgBITXPfvp4M', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='etQwfoTsnOQl3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['apFM5LAR2'])
        return self

    @reset_after_execution
    @doc(ZHplaC78vCAAs9nTV3tu)
    def ZHplaC78vCAAs9nTV3tu(self):
        self.menu_manage()
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['businessNo']})
        self.click(key='XlJJ8qsE6oCPR', desc='请输入业务单号', tag='input')
        self.ctrl_v()
        self.click(key='EhddtEwf8ZQaJ', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['apFM5LAR2'])
        return self


class P6xNXMkC4fE(CommonPages):
    """配件管理|配件库存|库存调拨"""

    def menu_manage(self):
        """菜单"""
        self.click(key='dvUR3mT2GDD7c', desc='配件管理', tag='span')
        self.scroll(element='gk72nOwGJhrvn')
        self.click(key='gk72nOwGJhrvn', desc='配件库存', tag='span')
        self.click(key='bkFeLwIMQ3XM4', desc='库存调拨', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(AdqaPYO38jf7TVM9akKm)
    def AdqaPYO38jf7TVM9akKm(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='aoLIN5mholHhH', desc='新增调拨', tag='span')
        self.click(key='s6GPe0CyphN53', desc='请选择调出仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='AtAMsi2iYcTW5', desc='请选择调入仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='AyQsxLIlfjb5c', text='备注', desc='请输入备注', tag='input')
        self.click(key='aT6ec33TnAmP1', desc='请输入物品编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='TUj2dt4ohBzmo', desc='搜索添加', tag='span')
        self.click(key='pbeJUl7PKmgdb', desc='@快递易图标开关', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='sHxSq40w3FREF', desc='请选择快递公司', tag='input')
        self.down_enter()
        self.click(key='Azph0v4iPlQtR', desc='计算运费', tag='span')
        self.click(key='F2luLf7RqcpYg', desc='确定', tag='span')
        self.capture_api_request(url_keyword=self.URL['x79aTjjzc'])
        return self

    @reset_after_execution
    @doc(UXuoreny4UjWmENBXQgX)
    def UXuoreny4UjWmENBXQgX(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='i1YCR2emBYfZS', desc='新增调拨', tag='span')
        self.click(key='wifT30YvUns15', desc='请选择调出仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='hn6poRhzpIs8x', desc='请选择调入仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='M5JYRjQb2aTl8', text='备注', desc='请输入备注', tag='input')
        self.click(key='FyuepUenkA3Ex', desc='选择添加', tag='span')
        self.click(key='F12z9wtgoF6NJ', desc='搜索', tag='span', p_tag='div', p_name='el-dialog__body')
        self.tab_space(3)
        self.tab_space(1)
        self.scroll(element='xRtFZsNS8OSQ1')
        self.click(key='xRtFZsNS8OSQ1', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择物品')
        self.click(key='gEsVpv7QQiAqe', desc='确定', tag='span')
        self.capture_api_request(url_keyword=self.URL['x79aTjjzc'])
        return self

    @reset_after_execution
    @doc(NvbF3ZipfMr4hBRl0nQ1)
    def NvbF3ZipfMr4hBRl0nQ1(self):
        self.menu_manage()
        self.file.get_attachment_data('attachment_allocation')
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='AD1i4h7F9NkG7', desc='新增调拨', tag='span')
        self.click(key='xawTuZucMTy7O', desc='请选择调出仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='joLsSLYTdZidb', desc='请选择调入仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='F7ZQKkkAOov7I', text='备注', desc='请输入备注', tag='input')
        self.click(key='KhtEiVu8horo4', desc='导入', tag='span')
        self.upload_file(key='YBLxgdlfpf89I', file_path=self.file_path('attachment_allocation'))
        self.click(key='vrJMI5T5PhKec', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.click(key='YTPQb0NMsu9T5', desc='确定', tag='span')
        self.capture_api_request(url_keyword=self.URL['x79aTjjzc'])
        return self

    @reset_after_execution
    @doc(zwNZnOUV0fJtHzKSpk1f)
    def zwNZnOUV0fJtHzKSpk1f(self):
        self.menu_manage()
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='B1iJmRVK67qMn', desc='新增调拨', tag='span')
        self.click(key='iOXWgiHCxVi4t', desc='请选择调出仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='V0T8QlyGKMjCO', desc='请选择调入仓库', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter(2)
        self.input(key='vWeAhnyLn3IvX', text='备注', desc='请输入备注', tag='input')
        self.click(key='tqdf0mxbaShby', desc='选择添加', tag='span')
        self.click(key='UN6VDUJUAucIl', desc='搜索', tag='span', p_tag='div', p_name='el-dialog__body')
        self.tab_space(3)
        self.scroll(element='vynTcwnkdhM2J')
        self.click(key='vynTcwnkdhM2J', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择物品')
        self.click(key='nUJkHqvLhrIcC', desc='确定', tag='span')
        self.capture_api_request(url_keyword=self.URL['x79aTjjzc'])
        return self

    @reset_after_execution
    @doc(vy4GQrC9c2PByhpKlKX7)
    def vy4GQrC9c2PByhpKlKX7(self):
        self.menu_manage()
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='jO9RWxhARikYO', desc='接收', tag='span', p_tag='td', p_name='el-table_1_column_15   el-table__cell')
        self.click(key='mKgxB5G2uk0uF', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['qIZUVHhiB'])
        return self

    @reset_after_execution
    @doc(HYzXRVJ2N0MDfAwPg4mA)
    def HYzXRVJ2N0MDfAwPg4mA(self):
        self.menu_manage()
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW(data='a')
        ParamCache.cache_object({"i":  obj['itemList'][0]['articlesNo']})
        self.click(key='PZVPUfKY9jLId', desc='扫码接收', tag='span')
        self.click(key='c81ME3K0Fl9KG', desc='请输入物品编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='jMiO5sPn5byLB', desc='添加', tag='span')
        self.click(key='D0TWf6Ohhv4TL', desc='接收入库', tag='span')
        return self

    @reset_after_execution
    @doc(SfRJFEo1omEqQEMXCt1A)
    def SfRJFEo1omEqQEMXCt1A(self):
        self.menu_manage()
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.click(key='o2gFWjED9JV99', desc='撤销', tag='span', p_tag='td', p_name='el-table_1_column_15   el-table__cell')
        self.click(key='HLuJtfvEomEza', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer')
        self.capture_api_request(url_keyword=self.URL['lBPBIvUgX'])
        return self

    @reset_after_execution
    @doc(U2Z6NYRuai5n0iI9gc5N)
    def U2Z6NYRuai5n0iI9gc5N(self):
        self.menu_manage()
        self.click(key='rCa9ujKdxfoYe', desc='导出', tag='span')
        return self

    @reset_after_execution
    @doc(irVf881IgnSudhdqrzNT)
    def irVf881IgnSudhdqrzNT(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='y6OSRlu1ddVBA', desc='请输入调拨单号', tag='input')
        self.ctrl_v()
        self.click(key='P0bheCaxag3lm', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(uxleDdCbgv5xe0Yh9ihY)
    def uxleDdCbgv5xe0Yh9ihY(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='Q7yC345ZXS6XD', desc='请选择调出仓库', tag='input')
        self.down_enter()
        self.click(key='AUwfiWVqeUM8U', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(GEzDUNHZDHJGT31d5arP)
    def GEzDUNHZDHJGT31d5arP(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='S6YA2tZPqU1Xj', desc='请选择调入仓库', tag='input')
        self.down_enter(2)
        self.click(key='GCV1BOBbWDdMc', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(ykbpvOAyRCpcWTc8FTo0)
    def ykbpvOAyRCpcWTc8FTo0(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='uZbkMyPS0Ricn', desc='请选择调拨人', tag='input')
        self.down_enter()
        self.click(key='fq1V1rnVfKrU7', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(N7hyMWrgBhZs95uhMTfo)
    def N7hyMWrgBhZs95uhMTfo(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='DeQ0QPDiNmwOZ', desc='请选择接收状态', tag='input')
        self.down_enter()
        self.click(key='zXRNLK1hZ11HO', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(gMOD5rLLkrIFYE4i7uWv)
    def gMOD5rLLkrIFYE4i7uWv(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='l5TwtkWGHHlGP', desc='请选择最新操作人', tag='input')
        self.down_enter()
        self.click(key='JQKeiUKIKHkLJ', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(qUeEiqtgrjyltpAB3WwJ)
    def qUeEiqtgrjyltpAB3WwJ(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='OB7J9zoRW4exZ', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='tSl4Wi35PWYOf', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='N1RgqrcdcWguk', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self

    @reset_after_execution
    @doc(boCbPTo0KQQbybfPC7Dp)
    def boCbPTo0KQQbybfPC7Dp(self):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='Knne86SmoONnJ', desc='开始日期', text=self.get_the_date(), index=2, tag='input')
        self.input(key='IToAYv1WuUrCh', desc='结束日期', text=self.get_the_date(days=1), index=2, tag='input')
        self.esc()
        self.click(key='uAZeq76hsFmiY', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['Vqx4RAgDI'])
        return self


class S250zQ3JaPt(CommonPages):
    """配件管理|配件销售|销售售后列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='RHNNosAyCFhP7', desc='配件管理', tag='span')
        self.click(key='EQPxQRDduJUZv', desc='配件销售', tag='span')
        self.click(key='DjxB5xJk6Xn3F', desc='销售售后列表', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(fQ4Cx53aMDNueSRTtdCt)
    def fQ4Cx53aMDNueSRTtdCt(self):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='B2gZydBJwKVSJ', desc='请输入售后单号', tag='input')
        self.ctrl_v()
        self.click(key='XFmwmcskhdCl1', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['r9ytswUaJ'])
        return self

    @reset_after_execution
    @doc(M2uPO43Gwj1MxRNJdmCn)
    def M2uPO43Gwj1MxRNJdmCn(self):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='tnC0NwJCAN4TM', desc='请选择售后类型', tag='input')
        self.down_enter(2)
        self.click(key='JhRqNc7em3vZt', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['r9ytswUaJ'])
        return self

    @reset_after_execution
    @doc(cUNSieph0X3TfNdfkcSr)
    def cUNSieph0X3TfNdfkcSr(self):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='ge3hdhzf1LfGE', desc='请选择售后客户', tag='input')
        self.down_enter(2)
        self.click(key='Bs9pLH9DryflP', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['r9ytswUaJ'])
        return self

    @reset_after_execution
    @doc(okQmkaKm4xMprd8BtEc3)
    def okQmkaKm4xMprd8BtEc3(self):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.menu_manage()
        self.click(key='Q8N8WuOeXSxh1', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='OaivxJJUzjaJH', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['r9ytswUaJ'])
        return self

    @reset_after_execution
    @doc(S5HIKmlK3427TT3VXmlV)
    def S5HIKmlK3427TT3VXmlV(self):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.menu_manage()
        self.click(key='JY8dMGNRpz6q7', desc='请选择操作人', tag='input')
        self.down_enter()
        self.click(key='lv54hLQMMefF2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['r9ytswUaJ'])
        return self

    @reset_after_execution
    @doc(XODp5acGT6jdcx10I682)
    def XODp5acGT6jdcx10I682(self):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.menu_manage()
        self.input(key='HVyVNy95PiarZ', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='ios6fFnO1hDvm', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='AxH4TZH9OD5XP', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['r9ytswUaJ'])
        return self
