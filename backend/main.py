from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import csv
import os
import sys


# =========================================================
# PATH SETUP
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ML_ENGINE_DIR = os.path.join(
    BASE_DIR,
    "ml-engine"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# Allow Python to find matching_engine.py
if ML_ENGINE_DIR not in sys.path:
    sys.path.insert(0, ML_ENGINE_DIR)


# =========================================================
# IMPORT MATCHING ENGINE
# =========================================================

from matching_engine import (
    calculate_match,
    get_matched_skills,
    get_missing_skills
)


# =========================================================
# FILE PATHS
# =========================================================

INTERNS_FILE = os.path.join(
    DATA_DIR,
    "interns.csv"
)

OPPORTUNITIES_FILE = os.path.join(
    DATA_DIR,
    "opportunities.csv"
)


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="SmartMatch API",
    version="1.0.0",
    description="AI-powered internship matching system"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# REQUEST MODEL
# =========================================================

class InternRequest(BaseModel):
    name: str
    skills: str
    location: str
    experience: int = Field(ge=0)
    education: str

# =========================================================
# LOAD CSV
# =========================================================

def load_csv(filename):
    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "SmartMatch API is running!",
        "status": "success"
    }


# =========================================================
# GET OPPORTUNITIES
# =========================================================

@app.get("/opportunities")
def get_opportunities():

    opportunities = load_csv(
        OPPORTUNITIES_FILE
    )

    return {
        "total": len(opportunities),
        "opportunities": opportunities
    }


# =========================================================
# GET MATCHES
# =========================================================

@app.post("/matches")
def get_matches(intern_data: InternRequest):

    # -----------------------------------------------------
    # Load opportunities
    # -----------------------------------------------------

    opportunities = load_csv(
        OPPORTUNITIES_FILE
    )

    # -----------------------------------------------------
    # Convert user input into dictionary
    # -----------------------------------------------------

    intern = {
        "id": "user",
        "name": intern_data.name,
        "skills": intern_data.skills,
        "location": intern_data.location,
        "experience": str(intern_data.experience),
        "education": intern_data.education
    }

    results = []

    # -----------------------------------------------------
    # Compare user with every opportunity
    # -----------------------------------------------------

    for opportunity in opportunities:

        # Calculate overall score
        score = calculate_match(
            intern,
            opportunity
        )

        # Find matched skills
        matched_skills = get_matched_skills(
            intern["skills"],
            opportunity["skills"]
        )

        # Find missing skills
        missing_skills = get_missing_skills(
            intern["skills"],
            opportunity["skills"]
        )

        # Add result
        results.append({
            "company": opportunity["company"],
            "role": opportunity["role"],
            "location": opportunity["location"],
            "required_skills": opportunity["skills"],
            "match_score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })
    # -----------------------------------------------------
    # Highest score first
    # -----------------------------------------------------

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    # -----------------------------------------------------
    # Return top 10
    # -----------------------------------------------------

    return {
        "intern": intern_data.name,
        "total_opportunities": len(results),
        "matches": results[:10]
    }