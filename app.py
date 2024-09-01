import os
import requests
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain.schema import Document
from typing import List, Optional

# Defina a variável de ambiente USER_AGENT
os.environ["USER_AGENT"] = "MyUserAgent/1.0"

# Carrega as variáveis do arquivo .env
load_dotenv()

# Verifique se a chave foi carregada
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("A chave de API da OpenAI não foi encontrada. Defina a variável de ambiente `OPENAI_API_KEY`.")

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Configurando o logging para monitoramento detalhado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RAGSystem:
    def __init__(self, document_source: str, model_name: str = "gpt-3.5-turbo", chunk_size: int = 1000, chunk_overlap: int = 200):
        self.document_source = document_source
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_store = None
        self.qa_chain = None
        self.retriever = None

        # Obtenha a chave de API da OpenAI do ambiente
        self.openai_api_key = openai_api_key
        self.timeout = 10  # Timeout para requisições à API

    def load_content(self) -> str:
        """
        Carrega o conteúdo do documento.
        """
        try:
            logging.info(f"Carregando conteúdo do documento: {self.document_source}")
            response = requests.get(self.document_source, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao carregar conteúdo do documento: {e}")
            raise

    def split_document(self, content: str) -> List[Document]:
        """
        Divide o conteúdo em chunks para facilitar a criação da Vector Store.
        """
        logging.info("Dividindo o documento em chunks.")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = text_splitter.split_text(content)
        return [Document(page_content=chunk) for chunk in chunks]

    def create_vector_store(self, docs: List[Document]):
        """
        Cria a Vector Store com os embeddings dos chunks.
        """
        logging.info("Criando a Vector Store com embeddings.")
        embedding_model = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.vector_store = FAISS.from_documents(docs, embedding_model)
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    def setup_qa_chain(self):
        """
        Configura o QA Chain com o modelo de linguagem e o retriever.
        """
        logging.info("Configurando o QA Chain.")
        llm_model = ChatOpenAI(model=self.model_name, openai_api_key=self.openai_api_key)
        self.qa_chain = RetrievalQA.from_chain_type(llm=llm_model, retriever=self.retriever)

    def generate_answer(self, question: str) -> str:
        """
        Gera uma resposta baseada em uma pergunta e no conteúdo do documento.
        """
        try:
            logging.info(f"Gerando resposta para a pergunta: {question}")
            
            # Verifica se a pergunta já está no cache
            cache_key = f"cache_{question}"
            if cache_key in session:
                logging.info("Resposta carregada do cache.")
                return session[cache_key]

            # Gerar resposta usando o sistema
            response = self.qa_chain.invoke({"query": question})
            
            # Extraindo apenas o resultado da resposta
            result = response.get("result", "Desculpe, ocorreu um erro ao gerar a resposta.")
            logging.info(f"Resposta gerada: {result}")

            # Salva a resposta no cache
            session[cache_key] = result
            session.modified = True
            
            return result
        except Exception as e:
            logging.error(f"Erro ao gerar a resposta: {e}")
            return "Desculpe, ocorreu um erro ao gerar a resposta."

    def run(self, question: str) -> Optional[str]:
        """
        Executa o pipeline completo do sistema RAG.
        """
        try:
            # Carregar conteúdo do documento
            content = self.load_content()

            # Dividir o documento em chunks
            docs = self.split_document(content)

            # Criar Vector Store
            self.create_vector_store(docs)

            # Configurar QA Chain
            self.setup_qa_chain()

            # Gerar resposta
            return self.generate_answer(question)
        except Exception as e:
            logging.error(f"Erro na execução do pipeline RAG: {e}")
            return None

# Instância do sistema RAG
document_source = "https://pt.wikipedia.org/wiki/Twitter"
rag_system = RAGSystem(document_source)

@app.route("/", methods=["GET", "POST"])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == "POST":
        question = request.form["question"]
        answer = rag_system.run(question)

        # Adicionando a pergunta e resposta ao histórico
        session['chat_history'].append({'user': True, 'text': question})
        session['chat_history'].append({'user': False, 'text': answer})
        session.modified = True

    return render_template("index.html", chat_history=session['chat_history'])

if __name__ == "__main__":
    rag_system.run("")  # Carrega o conteúdo do documento e configura o sistema
    app.run(debug=True)
