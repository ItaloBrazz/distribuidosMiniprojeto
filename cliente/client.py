import requests, os, sys
SERVER = os.getenv("SERVER_URL","http://servidor:5000/process")
def send(path):
    with open(path,"rb") as f:
        r = requests.post(SERVER, files={"image": f})
        print(r.status_code, r.text)
if __name__ == "__main__":
    if len(sys.argv)<2:
        print("usage: python client.py <image_path>")
    else:
        send(sys.argv[1])
