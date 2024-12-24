from django.urls import path
from .views import UploadPDFView, QuestionListView, QuestionDetailView

urlpatterns = [
    path('upload-pdf/', UploadPDFView.as_view(), name='upload-pdf'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]
