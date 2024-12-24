from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from admin_api.models import Question


class QuestionListView(APIView):
    """Retrieve all questions based on course_id and exam_type"""

    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get('course_id')
        exam_type = request.query_params.get('exam_type')

        if not course_id or not exam_type:
            return Response({'error': 'course_id and exam_type fileds are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
        questions = Question.objects.filter(course_id=course_id, exam_type=exam_type)
        if not questions.exists():
            return Response({'error': f'No questions found for the given {course_id} and {exam_type}'}, status=status.HTTP_404_NOT_FOUND)
        
        data = [
            {
                'id': question.id,
                'text': question.text,
                'options': question.options,
            } for question in questions
        ]
        return Response(data, status=status.HTTP_200_OK)
    


class SubmitAnswersView(APIView):
    """Confirm user's answers."""

    def post(self, request, *args, **kwargs):
        submissions = request.data.get('submissions')

        if not submissions or not isinstance(submissions, list):
            return Response({'error': 'Invalid submission format'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        for submission in submissions:
            question_id = submission.get('question_id')
            chosen_option = submission.get('chosen_option')

            if not question_id or not chosen_option:
                return Response({'error': 'Each submision must include the question_id and chosen_option'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                question = Question.objects.get(id=question_id)
                is_correct = question.correct_option == chosen_option
                results.append({
                    'question_id': question_id,
                    'chosen_option': chosen_option,
                    'correct': is_correct
                })
            except Question.DoesNotExist:
                return Response({'error': f'Question with id {question_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'results': results}, status=status.HTTP_200_OK)

