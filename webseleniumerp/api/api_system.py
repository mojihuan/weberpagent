# coding: utf-8
import json
from common.base_api import BaseApi


class R6KHF22ppb171nXthYQIM(BaseApi):
    """系统管理|消息接收配置"""

    def YKyJlL3xPclZ(self, headers=None):
        """消息接收配置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Ukseqcbhp'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', [])


class Rlt8nMPRFg5VWyVNDL5yL(BaseApi):
    """系统管理|接口缓存日志"""

    def G3dL3lluoRrj(self, headers=None):
        """接口缓存日志列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['tJkOC7deN'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class CgfWew7vZc9C4wjoPrJbl(BaseApi):
    """系统管理|部门管理"""

    def hxwGKYs7sxKl(self, headers=None):
        """部门管理列表"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['cn3PAQo25'], headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class PlqvSQxF6Sehfpp9ACbOy(BaseApi):
    """系统管理|导入模板管理"""

    def H7VPYYdtX8fE(self, headers=None):
        """导入模板列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['agRtj7Ybg'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class VT5NE5myi3oXqlTXJZdCK(BaseApi):
    """系统管理|字典管理"""

    def NzQHWJt2kjte(self, headers=None):
        """字典管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "params": {}}
        response = self.request_handle('post', self.urls['iIToR3jDm'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class NRLFrR9AINYsTUIXq0IRn(BaseApi):
    """系统管理|关键词配置"""

    def ExqbBcJXscBC(self, headers=None):
        """关键词配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['isPg8kGTU'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class Q8OvSXksksDjZpL6LBBTR(BaseApi):
    """系统管理|导出列表"""

    def WPRG5rjvVxID(self, headers=None):
        """导出列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['jVxXCwdJ7'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class ANN4Pn1GSqOeDFqaeoJAa(BaseApi):
    """系统管理|基础设置|常规配置"""

    def SGeF6FBa7Ni6(self, headers=None):
        """常规配置列表"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['NQUKbW5Bv'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'rows', list)


class Y3PJwfdBL5LACIVhOIZTm(BaseApi):
    """系统管理|接口缓存日志"""

    def bk9DYvXzt98D(self, headers=None):
        """接口缓存日志"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['tJkOC7deN'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class Z75Q14wgT5IlLeeo1DeVv(BaseApi):
    """系统管理|接口管理"""

    def qQdiKvd1gy7n(self, headers=None):
        """接口管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['RyIo8DXve'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class UvOKb5AtO4icTrHYXAn0n(BaseApi):
    """系统管理|国际化配置"""

    def l721kKEys6x5(self, headers=None):
        """配置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['RCfrEWrv9'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)


class I0UQFvFxtSK3giDbJfZdu(BaseApi):
    """系统管理|关键字配置"""

    def QgHwuqNT2LMS(self, headers=None):
        """关键字配置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "params": {}}
        response = self.request_handle('post', self.urls['isPg8kGTU'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class AOPo404ZsB2TuXUe82km1(BaseApi):
    """系统管理|日志管理|操作日志"""

    def OU3RpJFCUNwI(self, headers=None):
        """操作日志列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['TuCCqLTh6'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def zSmrPQBaXAEO(self, headers=None):
        """登录日志列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['gKXHmsyQh'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class D9mUzcb6PyFDeMhEuOwTE(BaseApi):
    """系统管理|菜单管理"""

    def syeaTPBqyslA(self, headers=None):
        """菜单管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['dvsTQqyY5'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class N1RlStO07A2eNJNlzaRyH(BaseApi):
    """系统管理|通知公告"""

    def GIPoO9r7rOXd(self, headers=None):
        """通知公告列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['rsJ71COfy'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class DTZ91OwAbyETqjNNciasZ(BaseApi):
    """系统管理|参数设置"""

    def YmY6nxA20n5e(self, headers=None):
        """参数设置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "params": {}}
        response = self.request_handle('post', self.urls['S0bWhpj4F'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class VOi8kyt95amMjMlvY8pJZ(BaseApi):
    """系统管理|岗位管理"""

    def vOJQZTt8JXuJ(self, headers=None):
        """角色管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['bvOnBsr7L'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class NFC3xMhX4GDGIvJt83Tz4(BaseApi):
    """系统管理|基础设置|打印标签模板配置"""

    def IPfIlLKjjyMM(self, headers=None):
        """打印标签模板配置列表"""
        headers = headers or self.headers['main']
        data = {"params": {**self.get_page_params(), "name": "", "ismain": ""}}
        response = self.request_handle('post', self.urls['N1awWeNZc'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class BQJ3yjBQ5vaVaJLwAX1jr(BaseApi):
    """系统管理|基础设置|质检条码打印配置"""

    def oMRsX0sjnR7d(self, headers=None):
        """质检条码打印配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['F86LDgykt'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class RHcZeNbg9VX9tO6T4dLwL(BaseApi):
    """系统管理|基础设置|质检模板打印配置"""

    def u3A38djBBEhA(self, headers=None):
        """质检模板打印配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['lUVvrFSsd'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class EdbcuiT6q4uDVZbB8nCqk(BaseApi):
    """系统管理|壹查查管理"""

    def gcunilbP9D0I(self, headers=None):
        """查询记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Pi4YqJvuf'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class OJP0vWAYXZXG33pavP5lX(BaseApi):
    """系统管理|角色管理"""

    def Uepahtz5UPuK(self, headers=None):
        """角色管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['djlgLhYCq'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class RMgCwZF84pZe4Io1Je8Vu(BaseApi):
    """系统管理|第三方账号管理"""

    def TYIgJeWEiVPu(self, headers=None):
        """采购列表"""
        headers = headers or self.headers['main']
        data = {'classId': "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['PO59t8PGp'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def ektcdtPGaGnj(self, headers=None):
        """销售列表"""
        headers = headers or self.headers['main']
        data = {'classId': "2", **self.get_page_params()}
        response = self.request_handle('post', self.urls['NQUKbW5Bv'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def kZWJsYmRWxEf(self):
        """获取采购账号id"""
        return self._get_field_copy_value('TYIgJeWEiVPu', 'main', 'id')


class K5PFamUMZnUdvWDYKxdNk(BaseApi):
    """系统管理|用户管理"""

    def ve6d03NBKSrP(self, headers=None):
        """用户管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'params': {}}
        response = self.request_handle('post', self.urls['NHeUFMvMt'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def Ae1Zt6ZiWt5z(self):
        """获取用户id"""
        return self._get_field_copy_value('ve6d03NBKSrP', 'main', 'userId')

    def ztstv48nYgYW(self):
        """获取用户id"""
        return self._get_field_copy_value('ve6d03NBKSrP', 'vice', 'userId')

    def YEPWmdrz4R2Y(self):
        """获取第二条用户id"""
        return self._get_field_copy_value('ve6d03NBKSrP', 'main', 'userId', index=1)

    def gIWHCGuW3qqe(self):
        """获取用户名称"""
        return self._get_field_copy_value('ve6d03NBKSrP', 'main', 'userName')

    def aOwdVLwXzO6f(self):
        """获取用户id"""
        return self._get_field_copy_value('ve6d03NBKSrP', 'idle', 'userId')

    def MmYE3zmy4nRl(self):
        """获取用户id"""
        return self._get_field_copy_value('ve6d03NBKSrP', 'camera', 'userId')


class KS9xZ6UDYk9dq6xnv7T0t(BaseApi):
    """系统管理|仓库管理"""

    def gbTEU7P10lDf(self, headers=None):
        """仓库管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['efEJBIzNy'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def w6NzYX8tgUAr(self):
        """获取深圳配件仓id"""
        return self._get_field_copy_value('gbTEU7P10lDf', 'main', 'id')

    def yNOMoxdkvP0y(self):
        """获取广州物品仓id"""
        return self._get_field_copy_value('gbTEU7P10lDf', 'main', 'id', index=1)

    def dTTvelGrt6RF(self):
        """获取默认物品仓id"""
        return self._get_field_copy_value('gbTEU7P10lDf', 'main', 'id', index=2)

    def WuzYTkWyJjXJ(self):
        """获取默认配件仓id"""
        return self._get_field_copy_value('gbTEU7P10lDf', 'main', 'id', index=3)

    def fSZMiSz97PD8(self):
        """获取仓库id"""
        return self._get_field_copy_value('gbTEU7P10lDf', 'vice', 'id')


class WziJGBshZjou10L8PleRe(BaseApi):
    """系统管理|基础设置|工单配置"""

    def keAqvfuWduT9(self, headers=None):
        """瑕疵项列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['D1jH3zgpB'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def tJ7mRunfhfkN(self, headers=None, i=None):
        """业务工序列表
        i：业务名称 付款 报价 退货 工序
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'name': i}
        response = self.request_handle('post', self.urls['sUrRxJ6V2'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class OaB1cW5EulvA3aT5FalE3(BaseApi):
    """系统管理|日志管理|价格计算日志"""

    def reXo3OeJGpBX(self, headers=None):
        """价格计算日志列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['yX4iSeJzd'], data=json.dumps(data),  headers=headers)
        return self.get_response_data(response, 'rows', list)


class HQjPq9KaQGYorM0txj58i(BaseApi):
    """系统管理|权限列表"""

    def PXWuxgpS3xAc(self, headers=None):
        """权限列表"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['qKbwUThei'], headers=headers)
        data = self.get_response_data(response, 'permissions', list)
        # 将请求结果保存到当前路径得permission.json文件中
        filename = 'permission_main.json'
        self.save_json_file(data, filename)
        return data


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
