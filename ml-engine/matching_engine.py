import csv
import os
import re


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

INTERNS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "interns.csv"
)

OPPORTUNITIES_FILE = os.path.join(
    BASE_DIR,
    "data",
    "opportunities.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "matches.csv"
)


# =========================================================
# LOAD CSV
# =========================================================

def load_csv(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        return list(
            csv.DictReader(file)
        )


# =========================================================
# SKILL NORMALIZATION
# =========================================================

SKILL_ALIASES = {

    "ml": "machine learning",
    "machine-learning": "machine learning",
    "machinelearning": "machine learning",

    "ai": "artificial intelligence",

    "dl": "deep learning",
    "deep-learning": "deep learning",

    "nlp": "natural language processing",

    "js": "javascript",
    "reactjs": "react",
    "react.js": "react",

    "nodejs": "node.js",
    "node js": "node.js",

"postgres": "postgresql",
    "mongodb": "mongodb",

    "py": "python",

    "data analytics": "data analysis",
    "data-analysis": "data analysis",

    "excel": "excel",

    "aws cloud": "aws",

    "amazon web services": "aws"
}


def normalize_skill(skill):

    skill = skill.strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    if skill in SKILL_ALIASES:

        return SKILL_ALIASES[skill]

    return skill


# =========================================================
# SKILL CLEANING
# =========================================================

def clean_skills(skill_text):

    if not skill_text:
        return []

    skills = re.split(
        r"[;,]",
        skill_text
    )

    cleaned = []

    for skill in skills:

        skill = normalize_skill(skill)

        if skill and skill not in cleaned:

            cleaned.append(skill)

    return cleaned


# =========================================================
# SKILL MATCHING
# =========================================================

def skills_match(
    intern_skill,
    opportunity_skill
):

    intern_skill = normalize_skill(
        intern_skill
    )

    opportunity_skill = normalize_skill(
        opportunity_skill
    )

    # Only exact normalized matches are accepted.
    # Skill variations are handled through SKILL_ALIASES.

    if intern_skill == opportunity_skill:
        return True

    return False

# =========================================================
# SKILL SIMILARITY
# =========================================================

def calculate_skill_similarity(
    intern_skills,
    opportunity_skills
):

    intern_list = clean_skills(
        intern_skills
    )

    opportunity_list = clean_skills(
        opportunity_skills
    )

    if not intern_list or not opportunity_list:

        return 0

    matched_count = 0

    for opportunity_skill in opportunity_list:

        for intern_skill in intern_list:

            if skills_match(
                intern_skill,
                opportunity_skill
            ):

                matched_count += 1

                break

    # Percentage of required skills
    # that the intern already possesses

    score = (
        matched_count
        / len(opportunity_list)
    ) * 100

    return min(
        score,
        100
    )


# =========================================================
# MATCHED SKILLS
# =========================================================

def get_matched_skills(
    intern_skills,
    opportunity_skills
):

    intern_list = clean_skills(
        intern_skills
    )

    opportunity_list = clean_skills(
        opportunity_skills
    )

    matched = []

    for opportunity_skill in opportunity_list:

        for intern_skill in intern_list:

            if skills_match(
                intern_skill,
                opportunity_skill
            ):

                if opportunity_skill not in matched:

                    matched.append(
                        opportunity_skill
                    )

                break

    return ", ".join(
        matched
    )


# =========================================================
# MISSING SKILLS
# =========================================================

def get_missing_skills(
    intern_skills,
    opportunity_skills
):

    intern_list = clean_skills(
        intern_skills
    )

    opportunity_list = clean_skills(
        opportunity_skills
    )

    missing = []

    for opportunity_skill in opportunity_list:

        found = False

        for intern_skill in intern_list:

            if skills_match(
                intern_skill,
                opportunity_skill
            ):

                found = True

                break

        if not found:

            missing.append(
                opportunity_skill
            )

    return ", ".join(
        missing
    )


# =========================================================
# LOCATION SCORE
# =========================================================

def calculate_location_score(
    intern,
    opportunity
):

    intern_location = (
        intern.get("location", "")
        .strip()
        .lower()
    )

    opportunity_location = (
        opportunity.get("location", "")
        .strip()
        .lower()
    )

    if (
        intern_location
        and opportunity_location
        and intern_location == opportunity_location
    ):

        return 100

    return 40


# =========================================================
# EXPERIENCE SCORE
# =========================================================

def calculate_experience_score(
    intern,
    opportunity
):

    try:

        intern_experience = int(
            float(
                intern.get(
                    "experience",
                    0
                )
            )
        )

    except:

        intern_experience = 0

    try:

        required_experience = int(
            float(
                opportunity.get(
                    "min_experience",
                    0
                )
            )
        )

    except:

        required_experience = 0

    # No experience required

    if required_experience <= 0:

        return 100

    # Candidate meets requirement

    if intern_experience >= required_experience:

        return 100

    # Candidate has less experience

    score = (
        intern_experience
        / required_experience
    ) * 100

    return min(
        score,
        100
    )


# =========================================================
# EDUCATION SCORE
# =========================================================

def calculate_education_score(
    intern,
    opportunity
):

    intern_education = (
        intern.get("education", "")
        .strip()
        .lower()
    )

    required_education = (
        opportunity.get("education", "")
        .strip()
        .lower()
    )

    if not required_education:

        return 100

    if (
        intern_education
        and intern_education == required_education
    ):

        return 100

    # Related engineering degrees

    engineering_degrees = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "m.tech",
        "mtech"
    ]

    if (
        intern_education in engineering_degrees
        and required_education in engineering_degrees
    ):

        return 90

    return 50


