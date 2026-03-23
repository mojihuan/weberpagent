# coding: utf-8
import os
from config.settings import DATA_PATHS
from common.base_page import BasePage, ImportDataEdit
from common.import_desc import *


class MallProductShelvesPages(BasePage):
    """商城管理|商品上架"""

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []


