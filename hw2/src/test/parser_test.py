# #!/usr/bin/env python

__author__ = 'Leonid'

import unittest
from datetime import date

from lib import data_parser


class DataParserTest(unittest.TestCase):
    ward_neighborhood_file_name = 'ward_neighborhood_mapping_test.csv'
    sweep_file_name = 'sweeping_schedule_test.csv'
    towed_file_name = 'towed_vehicles_test.csv'

    def test_get_sweeping_data(self):
        test_data = data_parser.get_sweeping_data(self.sweep_file_name)
        expected_data = {'west': [date(2015, 11, 3), date(2015, 11, 4), date(2015, 6, 1), date(2015, 6, 2)]}
        self.assertEqual(test_data, expected_data)

    def test_get_towed_data(self):
        test_data = data_parser.get_towed_data(self.towed_file_name)
        expected_data = {'west': [date(2015, 9, 9), date(2015, 9, 9)], 'downtown': [date(2015, 9, 9), date(2015, 9, 9)]}
        self.assertEqual(test_data, expected_data)

    def test_get_ward_neighborhood_map(self):
        test_data = data_parser.get_ward_neighborhood_map(self.ward_neighborhood_file_name)
        expected_data = {1: 'downtown', 2: 'downtown'}
        self.assertEqual(test_data, expected_data)

    def test_get_number_of_towed_vehicles_by_neighborhood(self):
        test_data = data_parser.get_number_of_towed_vehicles_by_neighborhood('west', self.towed_file_name)
        expected_data = {date(2015, 9, 9): 2}
        self.assertEqual(test_data, expected_data)

    def test_street_cleaning_by_neighborhood(self):
        test_data = data_parser.street_cleaning_by_neighborhood('west', self.towed_file_name, self.sweep_file_name)
        expected_data = {date(2015, 9, 9): False}
        self.assertEqual(test_data, expected_data)


if __name__ == '__main__':
    unittest.main()
