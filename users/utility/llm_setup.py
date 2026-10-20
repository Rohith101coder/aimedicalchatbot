# users/utility/llm_setup.py

from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dotenv import load_dotenv
import os
import torch

load_dotenv()

class LLMInitializer:
    def __init__(self):
        # Use HF Transformers model (NOT GGML)
        self.model_name = os.getenv(
            "MODEL_NAME",
            "microsoft/phi-2"
        )
        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-mpnet-base-v2"
        )

    def initialize_llm(self):
        print(f"Loading HF model: {self.model_name}")

        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )

        text_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=600,
            temperature=0.8,
            top_k=50,
            do_sample=True,
        )

        return HuggingFacePipeline(pipeline=text_pipeline)

    def initialize_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )
