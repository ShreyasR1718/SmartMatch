import csv
import random

random.seed(42)

names = [
    "Rahul", "Arjun", "Priya", "Ananya", "Kiran",
    "Neha", "Vivek", "Sneha", "Aditya", "Meera",
    "Rohan", "Pooja", "Akash", "Divya", "Nikhil",
    "Aishwarya", "Varun", "Kavya", "Sahil", "Isha",
    "Manish", "Shreya", "Harsh", "Nandini", "Ritesh",
    "Swathi", "Abhishek", "Tanvi", "Yash", "Pallavi",
    "Aman", "Sanjana", "Ravi", "Keerthi", "Dhanush",
    "Anjali", "Surya", "Deepika", "Karthik", "Lakshmi",
    "Rohit", "Bhavana", "Darshan", "Sakshi", "Vishal",
    "Manya", "Pranav", "Shruthi", "Gaurav", "Sowmya"
]

skills = [
    "Python",
    "Java",
    "JavaScript",
    "React",
    "Node.js",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "Pandas",
    "Django",
    "Spring Boot",
    "AWS",
    "Docker",
    "MongoDB",
    "PostgreSQL",
    "TensorFlow",
    "Power BI",
    "HTML",
    "CSS",
    "Git"
]

locations = [
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Mumbai",
    "Mysore",
    "Delhi",
    "Kochi"
]

education_options = [
    "B.Tech",
    "B.E",
    "BCA",
    "MCA",
    "M.Tech"
]

rows = []

for i, name in enumerate(names, start=1):
    selected_skills = random.sample(skills, random.randint(3, 6))

    rows.append({
        "id": i,
        "name": name,
        "skills": ";".join(selected_skills),
        "location": random.choice(locations),
        "experience": random.randint(0, 5),
        "education": random.choice(education_options)
    })

with open("interns.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "id",
        "name",
        "skills",
        "location",
        "experience",
        "education"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)

print("Successfully generated 50 interns!")