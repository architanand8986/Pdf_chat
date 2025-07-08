# Django PDF Chat Application

A powerful Django web application that allows users to upload PDF documents and chat with them using AI. Built with LangChain, Groq, and HuggingFace for intelligent document processing and conversation.

## 🚀 Features

- **PDF Upload & Processing**: Upload PDF documents and extract text content
- **AI-Powered Chat**: Chat with your documents using Groq's Mixtral LLM
- **Vector Search**: Efficient document retrieval using FAISS and HuggingFace embeddings
- **Conversation Memory**: Maintains chat history for contextual responses
- **Responsive UI**: Clean Bootstrap 5 interface with real-time chat
- **Document Management**: View all uploaded documents and their processing status
- **RAG Implementation**: Retrieval-Augmented Generation for accurate responses

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **AI/ML**: 
  - LangChain & LangChain-Community
  - Groq API (Mixtral-8x7b-32768)
  - HuggingFace Embeddings (sentence-transformers)
  - FAISS Vector Database
- **Frontend**: Bootstrap 5, JavaScript (ES6+)
- **Database**: SQLite (easily configurable to PostgreSQL/MySQL)
- **File Processing**: PyPDF2

## 📋 Prerequisites

- Python 3.8+
- Groq API Key (get from [Groq Console](https://console.groq.com/))
- Git

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pdf-chat-django
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```
pdf_chat/
├── manage.py
├── requirements.txt
├── .env
├── README.md
├── pdf_chat/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── chat/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   └── migrations/
├── templates/
│   ├── base.html
│   └── chat/
│       ├── index.html
│       └── chat.html
├── media/
│   └── pdfs/
└── static/
```

## 🎯 Usage

### 1. Upload PDF Documents
- Navigate to the home page
- Enter a title for your document
- Select a PDF file (max size configurable)
- Click "Upload & Process"

### 2. Chat with Documents
- Once processing is complete, click "Chat" on any document
- Ask questions about the document content
- Get AI-powered responses based on the document

### 3. View Chat History
- All conversations are saved and displayed
- Previous questions and answers are shown when you return to a chat

## 🔧 Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
DEBUG=True
SECRET_KEY=your_secret_key_here
```

### Model Configuration
In `chat/services.py`, you can modify:
- **LLM Model**: Change `model_name` in ChatGroq initialization
- **Embedding Model**: Modify `model_name` in HuggingFaceEmbeddings
- **Chunk Size**: Adjust `chunk_size` and `chunk_overlap` in text splitter
- **Memory Window**: Change `k` value in ConversationBufferWindowMemory

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with document list |
| POST | `/upload/` | Upload PDF document |
| GET | `/chat/<doc_id>/` | Chat interface for document |
| POST | `/api/chat/` | Chat API endpoint |

## 🔒 Security Features

- CSRF protection enabled
- File type validation (PDF only)
- Input sanitization
- Error handling and logging

## 🚀 Production Deployment

### Database Configuration
Replace SQLite with PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pdf_chat_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files
```bash
python manage.py collectstatic
```

### Environment Variables
Set in production:
```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 🛡️ Troubleshooting

### Common Issues

1. **Groq API Key Error**
   - Ensure your API key is correctly set in `.env`
   - Check if your API key has sufficient credits

2. **PDF Processing Fails**
   - Verify the PDF is not corrupted
   - Check if the PDF has extractable text (not just images)

3. **Memory Issues**
   - For large PDFs, consider reducing chunk size
   - Implement persistent vector storage for production

4. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the AI framework
- [Groq](https://groq.com/) for the LLM API
- [HuggingFace](https://huggingface.co/) for embeddings
- [Bootstrap](https://getbootstrap.com/) for UI components

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Multiple file format support (DOCX, TXT, etc.)
- [ ] Persistent vector storage with ChromaDB/Pinecone
- [ ] Multi-language support
- [ ] Advanced chat features (file attachments, citations)
- [ ] Docker containerization
- [ ] REST API for external integrations
- [ ] Real-time collaboration features

---

**Made with ❤️ using Django, LangChain, and Groq**
