import openai
from dotenv import load_dotenv
import os

# Load OpenAI API key
load_dotenv()
api_key = os.getenv("API_KEY")
openai.api_key = api_key


# Function to chat with GPT-3
def chat_with_gpt3(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.8,
    )
    print("API prompted")
    return response.choices[0].message['content'].strip()


def compare_mode_interaction(skills_matrix_file, job_advert_file):
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

    prompt = f"Here is a skills matrix: {skills_matrix}\nAnd a job advert: {job_advert}\nWhat is the percentage of matching skills?"

    ai_response = chat_with_gpt3(prompt)

    with open('api_responses.txt', 'a') as f:
        f.write(f'API Response: {ai_response}\n')

    print("Compare mode done.")
    return ai_response


if __name__ == "__main__":
    skills_matrix_file = "skills_matrix.txt"
    job_advert_file = "job_advert.txt"
    compare_mode_interaction(skills_matrix_file, job_advert_file)