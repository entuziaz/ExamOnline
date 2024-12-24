import pytest
from rest_framework.test import APIClient
from admin_api.models import Question



@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_question_list_success(api_client):
    Question.objects.create(
        text="What is 2 + 2?",
        options=["2", "3", "4", "5"],
        correct_option="4",
        course_id=101,
        exam_type="final"
    )
    response = api_client.get('/user-api/questions/?course_id=101&exam_type=final')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_question_list_with_no_questions(api_client):
    """Test retrieving questions when no matching questions exist."""
    response = api_client.get('/user-api/questions/?course_id=999&exam_type=mock')
    assert response.status_code == 404
    assert 'error' in response.json()


@pytest.mark.django_db
def test_submit_answers_success(api_client):
    question = Question.objects.create(
        text="What is 2 + 2?",
        options=["2", "3", "4", "5"],
        correct_option="4",
        course_id=101,
        exam_type="final"
    )
    payload = {
        "submissions": [
            {"question_id": question.id, "chosen_option": "4"}
        ]
    }
    response = api_client.post('/user-api/submit/', payload, format='json')
    assert response.status_code == 200
    assert response.json()['results'][0]['correct'] is True



@pytest.mark.django_db
def test_submit_answers_with_invalid_format(api_client):
    """Test submitting answers with invalid data format."""
    response = api_client.post('/user-api/submit/', {}, format='json')
    assert response.status_code == 400
    assert 'error' in response.json()


@pytest.mark.django_db
def test_submit_answers_with_missing_fields(api_client):
    """Test submitting answers with missing required fields."""
    payload = {
        "submissions": [
            {"chosen_option": "4"}  # Missing question_id
        ]
    }
    response = api_client.post('/user-api/submit/', payload, format='json')
    assert response.status_code == 400
    assert 'error' in response.json()
