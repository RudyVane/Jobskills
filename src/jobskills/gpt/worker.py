from jobskills.jobqueue import get_redis_settings
from gpt import api_interaction


async def gpt_handler(ctx, job_id):
    # Fetch the scraped content and resume file from Redis using the unique identifier
    scraped_content = await ctx['redis'].get(job_id + "_scraped")
    resume_content = await ctx['redis'].get(job_id + "_resume")
    
    # Pass the scraped content and resume to the GPT script for comparison
    result = api_interaction(resume_content, scraped_content)
    
    # Handle the result as needed (e.g., send back to the user on Discord)



class WorkerSettings:
    functions = [gpt_handler]
    queue_name = "arq:openai"


    redis_settings = get_redis_settings()

