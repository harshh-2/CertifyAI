import json
import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = Path(__file__).parent.parent / "domain_skill (1).json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    DATA = json.load(f)


class CertifyAIChatbot:
    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.texts = []
        for d in DATA:
            block = f"Domain: {d['domain']}\n"
            for c in d["certifications"]:
                block += f"{c['name']} by {c['provider']}\n"
            self.texts.append(block)

        embeddings = self.model.encode(self.texts)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype("float32"))

        self.history = []

    def reply(self, question):

        q_emb = self.model.encode([question]).astype("float32")
        _, idx = self.index.search(q_emb, 1)

        context = self.texts[idx[0][0]]

        prompt = f"""
You are CertifyAI, a student career assistant.

Use this info:
{context}

Conversation:
{self.history}

User: {question}
Answer clearly and helpfully.
"""

        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        answer = res.choices[0].message.content
        self.history.append(f"User:{question}\nBot:{answer}")

        return answer
