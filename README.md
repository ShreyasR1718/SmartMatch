# SmartMatch – AI-Powered Internship Recommendation System

SmartMatch is an AI-powered internship recommendation system that matches student profiles with suitable internship opportunities based on skills, location, experience, and education.

## Features

- Skill-based internship matching
- Skill normalization and alias handling
- Location compatibility scoring
- Experience-based scoring
- Education compatibility scoring
- Weighted match score calculation
- Matched and missing skill identification
- Top-10 internship recommendations
- REST API using FastAPI
- Interactive frontend
- Swagger API documentation
- Input validation using Pydantic
- Generated internship and candidate datasets
- Pairwise match dataset generation

## System Architecture

```text
Student Profile
      |
      v
   Frontend
      |
      v
 FastAPI Backend
      |
      v
 Matching Engine
      |
      +-------------------+
      |                   |
      v                   v
Intern Data        Opportunity Data
      |                   |
      +---------+---------+
                |
                v
       Match Score Calculation
                |
                v
       Ranked Recommendations
                |
                v
             Frontend


Matching Method

SmartMatch calculates a weighted score using four factors:

Factor	Weight
Skills	65%
Location	15%
Experience	10%
Education	10%

The final score is used to rank internship opportunities and return the top recommendations.

Skill Matching

The system normalizes skills before comparison. Examples include:

ML → Machine Learning
ReactJS → React
NodeJS → Node.js
Postgres → PostgreSQL
Py → Python
NLP → Natural Language Processing

Matching uses normalized exact skill comparison to avoid incorrect partial matches such as:
Java incorrectly matching JavaScript
SQL incorrectly matching PostgreSQL

Project Structure:
SmartMatch Project/
│
├── backend/
│   └── main.py
│
├── ml-engine/
│   ├── matching_engine.py
│   └── requirements.txt
│
├── data/
│   ├── interns.csv
│   ├── opportunities.csv
│   ├── matches.csv
│   ├── generate_interns.py
│   └── generate_opportunities.py
│
├── frontend/
│   └── index.html
│
├── docs/
│
├── tests/
│
├── .gitignore
└── README.md

Dataset

The project includes:

50 internship candidate records
30 internship opportunity records
1,500 generated candidate-opportunity match records

The 1,500 match records represent the pairwise combinations of the 50 candidates and 30 opportunities.

Backend:
The backend is implemented using FastAPI.

Run the backend from the backend directory,
code:uvicorn main:app --reload --port 8000

The API will be available at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
Frontend

The frontend is a browser-based interface located in:

frontend/index.html

It communicates with the FastAPI backend and displays the recommended internships, match scores, matched skills, missing skills, and explanations.

The frontend can be opened using VS Code Live Server.

API Endpoint
POST /matches

Accepts an internship candidate profile containing:

{
  "name": "Rahul",
  "skills": "Python, SQL, Machine Learning",
  "location": "Bangalore",
  "experience": 2,
  "education": "B.Tech"
}

The API returns ranked internship recommendations including:

Company
Role
Location
Required skills
Match score
Matched skills
Missing skills
Validation

The API validates user input using Pydantic.

Examples of invalid inputs that are rejected:

Missing required fields
Non-numeric experience
Negative experience values

The API returns appropriate HTTP 422 validation responses for invalid requests.

Testing

The implemented system was tested using 18 test cases covering:

Normal multi-skill candidate
Frontend candidate profile
SQL/PostgreSQL matching validation
Candidate with very few skills
Location mismatch
Direct API request
Missing required field
Invalid experience type
Empty skills
Negative experience
Zero experience boundary
Skill alias validation
Case-insensitive matching
Extra spaces in skills
Unknown skills
Location and education variation
Ranking validation
Final frontend end-to-end test

All 18/18 tests passed after the identified matching and validation issues were fixed.

Known Limitations
Recommendations are based on the available dataset.
The current system uses deterministic weighted scoring rather than a trained machine-learning model.
Location mismatch reduces the score but does not completely exclude an opportunity.
The system currently returns the top 10 recommendations.
The frontend is designed as a local development interface and is not deployed as a production application.
Future Enhancements

Possible future improvements include:

Integration with real internship platforms
Larger and continuously updated datasets
Semantic skill similarity using embeddings
User authentication
Candidate profile persistence
Internship filtering and search
Production deployment
Feedback-based recommendation improvement
More advanced machine-learning recommendation models
Technologies Used
Python
FastAPI
Pydantic
Pandas
HTML
CSS
JavaScript
REST API
CSV datasets
VS Code
Git and GitHub
Project Status

Completed and tested

The current implementation has been tested end-to-end, including backend API functionality, matching logic, validation, ranking, and frontend recommendations.