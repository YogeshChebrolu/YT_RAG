from yt_rag.vector_store.fastembed_model import EmbedModels
import logging
import os
logger = logging.getLogger(__name__)

image_embeddings=EmbedModels.Image_Embedding_model

text_embeddings=EmbedModels.Text_Embedding_model

def list_folder_contents_os_walk(start_path):
    total_files=[]
    for root, dirs, files in os.walk(start_path):
        if dirs:
          for dir in dirs:
            for file in files:
              file_path=root+"/"+dir+"/"+file
              total_files.append(file_path)
        else:
          for file in files:
            file_path=root+"/"+file
            total_files.append(file_path)
           
    return total_files


def create_image_embeddings(images):
  embeddings = list(image_embeddings.embed(images))
  logger.info(f"Image to embeddings completed")
  return embeddings

def create_text_embeddings(query):
  embeddings=list(text_embeddings.embed([query]))
  return embeddings[0]

def create_text_embeddings_batch(texts):
  """Create embeddings for multiple texts at once for better performance"""
  embeddings = list(text_embeddings.embed(texts))
  return embeddings

def create_embeddings_from_folder(folder):
  files=list_folder_contents_os_walk(folder)
  embeddings=create_image_embeddings(files)
  return embeddings