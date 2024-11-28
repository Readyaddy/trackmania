import transformers

print(transformers.__version__)

import requests
from PIL import Image
from transformers import (
  LlavaForConditionalGeneration,
  AutoTokenizer,
  CLIPImageProcessor
)
from processing_llavagemma import LlavaGemmaProcessor

checkpoint = "Intel/llava-gemma-2b"

model = LlavaForConditionalGeneration.from_pretrained(checkpoint)
processor = LlavaGemmaProcessor(
    tokenizer=AutoTokenizer.from_pretrained(checkpoint),
    image_processor=CLIPImageProcessor.from_pretrained(checkpoint),
)

model.to('cuda')


prompt = processor.tokenizer.apply_chat_template(
    [{'role': 'user', 'content': "What's the content of the image?<image>"}],
    tokenize=False,
    add_generation_prompt=True
)
url = "https://www.ilankelman.org/stopsigns/australia.jpg"
image = Image.open(requests.get(url, stream=True).raw)
inputs = processor(text=prompt, images=image, return_tensors="pt")
inputs = {k: v.to('cuda') for k, v in inputs.items()}
      
# Generate
generate_ids = model.generate(**inputs, max_length=30)
output = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(output)