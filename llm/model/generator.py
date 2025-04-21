# generator.py

# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM

# class Generator:
#     def __init__(self, model_name: str = "kakaocorp/KoGPT", device: str = None, max_new_tokens: int = 512):
#         self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
#         self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(self.device)
#         self.model.eval()
#         self.max_new_tokens = max_new_tokens

#     def generate(self, prompt: str) -> str:
#         inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
#         with torch.no_grad():
#             output = self.model.generate(
#                 **inputs,
#                 max_new_tokens=self.max_new_tokens,
#                 pad_token_id=self.tokenizer.eos_token_id,
#                 do_sample=False,
#                 top_k=50,
#                 top_p=0.95
#             )
#         result = self.tokenizer.decode(output[0], skip_special_tokens=True)

#         # [답변] 이후 텍스트만 추출
#         if "[답변]" in result:
#             return result.split("[답변]")[-1].strip()
#         print("답변내용:",result.strip())
#         return result.strip()

import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM


def remove_duplicate_sentences(text: str) -> str:
    seen = set()
    result = []
    for sentence in re.split(r'(?<=[.!?])\s+', text):
        clean = sentence.strip()
        if clean and clean not in seen:
            result.append(clean)
            seen.add(clean)
    return " ".join(result)

def trim_incomplete_last_sentence(text: str) -> str:
    if not text.endswith(('.', '!', '?')):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return ' '.join(sentences[:-1])
    return text


class Generator:
    def __init__(self, model_name: str = "kakaocorp/KoGPT", device: str = None, max_new_tokens: int = 512):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(self.device)
        self.model.eval()
        self.max_new_tokens = max_new_tokens

    def _clean_repetitions(self, text: str) -> str:
        text = re.sub(r'(\[[^\[\]]+\])(\s*\1){2,}', r'\1', text)
        text = re.sub(r'(\[[^\[\]]{2,8}\]){3,}', '', text)
        return text.strip()

    def _format_numbered_list(self, text: str) -> str:
        text = re.sub(r'(?<!\n)(\d+)\.\s*', r'\n\1. ', text)
        return re.sub(r'\n{2,}', '\n', text).strip()

    def _renumber_list_items(self, text: str) -> str:
        lines = re.split(r'(?<=\n)|(?=\d+\.)', text)
        new_lines, count = [], 1
        for line in lines:
            if re.match(r'^\d+\.', line.strip()):
                new_lines.append(f"{count}. {line.strip()[2:].strip()}")
                count += 1
            else:
                new_lines.append(line.strip())
        return "\n".join(filter(None, new_lines))

    def generate(self, document_text: str, use_numbering: bool = False) -> str:
        prompt = (
            "[문서 시작]\n"
            + document_text +
            "\n[문서 끝]\n\n"
            "문서 내용을 바탕으로 핵심을 간결하게 정리해줘. 매 문장마다 번호 사용을 지양해줘."
            "중복 없이 10문장 미만으로 정리해줘. "
            "친절한 상담사 말투로 변환해서 정리해줘.\n[답변]"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(self.device)
        input_length = inputs['input_ids'].shape[1]

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                # top_k=3,
                top_p=1,
                temperature=0.7,
                early_stopping=True
            )

        # 생성된 토큰에서 입력 길이 이후만 디코딩
        generated_tokens = output[0][input_length:]
        answer = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

        # '[답변]' 이후만 추출
        # 후처리
        if use_numbering:
            answer = self._format_numbered_list(answer)
            answer = self._renumber_list_items(answer)

        answer = self._clean_repetitions(answer)
        answer = remove_duplicate_sentences(answer)
        answer = trim_incomplete_last_sentence(answer)

        return answer

