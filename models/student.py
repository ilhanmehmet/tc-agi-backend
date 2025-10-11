from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Student:
    def __init__(self, model_name="facebook/opt-350m"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16
        )
        self.model.train()

    def learn_from_teacher(self, prompt: str, response: str):
        # Burada distillation işlemi yapılacak
        inputs = self.tokenizer(prompt + response, return_tensors="pt")
        # Modelin çalıştığı cihaza tensörleri taşı
        inputs = {key: value.to(self.model.device) for key, value in inputs.items()}
        outputs = self.model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        loss.backward()
        # Burada modelin bir adım güncellenmesi gerekir
        # Basit bir örnek için sadece loss hesaplıyoruz
        print(f"Student loss: {loss.item()}")
        return loss.item()

    def generate(self, prompt: str, max_length: int = 256):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        # Modelin çalıştığı cihaza tensörleri taşı
        inputs = {key: value.to(self.model.device) for key, value in inputs.items()}
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
