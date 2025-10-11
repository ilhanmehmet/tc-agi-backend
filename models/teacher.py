from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Teacher:
    def __init__(self, model_name="facebook/opt-350m"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.model.eval()

    def generate(self, prompt: str, max_length: int = 512):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        # Modelin çalıştığı cihaza tensörleri taşı
        inputs = {key: value.to(self.model.device) for key, value in inputs.items()}
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def distill_to(self, student, prompt: str):
        # Öğrenciye soft-labels veya prompt + yanıt ver
        response = self.generate(prompt)
        student.learn_from_teacher(prompt, response)
        return response
