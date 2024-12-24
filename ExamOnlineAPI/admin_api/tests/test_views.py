import os
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from admin_api.models import Question
from admin_api.utils import extract_data_from_pdf


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_pdf():
    return os.path.join(os.path.dirname(__file__), 'sample.pdf')

# @pytest.fixture
# def upload_url():
#     return '/admin-api/upload-pdf/'



@pytest.fixture
def sample_question(db):
    """Create a sample question for testing."""
    return Question.objects.create(
        text="Sample question?",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        correct_option="Option 1",
        course_id=101,
        exam_type="midterm"
    )


@pytest.mark.django_db
def test_upload_pdf_success(api_client, mocker, sample_pdf):
    """Test uploading a bulk of questions from a PDF file."""
    mock_extract_data = mocker.patch('admin_api.utils.extract_data_from_pdf')
    mock_extract_data.return_value = [
        {'text': 'What is 2 + 2?', 'options': ['2', '3', '4', '5'], 'correct_option': '4'},
        {'text': 'What is the capital of France?', 'options': ['Berlin', 'Madrid', 'Paris', 'Rome'], 'correct_option': 'Paris'},
    ]
    with open(sample_pdf, 'rb') as pdf_file:
        response = api_client.post('/admin-api/upload-pdf/', {
            'file': pdf_file,
            'exam_type': 'Math',
            'course_id': 1,
        }, format='multipart')

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    assert response.status_code == status.HTTP_201_CREATED, f"Expected 201 but got {response.status_code}"


@pytest.mark.django_db
def test_upload_invalid_pdf(api_client, mocker, sample_pdf):
    """Test uploading a non-PDF file."""
    mock_extract_data = mocker.patch('admin_api.views.extract_data_from_pdf', return_value=[])

    with open(sample_pdf, 'rb') as pdf_file:
        response = api_client.post('/admin-api/upload-pdf/', {
            'file': pdf_file,
            'exam_type': 'Math',
            'course_id': 1,
        }, format='multipart')
    mock_extract_data.assert_called_once()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'error': 'No questions found in PDF'}





def test_get_questions(api_client, sample_question):
    """Test fetching all questions."""
    response = api_client.get('/admin-api/questions/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) == 1
    assert data["questions"][0]["text"] == sample_question.text


@pytest.mark.django_db
def test_create_question(api_client):
    """Test creating a new question."""
    payload = {
        "text": "New question?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_option": "Option A",
        "course_id": 202,
        "exam_type": "final"
    }
    response = api_client.post('/admin-api/questions/', payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["text"] == payload["text"]
    assert data["options"] == payload["options"]
    assert data["correct_option"] == payload["correct_option"]


def test_create_question_missing_field(api_client):
    """Test creating a question with missing fields."""
    payload = {
        "text": "Incomplete question?",
        "options": ["Option A", "Option B"]
    }
    response = api_client.post('/admin-api/questions/', payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "error" in data


def test_get_question_detail(api_client, sample_question):
    """Test retrieving a single question."""
    response = api_client.get(f'/admin-api/questions/{sample_question.id}/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == sample_question.text
    assert data["options"] == sample_question.options


@pytest.mark.django_db
def test_get_question_not_found(api_client):
    """Test retrieving a non-existent question."""
    response = api_client.get('/admin-api/questions/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "error" in data


def test_update_question(api_client, sample_question):
    """Test updating an existing question."""
    payload = {
        "text": "Updated question?",
        "options": ["Option X", "Option Y", "Option Z"],
        "correct_option": "Option X"
    }
    response = api_client.put(f'/admin-api/questions/{sample_question.id}/', payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == payload["text"]
    assert data["options"] == payload["options"]
    assert data["correct_option"] == payload["correct_option"]


def test_delete_question(api_client, sample_question):
    """Test deleting a question."""
    response = api_client.delete(f'/admin-api/questions/{sample_question.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Question.objects.filter(id=sample_question.id).exists()


@pytest.mark.django_db
def test_delete_question_not_found(api_client):
    """Test deleting a non-existent question."""
    response = api_client.delete('/admin-api/questions/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "error" in data