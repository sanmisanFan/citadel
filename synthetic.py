import random
import json
import flor


# Function to generate a fake author name by randomly choosing first and last names
def generate_fake_author():
    first_names = [
        "John",
        "James",
        "Robert",
        "Michael",
        "William",
        "David",
        "Richard",
        "Joseph",
        "Charles",
        "Thomas",
        "Christopher",
        "Daniel",
        "Matthew",
        "Anthony",
        "Mark",
        "Paul",
        "Steven",
        "Andrew",
        "Kenneth",
        "Joshua",
        "Kevin",
        "Brian",
        "George",
        "Edward",
        "Ronald",
        "Timothy",
        "Jason",
        "Jeffrey",
        "Ryan",
        "Jacob",
        "Ethan",
        "Alexander",
        "Henry",
        "Samuel",
        "Dylan",
        "Luke",
        "Gabriel",
        "Anthony",
        "Isaac",
        "Grayson",
        "Owen",
        "Julian",
        "Levi",
        "Coleman",
        "Everett",
        "Bryce",
        "Mary",
        "Patricia",
        "Jennifer",
        "Linda",
        "Elizabeth",
        "Barbara",
        "Susan",
        "Jessica",
        "Sarah",
        "Karen",
        "Nancy",
        "Lisa",
        "Margaret",
        "Betty",
        "Sandra",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
        "Thompson",
        "White",
        "Harris",
        "Sanchez",
        "Clark",
        "Ramirez",
        "Lewis",
        "Robinson",
        "Walker",
        "Young",
        "Allen",
        "King",
        "Wright",
        "Scott",
        "Torres",
        "Nguyen",
        "Hill",
        "Flores",
        "Green",
        "Adams",
        "Nelson",
        "Baker",
        "Hall",
        "Rivera",
        "Campbell",
        "Mitchell",
        "Carter",
        "Roberts",
    ]
    return random.choice(first_names) + " " + random.choice(last_names)


# Function to generate a fake paper title by randomly choosing a noun and subject
def generate_fake_title():
    nouns = [
        "Review",
        "Comparison",
        "Exploration",
        "Assessment",
        "Examination",
        "Survey",
        "Analysis",
        "Research",
        "Investigation",
        "Observation",
        "Measurement",
        "Testing",
        "Validation",
        "Verification",
        "Application",
    ]
    subjects = [
        "Quantum Mechanics",
        "Global Warming",
        "Artificial Intelligence",
        "Cryptography",
        "Biochemistry",
        "Molecular Biology",
        "Neuroscience",
        "Particle Physics",
        "Environmental Science",
        "Ecology",
        "Robotics",
        "Software Engineering",
        "Sociology",
        "Public Health",
        "Graphic Design",
    ]

    return random.choice(nouns) + " of " + random.choice(subjects)


# Function to generate a fake journal name by randomly choosing from a list
def generate_fake_journal():
    journals = [
        "Journal of Advanced Research",
        "International Journal of Scientific Studies",
        "Global Science Review",
    ]
    return random.choice(journals)


# Function to generate a fake citation using the previously defined functions
def generate_fake_citation():
    return f"{generate_fake_author()} et al., {generate_fake_title()}, {generate_fake_journal()}, {random.randint(1990, 2022)}."


# Function to generate a fake paper with a specified number of citations
def generate_paper(num_citations):
    paper = {
        "title": generate_fake_title(),
        "Author": generate_fake_author(),
        "abstract": "This is a fake abstract.",
        "introduction": "This is a fake introduction.",
        "body": "This is the main body of the paper.",
        "conclusion": "This is a fake conclusion.",
        "references": [generate_fake_citation() for _ in range(num_citations)],
    }
    return paper


# Define the seed for reproducibility
random.seed(flor.arg("seed", random.randint(0, 1e4)))

# Number of papers to generate
num_papers = flor.arg("num_papers", 10)

# Generate a list of papers with a random number of citations each
papers = [generate_paper(random.randint(5, 15)) for _ in range(num_papers)]


# Add a common citation to the last three papers to create a citation ring
for i in range(3):
    common_citation = generate_fake_citation()
    for paper in papers[-3:]:  # Assume last three papers are in a citation ring
        paper["references"].append(common_citation)


# Write the generated papers
for paper in flor.loop("paper", papers):
    flor.log("title", paper["title"])
    flor.log("author", paper["Author"])
    flor.log("references", paper["references"])
