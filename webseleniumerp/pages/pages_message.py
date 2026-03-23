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

class MessageReleaseListPages(CommonPages):
    """消息管理|消息发布列表"""


    def menu_manage(self):
        """菜单"""
        (self.scroll('message_manage_menu', desc='消息管理')
         .step(key='message_manage_menu', desc='消息管理')
         .step(key='menu', desc='消息发布列表')
         .wait())
        return self

    @reset_after_execution
    @doc(m_publish_the_message)
    def publish_the_message(self):
        self.menu_manage()
        (self.step(key='release_new_news', desc='发布新消息')
         .step(key='message_type', desc='消息类型')
         .custom(lambda: self.up_arrow_return())
         .step(key='message_title', value='消息标题' + self.number, action='input', desc='消息标题')
         .step(key='message_content', value='消息内容' + self.number, action='input', desc='消息内容')
         .step(key='upload_file',value= self.file_path('img'), action='upload', desc='上传图片')
         .step(key='release_method', desc='站内信')
         .step(key='release_channel', desc='壹准速收小程序')
         .step(key='release_time', desc='立即发布')
         .scroll('submit_for_review', desc='提交审核')
         .step(key='submit_for_review', desc='提交审核')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(m_release_new_news_preview_release)
    def release_new_news_preview_release(self):
        self.menu_manage()
        (self.step(key='release_new_news', desc='发布新消息')
         .step(key='message_type', desc='消息类型')
         .custom(lambda: self.up_arrow_return())
         .step(key='message_title', value='消息标题' + self.number, action='input', desc='消息标题')
         .step(key='message_content',value= '消息内容' + self.number, action='input', desc='消息内容')
         .step(key='release_method', desc='站内信')
         .step(key='release_channel', desc='壹准速收小程序')
         .step(key='release_time', desc='立即发布')
         .step(key='preview', desc='预览')
         .step(key='close', desc='关闭')
         .scroll('review_and_release')
         .step(key='review_and_release', desc='审核并发布')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(m_approved)
    def approved(self):
        self.menu_manage()
        (self.step(key='radio_btn', desc='单选')
         .step(key='bulk_review_button', desc='批量审核')
         .step(key='through', desc='通过')
         .step(key='message_review_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(m_refuse)
    def refuse(self):
        self.menu_manage()
        (self.step(key='radio_btn', desc='单选')
         .step(key='bulk_review_button', desc='批量审核')
         .step(key='refuse', desc='审核不通过')
         .step(key='reason_refusal', value=self.serial, action='input', desc='不通过原因')
         .step(key='message_review_confirmation', desc='确定')
         .wait())
        return self
