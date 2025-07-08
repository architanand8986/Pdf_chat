import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from .models import PDFDocument, ChatMessage
from .services import PDFChatService

def index(request):
    documents = PDFDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'chat/index.html', {'documents': documents})

def upload_pdf(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        
        if title and file:
            # Check if file is PDF
            if not file.name.lower().endswith('.pdf'):
                messages.error(request, 'Please upload a PDF file.')
                return redirect('chat:index')
            
            # Save the document
            doc = PDFDocument.objects.create(title=title, file=file)
            
            # Process the PDF
            try:
                chat_service = PDFChatService()
                chat_service.process_pdf(doc)
                doc.processed = True
                doc.save()
                messages.success(request, 'PDF uploaded and processed successfully!')
            except Exception as e:
                messages.error(request, f'Error processing PDF: {str(e)}')
            
            return redirect('chat:index')
    
    return redirect('chat:index')

def chat_with_pdf(request, doc_id):
    document = get_object_or_404(PDFDocument, id=doc_id)
    chat_messages = ChatMessage.objects.filter(document=document).order_by('timestamp')
    return render(request, 'chat/chat.html', {
        'document': document,
        'messages': chat_messages  # Fixed variable name conflict
    })

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            doc_id = data.get('doc_id')
            question = data.get('question')
            
            document = get_object_or_404(PDFDocument, id=doc_id)
            
            if not document.processed:
                return JsonResponse({'error': 'Document not yet processed'}, status=400)
            
            # Get chat service and process question
            chat_service = PDFChatService()
            answer = chat_service.chat_with_pdf(document, question)
            
            # Save the conversation
            ChatMessage.objects.create(
                document=document,
                question=question,
                answer=answer
            )
            
            return JsonResponse({
                'answer': answer,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)