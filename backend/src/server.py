from flask import Flask
from flask import request, jsonify
from markupsafe import escape
from flask_cors import CORS
from backend.src.rag import RAG
import requests
import json

__OK__ = 200
__INTERNAL_ERROR__ = 400
__NOT_FOUND__ = 404 


rag = RAG()
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
        prompt = f"Answer this question: {prompt}\nAnswer shortly."
        # Define the data to be sent
        data = {
            "model": "llama2",
            "prompt": prompt,
            "keep_alive": 0
        }
        response = requests.post("127.0.0.1:11434", data=json.dumps(data), headers={'Content-Type': 'application/json'}, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Process the stream of responses
            for line in response.iter_lines():
                if line:  # filter out keep-alive new lines
                    json_response = json.loads(line.decode('utf-8')) #this is the response to integrate in return
                    if json_response.get('done'):
                        break
                    print(json_response["response"], end='')
                    # Check if this is the final piece of the response

        else:
            print("Error:", response.status_code)

        #return jsonify({"response": rag.get_top_k_embeddings(prompt)[0].page_content}), __OK__ #integrate to here
        return json_response, __OK__


if __name__ == '__main__':
    app.run()