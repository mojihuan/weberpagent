"""LocatorChainBuilder -- 从 DOMInteractedElement 提取多策略定位器链。

按优先级排序: XPath -> CSS by ID -> CSS by data-testid -> get_by_role -> get_by_placeholder。
每个操作最多 3 个定位器 (per D-02)。
"""
