from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('chat/<int:doc_id>/', views.chat_with_pdf, name='chat_with_pdf'),
    path('api/chat/', views.chat_api, name='chat_api'),
]