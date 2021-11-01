import redis
from config_parser import env
from actions.log_config import logger

redis_host = env["redis"]["host"]
redis_port = env["redis"]["port"]


r = redis.Redis(host=redis_host, port=redis_port, db=6, decode_responses=True)

def get_parent_button(schoolId):
    try:
        logger.info("connected to redis server successfully")
        query = f"schoolid:{schoolId}"
        logger.info(f"School data is:\n{r.hgetall(query)}")
        return r.hgetall(query)
    except Exception as e:
        logger.exception("Error message: {e}")
        raise ConnectionError

def read_obj(id):
    try:
        query = f"buttonid:{id}"
        logger.info("connected to redis server successfully")
        logger.info(f"button object data is:\n{r.hgetall(query)}")
        return r.hgetall(query)
    except Exception as e:
        logger.exception("Error message: {e}")
        raise ConnectionError





