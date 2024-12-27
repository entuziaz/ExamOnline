# ExamOnline: PDF Question Upload and Review System

## Overview

The **ExamOnline** project allows administrators to upload PDFs containing exam questions, extract the questions, and review them before saving them into the database. It also allow anonymous users to take exams, view questions and submit answers to compare with the correct answers. 


**Check out the full API documenation that shows all endpoints, sample requests and responses and other contextual details in the [developer docs](https://jkaylight.gitbook.io/examonline).**


---
## Key Features

1. **Authentication and Authorization**: Admins can register, login and logout of sessions to access admin endpoints.
1. **Upload PDF**: An admin uploads a PDF file containing the exam questions to the system.
2. **Extract Questions**: The system extracts the questions from the PDF file, highlighting each question's text and options.
3. **Review and Edit**: The extracted questions are returned for review.
4. **Save Questions**: After reviewing, the admin submits the questions for storage in the database.
5. **View, Edit and Delete Questions**: An admin can manually create, view, modify and delete questions.
5. **User Exam**: Users can select an exam, view the questions, select options and submit to see the correct answers.

---

## API Endpoints

### 1. **Upload PDF for Review**
**Endpoint**: `/admin-api/upload-pdf/`

**Method**: `POST`

**Description**: This endpoint allows an administrator to upload a PDF containing exam questions. The system will extract the questions and return them for review.

**Request**:
```bash
curl -X POST "http://127.0.0.1:8000/admin-api/upload-pdf/" \
     -H "Content-Type: multipart/form-data" \
     -H "Authorization: Token YOUR_AUTH_TOKEN" \
     -F "file=@/path/to/file.pdf"
```

**Response** (if successful):
```json
{
  "message": "File processed successfully. Please review the extracted questions.",
  "questions": [
    {
      "text": "The question text here...",
      "options": {
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
      },
      "correct_option": "A"
    },
    ...
  ]
}
```

**Notes**:
- The uploaded PDF file must contain the questions in a recognizable format.
- If no questions are extracted, an error message will be returned.
- The extracted questions will be available for review and potential editing.

---

### 2. **Confirm and Save Questions**
**Endpoint**: `/admin-api/confirm-questions/`

**Method**: `POST`

**Description**: After reviewing and editing the questions, administrators can submit the validated questions to be saved into the database.

**Request**:
```bash
curl -X POST "http://127.0.0.1:8000/admin-api/confirm-questions/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Token YOUR_AUTH_TOKEN" \
     -d '{
           "questions": [
               {"text": "Question 1", "options": {"A": "Option A", "B": "Option B"}, "correct_option": "A"},
               {"text": "Question 2", "options": {"A": "Option A", "B": "Option B"}, "correct_option": "B"}
           ],
           "exam_type": "waec",
           "course_id": 1
         }'
```

**Response** (if successful):
```json
{
  "message": "Questions saved successfully.",
  "created_questions": ["Question 1", "Question 2"]
}
```

**Notes**:
- This endpoint will save the reviewed questions into the database.
- The questions data must be in the correct format, including the question text, options, and the correct option.



### 5. **Retrieve Questions by Course and Exam Type**
**Endpoint**: `/user-api/questions/`

**Method**: `GET`

**Description**: This endpoint retrieves a list of questions based on the provided `course_id` and `exam_type`. It returns the questions along with their options for the user to view.

**Request**:
```bash
curl -X GET "http://127.0.0.1:8000/user-api/questions/?course_id=1&exam_type=waec"
```

**Response** (if successful):
```json
[
  {
    "id": 1,
    "text": "What is 2 + 2?",
    "options": {
      "A": "4",
      "B": "5",
      "C": "3",
      "D": "6"
    }
  },
  {
    "id": 2,
    "text": "What is the capital of France?",
    "options": {
      "A": "Berlin",
      "B": "Madrid",
      "C": "Paris",
      "D": "Rome"
    }
  }
]
```

**Notes**:
- The `course_id` and `exam_type` query parameters are required.
- If no questions are found for the provided parameters, a 404 error is returned.

---

### 6. **Submit Answers for Review**
**Endpoint**: `/user-api/submit/`

**Method**: `POST`

**Description**: This endpoint allows users to submit their answers to the questions. It validates the answers and returns whether the chosen options are correct.

**Request**:
```bash
curl -X POST "http://127.0.0.1:8000/user-api/submit/" \
     -H "Content-Type: application/json" \
     -d '{
           "submissions": [
               {
                   "question_id": 1,
                   "chosen_option": "A"
               },
               {
                   "question_id": 2,
                   "chosen_option": "C"
               }
           ]
         }'
```

**Response** (if successful):
```json
{
  "results": [
    {
      "question_id": 1,
      "chosen_option": "A",
      "correct": true
    },
    {
      "question_id": 2,
      "chosen_option": "C",
      "correct": true
    }
  ]
}
```



---

## Installation

To run the **ExamOnline** project locally, follow these steps:

### Prerequisites

- Python 3.8+
- Django 3.x
- SQLite (default database)
- Dependencies from `requirements.txt`

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/examonline.git
    cd examonline && cd ExamOnlineAPI
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

4. Run the development server:
    ```bash
    python manage.py runserver
    ```

5. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Dependencies

- **Django**: Web framework for building the API.
- **Django REST Framework**: For building RESTful APIs.
- **django-rest-framework-authtoken**: Token-based authentication for the API.
- **PDFPlumber**: PDF parsing for question extraction.

---

## Database Schema

### `admin_api_question`

- **text**: Text of the question (string).
- **options**: A dictionary containing the options for the question (e.g., `A`, `B`, `C`, `D`).
- **correct_option**: The correct answer for the question.
- **exam_type**: Type of exam (e.g., WAEC, JAMB).
- **course_id**: ID of the course to which the question belongs.

---

## Future Enhancements

- **User Interface**: Develop a web-based interface for administrators to upload, review, and save questions with ease.

---
