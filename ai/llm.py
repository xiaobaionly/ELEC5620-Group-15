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
        "openai": "gpt-4.1-mini",  # Default model switched to GPT-4.1-mini
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
        Generate a persuasive yet factual e-commerce product description.
        Tone: natural, warm, and subtly persuasive.
        """
        lang_norm = (lang or "en").strip().lower()
        if lang_norm in {"zh", "cn", "zh-cn", "chinese"}:
            prompt = f"""
                请用自然、吸引人的中文为以下农产品撰写电商商品文案：
                - 产品名称：{name}
                - 类别：{category}
                - 销售单位：{unit}
                - 库存：{stock}（总库存数量，不是单件数）
                要求：
                1. 用3–4句话描述。
                2. 语气温暖、真实、有购买吸引力，但不要夸张。
                3. 可自然提到库存数量，例如“现有{stock}{unit}现货”或“库存充足，欢迎选购”。
                4. 不要列点或标题，只写正文。
                """
            max_toks = 280
        else:
            prompt = f"""
                Write a short, engaging e-commerce product description for an agricultural item:
                - Product name: {name}
                - Category: {category}
                - Unit of sale: {unit}
                - Stock quantity: {stock} (total available, not per-unit)
                Guidelines:
                1. Use 3–4 natural sentences.
                2. Encourage the reader to purchase while sounding trustworthy and warm.
                3. Naturally mention stock, e.g. “Now {stock} kilograms available for order.”
                4. Avoid headings, lists, or marketing clichés; keep it concise and genuine.
                """
            max_toks = 220

        return self._chat(prompt, max_tokens=max_toks, temperature=0.8)

    def answer_question(self, question: str, product_context: str) -> str:
        """
        Answer a short customer question based on product info.
        Args:
            question: user question text
            product_context: product data context string
        """
        prompt = (
            "You are a helpful and friendly customer assistant for an agricultural marketplace.\n"
            "Use the provided product info to answer naturally and accurately.\n"
            "If the question is about price, stock, or shipping, use the numbers from context.\n"
            "Be concise (1–3 sentences) and polite.\n"
            f"Product information: {product_context}\n"
            f"Customer question: {question}"
        )
        return self._chat(prompt, max_tokens=200, temperature=0.5)
