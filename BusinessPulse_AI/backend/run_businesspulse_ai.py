from business_engine import BusinessEngine
from risk_engine import RiskEngine
from ai_insight_engine import AIInsightEngine
import json


def main():

    print("=" * 70)
    print("BUSINESSPULSE AI - DECISION INTELLIGENCE PIPELINE")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. BUSINESS INTELLIGENCE
    # --------------------------------------------------------

    print("\n[1/3] Running Business Intelligence Engine...")

    business_engine = BusinessEngine()

    business_summary = business_engine.executive_summary()

    print("✓ Business intelligence calculated")


    # --------------------------------------------------------
    # 2. RISK & ANOMALY ANALYSIS
    # --------------------------------------------------------

    print("\n[2/3] Running Risk & Anomaly Engine...")

    risk_engine = RiskEngine()

    risk_summary = risk_engine.analyze_risks()

    print("✓ Risk analysis completed")


    # --------------------------------------------------------
    # 3. AI INSIGHT GENERATION
    # --------------------------------------------------------

    print("\n[3/3] Running Gemini AI Insight Engine...")

    ai_engine = AIInsightEngine()

    ai_insights = ai_engine.generate_insights(
        business_summary,
        risk_summary
    )

    print("✓ AI insights generated")


    # --------------------------------------------------------
    # DISPLAY BUSINESS SUMMARY
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("BUSINESSPULSE BUSINESS SUMMARY")
    print("=" * 70)

    print(
        json.dumps(
            business_summary,
            indent=4,
            default=str
        )
    )


    # --------------------------------------------------------
    # DISPLAY RISK SUMMARY
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("BUSINESSPULSE RISK SUMMARY")
    print("=" * 70)

    print(
        json.dumps(
            risk_summary,
            indent=4,
            default=str
        )
    )


    # --------------------------------------------------------
    # DISPLAY AI INSIGHTS
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("BUSINESSPULSE AI EXECUTIVE INSIGHTS")
    print("=" * 70)

    print(
        json.dumps(
            ai_insights,
            indent=4,
            ensure_ascii=False
        )
    )


    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("BUSINESSPULSE AI PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()