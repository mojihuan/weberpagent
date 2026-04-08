"""Batch API endpoint integration tests."""
import pytest


@pytest.mark.asyncio
async def test_create_batch():
    """POST /batches creates batch with runs and starts execution."""
    pytest.skip("Waiting for batch API implementation")


@pytest.mark.asyncio
async def test_get_batch_status():
    """GET /batches/{id} returns batch status with run summaries."""
    pytest.skip("Waiting for batch API implementation")


@pytest.mark.asyncio
async def test_get_batch_runs():
    """GET /batches/{id}/runs returns runs belonging to a batch."""
    pytest.skip("Waiting for batch API implementation")
