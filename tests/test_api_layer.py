# -*- coding: utf-8 -*-

from .context import api_layer
import unittest


class AwsApiLayerTestSuite(unittest.TestCase):
    """Test cases for the api layer suite."""

    def test_regexp_file_timestamp(self):
        result = api_layer.parse_regexp(r"(.*)/([A-Za-z]+)_([\w_]+)_([\d]{8})([\d]{4})([\w]+)\.([\w]+)$",
                                        "api-gateway/tests/data/apple_health_tracking_201911231045steps.csv",
                                        ("directory",
                                         "company",
                                         "application",
                                         "date",
                                         "time",
                                         "activity",
                                         "file_type"))

        # Write test failures first
        self.assertEqual(result["directory"], "api-gateway/tests/data")
        self.assertEqual(result["company"], "apple")
        self.assertEqual(result["application"], "health_tracking")
        self.assertEqual(result["date"], "20191123")
        self.assertEqual(result["time"], "1045")
        self.assertEqual(result["activity"], "steps")


if __name__ == '__main__':
    unittest.main()
