import os
import json

# Try importing OpenAI safely
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def _clean_text(text, max_len=300):
    """Clean and trim extracted text for readable output."""
    text = " ".join(text.split())
    return text[:max_len] + "..." if len(text) > max_len else text


def rule_based_inference(content_blocks):
    """
    Fallback inference when OpenAI quota or API is unavailable.
    Uses rule-based grouping to simulate AI behavior.
    """

    modules = {}

    for text in content_blocks:
        lowered = text.lower()
        cleaned = _clean_text(text)

        if "security" in lowered or "privacy" in lowered:
            modules.setdefault(
                "Security & Privacy",
                {
                    "Description": "Security, privacy, and access control features.",
                    "Submodules": {}
                }
            )
            modules["Security & Privacy"]["Submodules"]["Security Settings"] = cleaned

        elif "account" in lowered:
            modules.setdefault(
                "Account Management",
                {
                    "Description": "Features related to managing user accounts and settings.",
                    "Submodules": {}
                }
            )
            modules["Account Management"]["Submodules"]["Account Settings"] = cleaned

        elif "plugin" in lowered:
            modules.setdefault(
                "Plugins",
                {
                    "Description": "Extending product functionality using plugins.",
                    "Submodules": {}
                }
            )
            modules["Plugins"]["Submodules"]["Plugin Usage"] = cleaned

        elif "install" in lowered or "setup" in lowered:
            modules.setdefault(
                "Getting Started",
                {
                    "Description": "Guidance for installation and initial product setup.",
                    "Submodules": {}
                }
            )
            modules["Getting Started"]["Submodules"]["Installation & Setup"] = cleaned

    # ✅ Always return a valid JSON array
    return [
        {
            "module": module,
            "Description": data["Description"],
            "Submodules": data["Submodules"]
        }
        for module, data in modules.items()
    ]


def infer_modules(content_blocks):
    """
    Main inference function:
    - Uses OpenAI if API key & quota are available
    - Automatically falls back to rule-based logic otherwise
    """

    if not content_blocks:
        return []

    # ---------- TRY AI INFERENCE ----------
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            documentation_text = "\n".join(content_blocks[:300])

            prompt = f"""
You are an expert documentation analyst.

TASK:
From the documentation content below:

1. Identify HIGH-LEVEL PRODUCT MODULES.
2. Identify SUBMODULES under each module.
3. Generate CLEAR, DETAILED descriptions.
4. Use ONLY the provided content.
5. DO NOT invent or assume features.
6. Output MUST be valid JSON ONLY.
7. Follow this EXACT JSON format:

[
  {{
    "module": "Module Name",
    "Description": "Module description",
    "Submodules": {{
      "Submodule Name": "Submodule description"
    }}
  }}
]

DOCUMENTATION CONTENT:
{documentation_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            print("⚠️ OpenAI unavailable, switching to rule-based inference.")
            print(f"Reason: {e}")

    # ---------- FALLBACK ----------
    return rule_based_inference(content_blocks)
