import redis
from helpers.envVars import redisHost, redisPort

client = redis.Redis(host=redisHost, port=redisPort)

def setData(key, value):
    client.set(key, value)

def getData(key):
    value = client.get(key)
    return value

def delData(key):
    value = client.delete(key)
    return value 