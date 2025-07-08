import os
import tempfile
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import Document
from django.conf import settings

class PDFChatService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama3-8b-8192",
            temperature=0.1
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vectorstores = {}
        self.chat_histories = {}
    
    def get_session_history(self, document_id: int) -> BaseChatMessageHistory:
        """Get or create chat history for a document"""
        if document_id not in self.chat_histories:
            self.chat_histories[document_id] = ChatMessageHistory()
        return self.chat_histories[document_id]
    
    def process_pdf(self, document):
        """Process PDF document and create vector store"""
        try:
            # Load PDF
            loader = PyPDFLoader(document.file.path)
            pages = loader.load()
            
            # Split text
            texts = self.text_splitter.split_documents(pages)
            
            # Create vector store
            vectorstore = FAISS.from_documents(texts, self.embeddings)
            
            # Store in memory (in production, use persistent storage)
            self.vectorstores[document.id] = vectorstore
            
            return True
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            raise e
    
    def chat_with_pdf(self, document, question: str) -> str:
        """Chat with the PDF document using updated LangChain approach"""
        try:
            # Get or create vector store
            if document.id not in self.vectorstores:
                self.process_pdf(document)
            
            vectorstore = self.vectorstores[document.id]
            
            # Create retriever
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            # Get chat history
            chat_history = self.get_session_history(document.id)
            
            # Create conversation chain with updated approach
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                return_source_documents=True,
                verbose=False
            )
            
            # Convert chat history to the format expected by the chain
            history_messages = []
            messages = chat_history.messages
            
            # Group messages into question-answer pairs
            for i in range(0, len(messages), 2):
                if i + 1 < len(messages):
                    history_messages.append((messages[i].content, messages[i + 1].content))
            
            # Get answer
            result = qa_chain({
                "question": question,
                "chat_history": history_messages
            })
            
            # Add to chat history
            chat_history.add_user_message(question)
            chat_history.add_ai_message(result["answer"])
            
            return result["answer"]
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"