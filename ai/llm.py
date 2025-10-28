# ai/llm.py
import os
from typing import Optional
from openai import OpenAI


class LLMClient:
    """
    Unified wrapper: supports OpenAI / DeepSeek / Dummy.
    - Preferred env vars: LLM_PROVIDER / LLM_API_KEY / LLM_MODEL
    - Also compatible with OPENAI_API_KEY / DEEPSEEK_API_KEY
    - Default model: gpt-4.1-mini (OpenAI)
    """

    # provider defaults
    _DEFAULT_MODELS = {
        "openai": "gpt-4.1-mini",   # Default model switched to GPT-4.1-mini
        "deepseek": "deepseek-chat",
    }

    _BASE_URLS = {
        "openai": "https://api.openai.com/v1",
        "deepseek": "https://api.deepseek.com/v1",
    }

    # initialization
    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        # Read provider/key from environment variables
        prov = (provider or os.getenv("LLM_PROVIDER") or "").strip().lower()
        key = api_key or os.getenv("LLM_API_KEY")

        # Try common variable names if not explicitly set
        if not key:
            if os.getenv("OPENAI_API_KEY"):
                prov = prov or "openai"
                key = os.getenv("OPENAI_API_KEY")
            elif os.getenv("DEEPSEEK_API_KEY"):
                prov = prov or "deepseek"
                key = os.getenv("DEEPSEEK_API_KEY")

        # Determine provider: use "openai" if a key exists, otherwise dummy
        if not prov:
            prov = "openai" if key else "dummy"

        self.provider = prov
        self.api_key = key or ""
        self.model = (
            model
            or os.getenv("LLM_MODEL")
            or self._DEFAULT_MODELS.get(self.provider, "")
        )

        # Initialize OpenAI-compatible client
        self.client: Optional[OpenAI] = None
        if self.provider in {"openai", "deepseek"} and self.api_key:
            base = self._BASE_URLS[self.provider]
            self.client = OpenAI(api_key=self.api_key, base_url=base)

        print(f"[LLMClient] Initialized provider={self.provider}, model={self.model}")

    # internal helpers
    def _dummy(self, prompt: str) -> str:
        """Return placeholder text when no API key is configured."""
        short = (prompt or "")[:160].replace("\n", " ")
        return f"[Dummy AI Output] {short} ..."

    def _chat(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> str:
        """Low-level chat wrapper for model calls."""
        if not self.client:
            # No client available → dummy output
            return self._dummy(prompt)

        if not self.model:
            return "[AI Error] No model configured. Please set LLM_MODEL in .env."

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            # Return a readable error message for debugging
            return f"[AI Error] provider={self.provider}, model={self.model}, error={e}"

    # public APIs
    def generate_product_desc(
        self, name: str, category: str, unit: str, stock: int, lang: str = "en"
    ) -> str:
        """
        Generate a concise e-commerce product description.
        Args:
            name: product name
            category: product category
            unit: sales unit (e.g., '1kg')
            stock: current stock quantity
            lang: output language ("en" or "zh")
        """
        lang_norm = (lang or "en").strip().lower()
        if lang_norm in {"zh", "cn", "zh-cn", "chinese"}:
            lang_norm = "Chinese"
        elif lang_norm in {"en", "english"}:
            lang_norm = "English"

        prompt = (
            f"Write a concise e-commerce product description in {lang_norm} for an agricultural product.\n"
            f"- Name: {name}\n- Category: {category}\n- Unit: {unit}\n- Stock: {stock}\n"
            f"Tone: factual, trustworthy, and specific; avoid hype; length 60–100 words."
        )
        return self._chat(prompt, max_tokens=180, temperature=0.6)

    def answer_question(self, question: str, product_context: str) -> str:
        """
        Answer a short customer question based on product info.
        Args:
            question: user question text
            product_context: product data context string
        """
        prompt = (
            "You are a concise customer support assistant for an agricultural marketplace.\n"
            "If price, stock, or logistics are asked, prefer the numbers in the context.\n"
            f"Product context: {product_context}\n"
            f"Question: {question}\n"
            "Answer briefly (1–3 sentences)."
        )
        return self._chat(prompt, max_tokens=200, temperature=0.5)
