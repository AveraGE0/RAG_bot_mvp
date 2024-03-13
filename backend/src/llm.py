from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from backend.src.config import LLM_MODEL_NAME, DEVICE, MAX_NEW_TOKENS
import logging
import torch

logger = logging.getLogger(__name__)


class LLM():
    def __init__(self, chat_template: dict) -> None:
        logger.info(f"loading model {LLM_MODEL_NAME}")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            #device_map="auto",
            quantization_config=bnb_config
        )
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
        self.READER_LLM = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text-generation",
            do_sample=True,
            temperature=0.2,
            repetition_penalty=1.1,
            return_full_text=False,
            max_new_tokens=500,
        )
        
        self.prompt_template = self.tokenizer.apply_chat_template(
            chat_template, tokenize=False, add_generation_prompt=True
        )

    def prompt_model(self, query: str, context: str, sources: str) -> str:
        """model_inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(DEVICE)
        attention_mask = model_inputs.attention_mask if "attention_mask" in model_inputs else None
        self.model.to(DEVICE)
        generated_ids = self.model.generate(model_inputs, attention_mask=attention_mask, max_new_tokens=MAX_NEW_TOKENS)
        out = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return out"""
        final_prompt = self.prompt_template.format(question=query, context=context, sources=sources)
        return self.READER_LLM(final_prompt)[0]["generated_text"]