from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('history/', views.history, name='history'),
    path('datasets/<int:pk>/report.pdf', views.dataset_report_pdf, name='dataset_report_pdf'),
]
