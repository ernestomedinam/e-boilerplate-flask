import pytest

from app_name.mock.models.mock import Mock


mock_data = {
    "name": "Some name",
    "parts": 4,
    "description": "just some mock of a mock!"
}

def test_create_mock(db_session):
    """ tests a mock object may be created """
    mock = Mock.create(**mock_data)
    assert isinstance(mock, Mock)

def test_update_mock(db_session):
    mock = Mock.create(**mock_data)
    updated = mock.update(parts=48)
    assert updated
    assert mock.parts == 48

def test_delete_mock(db_session):
    mock = Mock.create(**mock_data)
    mock_id = mock.id
    deleted = mock.delete()
    assert deleted
    query = Mock.get(id=mock_id)
    assert query is None
