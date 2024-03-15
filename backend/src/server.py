from flask import Flask, Response, request, jsonify
from markupsafe import escape
from flask_cors import CORS
from backend.src.rag import RAG
import requests
import json
import re

__OK__ = 200
__INTERNAL_ERROR__ = 400
__NOT_FOUND__ = 404 


rag = RAG()
app = Flask(__name__)
# allow cross-origin requests
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/bot", methods=['POST'])
def parse_request():
    # escape cause we dont like hackers
    prompt = escape(request.json["prompt"])
    if not prompt:
        return jsonify("Give me a prompt retard"), __OK__
    else:
        prompt = rag.get_prompt(prompt)

        # Define the data to be sent
        data = {
            "model": "llama2",
            "prompt": prompt,
            "keep_alive": 0
        }
        response = requests.post("http://127.0.0.1:11434/api/generate", data=json.dumps(data), headers={'Content-Type': 'application/json'}, stream=True)

        if response.status_code == 200:
            # Define a generator function that yields chunks of data
            def generate():
                for chunk in response.iter_content(chunk_size=8096):
                    yield chunk
            # Stream the response back to the client
            return Response(generate(), content_type=response.headers['Content-Type'])
        else:
            return jsonify({'error': 'Failed to get response from Ollama API'}), response.status_code

        #return jsonify({"response": rag.get_top_k_embeddings(prompt)[0].page_content}), __OK__ #integrate to here
        return json_response, __OK__


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)