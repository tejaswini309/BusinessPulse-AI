from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from business_engine import BusinessEngine
from risk_engine import RiskEngine
from ai_insight_engine import AIInsightEngine
from chatbot_engine import BusinessPulseChatbot

from forecasting_engine import ForecastingEngine
# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="BusinessPulse AI API",
    description="Enterprise Decision Intelligence API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    question: str


# ============================================================
# LOAD BUSINESSPULSE ENGINES
# ============================================================

print("Loading BusinessPulse AI engines...")

business_engine = BusinessEngine()

risk_engine = RiskEngine()

ai_engine = AIInsightEngine()

forecasting_engine = ForecastingEngine()

print("BusinessPulse AI engines loaded.")


# ============================================================
# GENERATE BUSINESS CONTEXT
# ============================================================

def get_business_context():

    business_summary = (
        business_engine.executive_summary()
    )

    risk_summary = (
        risk_engine.analyze_risks()
    )

    ai_insights = (
        ai_engine.generate_insights(
            business_summary,
            risk_summary
        )
    )

    return (
        business_summary,
        risk_summary,
        ai_insights
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "application": "BusinessPulse AI",
        "message": "BusinessPulse AI API is running"
    }


# ============================================================
# BUSINESS SUMMARY API
# ============================================================

@app.get("/business-summary")
def business_summary():

    try:

        business_data = (
            business_engine.executive_summary()
        )

        return {
            "status": "success",
            "data": business_data
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# RISK SUMMARY API
# ============================================================

@app.get("/risk-summary")
def risk_summary():

    try:

        risk_data = (
            risk_engine.analyze_risks()
        )

        return {
            "status": "success",
            "data": risk_data
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# AI EXECUTIVE INSIGHTS API
# ============================================================

@app.get("/ai-insights")
def ai_insights():

    try:

        business_data = (
            business_engine.executive_summary()
        )

        risk_data = (
            risk_engine.analyze_risks()
        )

        insights = (
            ai_engine.generate_insights(
                business_data,
                risk_data
            )
        )

        return {
            "status": "success",
            "data": insights
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

# ============================================================
# FORECASTING API
# ============================================================

@app.get("/forecast")
def forecast():

    try:

        forecast_data = (
            forecasting_engine.generate_forecast(
                periods=3
            )
        )

        return {
            "status": "success",
            "data": forecast_data
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

# ============================================================
# BUSINESS INSIGHTS API
# ============================================================
# Frontend-friendly endpoint.
#
# This endpoint provides:
#   1. Business performance
#   2. Risk analysis
#   3. AI executive insights
#
# The frontend can use this endpoint for the
# "Business Insights" section.
# ============================================================

@app.get("/business-insights")
def business_insights():

    try:

        # ----------------------------------------------------
        # BUSINESS PERFORMANCE
        # ----------------------------------------------------

        business_data = (
            business_engine.executive_summary()
        )


        # ----------------------------------------------------
        # RISK ANALYSIS
        # ----------------------------------------------------

        risk_data = (
            risk_engine.analyze_risks()
        )


        # ----------------------------------------------------
        # AI EXECUTIVE INSIGHTS
        # ----------------------------------------------------

        insights = (
            ai_engine.generate_insights(
                business_data,
                risk_data
            )
        )


        # ----------------------------------------------------
        # RETURN COMPLETE INSIGHT PACKAGE
        # ----------------------------------------------------

        return {
            "status": "success",

            "business_performance": business_data,

            "risk_analysis": risk_data,

            "ai_insights": insights
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# CHATBOT API
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # ----------------------------------------------------
        # GET USER QUESTION
        # ----------------------------------------------------

        question = request.question.strip()


        # ----------------------------------------------------
        # VALIDATE QUESTION
        # ----------------------------------------------------

        if not question:

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )


        # ----------------------------------------------------
        # GET CURRENT BUSINESSPULSE CONTEXT
        # ----------------------------------------------------

        (
            business_data,
            risk_data,
            insights
        ) = get_business_context()


        # ----------------------------------------------------
        # CREATE BUSINESSPULSE CHATBOT
        # ----------------------------------------------------

        chatbot = BusinessPulseChatbot(
            business_summary=business_data,
            risk_summary=risk_data,
            ai_insights=insights
        )


        # ----------------------------------------------------
        # ASK GEMINI
        # ----------------------------------------------------

        answer = chatbot.ask(question)


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return {
            "status": "success",
            "question": question,
            "answer": answer
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )