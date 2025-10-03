import redis, os, time, json, logging
r = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=int(os.getenv("REDIS_PORT","6379")), db=0)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("stock")

def process(payload):
    log.info("processing %s", payload.get("id"))
    time.sleep(1)
    log.info("done %s", payload.get("id"))

if __name__ == "__main__":
    while True:
        _, item = r.blpop("stock_queue")
        try:
            payload = json.loads(item)
        except Exception:
            continue
        process(payload)
