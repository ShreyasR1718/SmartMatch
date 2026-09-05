import csv
import random

companies = [
    "TechNova",
    "CodeCraft",
    "DataSphere",
    "CloudWorks",
    "InnoTech",
    "ByteLabs",
    "NextGen Systems",
    "DevCore",
    "AI Labs",
    "WebWorks"
]

roles = [
    "Python Developer Intern",
    "Data Analyst Intern",
    "Machine Learning Intern",
    "Web Development Intern",
    "Backend Developer Intern",
    "Frontend Developer Intern",
    "Software Engineering Intern",
    "AI Engineering Intern",
    "Cloud Engineering Intern",
    "Full Stack Developer Intern"
]

skills_pool = [
    "Python",
    "Java",
    "JavaScript",
    "React",
    "Node.js",
    "SQL",
    "MongoDB",
    "PostgreSQL",
    "Pandas",
    "Machine Learning",
    "Data Analysis",
    "HTML",
    "CSS",
    "Docker",
    "AWS",
    "Git",
    "Power BI",
    "TensorFlow"
]

locations = [
    "Bangalore",
    "Pune",
    "Chennai",
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Kochi"
]

education = [
    "B.Tech",
    "B.E",
    "MCA",
    "M.Tech",
    "BCA"
]

opportunities = []

for i in range(1, 31):
    role = random.choice(roles)

    selected_skills = random.sample(skills_pool, random.randint(3, 6))

    opportunity = {
        "id": i,
        "company": random.choice(companies),
        "role": role,
        "skills": ";".join(selected_skills),
        "location": random.choice(locations),
        "min_experience": random.randint(0, 2),
        "education": random.choice(education)
    }

    opportunities.append(opportunity)

with open("opportunities.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "id",
        "company",
        "role",
        "skills",
        "location",
        "min_experience",
        "education"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(opportunities)

print("Successfully generated 30 internship opportunities!")