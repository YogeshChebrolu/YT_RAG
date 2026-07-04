from google.genai import types
import requests
def extractimagename(retrieved_frames_metadata):  
  file_name=[]
  for item in retrieved_frames_metadata:
    absolute_image_path=item['image_path']
    absolute_image_path=absolute_image_path.replace("\\","/")
    parts = absolute_image_path.split('/')
    desired_parts = parts[-2:]
    extracted_path = '/'.join(desired_parts)
    file_name.append(extracted_path)
  return file_name[:2]

def extractchunk(retrieved_transcript_metadata):
  chunks=[]
  for item in retrieved_transcript_metadata:
    chunks.append(item['page_content'])
  return chunks[:3]

def image2bytes_converter(paths):
  encoded_images=[]
  for image in paths:
    with open(image, 'rb') as f:
        image_bytes = f.read()

    image_encoded = types.Part.from_bytes(
        data=image_bytes, mime_type="image/jpeg"
    )
    encoded_images.append(image_encoded)
  return encoded_images

def online_image_to_bytes(image_url=[]):
  images=[]
  for url in image_url:
    image_bytes = requests.get(url).content
    image = types.Part.from_bytes(
    data=image_bytes, mime_type="image/jpeg"
  )
    images.append(image)
  return images
  
