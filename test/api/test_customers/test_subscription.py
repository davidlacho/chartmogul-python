import unittest
from datetime import datetime

import requests_mock

from chartmogul import Config, CustomerSubscription


class CustomerSubscriptionsTestCase(unittest.TestCase):
    """
    Tests cancel, because it has custom path.
    """

    @requests_mock.mock()
    def test_cancel_subscription(self, mock_requests):
        """Test cancel (patch) subscription (cancelled_at)."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/import/subscriptions/some_uuid",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "uuid": "some_uuid",
                "external_id": "sub_0001",
                "customer_uuid": "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
                "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                "cancellation_dates": ["2016-01-15T00:00:00.000Z"],
                "data_source_uuid": "ds_fef05d54-47b4-431b-aed2-eb6b9e545430",
            },
        )
        config = Config("token")  # is actually checked in mock
        result = CustomerSubscription.cancel(
            config, uuid="some_uuid", data={"cancelled_at": datetime(2016, 1, 15, 0, 0, 0)}
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {"cancelled_at": "2016-01-15T00:00:00"})
        self.assertTrue(isinstance(result, CustomerSubscription))
        self.assertEqual(result.uuid, "some_uuid")

    @requests_mock.mock()
    def test_modify_subscription(self, mock_requests):
        """Test modify (patch) subscription (cancellation_dates)."""
        mock_requests.register_uri(
            "PATCH",
            "https://api.chartmogul.com/v1/import/subscriptions/some_uuid",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "uuid": "some_uuid",
                "external_id": "sub_0001",
                "customer_uuid": "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
                "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                "cancellation_dates": [],
                "data_source_uuid": "ds_fef05d54-47b4-431b-aed2-eb6b9e545430",
            },
        )
        config = Config("token")  # is actually checked in mock
        result = CustomerSubscription.modify(
            config, uuid="some_uuid", data={"cancellation_dates": []}
        ).get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(mock_requests.last_request.json(), {"cancellation_dates": []})
        self.assertEqual(result.__class__, CustomerSubscription)
        self.assertEqual(
            result.__dict__,
            CustomerSubscription(
                **{
                    "cancellation_dates": [],
                    "customer_uuid": "cus_f466e33d-ff2b-4a11-8f85-417eb02157a7",
                    "data_source_uuid": "ds_fef05d54-47b4-431b-aed2-eb6b9e545430",
                    "uuid": "some_uuid",
                    "external_id": "sub_0001",
                    "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                }
            ).__dict__,
        )

    @requests_mock.mock()
    def test_list_imported_subscriptions(self, mock_requests):
        """Test listing (get) subscriptions."""
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/import/customers/some_uuid/subscriptions",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "customer_uuid": "some_uuid",
                "subscriptions": [
                    {
                        "uuid": "sub_e6bc5407-e258-4de0-bb43-61faaf062035",
                        "external_id": "sub_0001",
                        "subscription_set_external_id": "sub_set_0001",
                        "plan_uuid": "pl_eed05d54-75b4-431b-adb2-eb6b9e543206",
                        "data_source_uuid": "ds_fef05d54-47b4-431b-aed2-eb6b9e545430",
                        "cancellation_dates": [],
                    }
                ],
                "cursor": "cursor==",
                "has_more": False,
            },
        )
        config = Config("token")  # is actually checked in mock
        result = CustomerSubscription.list_imported(config, uuid="some_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.__class__.__name__, CustomerSubscription._many.__name__)
        self.assertEqual(result.customer_uuid, "some_uuid")

    @requests_mock.mock()
    def test_all(self, mock_requests):
        """Test getting metrics of all subscriptions for a customer."""
        mock_requests.register_uri(
            "GET",
            "https://api.chartmogul.com/v1/customers/some_uuid/subscriptions",
            request_headers={"Authorization": "Basic dG9rZW46"},
            status_code=200,
            json={
                "entries": [
                    {
                        "id": 9306830,
                        "external_id": "sub_0001",
                        "plan": "PRO Plan (10,000 active cust.) monthly",
                        "quantity": 1,
                        "mrr": 70800,
                        "arr": 849600,
                        "status": "active",
                        "billing-cycle": "month",
                        "billing-cycle-count": 1,
                        "start-date": "2015-12-20T08:26:49-05:00",
                        "end-date": "2016-03-20T09:26:49-05:00",
                        "currency": "USD",
                        "currency-sign": "$",
                    }
                ],
                "has_more": False,
                "per_page": 200,
                "page": 1,
                "cursor": "cursor==",
            },
        )
        config = Config("token")  # is actually checked in mock
        result = CustomerSubscription.all(config, uuid="some_uuid").get()

        self.assertEqual(mock_requests.call_count, 1, "expected call")
        self.assertEqual(mock_requests.last_request.qs, {})
        self.assertEqual(result.__class__.__name__, CustomerSubscription._many.__name__)
        self.assertEqual(result.entries[0].external_id, "sub_0001")
        self.assertEqual(result.page, 1)
        self.assertEqual(result.cursor, "cursor==")
