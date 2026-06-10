import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from grades import is_int, data_into_buckets, get_dist_stats


class TestIsInt:
    def test_valid_integer(self):
        assert is_int("85") is True

    def test_zero(self):
        assert is_int("0") is True

    def test_negative(self):
        assert is_int("-5") is True

    def test_float_string(self):
        assert is_int("85.5") is False

    def test_empty_string(self):
        assert is_int("") is False

    def test_text(self):
        assert is_int("abc") is False

    def test_whitespace(self):
        assert is_int(" ") is False


class TestDataIntoBuckets:
    def test_empty(self):
        assert data_into_buckets([]) == [0, 0, 0, 0, 0, 0, 0]

    def test_below_50(self):
        assert data_into_buckets(["0", "30", "49"]) == [3, 0, 0, 0, 0, 0, 0]

    def test_50s(self):
        assert data_into_buckets(["50", "55", "59"]) == [0, 3, 0, 0, 0, 0, 0]

    def test_60s(self):
        assert data_into_buckets(["60", "65", "69"]) == [0, 0, 3, 0, 0, 0, 0]

    def test_70s(self):
        assert data_into_buckets(["70", "75", "79"]) == [0, 0, 0, 3, 0, 0, 0]

    def test_80s(self):
        assert data_into_buckets(["80", "85", "89"]) == [0, 0, 0, 0, 3, 0, 0]

    def test_90_and_above(self):
        assert data_into_buckets(["90", "95", "100"]) == [0, 0, 0, 0, 0, 3, 0]

    def test_nan_bucket(self):
        assert data_into_buckets(["n/a", "pass", ""]) == [0, 0, 0, 0, 0, 0, 3]

    def test_boundary_50_is_not_below_50(self):
        assert data_into_buckets(["50"])[0] == 0
        assert data_into_buckets(["50"])[1] == 1

    def test_boundary_90_is_not_in_80s(self):
        assert data_into_buckets(["90"])[4] == 0
        assert data_into_buckets(["90"])[5] == 1

    def test_mixed(self):
        grades = ["45", "55", "65", "75", "85", "95", "abc"]
        assert data_into_buckets(grades) == [1, 1, 1, 1, 1, 1, 1]


class TestGetDistStats:
    def test_returns_string(self):
        result = get_dist_stats(["70", "80", "90"])
        assert isinstance(result, str)

    def test_contains_expected_keys(self):
        result = get_dist_stats(["70", "80", "90"])
        for key in ("Total", "Mean", "Median", "Stdev", "Min", "Max", "Dist"):
            assert key in result

    def test_total_count(self):
        result = get_dist_stats(["70", "80", "90"])
        assert "Total: 3" in result

    def test_mean_value(self):
        result = get_dist_stats(["70", "80", "90"])
        assert "Mean: 80" in result

    def test_ignores_nan_in_stats(self):
        result = get_dist_stats(["70", "80", "90", "abc"])
        assert "Total: 4" in result
        assert "Mean: 80" in result

    def test_single_value_stdev_zero(self):
        result = get_dist_stats(["75"])
        assert "Stdev: 0" in result
