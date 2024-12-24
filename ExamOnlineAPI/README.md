
# Admin API for Question Management

This project is a Django REST framework (DRF) application that provides an API to manage exam questions, including uploading questions via PDF and performing CRUD operations.

## Features

- **Upload PDF**: Extract questions from a PDF file and save them to the database.
- **CRUD Operations**: Create, Read, Update, and Delete exam questions via the API.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/entuziaz/ExamOnline.git
   cd ExamOnlineAPI

   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Endpoints

### 1. **Upload PDF**
   - **URL**: `/admin-api/upload-pdf/`
   - **Method**: `POST`
   - **Payload**:
     ```json
     {
       "file": "PDF file (multipart/form-data)",
       "exam_type": "String",
       "course_id": "Integer"
     }
     ```

### 2. **CRUD Operations for Questions**
   - **Create**: `POST /admin-api/questions/`
   - **Read**: `GET /admin-api/questions/`
   - **Update**: `PUT /admin-api/questions/{id}/`
   - **Delete**: `DELETE /admin-api/questions/{id}/`

## Running Tests

1. Install test dependencies:
   ```bash
   pip install pytest pytest-django
   ```

2. Run the tests:
   ```bash
   pytest
   ```

## Project Structure

```plaintext
admin_api/
├── models.py         # Database models
├── views.py          # API views
├── serializers.py    # DRF serializers
├── utils.py          # Utility functions (e.g., PDF processing)
├── tests/            # Test cases
└── ...
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```
