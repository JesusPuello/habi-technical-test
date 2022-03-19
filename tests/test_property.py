import unittest
from unittest.mock import patch
from utils import my_sql_connector
from services import property_services


class TestPropertyServices(unittest.TestCase):
    def setUp(self):
        self.request_args = {"city": "bogotá", "year": 2000, "status_id": 3}

    def get_patched_connector(self):
        class PatchedCursor:
            def __init__(self) -> None:
                self.execute_calls = 0
                self.fetchall_calls = 0
                self.info = [
                    (
                        1,
                        "calle 23 #45-67",
                        "bogotá",
                        120000000,
                        "Hermoso apartamento en el centro de la ciudad",
                        2000,
                        "3",
                    ),
                    (
                        53,
                        "calle 23 #45-67q",
                        "bogotá",
                        120000000,
                        "Hermoso apartamento en el centro de la ciudad",
                        2000,
                        "3",
                    ),
                    (
                        2,
                        "calle 2 #45-67",
                        "medellin",
                        120000000,
                        "Hermoso apartamento en el centro de la ciudad",
                        2010,
                        "4",
                    ),
                    (
                        54,
                        "calle 23 #45-67q",
                        "bogotá",
                        120000000,
                        "Hermoso apartamento en el centro de la ciudad",
                        2011,
                        "5",
                    ),
                ]
                self.filtered_response = self.info.copy()

            def execute(self, sql: str):
                self.execute_calls += 1
                self.where = sql.split("where")[1].strip()
                extra_filters = self.where.split("and")
                extra_filters.pop(0)
                self.filtered_response = self.info.copy()
                for extra_filter in extra_filters:
                    extra_filter.strip()
                    value = extra_filter.split("=")[1].strip()
                    if "city" in extra_filter:
                        self.filtered_response = list(
                            filter(
                                lambda i: i[2] == value.replace("'", ""),
                                self.filtered_response,
                            )
                        )
                    if "year" in extra_filter:
                        self.filtered_response = list(
                            filter(lambda i: i[5] == int(value), self.filtered_response)
                        )
                    if "status_id" in extra_filter:
                        self.filtered_response = list(
                            filter(lambda i: i[6] == value, self.filtered_response)
                        )

            def fetchall(self):
                self.fetchall_calls += 1
                return self.filtered_response

        class PatchedConnector:
            def __init__(self) -> None:
                self.cursor = PatchedCursor()
                self.close_all_calls = 0

            def close_all(self) -> None:
                self.close_all_calls += 1
                pass

        self.connector = PatchedConnector()
        return self.connector

    def test_find_available_houses(self):
        with patch.object(my_sql_connector, "DatabaseHandler") as mocked_connector:
            mocked_connector.side_effect = self.get_patched_connector
            # No args call
            response = property_services.find_available_houses()
            self.assertEqual(
                self.connector.cursor.where, "status_id in ('3', '4', '5')"
            )
            self.assertEqual(self.connector.cursor.execute_calls, 1)
            self.assertEqual(self.connector.cursor.fetchall_calls, 1)
            self.assertEqual(self.connector.close_all_calls, 1)
            self.assertEqual(len(response), 4)
            # City arg call
            response = property_services.find_available_houses({"city": "bogotá"})
            self.assertEqual(
                self.connector.cursor.where,
                "status_id in ('3', '4', '5') and city = 'bogotá'",
            )
            self.assertEqual(self.connector.cursor.execute_calls, 1)
            self.assertEqual(self.connector.cursor.fetchall_calls, 1)
            self.assertEqual(self.connector.close_all_calls, 1)
            self.assertEqual(len(response), 3)
            # Year arg call
            response = property_services.find_available_houses({"year": 2011})
            self.assertEqual(
                self.connector.cursor.where,
                "status_id in ('3', '4', '5') and year = 2011",
            )
            self.assertEqual(self.connector.cursor.execute_calls, 1)
            self.assertEqual(self.connector.cursor.fetchall_calls, 1)
            self.assertEqual(self.connector.close_all_calls, 1)
            self.assertEqual(len(response), 1)
            # Status arg call
            response = property_services.find_available_houses({"status_id": 4})
            self.assertEqual(
                self.connector.cursor.where,
                "status_id in ('3', '4', '5') and status_id = 4",
            )
            self.assertEqual(self.connector.cursor.execute_calls, 1)
            self.assertEqual(self.connector.cursor.fetchall_calls, 1)
            self.assertEqual(self.connector.close_all_calls, 1)
            self.assertEqual(len(response), 1)
            # All args call
            response = property_services.find_available_houses(self.request_args)
            self.assertEqual(
                self.connector.cursor.where,
                "status_id in ('3', '4', '5') and city = 'bogotá' and year = 2000 and status_id = 3",
            )
            self.assertEqual(self.connector.cursor.execute_calls, 1)
            self.assertEqual(self.connector.cursor.fetchall_calls, 1)
            self.assertEqual(self.connector.close_all_calls, 1)
            self.assertEqual(len(response), 2)
