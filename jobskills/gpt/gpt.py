import openai
from dotenv import load_dotenv
import os
import time

# ToDo: Documentation.

load_dotenv()

api_key = os.getenv("API_KEY")
if api_key is None:
    print("Error: API_KEY not found in .env file")
    raise ValueError("API_KEY not found in .env file")
openai.api_key = api_key


# Function to extract skills from job advert.
# returns
def job_extract(prompt):
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI that understands both explicit and implicit meaning in text. "
                        "Please read the job advert provided and identify all the relevant technical "
                        "and non-technical skills mentioned. "
                        "Consider exact wording, synonyms, and related technologies. "
                        "Also, differentiate between required competencies and desirable skills. "
                        "Use this information to create a comprehensive list of skills found in the job advert.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.1,
            )
            print("API prompted")
            return response.choices[0].message["content"].strip()

        except openai.error.OpenAIError as e:
            print(
                f"An error occurred: {e}. Attempt {attempt + 1} of 3. Trying again after delay..."
            )
            time.sleep(10)

    print("API interaction failed. Please try again later.")
    exit(1)


# Function to compare extracted job skills with provided skill matrix.
# Returns a table showing the comparison
def job_compare(prompt, job_advert_list):
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Given the skills from the job advert: "
                        + str(job_advert_list)
                        + "\nand the provided skills matrix, construct a table with columns: "
                        "'Required Skill,' 'In Skills Matrix,' and 'Level of Proficiency.' "
                        + "\nFor each skill from the job advert, "
                        "determine if there's a direct match or a related term in the skills matrix. "
                        "If there is, note 'Yes' in the 'In Skills Matrix' column, "
                        "and specify the 'Level of Proficiency' from the skills matrix. "
                        "If not, write 'No' in the 'In Skills Matrix' column, "
                        "and leave 'Level of Proficiency' blank. "
                        + "\nKeep in mind that a skill might be expressed differently in the job advert "
                        "and the skills matrix. A term or a phrase might not match exactly "
                        "but could still refer to the same skill or a relevant one.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.1,
            )
            print("API prompted")
            return response.choices[0].message["content"].strip()

        except openai.error.OpenAIError as e:
            print(
                f"An error occurred: {e}. Attempt {attempt + 1} of 3. Trying again after delay..."
            )
            time.sleep(10)

    print("API interaction failed. Please try again later.")
    exit(1)


def api_interaction(skills_matrix_file, job_advert_file):
    print("Compare mode started.")
    try:
        with open(skills_matrix_file, "r") as file:
            skills_matrix = file.read()
    except FileNotFoundError:
        return "Skills Matrix file not found."
    try:
        with open(job_advert_file, "r") as file:
            job_advert = file.read().replace("\n", "")
    except FileNotFoundError:
        return "Job Advert file not found."
    prompt1 = (
        f"Here is a job advert: {job_advert}. \n "
        f"Please extract a list of all relevant skills mentioned in this advert. "
        f"Simplify or generalize the terminology where possible to facilitate matching with a skills matrix."
    )
    print("sending job advert for extraction")
    job_advert_list = job_extract(prompt1)
    print("job advert extracted: ")
        # testfile writes
    with open("api_responses.txt", "a") as f:
        f.write(f"API Response: job advert list; {job_advert_list}\n\n")
        # testfile writes
    print(f"API Response: job advert list; {job_advert_list}\n")
    
    prompt2 = (
        f"Here is a skills matrix: {skills_matrix}\nAnd a list of skills from a job advert: {job_advert_list}\n "
        f"please compare the two in a table format."
    )
    ai_response = job_compare(prompt2, job_advert_list)
        # testfile writes
    with open("api_responses.txt", "a") as f:
        f.write(f"API Response: comparison;{ai_response}\n\n")
        # testfile writes
    print(f"API Response: {ai_response}\n")
    print("Compare mode done.")
    return ai_response

# replace skills_matrix.txt with variable from bot
# replace job_advert.txt with actual job_advert scrape result 
if __name__ == "__main__":
    skills_matrix_file = "skills_matrix.txt"
    job_advert_file = "job_advert.txt"
    api_interaction(skills_matrix_file, job_advert_file)
