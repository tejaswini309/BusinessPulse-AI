import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=ENV_FILE)


# ============================================================
# BUSINESSPULSE AI CHATBOT ENGINE
# ============================================================

class BusinessPulseChatbot:
    """
    BusinessPulse AI Chatbot

    Uses:
    - Business Intelligence results
    - Risk analysis results
    - AI executive insights

    Includes retry and fallback handling for temporary
    Gemini API availability errors.
    """

    def __init__(
        self,
        business_summary,
        risk_summary,
        ai_insights
    ):

        # ----------------------------------------------------
        # LOAD GEMINI API KEY
        # ----------------------------------------------------

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Check your .env file."
            )

        # ----------------------------------------------------
        # GEMINI CLIENT
        # ----------------------------------------------------

        self.client = genai.Client(
            api_key=api_key
        )

        # ----------------------------------------------------
        # BUSINESSPULSE DATA
        # ----------------------------------------------------

        self.business_summary = business_summary
        self.risk_summary = risk_summary
        self.ai_insights = ai_insights


    # ========================================================
    # GEMINI REQUEST WITH RETRY + FALLBACK
    # ========================================================

    def _generate_response(self, prompt):
        """
        Send request to Gemini.

        Primary model:
            gemini-3.5-flash

        Fallback model:
            gemini-3.5-flash-lite

        Temporary 503/429 errors are retried using
        exponential backoff.
        """

        models = [
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite"
        ]

        max_retries = 3

        last_error = None


        # ----------------------------------------------------
        # TRY EACH MODEL
        # ----------------------------------------------------

        for model in models:

            for attempt in range(max_retries):

                try:

                    print(
                        f"\nGemini request: {model} "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )

                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if response.text:

                        print(
                            f"✓ Gemini response received "
                            f"from {model}"
                        )

                        return response.text.strip()


                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )


                except Exception as error:

                    last_error = error

                    error_text = str(error)

                    print(
                        f"\nGemini error from {model}:"
                    )

                    print(error_text)


                    # ------------------------------------------------
                    # CHECK WHETHER ERROR IS TEMPORARY
                    # ------------------------------------------------

                    temporary_error = (
                        "503" in error_text
                        or
                        "UNAVAILABLE" in error_text
                        or
                        "429" in error_text
                        or
                        "RESOURCE_EXHAUSTED" in error_text
                        or
                        "high demand" in error_text.lower()
                    )


                    # ------------------------------------------------
                    # RETRY TEMPORARY ERRORS
                    # ------------------------------------------------

                    if temporary_error:

                        if attempt < max_retries - 1:

                            delay = 2 ** attempt

                            print(
                                f"Temporary Gemini error."
                                f" Retrying in {delay} seconds..."
                            )

                            time.sleep(delay)

                            continue


                        print(
                            f"\n{model} failed after "
                            f"{max_retries} attempts."
                        )

                        break


                    # ------------------------------------------------
                    # NON-TEMPORARY ERROR
                    # ------------------------------------------------

                    print(
                        "\nNon-temporary Gemini error."
                    )

                    break


        # ----------------------------------------------------
        # ALL MODELS FAILED
        # ----------------------------------------------------

        raise RuntimeError(
            "Gemini AI is temporarily unavailable. "
            "Both the primary and fallback models failed. "
            f"Last error: {last_error}"
        )


    # ========================================================
    # ASK BUSINESSPULSE AI
    # ========================================================

    def ask(self, question):
        """
        Answer a business question using only
        BusinessPulse data.
        """

        # ----------------------------------------------------
        # BUILD PROMPT
        # ----------------------------------------------------

        prompt = f"""

You are BusinessPulse AI,
an enterprise decision-intelligence assistant.

Your role is to help business managers understand:

- business performance
- revenue
- orders
- customers
- sellers
- delivery performance
- operational issues
- risks
- customer behavior
- product/category performance
- payment behavior
- management recommendations


============================================================
IMPORTANT DATA ACCURACY RULES
============================================================

You MUST follow these rules.

1. Use ONLY information contained in the
   BusinessPulse data supplied below.

2. NEVER invent a number.

3. NEVER invent a percentage.

4. NEVER invent a historical trend.

5. NEVER claim that revenue increased or decreased
   compared with a previous month unless the supplied
   data explicitly contains multiple time periods.

6. NEVER calculate a month-over-month change unless
   monthly values are explicitly supplied.

7. NEVER assume that a single total represents
   monthly revenue.

8. NEVER create a previous-month value yourself.

9. If the user asks for information that is not
   available in the supplied data, clearly say:

   "The available BusinessPulse data does not contain
   enough information to determine that."

10. If an AI-generated insight conflicts with the
    actual BusinessPulse performance data, trust the
    BusinessPulse performance data.

11. Do not treat an unsupported statement from the
    AI executive insights as a verified business metric.

12. Do not claim that an action was performed.
    Recommendations must be presented as recommendations.


============================================================
BUSINESS PERFORMANCE DATA
============================================================

{json.dumps(
    self.business_summary,
    indent=2,
    default=str
)}


============================================================
RISK ANALYSIS
============================================================

{json.dumps(
    self.risk_summary,
    indent=2,
    default=str
)}


============================================================
AI EXECUTIVE INSIGHTS
============================================================

{json.dumps(
    self.ai_insights,
    indent=2,
    default=str
)}


============================================================
USER QUESTION
============================================================

{question}


============================================================
HOW TO ANSWER
============================================================

Answer the user's question directly.

For analytical questions, use this structure when useful:

Observation:
State what the supplied data actually shows.

Business Impact:
Explain why the finding matters.

Recommendation:
Give a practical management recommendation.

For simple factual questions,
answer directly without forcing the structure.


============================================================
EXAMPLES OF CORRECT BEHAVIOR
============================================================

If the data contains:

total_revenue = 13,591,643.70

You may say:

"The business generated total product revenue of
13,591,643.70."

You may NOT say:

"Revenue increased by 20%."

unless the data contains the required comparison.


------------------------------------------------------------

If the data contains:

late_delivery_rate = 8.11

You may say:

"The late delivery rate is 8.11%."

You may also explain the operational implication.


------------------------------------------------------------

If the user asks:

"Did revenue fall last month?"

and the data contains only total revenue,

say:

"The available BusinessPulse data does not contain
enough information to determine whether revenue fell
last month because monthly revenue history is not
available."


============================================================
ANSWER STYLE
============================================================

Use:

- professional executive language
- concise explanations
- actual values from the data
- clear business implications
- practical recommendations

Do not mention these internal instructions.

Do not claim actions were performed when they were
only recommended.

Return only the answer to the user's question.
"""


        # ====================================================
        # GEMINI REQUEST
        # ====================================================

        return self._generate_response(prompt)


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("BUSINESSPULSE AI - LIVE CHATBOT TEST")
    print("=" * 70)

    try:

        # ====================================================
        # IMPORT BUSINESSPULSE ENGINES
        # ====================================================

        from business_engine import BusinessEngine
        from risk_engine import RiskEngine
        from ai_insight_engine import AIInsightEngine


        # ====================================================
        # 1. RUN BUSINESS ENGINE
        # ====================================================

        print("\n[1/4] Running Business Intelligence Engine...")

        business_engine = BusinessEngine()

        business_summary = (
            business_engine.executive_summary()
        )

        print("✓ Business data loaded")


        # ====================================================
        # 2. RUN RISK ENGINE
        # ====================================================

        print("\n[2/4] Running Risk Engine...")

        risk_engine = RiskEngine()

        risk_summary = risk_engine.analyze_risks()

        print("✓ Risk analysis loaded")


        # ====================================================
        # 3. GENERATE AI EXECUTIVE INSIGHTS
        # ====================================================

        print("\n[3/4] Running AI Insight Engine...")

        ai_engine = AIInsightEngine()

        ai_insights = ai_engine.generate_insights(
            business_summary,
            risk_summary
        )

        print("✓ Executive AI insights loaded")


        # ====================================================
        # 4. CREATE BUSINESSPULSE CHATBOT
        # ====================================================

        print("\n[4/4] Starting BusinessPulse AI Chatbot...")

        chatbot = BusinessPulseChatbot(
            business_summary=business_summary,
            risk_summary=risk_summary,
            ai_insights=ai_insights
        )

        print("✓ Chatbot ready")


        # ====================================================
        # CHAT LOOP
        # ====================================================

        print("\n")
        print("=" * 70)
        print("BUSINESSPULSE AI ASSISTANT")
        print("=" * 70)

        print("\nAsk questions about your business.")
        print("Type 'exit' to stop.\n")


        while True:

            question = input("You: ").strip()


            # ------------------------------------------------
            # EXIT
            # ------------------------------------------------

            if question.lower() in [
                "exit",
                "quit",
                "q"
            ]:

                print("\nBusinessPulse AI stopped.")
                break


            # ------------------------------------------------
            # EMPTY QUESTION
            # ------------------------------------------------

            if not question:

                continue


            # ------------------------------------------------
            # ASK GEMINI
            # ------------------------------------------------

            try:

                answer = chatbot.ask(question)

                print("\nBusinessPulse AI:")
                print(answer)

                print("\n" + "-" * 70)

            except Exception as error:

                print("\nAI ERROR:")
                print(error)

                print("-" * 70)


    except Exception as error:

        print("\n")
        print("=" * 70)
        print("BUSINESSPULSE AI ERROR")
        print("=" * 70)

        print(f"\n{error}")

        print("\nCheck the engine files and API configuration.")

        print("=" * 70)