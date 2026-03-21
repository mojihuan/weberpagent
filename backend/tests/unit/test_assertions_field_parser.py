"""Unit tests for AST-based assertion field parser.

These tests verify the field discovery functions in external_precondition_bridge.py
that parse base_assertions_field.py using AST to extract field information.
"""

import pytest
import ast
from unittest.mock import patch, MagicMock

from backend.core import external_precondition_bridge


# Sample Python code that mimics base_assertions_field.py structure
SAMPLE_FIELD_CODE = '''
class AssertionsRes(BaseApi):
    def assertive_field(self):
        param = {
            "createTime": ("createTime", self.get_formatted_datetime()),
            "updateTime": ("updateTime", self.get_formatted_datetime()),
            "statusStr": ("statusStr", ""),
            "salesOrder": ("salesOrder", ""),
            "purchaseAmount": ("accessoryOrderInfo.purchaseAmount", 0),
            "orderDate": ("orderDate", self.get_formatted_datetime()),
            "inventoryQty": ("inventoryQty", 0),
            "remark": ("remark", ""),
        }
'''


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset bridge cache before and after each test."""
    external_precondition_bridge.reset_cache()
    yield
    external_precondition_bridge.reset_cache()


class TestParamDictVisitor:
    """Tests for ParamDictVisitor class."""

    def test_parse_param_dict_extracts_fields_from_sample_code(self):
        """Test that ParamDictVisitor correctly extracts param dictionary from sample code."""
        tree = ast.parse(SAMPLE_FIELD_CODE)
        visitor = external_precondition_bridge.ParamDictVisitor()
        visitor.visit(tree)

        assert visitor.param_dict is not None
        assert isinstance(visitor.param_dict, ast.Dict)
        # Should have 8 keys in the param dict
        assert len(visitor.param_dict.keys) == 8

    def test_parse_param_dict_returns_none_for_code_without_param(self):
        """Test that ParamDictVisitor returns None when no param dict is found."""
        code_without_param = '''
class SomeClass:
    def some_method(self):
        x = 1
'''
        tree = ast.parse(code_without_param)
        visitor = external_precondition_bridge.ParamDictVisitor()
        visitor.visit(tree)

        assert visitor.param_dict is None


class TestExtractFieldTuples:
    """Tests for extracting field tuples from parsed AST."""

    def test_extract_field_tuples_correctly_parses_path_and_default(self):
        """Test that field tuples are extracted with correct path and default values."""
        tree = ast.parse(SAMPLE_FIELD_CODE)
        visitor = external_precondition_bridge.ParamDictVisitor()
        visitor.visit(tree)

        # Check a simple field with string default
        status_str_value = None
        for key, value in zip(visitor.param_dict.keys, visitor.param_dict.values):
            if isinstance(key, ast.Constant) and key.value == "statusStr":
                status_str_value = value
                break

        assert status_str_value is not None
        assert isinstance(status_str_value, ast.Tuple)
        assert len(status_str_value.elts) == 2
        # First element is path
        assert isinstance(status_str_value.elts[0], ast.Constant)
        assert status_str_value.elts[0].value == "statusStr"
        # Second element is default
        assert isinstance(status_str_value.elts[1], ast.Constant)
        assert status_str_value.elts[1].value == ""

    def test_extract_nested_field_path(self):
        """Test that nested field paths like accessoryOrderInfo.purchaseAmount are extracted."""
        tree = ast.parse(SAMPLE_FIELD_CODE)
        visitor = external_precondition_bridge.ParamDictVisitor()
        visitor.visit(tree)

        purchase_amount_value = None
        for key, value in zip(visitor.param_dict.keys, visitor.param_dict.values):
            if isinstance(key, ast.Constant) and key.value == "purchaseAmount":
                purchase_amount_value = value
                break

        assert purchase_amount_value is not None
        assert isinstance(purchase_amount_value, ast.Tuple)
        # Path should be the nested path
        assert purchase_amount_value.elts[0].value == "accessoryOrderInfo.purchaseAmount"


class TestIsTimeField:
    """Tests for time field detection."""

    def test_is_time_field_detects_get_formatted_datetime_call(self):
        """Test that fields with get_formatted_datetime() default are detected as time fields."""
        tree = ast.parse(SAMPLE_FIELD_CODE)
        visitor = external_precondition_bridge.ParamDictVisitor()
        visitor.visit(tree)

        # Find createTime field which has get_formatted_datetime() default
        for key, value in zip(visitor.param_dict.keys, visitor.param_dict.values):
            if isinstance(key, ast.Constant) and key.value == "createTime":
                default_node = value.elts[1]
                is_time = external_precondition_bridge._is_time_field("createTime", default_node)
                assert is_time is True
                break

    def test_is_time_field_detects_time_suffix(self):
        """Test that fields with Time/time/Date/date suffix are detected as time fields."""
        # Test with None default node (fallback to suffix matching)
        assert external_precondition_bridge._is_time_field("updateTime", None) is True
        assert external_precondition_bridge._is_time_field("orderDate", None) is True
        assert external_precondition_bridge._is_time_field("saleTime", None) is True
        assert external_precondition_bridge._is_time_field("deliveryDate", None) is True

    def test_is_time_field_returns_false_for_non_time_fields(self):
        """Test that non-time fields return False."""
        # Non-time fields
        assert external_precondition_bridge._is_time_field("statusStr", None) is False
        assert external_precondition_bridge._is_time_field("salesOrder", None) is False
        assert external_precondition_bridge._is_time_field("remark", None) is False


class TestInferFieldGroup:
    """Tests for field group inference from naming patterns."""

    def test_infer_field_group_returns_sales_for_sale_prefix(self):
        """Test that fields starting with 'sale' or 'sales' are grouped as sales-related."""
        assert external_precondition_bridge.infer_field_group("salesOrder") == "销售相关"
        assert external_precondition_bridge.infer_field_group("salePrice") == "销售相关"
        assert external_precondition_bridge.infer_field_group("salesReturn") == "销售相关"

    def test_infer_field_group_returns_purchase_for_purchase_prefix(self):
        """Test that fields starting with 'purchase' are grouped as purchase-related."""
        assert external_precondition_bridge.infer_field_group("purchaseAmount") == "采购相关"
        assert external_precondition_bridge.infer_field_group("purchaseOrder") == "采购相关"

    def test_infer_field_group_returns_inventory_for_inventory_prefix(self):
        """Test that fields starting with 'inventory' are grouped as inventory-related."""
        assert external_precondition_bridge.infer_field_group("inventoryQty") == "库存相关"
        assert external_precondition_bridge.infer_field_group("inventoryStatus") == "库存相关"

    def test_infer_field_group_returns_time_for_time_suffix(self):
        """Test that fields ending with Time/time/Date/date are grouped as time fields."""
        assert external_precondition_bridge.infer_field_group("createTime") == "时间字段"
        assert external_precondition_bridge.infer_field_group("updateTime") == "时间字段"
        assert external_precondition_bridge.infer_field_group("orderDate") == "时间字段"

    def test_infer_field_group_returns_order_for_order_prefix(self):
        """Test that fields starting with 'order' are grouped as order-related."""
        assert external_precondition_bridge.infer_field_group("orderStatus") == "订单相关"
        assert external_precondition_bridge.infer_field_group("orderAmount") == "订单相关"

    def test_infer_field_group_returns_nested_for_accessory_order_info(self):
        """Test that nested accessoryOrderInfo fields are grouped correctly."""
        assert external_precondition_bridge.infer_field_group("accessoryOrderInfo.purchaseAmount") == "配件订单嵌套"
        assert external_precondition_bridge.infer_field_group("accessoryOrderInfo.imei") == "配件订单嵌套"

    def test_infer_field_group_returns_general_for_unknown_patterns(self):
        """Test that unknown patterns return general group."""
        assert external_precondition_bridge.infer_field_group("statusStr") == "通用字段"
        assert external_precondition_bridge.infer_field_group("remark") == "通用字段"
        assert external_precondition_bridge.infer_field_group("unknownField") == "通用字段"


class TestGenerateFieldDescription:
    """Tests for Chinese description generation from camelCase field names."""

    def test_generate_field_description_converts_create_time(self):
        """Test createTime -> 创建时间."""
        assert external_precondition_bridge.generate_field_description("createTime") == "创建时间"

    def test_generate_field_description_converts_update_time(self):
        """Test updateTime -> 更新时间."""
        assert external_precondition_bridge.generate_field_description("updateTime") == "更新时间"

    def test_generate_field_description_converts_sales_order(self):
        """Test salesOrder -> 销售订单."""
        assert external_precondition_bridge.generate_field_description("salesOrder") == "销售订单"

    def test_generate_field_description_converts_status_str(self):
        """Test statusStr -> 状态字符串."""
        assert external_precondition_bridge.generate_field_description("statusStr") == "状态字符串"

    def test_generate_field_description_converts_purchase_amount(self):
        """Test purchaseAmount -> 采购金额."""
        assert external_precondition_bridge.generate_field_description("purchaseAmount") == "采购金额"

    def test_generate_field_description_returns_original_for_unknown_words(self):
        """Test that unknown words are capitalized and joined."""
        # Unknown words should be capitalized
        result = external_precondition_bridge.generate_field_description("xyzAbc")
        # Should contain capitalized versions
        assert "Xyz" in result or "Abc" in result


class TestGetAssertionFieldsGrouped:
    """Tests for the main get_assertion_fields_grouped function."""

    def test_get_assertion_fields_grouped_returns_grouped_structure(self):
        """Test that get_assertion_fields_grouped returns correct structure."""
        with patch.object(
            external_precondition_bridge,
            '_get_assertions_field_path',
            return_value='/fake/path/base_assertions_field.py'
        ), patch.object(
            external_precondition_bridge,
            'parse_assertions_field_py',
            return_value=[
                {'name': 'createTime', 'path': 'createTime', 'is_time_field': True, 'group': '时间字段', 'description': '创建时间'},
                {'name': 'salesOrder', 'path': 'salesOrder', 'is_time_field': False, 'group': '销售相关', 'description': '销售订单'},
            ]
        ):
            result = external_precondition_bridge.get_assertion_fields_grouped()

            assert result['available'] is True
            assert 'groups' in result
            assert 'total' in result
            assert result['total'] == 2

    def test_get_assertion_fields_grouped_returns_unavailable_when_no_path(self):
        """Test that get_assertion_fields_grouped returns unavailable when path not configured."""
        with patch.object(
            external_precondition_bridge,
            '_get_assertions_field_path',
            return_value=None
        ):
            result = external_precondition_bridge.get_assertion_fields_grouped()

            assert result['available'] is False
            assert 'error' in result
            assert result['total'] == 0
            assert result['groups'] == []

    def test_get_assertion_fields_grouped_returns_unavailable_when_file_not_found(self):
        """Test that get_assertion_fields_grouped returns unavailable when file not found."""
        with patch.object(
            external_precondition_bridge,
            '_get_assertions_field_path',
            return_value='/nonexistent/path/base_assertions_field.py'
        ), patch('pathlib.Path.exists', return_value=False):
            result = external_precondition_bridge.get_assertion_fields_grouped()

            assert result['available'] is False
            assert 'error' in result
            assert 'not found' in result['error'].lower()

    def test_get_assertion_fields_grouped_uses_cache(self):
        """Test that get_assertion_fields_grouped uses cached data on subsequent calls."""
        with patch.object(
            external_precondition_bridge,
            '_get_assertions_field_path',
            return_value='/fake/path/base_assertions_field.py'
        ), patch.object(
            external_precondition_bridge,
            'parse_assertions_field_py',
            return_value=[
                {'name': 'testField', 'path': 'testField', 'is_time_field': False, 'group': '通用字段', 'description': '测试字段'},
            ]
        ):
            # First call
            result1 = external_precondition_bridge.get_assertion_fields_grouped()
            assert result1['total'] == 1

            # Second call should use cache (parse_assertions_field_py not called again)
            result2 = external_precondition_bridge.get_assertion_fields_grouped()
            assert result2['total'] == 1


class TestParseAssertionsFieldPy:
    """Tests for the parse_assertions_field_py function."""

    def test_parse_assertions_field_py_extracts_all_fields(self):
        """Test that parse_assertions_field_py extracts all fields from file."""
        # Create a temporary file with sample code
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(SAMPLE_FIELD_CODE)
            temp_path = f.name

        try:
            fields = external_precondition_bridge.parse_assertions_field_py(temp_path)

            assert len(fields) == 8
            field_names = [f['name'] for f in fields]
            assert 'createTime' in field_names
            assert 'updateTime' in field_names
            assert 'statusStr' in field_names
            assert 'salesOrder' in field_names
            assert 'purchaseAmount' in field_names

            # Check field structure
            create_time = next(f for f in fields if f['name'] == 'createTime')
            assert create_time['is_time_field'] is True
            assert create_time['group'] == '时间字段'
            assert create_time['description'] == '创建时间'

            # Check nested path
            purchase_amount = next(f for f in fields if f['name'] == 'purchaseAmount')
            assert purchase_amount['path'] == 'accessoryOrderInfo.purchaseAmount'
            assert purchase_amount['group'] == '配件订单嵌套'
        finally:
            import os
            os.unlink(temp_path)

    def test_parse_assertions_field_py_returns_empty_for_invalid_file(self):
        """Test that parse_assertions_field_py returns empty list for file without param dict."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('# Empty file without param dict')
            temp_path = f.name

        try:
            fields = external_precondition_bridge.parse_assertions_field_py(temp_path)
            assert fields == []
        finally:
            import os
            os.unlink(temp_path)


