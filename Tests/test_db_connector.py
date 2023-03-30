"""Tests the db_connector module"""
import db_connector as dbc

# Test Cases
class TestCases:
    """Used to conduct test cases on db_connector module"""
    def test_case1(self):
        """Test 1: Checks if module can detect filename length in search"""
        assert dbc.db_connector_profiler() == 0