# =========================================================
# SCORE BREAKDOWN
# =========================================================

def calculate_score_breakdown(
    intern,
    opportunity
):

    # -----------------------------------------------------
    # 1. Skills
    # -----------------------------------------------------

    skill_score = calculate_skill_similarity(
        intern.get("skills", ""),
        opportunity.get("skills", "")
    )

    # -----------------------------------------------------
    # 2. Location
    # -----------------------------------------------------

    location_score = calculate_location_score(
        intern,
        opportunity
    )

    # -----------------------------------------------------
    # 3. Experience
    # -----------------------------------------------------

    experience_score = calculate_experience_score(
        intern,
        opportunity
    )

    # -----------------------------------------------------
    # 4. Education
    # -----------------------------------------------------

    education_score = calculate_education_score(
        intern,
        opportunity
    )

    # -----------------------------------------------------
    # FINAL SCORE
    #
    # Skills      = 65%
    # Location    = 15%
    # Experience  = 10%
    # Education   = 10%
    # -----------------------------------------------------

    final_score = (
        skill_score * 0.65
        + location_score * 0.15
        + experience_score * 0.10
        + education_score * 0.10
    )

    return {

        "skill_score": round(
            skill_score,
            2
        ),

        "location_score": round(
            location_score,
            2
        ),

        "experience_score": round(
            experience_score,
            2
        ),

        "education_score": round(
            education_score,
            2
        ),

        "final_score": round(
            final_score,
            2
        )
    }


# =========================================================
# FINAL MATCH SCORE
# =========================================================

def calculate_match(
    intern,
    opportunity
):

    breakdown = calculate_score_breakdown(
        intern,
        opportunity
    )

    return breakdown["final_score"]


# =========================================================
# MATCH EXPLANATION
# =========================================================