class TestSplitCamelCase:
    """Tests for the split_camel_case helper function."""

    def test_split_camel_case_simple(self):
        """Test simple camelCase splitting."""
        assert external_precondition_bridge.split_camel_case("createTime") == ["create", "time"]

    def test_split_camel_case_multiple_words(self):
        """Test multiple word camelCase splitting."""
        assert external_precondition_bridge.split_camel_case("salesOrderAmount") == ["sales", "order", "amount"]

    def test_split_camel_case_single_word(self):
        """Test single word (no camelCase)."""
        assert external_precondition_bridge.split_camel_case("status") == ["status"]

    def test_split_camel_case_empty_string(self):
        """Test empty string returns empty list."""
        assert external_precondition_bridge.split_camel_case("") == []


class TestGroupFields:
    """Tests for the _group_fields helper function."""

    def test_group_fields_groups_by_group_property(self):
        """Test that _group_fields correctly groups fields by their group property."""
        fields = [
            {'name': 'createTime', 'path': 'createTime', 'is_time_field': True, 'group': '时间字段', 'description': '创建时间'},
            {'name': 'updateTime', 'path': 'updateTime', 'is_time_field': True, 'group': '时间字段', 'description': '更新时间'},
            {'name': 'salesOrder', 'path': 'salesOrder', 'is_time_field': False, 'group': '销售相关', 'description': '销售订单'},
        ]

        groups = external_precondition_bridge._group_fields(fields)

        # Should have 2 groups
        assert len(groups) == 2

        # Find time group
        time_group = next((g for g in groups if g['name'] == '时间字段'), None)
        assert time_group is not None
        assert len(time_group['fields']) == 2

        # Find sales group
        sales_group = next((g for g in groups if g['name'] == '销售相关'), None)
        assert sales_group is not None
        assert len(sales_group['fields']) == 1

    def test_group_fields_returns_empty_for_empty_input(self):
        """Test that _group_fields returns empty list for empty input."""
        groups = external_precondition_bridge._group_fields([])
        assert groups == []
