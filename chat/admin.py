# chat/admin.py
from django.contrib import admin
from .models import PDFDocument, ChatMessage

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'processed']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['title']
    readonly_fields = ['uploaded_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['document', 'question', 'timestamp']
    list_filter = ['timestamp', 'document']
    search_fields = ['question', 'answer']
    readonly_fields = ['timestamp']