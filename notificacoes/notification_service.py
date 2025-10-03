from flask import Flask, request, jsonify
import os, logging, redis, json

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST","redis"), port=int(os.getenv("REDIS_PORT","6379")), db=0)
logging.basicConfig(level=logging.INFO)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json() or {}
    try:
        r.rpush("notifications", json.dumps(data))
    except Exception:
        pass
    app.logger.info("notify: %s", data)
    return jsonify({"status":"ok"}), 200

@app.route("/poll", methods=["GET"])
def poll():
    msgs = []
    while True:
        item = r.lpop("notifications")
        if not item:
            break
        msgs.append(json.loads(item))
    return jsonify(msgs), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
