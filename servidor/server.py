from flask import Flask, request, jsonify
from PIL import Image
import os, uuid, redis, requests, io, json
from datetime import datetime

app = Flask(__name__)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "http://notificacoes:5001/notify")

def to_grayscale(img):
    return img.convert("L").convert("RGB")

def to_sepia(img):
    sep = img.convert("RGB")
    width, height = sep.size
    pixels = sep.load()
    for x in range(width):
        for y in range(height):
            r0,g0,b0 = pixels[x,y]
            tr = int(0.393*r0 + 0.769*g0 + 0.189*b0)
            tg = int(0.349*r0 + 0.686*g0 + 0.168*b0)
            tb = int(0.272*r0 + 0.534*g0 + 0.131*b0)
            pixels[x,y] = (min(255,tr), min(255,tg), min(255,tb))
    return sep

def vintage(img):
    g = img.convert("L")
    g = g.point(lambda p: p * 0.9)
    return g.convert("RGB")

@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error":"no image"}), 400
    f = request.files["image"]
    try:
        img = Image.open(io.BytesIO(f.read()))
    except Exception as e:
        return jsonify({"error":"invalid image"}), 400
    uid = str(uuid.uuid4())[:8]
    basename = f"{uid}"
    bw = to_grayscale(img)
    sep = to_sepia(img)
    vint = vintage(img)
    bw_path = os.path.join(OUTPUT_DIR, f"{basename}_bw.jpg")
    sep_path = os.path.join(OUTPUT_DIR, f"{basename}_sepia.jpg")
    vint_path = os.path.join(OUTPUT_DIR, f"{basename}_vintage.jpg")
    bw.save(bw_path, "JPEG")
    sep.save(sep_path, "JPEG")
    vint.save(vint_path, "JPEG")
    payload = {
        "id": basename,
        "files": [os.path.basename(bw_path), os.path.basename(sep_path), os.path.basename(vint_path)],
        "time": datetime.utcnow().isoformat()
    }
    r.rpush("stock_queue", json.dumps(payload))
    try:
        requests.post(NOTIFICATION_URL, json=payload, timeout=2.0)
    except Exception:
        pass
    return jsonify(payload), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
