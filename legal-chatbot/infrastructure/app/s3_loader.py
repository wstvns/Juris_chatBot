import boto3
import os
from typing import List
from langchain.schema import Document
import mimetypes

class S3DocumentLoader:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_documents(self, local_directory: str):
        """Faz o upload dos arquivos de um diretório local para o S3"""
        for root, _, files in os.walk(local_directory):
            for file in files:
                file_path = os.path.join(root, file)
                s3_key = os.path.relpath(file_path, local_directory)
                try:
                    self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
                    print(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_key}")
                except Exception as e:
                    print(f"Erro ao fazer upload de {file_path}: {e}")

    def load_documents_from_s3(self) -> List[Document]:
        """Carrega documentos do bucket S3 e retorna uma lista de Documentos"""
        documents = []
        continuation_token = None

        while True:
            # Chama list_objects_v2 com paginação
            list_args = {'Bucket': self.bucket_name}
            if continuation_token:
                list_args['ContinuationToken'] = continuation_token

            response = self.s3_client.list_objects_v2(**list_args)

            if 'Contents' in response:
                for obj in response['Contents']:
                    s3_key = obj['Key']
                    try:
                        # aqui vai verificar se é txt
                        mime_type, _ = mimetypes.guess_type(s3_key)
                        if mime_type and mime_type.startswith('text'):
                            obj_data = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
                            try:
                                # teanta decodificar com UTF-8
                                content = obj_data['Body'].read().decode('utf-8')
                            except UnicodeDecodeError:
                                # caso falhe dá try com ISO-8859-1. olhem de onde tirei https://stackoverflow.com/questions/1893946/iso-8859-1-vs-utf-8
                                content = obj_data['Body'].read().decode('ISO-8859-1')
                            document = Document(page_content=content, metadata={"s3_key": s3_key})
                            documents.append(document)
                        else:
                            print(f"O arquivo {s3_key} não é um arquivo de texto.")
                    except Exception as e:
                        print(f"Erro ao processar o arquivo {s3_key}: {e}")

            # verifica se tem continuacao na proxima page
            continuation_token = response.get('NextContinuationToken')
            if not continuation_token:
                break

        return documents


'''
import boto3
import os
from typing import List
from langchain.schema import Document  # Certifique-se de que está instalado no ambiente

class S3DocumentLoader:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_documents(self, local_directory: str):
        for root, _, files in os.walk(local_directory):
            for file in files:
                file_path = os.path.join(root, file)
                s3_key = os.path.relpath(file_path, local_directory)
                self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
                print(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_key}")

    def load_documents_from_s3(self) -> List[Document]:
        documents = []
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)

        if 'Contents' in response:
            for obj in response['Contents']:
                s3_key = obj['Key']
                obj_data = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
                content = obj_data['Body'].read().decode('utf-8')
                document = Document(page_content=content, metadata={"s3_key": s3_key})
                documents.append(document)

        return documents
'''