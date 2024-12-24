from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Question
from .utils import extract_data_from_pdf  
import logging


logger = logging.getLogger(__name__)


class UploadPDFView(APIView):
    """
    Upload a list of questions from a PDF file.
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            pdf_file = request.FILES.get('file')
            exam_type = request.data.get('exam_type')
            course_id = request.data.get('course_id')

            if not pdf_file:
                return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

            if not pdf_file.name.endswith('.pdf'):
                return Response({'error': 'Invalid file format. Only PDF is allowed'}, status=status.HTTP_400_BAD_REQUEST)

            file_path = f'/tmp/{pdf_file.name}'
            with open(file_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            try:
                questions_data = extract_data_from_pdf(file_path)
            except Exception as e:
                logger.error(f"Error extracting data from PDF: {str(e)}") 
                return Response({'error': f'Error extracting data from PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Ensure no empty questions_data causes success response
            if not questions_data:
                logger.warning("No questions extracted from PDF.")
                return Response({'error': 'No questions found in PDF'}, status=status.HTTP_400_BAD_REQUEST)


            created_questions = []
            # Proceed to save valid questions
            for question_data in questions_data:
                try:
                    existing_question = Question.objects.filter(text=question_data['text'], exam_type=exam_type).first()

                    if existing_question:
                        print(f"Question already exists: {question_data['text']}")
                        continue

                    Question.objects.create(
                        text=question_data['text'],
                        options=question_data['options'],
                        correct_option=question_data['correct_option'],
                        course_id=course_id,
                        exam_type=exam_type, 
                    )

                except Exception as e:
                    print(f"Error saving question: {question_data['text']}. Error: {str(e)}")
                    logger.error(f"Error saving question: {question_data['text']}. Error: {str(e)}")
                    continue

            response_data = {
                "message": "File processed successfully and saved.",
                "created_questions": created_questions,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}") 
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionListView(APIView):
    """
    Retrieve list of questions and create a new question.
    """
    def get(self, request, *args, **kwargs):
        try:
            questions = Question.objects.all()
            data = [
                {
                    'id': q.id,
                    'text': q.text,
                    'options': q.options,
                    'correct_option': q.correct_option,
                    'course_id': q.course_id,
                    'exam_type': q.exam_type,
                }
                for q in questions
            ]
            return Response({'questions': data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching questions: {str(e)}")
            return Response({'error': 'Error fetching questions'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            text = request.data.get('text')
            options = request.data.get('options')
            correct_option = request.data.get('correct_option')
            course_id = request.data.get('course_id')
            exam_type = request.data.get('exam_type')

            if not all([text, options, correct_option, course_id, exam_type]):
                return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            question = Question.objects.create(
                text=text,
                options=options,
                correct_option=correct_option,
                course_id=course_id,
                exam_type=exam_type
            )
            return Response({
                'id': question.id,
                'text': question.text,
                'options': question.options,
                'correct_option': question.correct_option,
                'course_id': question.course_id,
                'exam_type': question.exam_type,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating question: {str(e)}")
            return Response({'error': 'Error creating question'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionDetailView(APIView):
    """
    Retrieve, update, or delete a question instance.
    """
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        try:
            question = self.get_object(pk)
            if not question:
                return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'id': question.id,
                'text': question.text,
                'options': question.options,
                'correct_option': question.correct_option,
                'course_id': question.course_id,
                'exam_type': question.exam_type,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving question: {str(e)}")
            return Response({'error': 'Error retrieving question'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, *args, **kwargs):
        try:
            question = self.get_object(pk)
            if not question:
                return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

            text = request.data.get('text', question.text)
            options = request.data.get('options', question.options)
            correct_option = request.data.get('correct_option', question.correct_option)
            course_id = request.data.get('course_id', question.course_id)
            exam_type = request.data.get('exam_type', question.exam_type)

            question.text = text
            question.options = options
            question.correct_option = correct_option
            question.course_id = course_id
            question.exam_type = exam_type
            question.save()

            return Response({
                'id': question.id,
                'text': question.text,
                'options': question.options,
                'correct_option': question.correct_option,
                'course_id': question.course_id,
                'exam_type': question.exam_type,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating question: {str(e)}")
            return Response({'error': 'Error updating question'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, *args, **kwargs):
        try:
            question = self.get_object(pk)
            if not question:
                return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

            question.delete()
            return Response({'message': 'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting question: {str(e)}")
            return Response({'error': 'Error deleting question'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)