import boto3
from langchain.vectorstores import Chroma
from langchain.embeddings import BedrockEmbeddings
from langchain.llms import Bedrock
from langchain.chains import RetrievalQA

class RAGEngine:
    def __init__(self, s3_loader, bucket_name):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.documents = s3_loader.load_documents_from_s3()
        
        # Embeddings com titan v1
        self.embeddings = BedrockEmbeddings(
            client=self.bedrock_client,
            model_id="amazon.titan-embed-text-v1"
        )
        
        # index com Chroma
        self.vectorstore = Chroma.from_documents(
            self.documents, 
            self.embeddings
        )
        
        # llm tbm do titan
        self.llm = Bedrock(
            client=self.bedrock_client,
            model_id="amazon.titan-text-express-v1"
        )
        
        # configuracao do RetrievalQA (piada: é o fruto proibido pra llm)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever()
        )
    
    def query(self, pergunta: str) -> str:
        """Executa consulta nos docs"""
        resposta = self.qa_chain.run(pergunta)
        return resposta