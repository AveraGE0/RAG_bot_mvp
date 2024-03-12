from flask import Flask
from flask import request, jsonify
from markupsafe import escape
from flask_cors import CORS


__OK__ = 200
__INTERNAL_ERROR__ = 400
__NOT_FOUND__ = 404 


app = Flask(__name__)
# allow cross-origin requests
cors = CORS(app, resources={r"/bot": {"origins": "*"}})


@app.route("/bot", methods=['POST'])
def parse_request():
    # escape cause we dont like hackers
    prompt = escape(request.json["prompt"])
    if not prompt:
        return jsonify("Give me a prompt retard"), __OK__
    else:
        return jsonify({"response": "Backend barebone is working!"}), __OK__


if __name__ == '__main__':
    app.run()