def generate_match_explanation(
    intern,
    opportunity
):

    matched = get_matched_skills(
        intern.get("skills", ""),
        opportunity.get("skills", "")
    )

    missing = get_missing_skills(
        intern.get("skills", ""),
        opportunity.get("skills", "")
    )

    breakdown = calculate_score_breakdown(
        intern,
        opportunity
    )

    reasons = []

    # -----------------------------------------------------
    # Skills explanation
    # -----------------------------------------------------

    if matched:

        reasons.append(
            f"You match these required skills: {matched}."
        )

    else:

        reasons.append(
            "Your current skills have limited overlap with the required skills."
        )

    # -----------------------------------------------------
    # Missing skills
    # -----------------------------------------------------

    if missing:

        reasons.append(
            f"Skills you could improve: {missing}."
        )

    # -----------------------------------------------------
    # Location
    # -----------------------------------------------------

    intern_location = (
        intern.get("location", "")
        .strip()
        .lower()
    )

    opportunity_location = (
        opportunity.get("location", "")
        .strip()
        .lower()
    )

    if (
        intern_location
        and opportunity_location
        and intern_location == opportunity_location
    ):

        reasons.append(
            "The internship location matches your preferred location."
        )

    else:

        reasons.append(
            f"The internship is located in "
            f"{opportunity.get('location', 'another location')}."
        )

    # -----------------------------------------------------
    # Education
    # -----------------------------------------------------

    if breakdown["education_score"] >= 90:

        reasons.append(
            "Your education matches the internship requirement."
        )

    else:

        reasons.append(
            "Your education does not exactly match the listed requirement."
        )

    # -----------------------------------------------------
    # Experience
    # -----------------------------------------------------

    if breakdown["experience_score"] == 100:

        reasons.append(
            "Your experience meets the required experience level."
        )

    else:

        reasons.append(
            "You have less experience than the listed requirement."
        )

    return " ".join(
        reasons
    )


# =========================================================
# GENERATE ALL MATCHES
# =========================================================

def generate_matches():

    interns = load_csv(
        INTERNS_FILE
    )

    opportunities = load_csv(
        OPPORTUNITIES_FILE
    )

    matches = []

    print()
    print("=" * 60)

    print(
        "SMARTMATCH - INTERNSHIP RECOMMENDATION ENGINE"
    )

    print("=" * 60)
    print()

    print(
        f"Loaded interns: {len(interns)}"
    )

    print(
        f"Loaded opportunities: {len(opportunities)}"
    )

    print()

    # -----------------------------------------------------
    # Compare every intern with every opportunity
    # -----------------------------------------------------

    for intern in interns:

        for opportunity in opportunities:

            breakdown = calculate_score_breakdown(
                intern,
                opportunity
            )

            matched_skills = get_matched_skills(
                intern["skills"],
                opportunity["skills"]
            )

            missing_skills = get_missing_skills(
                intern["skills"],
                opportunity["skills"]
            )

            explanation = generate_match_explanation(
                intern,
                opportunity
            )

            matches.append({

                "intern_id":
                    intern["id"],

                "intern_name":
                    intern["name"],

                "opportunity_id":
                    opportunity["id"],

                "company":
                    opportunity["company"],

                "role":
                    opportunity["role"],

                "location":
                    opportunity["location"],

                "required_skills":
                    opportunity.get(
                        "skills",
                        ""
                    ),

                "match_score":
                    breakdown["final_score"],

                "skill_score":
                    breakdown["skill_score"],

                "location_score":
                    breakdown["location_score"],

                "experience_score":
                    breakdown["experience_score"],

                "education_score":
                    breakdown["education_score"],

                "matched_skills":
                    matched_skills,

                "missing_skills":
                    missing_skills,

                "explanation":
                    explanation
            })

    # -----------------------------------------------------
    # Sort highest score first
    # -----------------------------------------------------

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    # -----------------------------------------------------
    # Save results
    # -----------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [

            "intern_id",
            "intern_name",
            "opportunity_id",
            "company",
            "role",
            "location",
            "required_skills",
            "match_score",
            "skill_score",
            "location_score",
            "experience_score",
            "education_score",
            "matched_skills",
            "missing_skills",
            "explanation"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            matches
        )

    # -----------------------------------------------------
    # Terminal output
    # -----------------------------------------------------

    print(
        "Matching completed successfully!"
    )

    print(
        f"Total matches generated: {len(matches)}"
    )

    print()

    print(
        "Results saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print()

    print(
        "TOP 10 MATCHES"
    )

    print(
        "-" * 60
    )

    for match in matches[:10]:

        print(
            f'{match["intern_name"]} -> '
            f'{match["company"]} | '
            f'{match["role"]} | '
            f'{match["match_score"]}%'
        )

    print()

    print(
        "=" * 60
    )


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":

    generate_matches()