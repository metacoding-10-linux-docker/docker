from flask import Flask, Response, send_file
import os

app = Flask(__name__)

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
      <body>
        <h2>NGINX CACHE</h2>
      </body>
    </html>
    """
    return Response(html, mimetype="text/html")
  
# 이미지 요청
@app.route("/image.png")
def get_image():
    image_path = os.path.join(os.path.dirname(__file__), "image.png")
    return send_file(image_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)