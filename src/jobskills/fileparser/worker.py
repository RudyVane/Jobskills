from fileparser import file_parsing

from jobskills.jobqueue import get_redis_settings


async def fileparser_handler(arq_ctx, file):
    return file_parsing(file)


class WorkerSettings:
    functions = [fileparser_handler]
    queue_name = "arq:parsing"

    redis_settings = get_redis_settings()
