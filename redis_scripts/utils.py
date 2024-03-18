from redis import Redis

def connect_to_redis(host, port):
    return Redis(host=host, port=port)