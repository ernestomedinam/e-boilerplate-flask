import pytest
from app_name.mock.models import Mock
from sqlalchemy.exc import IntegrityError

def test_mock_db_crud(db_session):
    """ test a mock object crud is working. """
    test_payload = {
        "name": "some name",
        "parts": 4,
        "description": "just some mock object's description."
    }
    test_mock_instance = Mock(test_payload)
    db_session.add(test_mock_instance)
    db_session.commit()
    query = db_session.query(Mock).filter_by(
        name=test_payload["name"]
    )
    assert len(query.all()) > 0
    mock_id = query.all()[0].id
    # test cannot create another with same name
    test_payload["parts"] = 2
    test_payload["description"] = "another one... with less parts!"
    test_mock_instance = Mock(test_payload)
    db_session.add(test_mock_instance)
    with pytest.raises(IntegrityError):
        assert db_session.commit()
    db_session.rollback()
    # test edit mock's properties
    test_payload["name"] = "Newman"
    mock_instance = db_session.query(Mock).filter_by(
        id=mock_id
    ).one_or_none()
    mock_instance.name = test_payload["name"]
    db_session.commit()
    mock_instance = db_session.query(Mock).filter_by(
        name=test_payload["name"]
    ).one_or_none()
    assert mock_instance is not None
    assert mock_instance.name == test_payload["name"]
    # test delete mock
    db_session.delete(mock_instance)
    db_session.commit()
    mock_instance = db_session.query(Mock).filter_by(
        name=test_payload["name"]
    ).one_or_none()
    assert mock_instance is None

def test_mock_fn_crud(db_session):
    """ test object methods for mock crud """
    test_payload = {
        "name": "from the web",
        "parts": 7,
        "description": "one part per day of the week seems to workout."
    }
    # test create method
    create_result = Mock.create(test_payload)
    assert create_result["status_code"] == 201
    mock_id = create_result["text"]["id"]
    # query for mock_instance
    requested_mock = db_session.query(Mock).filter_by(
        id=mock_id
    ).one_or_none()
    assert requested_mock.parts == 7
    # test update method
    update_result = requested_mock.update({
        "parts": 9
    })
    assert update_result["status_code"] == 200
    # test delete method
    another_mock = db_session.query(Mock).filter_by(
        id=mock_id
    ).one_or_none()
    delete_result = Mock.delete(another_mock.id) 
    assert delete_result["status_code"] == 204
