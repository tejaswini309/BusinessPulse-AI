import os
import json
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=ENV_FILE)


# ============================================================
# AI INSIGHT ENGINE
# ============================================================

class AIInsightEngine:
    """
    BusinessPulse AI – AI Insight Engine

    Converts business and risk engine results into
    executive-level AI business insights using Gemini.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Check your .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Current stable model
        self.primary_model = "gemini-3.5-flash"

        # Lower-cost fallback model
        self.fallback_model = "gemini-3.5-flash-lite"


    # ========================================================
    # GENERATE BUSINESS INSIGHTS
    # ========================================================

    def generate_insights(
        self,
        business_summary,
        risk_summary
    ):
        """
        Generate structured AI-powered
        executive business insights.
        """

        # ----------------------------------------------------
        # BUILD PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are the AI decision-intelligence engine for BusinessPulse AI,
an enterprise business analytics platform.

Your job is to analyze the business performance results and
risk analysis results supplied below.

IMPORTANT:
Use ONLY the information provided in the data.
Do not invent numbers.
Do not invent trends.
Do not assume information that is not present.

============================================================
BUSINESS PERFORMANCE RESULTS
============================================================

{json.dumps(
    business_summary,
    indent=2,
    default=str
)}

============================================================
RISK ANALYSIS RESULTS
============================================================

{json.dumps(
    risk_summary,
    indent=2,
    default=str
)}

============================================================
TASK
============================================================

Generate executive-level business insights.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "executive_summary": "",
    "revenue_insight": "",
    "risk_alert": "",
    "operational_insight": "",
    "recommendation": "",
    "estimated_impact": ""
}}

============================================================
REQUIREMENTS
============================================================

executive_summary:
Give a concise overall assessment of business performance.

revenue_insight:
Explain important revenue, order, customer or profitability
movements visible in the supplied results.

risk_alert:
Identify the most important business risk.

operational_insight:
Explain the operational problem behind the performance.

recommendation:
Give a practical action management should take.

estimated_impact:
Explain the potential business benefit or financial impact
if the recommendation is implemented.

============================================================
RULES
============================================================

1. Do not invent numbers.

2. Do not invent trends.

3. Use actual values from the supplied data whenever available.

4. If the supplied data does not contain enough information
   to determine something, clearly say so.

5. Keep the language professional.

6. Write for an executive business dashboard.

7. Return ONLY valid JSON.

8. Do not use Markdown code fences.

9. Do not add explanations outside the JSON.
"""


        # ====================================================
        # TRY PRIMARY GEMINI MODEL
        # ====================================================

        response = None

        try:

            print(
                f"Trying Gemini model: "
                f"{self.primary_model}"
            )

            response = self.client.models.generate_content(
                model=self.primary_model,
                contents=prompt
            )

            print(
                f"Gemini model successful: "
                f"{self.primary_model}"
            )

        except Exception as primary_error:

            print(
                f"Primary Gemini model failed: "
                f"{primary_error}"
            )

            # ================================================
            # TRY FALLBACK MODEL
            # ================================================

            try:

                print(
                    f"Trying fallback Gemini model: "
                    f"{self.fallback_model}"
                )

                response = self.client.models.generate_content(
                    model=self.fallback_model,
                    contents=prompt
                )

                print(
                    f"Gemini fallback successful: "
                    f"{self.fallback_model}"
                )

            except Exception as fallback_error:

                print(
                    f"Fallback Gemini model failed: "
                    f"{fallback_error}"
                )

                raise RuntimeError(
                    "Gemini AI request failed.\n"
                    f"Primary model error: {primary_error}\n"
                    f"Fallback model error: {fallback_error}"
                )


        # ====================================================
        # EXTRACT RESPONSE
        # ====================================================

        if response is None:

            raise RuntimeError(
                "Gemini returned no response."
            )


        result = response.text.strip()


        # ====================================================
        # CLEAN MARKDOWN JSON
        # ====================================================

        # Remove ```json
        result = re.sub(
            r"^```json\s*",
            "",
            result,
            flags=re.IGNORECASE
        )

        # Remove ```
        result = re.sub(
            r"\s*```$",
            "",
            result
        )

        result = result.strip()


        # ====================================================
        # CONVERT RESPONSE TO JSON
        # ====================================================

        try:

            insights = json.loads(result)

            return insights

        except json.JSONDecodeError:

            # -----------------------------------------------
            # TRY TO FIND JSON OBJECT INSIDE RESPONSE
            # -----------------------------------------------

            json_match = re.search(
                r"\{.*\}",
                result,
                re.DOTALL
            )

            if json_match:

                try:

                    insights = json.loads(
                        json_match.group(0)
                    )

                    return insights

                except json.JSONDecodeError:
                    pass


            # -----------------------------------------------
            # FALLBACK RESPONSE
            # -----------------------------------------------

            return {
                "executive_summary": result,
                "revenue_insight": "",
                "risk_alert": "",
                "operational_insight": "",
                "recommendation": "",
                "estimated_impact": ""
            }


# ============================================================
# TEST AI INSIGHT ENGINE
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("BUSINESSPULSE AI - AI INSIGHT ENGINE TEST")
    print("=" * 70)


    # --------------------------------------------------------
    # SAMPLE BUSINESS DATA
    # --------------------------------------------------------

    sample_business_summary = {

        "total_revenue": 13590000,

        "total_orders": 99000,

        "total_customers": 96000,

        "average_order_value": 136.68

    }


    # --------------------------------------------------------
    # SAMPLE RISK DATA
    # --------------------------------------------------------

    sample_risk_summary = {

        "late_delivery_rate": 8.1,

        "cancellation_rate": 0.6,

        "risk_status": "Moderate"

    }


    # --------------------------------------------------------
    # CREATE ENGINE
    # --------------------------------------------------------

    engine = AIInsightEngine()


    # --------------------------------------------------------
    # GENERATE INSIGHTS
    # --------------------------------------------------------

    insights = engine.generate_insights(

        sample_business_summary,

        sample_risk_summary

    )


    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print("\nAI EXECUTIVE INSIGHTS")

    print("=" * 70)

    print(
        json.dumps(
            insights,
            indent=4,
            ensure_ascii=False
        )
    )

    print("\n" + "=" * 70)

    print(
        "AI INSIGHT ENGINE TEST COMPLETED"
    )

    print("=" * 70)