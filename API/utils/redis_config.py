import redis
# from API.utils.auth import authenticByToken

Pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


