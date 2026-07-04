from fastembed import ImageEmbedding, TextEmbedding

image_model = ImageEmbedding("Qdrant/clip-ViT-B-32-vision")
text_model = TextEmbedding(model_name="Qdrant/clip-ViT-B-32-text")

class EmbedModels:
  Image_Embedding_model=image_model
  Text_Embedding_model=text_model
  