from django.urls import path
from .views import CSVUploadAPIView

urlpatterns = [
    path('upload-csv/', CSVUploadAPIView.as_view(), name='upload-csv'),
]