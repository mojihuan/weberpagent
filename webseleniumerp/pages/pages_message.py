# coding: utf-8
import os
from config.settings import DATA_PATHS
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.import_desc import *


class CommonPages(BasePage):

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

class Alkolwr5Vbg(CommonPages):
    """消息管理|消息发布列表"""


    def menu_manage(self):
        """菜单"""
        (self.scroll('message_manage_menu', desc='消息管理')
         .step(key='mMT5P1QIzQnAS', desc='消息管理')
         .step(key='hhEu9jRb0fUHK', desc='消息发布列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p2KvndGL0zVJEDKHGIPU)
    def p2KvndGL0zVJEDKHGIPU(self):
        self.menu_manage()
        (self.step(key='Oda242uO25XLg', desc='发布新消息')
         .step(key='r3dLcLuozor5W', desc='消息类型')
         .custom(lambda: self.up_enter())
         .step(key='Dn5bHwJy7WXKe', value='消息标题' + self.number, action='input', desc='消息标题')
         .step(key='M1H11R4eCNKZp', value='消息内容' + self.number, action='input', desc='消息内容')
         .step(key='AMjzVrHpypNW4',value= self.file_path('img'), action='upload', desc='上传图片')
         .step(key='MhjAXSKRamaBj', desc='站内信')
         .step(key='klMTFohcAmywQ', desc='壹准速收小程序')
         .step(key='bMqPHEuUVRAJ8', desc='立即发布')
         .scroll('submit_for_review', desc='提交审核')
         .step(key='hVPwFmUSGHtMl', desc='提交审核')
         .step(key='Dht20GwM8TSvC', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(JERvfLXoEn18N8nGDyMd)
    def JERvfLXoEn18N8nGDyMd(self):
        self.menu_manage()
        (self.step(key='kG2IBDWkcg5w3', desc='发布新消息')
         .step(key='IqTJ5CWg8OKQE', desc='消息类型')
         .custom(lambda: self.up_enter())
         .step(key='yu8iXmMvlH8JI', value='消息标题' + self.number, action='input', desc='消息标题')
         .step(key='c8wbiUfoUOxhw',value= '消息内容' + self.number, action='input', desc='消息内容')
         .step(key='XrjMBfZRgebz9', desc='站内信')
         .step(key='SkNPeqnt18mf6', desc='壹准速收小程序')
         .step(key='TrgapRFqmMzv5', desc='立即发布')
         .step(key='aj5CLpk950a87', desc='预览')
         .step(key='LSieRMUF2srkq', desc='关闭')
         .scroll('review_and_release')
         .step(key='UXsnzRZe2vxGC', desc='审核并发布')
         .step(key='BfkskPVr2RTnE', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(FAEFTmKmDM49LcbTv3tL)
    def FAEFTmKmDM49LcbTv3tL(self):
        self.menu_manage()
        (self.step(key='n0r8pnqUZUX1k', desc='单选')
         .step(key='G0bUQs41t77fb', desc='批量审核')
         .step(key='a90eEOFGdzY7U', desc='通过')
         .step(key='NyKqxVvM4ysmq', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(refuse)
    def refuse(self):
        self.menu_manage()
        (self.step(key='WfqspZ4WGwFan', desc='单选')
         .step(key='ALvrBqtpc5BLu', desc='批量审核')
         .step(key='pLANnzZdPNQc3', desc='审核不通过')
         .step(key='JYQOAB9RNwPR3', value=self.serial, action='input', desc='不通过原因')
         .step(key='ZvkDjRSym0nu7', desc='确定')
         .wait())
        return self
