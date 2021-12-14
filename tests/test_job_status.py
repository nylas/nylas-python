from datetime import datetime

import pytest
from nylas.client.restful_models import JobStatus


@pytest.mark.usefixtures("mock_job_statuses")
def test_first_job_status(api_client):
    job_status = api_client.job_statuses.first()
    assert isinstance(job_status, JobStatus)


@pytest.mark.usefixtures("mock_job_statuses")
def test_all_job_status(api_client):
    job_statuses = api_client.job_statuses.all()
    assert len(job_statuses) == 2
    for job_status in job_statuses:
        assert isinstance(job_status, JobStatus)


@pytest.mark.usefixtures("mock_job_statuses")
def test_job_status(api_client):
    job_status = api_client.job_statuses.first()
    assert job_status["account_id"] == "test_account_id"
    assert job_status["action"] == "save_draft"
    assert job_status["id"] == "test_id"
    assert job_status["job_status_id"] == "test_job_status_id"
    assert job_status["object"] == "message"
    assert job_status["status"] == "successful"
    assert job_status["created_at"] == datetime(2021, 6, 4, 22, 36)


@pytest.mark.usefixtures("mock_job_statuses")
def test_job_status_is_successful(api_client):
    job_status = api_client.job_statuses.first()
    assert job_status.is_successful() is True


@pytest.mark.usefixtures("mock_job_statuses")
def test_job_status_is_successful_false(api_client):
    job_status = api_client.job_statuses.first()
    job_status.status = "failed"
    assert job_status.is_successful() is False
