# coding: utf-8
from common.base_api import BaseApi
from common.import_api import ImportApi
from common.import_request import ImportRequest


class CommonFront(BaseApi):
    """前置条件"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = ImportRequest()
        self.api = ImportApi()

    def execute_operations(self, operations_dict, data):
        """通用操作执行方法"""
        actions = operations_dict.get(data)
        if not actions:
            raise ValueError(f"无效的操作参数 '{data}'")
        for action in actions:
            action()


class PreFront(CommonFront):

    def login_operations(self):
        """登录"""
        pass

    def operations(self, data=None):
        pre_step = {
            # 配件管理|配件采购|新增采购单
            'bAym': [self.request.EdqL4NE5hk.niKwILpBHogDvGt52uEB],  # 手机-新增采购单未付款已到货
            'jVML': [self.request.EdqL4NE5hk.nBfEGGe1LJguXHi6aesS],  # 笔记本电脑-新增采购单未付款在路上
            'PfLo': [self.request.EdqL4NE5hk.rYvpUsdluGutOhIhm7af],  # 平板电脑-新增采购单已付款在路上
            'dsm4': [self.request.EdqL4NE5hk.fi51E5jCFUxE1nLYPO7w],  # 智能手表-新增采购单已付款已到货
            # 配件管理|配件销售|销售列表
            'Ab3A': [self.request.R3Xo25O7tV.ivhxLmwFUYJ160MKBThl],  # 销售出库-未收款
            'uyEh': [self.request.R3Xo25O7tV.btbwOSZldzzeYBn6qsYo],  # 销售出库-已收款
            'GM4P': [self.request.R3Xo25O7tV.dvDaOWftNEncBuIMeo7h],  # 销售售后退差价
            'wTnl': [self.request.R3Xo25O7tV.bovLHIlzJSfrRryibqyF],  # 销售售后退货退款-未收货
            'yZMr': [self.request.R3Xo25O7tV.ye7ARAsQ9uacwEptFiSV],  # 销售出库-快递易
            # 配件管理|配件库存|库存调拨
            'PBkr': [self.request.KofyeHTY2V.AdqaPYO38jf7TVM9akKm],  # 新增调拨
            'wyCv': [self.request.KofyeHTY2V.SfRJFEo1omEqQEMXCt1A],  # 撤销
            'yQq9': [self.request.KofyeHTY2V.vy4GQrC9c2PByhpKlKX7],  # 接收
            'hmX8': [self.request.KofyeHTY2V.UXuoreny4UjWmENBXQgX],  # 多物品调拨
            # 配件管理|配件库存|库存列表
            'KDsB': [self.request.NccuqXjU5C.oqmc5nwi0399dzltytx2],  # 库存移交给库存配件
            # 配件管理|入库管理|待接收物品
            'JAn4': [self.request.GGZectTPpu.do56fxxjyrxq3jf44spl],  # 接收物品
            # 配件管理|移交接收管理|移交记录
            'MvVP': [self.request.BVA8mmtbcT.z36rbt8nuevvk5zw0ev1],  # 批量移交取消
            # 配件管理|入库管理|旧配件入库
            'YqTl': [self.request.HkVg66f8Mk.sPBqvfYc9boVR4rGIL4w],  # 手机-新增采购单
            # 配件管理|配件维护
            'yNNo': [self.request.A3AKRuhANY.vnsg549qqo4e8la9pvyz],  # 新增配件维护-停用
            'DisX': [self.request.A3AKRuhANY.sk6ol090tlyb6qyetwl2],  # 新增配件维护-启用
            # 配件管理|入库管理|新到货入库
            'LJs9': [self.request.OS9qwvYXb5.Jslqnx0TJYAcPWsTNgWG],  # 新到货入库
            # 财务管理|业务记账|预付预收
            'OBvm': [self.request.UjpqCZlmIK.f9xh8uqQHD61p0h46zFQ],  # 新增预付单
            'e5xB': [self.request.UjpqCZlmIK.A7yoyiFi7P8jDGNe67Y0],  # 新增预收单
            # 运营中心|收货入库
            'JIP9': [self.request.NDafRJuz1F.IYU1aVy8aH3qWm62ZtJp],  # 收货入库
            'cTZm': [self.request.NDafRJuz1F.JdFjESShYyLExa0NBUR4],  # 收货入库-X
            'cCQZ': [self.request.NDafRJuz1F.zd9DnAScYux2tHzIRjJT],  # 收货入库-本地报价专用
            # 运营中心|质检管理
            'XK30': [self.request.LCfJXeE7Mf.knHZe0CfAp1HXSNNW4nG],  # 批量接收
            'BriN': [self.request.LCfJXeE7Mf.TJXWHGYpzVeCuC3cZjrH, self.wait_default],  # 提交质检结果
            'Kwz9': [self.request.LCfJXeE7Mf.jN6h3HHrblYl6XRDrjRp],  # 批量接收-X
            'Q7Xz': [self.request.LCfJXeE7Mf.RXoB3Agr98ilYZlNb5FZ],  # 无需质检
            'Rbd1': [self.request.LCfJXeE7Mf.zBKyvA1lFKeRAKK0WXqg, self.wait_default],  # 提交质检结果不传图
            'preu': [self.request.LCfJXeE7Mf.rqPmiTtsuecNOe8Qa0FW, self.wait_default],  # 提交质检结果-X
            'UXXj': [self.request.LCfJXeE7Mf.eoidlhlWuLRCRQL3uNIN],  # 批量接收
            'KXoh': [self.request.LCfJXeE7Mf.NGkklZ12l2IiB7qVbQxE, self.wait_default],  # 提交质检结果
            'FYzF': [self.request.LCfJXeE7Mf.CLRwZ9FXvcE5gCYCPdSF],  # 批量接收
            'ACKg': [self.request.LCfJXeE7Mf.JO1O4Cu3NqUy2eHg71Sb],  # 提交质检结果
            'LLx3': [self.request.LCfJXeE7Mf.EqKnTwPFi7SMTAPIanzC],  # 批量接收-本地报价专用
            'CqTl': [self.request.LCfJXeE7Mf.oKZEC3OeI0tWc8WLWpY3, self.wait_default],  # 提交质检结果-本地报价专用
            # 运营中心|退货管理
            'hkXQ': [self.request.PrpdxJpu3k.BBIpXJ7xM3RSMC8Gh7uI],  # 邮寄退货出库
            'pdTz': [self.request.PrpdxJpu3k.zdM1FoDt6AVwrkGz7nPX],  # 自提退货出库
            # 运营中心|物品出库
            'cahv': [self.request.Pzx3xU1ulY.YtFzTr37KoEb6ObJhKgF],  # 销售出库
            # 运营中心|壹准拍机|售后管理|售后订单
            'NiF8': [self.request.ADixIQYwld.yCDOX9xAevVaoqLEO8Xh],  # 审核优先补差-X
            's522': [self.request.ADixIQYwld.SLVYtmn8n4nMwNGpeuK5],  # 审核退货退款
            'EuOa': [self.request.ADixIQYwld.m2P7xHJlv31GMBi1Qzjb],  # 签收入库-X
            'trt4': [self.request.ADixIQYwld.Om4GtulmnevZNOlqppff],  # 审核优先补差
            'zEPV': [self.request.ADixIQYwld.oUd1bU9wcVj8ujL9j9cI],  # 复检审核拒绝
            'NCSB': [self.request.ADixIQYwld.hjEKlIzRRSYkSa8yshVM],  # 签收入库
            'C17D': [self.request.ADixIQYwld.nAYT9Iv7RAHKUiNICWDZ],  # 审核仅退差
            # 运营中心|待报价物品
            'q9eJ': [self.request.Qc3N4qmsX7.h86Q9EJJuji9EAcwmnZd],  # 商品报价
            # 平台管理|运营中心|待指定物品
            'KnkQ': [self.request.X7hPGKXTGz.designated_recyclers],  # 指定供应商
            # 平台管理|卖场管理|直拍卖场列表
            'IcRG': [self.request.UVTJ3GwNrM.dkzcGVBC4f0eOkX7psWu],  # 创建指定5分钟卖场
            'z2MU': [self.request.UVTJ3GwNrM.i2PADX8AIUDmt1eH6XmL, self.wait_until_next_five_minute],  # 添加商品上架
            'zlAu': [self.request.UVTJ3GwNrM.YOZXR96FA6wK0SgiwgLh, ],  # 创建卖场仅保存
            'DpA7': [self.request.UVTJ3GwNrM.S9rWKvQ89U7Uknx1aXeR],  # 下架
            # 平台管理|壹准拍机|售后管理|申诉管理
            'mw4N': [self.request.V35pu3YhqH.Or5VGbcLZ6drxl8wkMSR],  # 审核退货退款
            'r1GJ': [self.request.V35pu3YhqH.Ms6Xyable2b9S87LhPZd],  # 审核优先补差
            # 平台管理|卖场管理|暗拍卖场列表
            'Lmb4': [self.request.G4BNkqhL40.oQ4T86fmEaH8KwhBSxP3],  # 创建卖场
            'naBM': [self.request.G4BNkqhL40.O4GTsiJ6xj3TEtnNe5vS],  # 创建指定5分钟卖场
            'e8Bq': [self.request.G4BNkqhL40.SML4kMf2uJffhQbwtUx6],  # 下架
            'xNAC': [self.request.G4BNkqhL40.gnlGXVVK4aiBrYlOX6oB, self.wait_until_next_five_minute],  # 添加商品上架
            'TBmR': [self.request.G4BNkqhL40.MLwLbgD1GL9V7rRzU5DF],  # 创建卖场仅保存
            # 平台管理|消息管理|消息发布列表
            'xblM': [self.request.SMtCxoJnmP.G9C97BkpOngHG41cgA0L],  # 平台审核通过
            # 平台管理|虚拟库存|上拍商品管理
            'F0Hr': [self.request.ONWaZZcZFp.fSkueYEb8y8LbP6qtAqN],  # 添加商品上架
            # 保卖管理|订单列表
            'PIGP': [self.request.ZEvt5QWNey.GIh2R4s4U7in3JVtx4Fh],  # 快速保卖
            'XNaM': [self.request.ZEvt5QWNey.UxlDI72fkMivOA7TlGvw],  # 提交发货
            # 商品采购|采购管理|新增采购单
            'ekBx': [self.request.ZTKvMx4gs4.N4CQUFEbAhA6O3SqB3ap],  # 新增采购单未付款入库
            'XLBD': [self.request.ZTKvMx4gs4.LTMkAl3mr9wdiYoATjak],  # 新增采购单未付款在路上
            'CFo3': [self.request.ZTKvMx4gs4.Iv2a1sAnyG1YRbkyU84V],  # 新增采购单-部分已付款入库
            'MwyC': [self.request.ZTKvMx4gs4.UXWWtbpIHPQ9A7QMbtc9],  # 新增采购单未付款未发货
            'ciS4': [self.request.ZTKvMx4gs4.W8Tva7jFU0AkEqegXRnE],  # 新增采购单-全部已付款入库
            # 商品采购|采购管理|采购订单列表
            'clfp': [self.request.G4EaCouJoJ.V3OaBTTJgYrJQyoMmypY],  # 采购仅退款
            'TFma': [self.request.G4EaCouJoJ.FxIuRXAgm25KpkG1vYdL],  # 发货
            # 商品采购|采购管理|采购工单
            'IcFU': [self.request.EE20RTANF9.rfP03M51AR6P1V5a2zV9],  # 新增采购工单
            'YS1c': [self.request.EE20RTANF9.v7dp0gZaBk5c5dnae7G3],  # 开始任务
            'MbiP': [self.request.EE20RTANF9.RB3GNQ8IJqAeegDYmA32],  # 结束任务
            'mybg': [self.request.EE20RTANF9.HTjf6RsIbsSIfYSwsXzv],  # 开始报工
            'ZcF1': [self.request.EE20RTANF9.H7QZrgxeJPrgyVASQvUy],  # 添加特殊工序-报价
            'uVt1': [self.request.EE20RTANF9.hsFfIhIFCLXHb4x2J1CC],  # 添加特殊工序-退货
            'DoNc': [self.request.EE20RTANF9.LrMhNar9BE7bRoEWOGFt],  # 添加特殊工序-付款
            # 商品采购|采购售后管理|待接收物品
            'WVKb': [self.request.LZnv9DokCX.kDYL6B67bVRYqDohXGBm],  # 接收物品
            # 商品采购|采购售后管理|待售后列表
            'O09i': [self.request.WdU75jpBUw.EXJN6Kfs99I6kkD0lNX2],  # 售后退货退款
            'LuOO': [self.request.WdU75jpBUw.p2NxayPBZqnmytlhtjEy],  # 售后换货
            'gfHM': [self.request.WdU75jpBUw.WCIspC62VSOcHhuvk6oH],  # 售后拒退退回
            'vQ7r': [self.request.WdU75jpBUw.iWItsJtwj5CLc0GYimGA],  # 售后退差价
            # 商品采购|采购任务
            'odNU': [self.request.SDhYvjpFxu.tuGormTpYPA2aELsOzkM],  # 新建采购任务
            'D6bk': [self.request.SDhYvjpFxu.Jo3v4QXhq0GyXeDDjAG8],  # 更新初体验
            # 帮卖管理|帮卖上架列表
            'x1dy': [self.request.N1bdBTU6wm.x2Ue8YzUHAdfE5e1ah2B],  # 添加物品
            'VrYn': [self.request.N1bdBTU6wm.YehoAEPuerEeCRCU2qEI],  # 删除物品
            'SbHY': [self.request.N1bdBTU6wm.vsKRonFDNGzytQja2jna],  # 保存期望价格
            'AWj7': [self.request.N1bdBTU6wm.gHXYe9nXDQKo8k2pCpHF],  # 帮卖下单
            'xPPm': [self.request.N1bdBTU6wm.PatKHW4ZM1AOnRz4wYCa],  # 快递易发货
            'BDSs': [self.request.N1bdBTU6wm.CtZUckEy9Xr7Q9rhDgM9],  # 自行邮寄发货
            'ZA5N': [self.request.N1bdBTU6wm.lUGAPOtEUoXAYtTaa2Jb],  # 自己送发货
            'Ez0X': [self.request.N1bdBTU6wm.fBkRLU5PnvGYpBfZdMYx],  # 申请退机
            'ZyMU': [self.request.N1bdBTU6wm.iCbN7kUssvEHLZtMSh1V],  # 保卖买断下单
            'pA7y': [self.request.N1bdBTU6wm.iPBfiMFiHxZjY3ZEwdIp],  # 保卖分润下单
            'Px7B': [self.request.N1bdBTU6wm.fNG49PWF3oUJGnsMAIuf],  # 确认保卖
            'UWBK': [self.request.N1bdBTU6wm.EjR5pz1y2L10GHnV2z4v],  # 申请议价
            # 帮卖管理|帮卖来货列表
            'Sh3x': [self.request.KtEAxo6C4B.UEgbcBjQGEn3BLntI6lb],  # 去质检
            'RGCO': [self.request.KtEAxo6C4B.aR4vvS8nfanSGlBbfKzT],  # 去退机自己送
            'weY4': [self.request.KtEAxo6C4B.puhf4ZwCo9hIo0rzm7zd],  # 去退机自行邮寄
            # 库存管理|入库管理|物流签收入库
            'WZaL': [self.request.IPBU7G33xP.hhbi3Grk7w3kXVnHxfNE],  # 来货物流签收入库
            'HfW9': [self.request.IPBU7G33xP.Jv79uDAMnGFSvRHesu0B],  # 物流签收入库
            # 库存管理|出库管理|销售出库
            'vhyj': [self.request.XwUhCCnV8j.P7mmCcwk64F1knIdDObr],  # 销售出库-来货
            'HRTZ': [self.request.XwUhCCnV8j.cuv4NM82E2Es3yAJkvoi],  # 销售出库未收款
            'boSK': [self.request.XwUhCCnV8j.sX84nolF0TRL5RWSl6zx],  # 销售出库已收款
            # 库存管理|库存列表
            'wQ7u': [self.request.HSA1BkiNHU.cZDVh5eyHxStC2Mli9DI],  # 库存移交销售
            'aMWA': [self.request.HSA1BkiNHU.wWBLmKauWABXgA16zGq5],  # 库存移交质检给库管
            'oSUT': [self.request.HSA1BkiNHU.yPtmSmB6LgGBHuYKQex9],  # 库存移交质检
            'QKxH': [self.request.HSA1BkiNHU.D3dsNkrEsGlGWkoAbUvn],  # 库存移交维修给库管
            'LrYx': [self.request.HSA1BkiNHU.cQRfPcjML2Pxryt529f9],  # 库存移交维修
            'Fv9l': [self.request.HSA1BkiNHU.ELzKzsnP7DBzS58RhuRV],  # 库存移交采购售后
            'nxWZ': [self.request.HSA1BkiNHU.n6qVaJNnhR6yKFZDvMpU],  # 库存移交采购售后给库管
            'DT6i': [self.request.HSA1BkiNHU.BqEQ0BTtXXYnqUFLxnUK],  # 库存移交销售给库管
            'Y1eX': [self.request.HSA1BkiNHU.OAvKjuICy5p7SX9qfvX4],  # 库存移交送修
            'wpto': [self.request.HSA1BkiNHU.xrzuFX14hLZb53t2Dpl4],  # 库存移交送修给库管
            # 库存管理|库存调拨
            'psOC': [self.request.InLEWxc2tL.TkJYyYtSzad1UKsgz33u],  # 新增仓库调拨
            # 库存管理|出库管理|仅出库订单列表
            'mL8f': [self.request.MLkZRHOuRf.ZUdNkyxThIMbrQMjq4A0],  # 仅出库订单
            # 库存管理|库存盘点
            'vVf7': [self.request.F0teh65lah.yfkRUCxXwAxP0gqU85sU],  # 新增盘点》提交盘点》完成库存盘点
            # 库存管理|出库管理|采购售后出库
            'v6AD': [self.request.GrqUVUXI3u.DZpllRLFofze0dkHhqfW],  # 采购售后出库
            # 库存管理|出库管理|地址管理
            'vyTx': [self.request.MTI16ub3xa.SJlFNv1wjIprgodoi79t],  # 新增收货地址
            # 库存管理|出库管理|送修出库
            'yhRO': [self.request.S9pHfGlZA1.Qp71Bn8xqI3rvwuJ9xCr],  # 送修出库
            # 商品销售|销售售后管理|销售售后处理
            'jw4U': [self.request.EPSnRVHPCS.DjkghfK5et2Z3KvN6d3n],  # 销售售后退货
            'oK7U': [self.request.EPSnRVHPCS.w2XcfZ42REixTHsF0D6w],  # 仅退配件入库
            'NIMm': [self.request.EPSnRVHPCS.kveY9vSZiCveNHGRKZ5u],  # 仅退配件在路上
            # 商品销售|销售管理|销售上架
            'In7Z': [self.request.JhWPhXjKbY.kiSivAHj3Vab5m78JpuW],  # 销售上架物品
            # 商品销售|销售管理|待销售物品
            'yoQr': [self.request.K840BKXUBB.BjtCW4zAlmHFf4hnEsyK],  # 销售预售出库
            # 消息管理|消息发布列表
            'IBY2': [self.request.QRSsWbYWV1.p2KvndGL0zVJEDKHGIPU],  # 消息发布新消息提交审核
            'qVoK': [self.request.QRSsWbYWV1.qJP3yR1nymSHmVoKgKFz],  # 消息发布新消息审核通过
            # 钱包管理|钱包中心
            'Ufaw': [self.request.PNng2wLCAK.JxIyyg72fjeXbmTdyUr7],  # 钱包对公转账支付充值
            # 质检管理|先质检后入库
            'XaUk': [self.request.DItqmHbtYn.cKaXogneNjTTTmAdUTcW],  # 新增人工质检数据
            # 质检管理|质检中物品
            'wOOy': [self.request.BN75aoC3Ic.RMOcTd2L2tS32gouvcPO],  # 质检提交质检结果不移交
            # 质检管理|质检内容模版
            'ZyCo': [self.request.GEh4rKFYZs.GySsTzThuG7Y0qU4dr6w],  # 新增质检模版
            # 维修管理|维修中物品
            'OAU3': [self.request.W0EPs560MV.PYrzOPhQBEGaXo51nyaY],  # 提交维修结果
            # 维修管理|维修项目列表
            'cVtB': [self.request.KHgN9h3KO8.nlv33W6U8Vz79YQ8bpFf],  # 新增机型配置
            # 维修管理|维修审核列表
            'fwCA': [self.request.QSG3XpHrLa.InAnaHvFTy76b32mumFp],  # 维修审核通过
            # 送修管理|已送修物品
            'pqYJ': [self.request.FU9FBZt4ek.oaxztsMnbnAXzAxWj6JK],  # 送修完成入库
            # 保卖小程序|首页
            'spKR': [self.request.ZTIxIMcZz7.Cb5TwEFeOGRjQqpsPYhX],  # 精确发货创建订单
            'gpvd': [self.request.ZTIxIMcZz7.Sx6ZHoGa30GK1xH2QbdF],  # 质检服务创建订单
            # 保卖小程序|我的
            'dKLc': [self.request.FoIA7X707t.oOoG2Yvd9naVzPCCZOBU],  # 自行邮寄发货
            'xfzp': [self.request.FoIA7X707t.vSYI2uUTSCpcmhYjD9PL],  # 邮寄退货
            'fNXh': [self.request.FoIA7X707t.opIdDf5eKi5IeleUQBrA],  # 自提退货
            'HfWO': [self.request.FoIA7X707t.IXznmT0bw7FbeHeJCKo6],  # 销售物品
            'VyCN': [self.request.FoIA7X707t.GWIqOqgj1k2cLGBWcfJP],  # 自行邮寄发货-X
            'XkUg': [self.request.FoIA7X707t.cWki4FW4tSlwK63nwMDm],  # 顺丰快递发货-X
            'wle3': [self.request.FoIA7X707t.dkzE7aNehgS9qMzBIRzf],  # 顺丰快递发货
            'xKNk': [self.request.FoIA7X707t.O9TSVizVMFbBHj4PSQi5],  # 取消销售
            'RVtq': [self.request.FoIA7X707t.D1O3SOVl05gD2Lts19A9],  # 复检
            'rI0G': [self.request.FoIA7X707t.Np66pyiMQJz6zbkMLvGH],  # 取消退货
            'BXks': [self.request.FoIA7X707t.fK0PREFRv2Msvl2flpXO],  # 自己送货-本地报价专用
            # 竞拍小程序|竞拍
            'dJeB': [self.request.DuLudPwrAY.SAnRSrq1160pZali4yIf, self.wait_for_five_minutes],  # 直拍出价
            'OAqF': [self.request.DuLudPwrAY.ooh8smtEbSrtOuUNqjJa, self.wait_for_five_minutes],  # 暗拍出价
            # 竞拍小程序|我的
            'VMhm': [self.request.RQTYlCj2X9.c71cLTyRLuY4tAw5OBlV],  # 确认收货
            'kxvu': [self.request.RQTYlCj2X9.aVXdmJVbK9wjjXJCBjst],  # 申请售后
            'Y61c': [self.request.RQTYlCj2X9.ZLMjQKplgxx6Krvopxg7],  # 去发货自己送-X
            'GJ8B': [self.request.RQTYlCj2X9.fujEfOlXIMCY3oXrDNVd],  # 去发货自叫物流
            'INjZ': [self.request.RQTYlCj2X9.xYF6VMP7gVBubHHeRksW],  # 待申诉我要申诉
            'WShX': [self.request.RQTYlCj2X9.Ly41cUm9R4N75FqquckG],  # 改自提
            'pNX9': [self.request.RQTYlCj2X9.FFK90vpcso9aPNnQyAWS],  # 去发货自己送
        }

        # 合并所有操作字典为一个大字典
        operations = {
            **pre_step,
        }
        # 如果传入的是字符串，则转换为列表
        if isinstance(data, str):
            data = [data]

        # 遍历每个 key 并执行对应的操作
        for key in data:
            self.execute_operations(operations, key)
