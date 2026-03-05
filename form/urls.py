from django.urls import path
from .views import *
urlpatterns = [
    path('responses/',                 AllResponsesView.as_view()),
    path('response/save/',             SaveResponseView.as_view()),
    path('response/<str:metric_id>/',  SingleResponseView.as_view()),

    path('document/upload/',           DocumentUploadView.as_view()),
    path('documents/<str:metric_id>/', DocumentListView.as_view()),
    path('document/<int:doc_id>/',     DocumentDeleteView.as_view()),

    path('settings/',                  InstitutionSettingsView.as_view()),

    path('completion/',                CompletionStatusView.as_view()),
]
