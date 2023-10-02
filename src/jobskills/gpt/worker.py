from jobskills.jobqueue import get_redis_settings
from gpt import api_interaction



from jobskills.jobqueue import get_queue, get_redis_settings

async def gpt_handler(arq_ctx, scraped_data, file_content):
    
    return api_interaction(file_content, scraped_data)



class WorkerSettings:
    functions = [gpt_handler]
    queue_name = "arq:openai"


    redis_settings = get_redis_settings()

