from nylas.resources.scheduler import Scheduler


class TestScheduler:
    def test_get_availability(self, http_client_response):
        scheduler = Scheduler(http_client_response)
        query_params = {
            "start_time": 1730725200,
            "end_time": 1730727000,
            "configuration_id": "configuration-123",
        }

        scheduler.get_availability(query_params=query_params)

        http_client_response._execute.assert_called_once_with(
            "GET",
            "/v3/scheduling/availability",
            query_params=query_params,
            overrides=None,
        )
