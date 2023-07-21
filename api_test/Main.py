import openai
from dotenv import load_dotenv
import os
# ToDo: change files from txt to json.

load_dotenv()

api_key = os.getenv("API_KEY")
if api_key is None:
    print("Error: API_KEY not found in .env file")
    raise ValueError("API_KEY not found in .env file")
openai.api_key = api_key


# Function to chat with GPT-3
def job_extract(prompt):
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
                "Use this information to create a comprehensive list of skills found in the job advert."
            },
            {
                "role": "user", "content": prompt
            }
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.1,
    )
    print("API prompted")
    return response.choices[0].message['content'].strip()


def chat_with_gpt3(prompt, job_advert_list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Given the extracted list of skills from the job advert: " + str(job_advert_list) +
               "\nand the provided skills matrix, generate a table with the following columns: 'Required Skill,' 'In Skills Matrix,' 'Level of Proficiency.' " +
               "\nIn the 'Skill/Experience' column, list all the skills extracted from the job advert. " +
               "\nFor each listed skill, check if it appears in the provided skills matrix. If it does, indicate 'Yes' in the 'In Skills Matrix' column and provide the level of proficiency from the skills matrix in the 'Level of Proficiency' column. " +
               "\nIf a skill doesn't appear in the skills matrix, indicate 'No' in the 'In Skills Matrix' column and leave the 'Level of Proficiency' column empty. " +
               "\nConsider variations in terminology, phrasing, or spelling that might indicate a match between a skill in the job advert and a skill in the skills matrix."

            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.1,
    )
    print("API prompted")
    return response.choices[0].message['content'].strip()


def api_interaction(skills_matrix_file, job_advert_file):
    print("Compare mode started.")
    try:
        with open(skills_matrix_file, 'r') as file:
            skills_matrix = file.read()
    except FileNotFoundError:
        return "Skills Matrix file not found."

    try:
        with open(job_advert_file, 'r') as file:
            job_advert = file.read().replace('\n', '')
    except FileNotFoundError:
        return "Job Advert file not found."
    prompt1 = f"Here is a job advert: {job_advert}. \n " \
              f"Please extract a list of all relevant skills mentioned in this advert. " \
              f"Simplify or generalize the terminology where possible to facilitate matching with a skills matrix."
    print("sending job advert for extraction")
    job_advert_list = job_extract(prompt1)
    print("job advert extracted: ")
    print(f'API Response: job advert list; {job_advert_list}\n')
    prompt2 = f"Here is a skills matrix: {skills_matrix}\nAnd a list of skills from a job advert: {job_advert_list}\n " \
              f"please compare the two in a table format."
    ai_response = chat_with_gpt3(prompt2, job_advert_list)


    with open('api_responses.txt', 'a') as f:
        f.write(f'API Response: {ai_response}\n\n')
    print(f'API Response: {ai_response}\n')
    print("Compare mode done.")
    return ai_response


if __name__ == "__main__":
    skills_matrix_file = "skills_matrix.txt"
    job_advert_file = "job_advert.txt"
    api_interaction(skills_matrix_file, job_advert_file)