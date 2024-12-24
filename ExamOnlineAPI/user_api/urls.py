from django.urls import path
from .views import QuestionListView, SubmitAnswersView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('submit/', SubmitAnswersView.as_view(), name='submit-answers'),
]