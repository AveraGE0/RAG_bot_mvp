from flask import Flask, Response, request, jsonify, make_response
from markupsafe import escape
from flask_cors import CORS
from backend.src.rag import RAG
from backend.src.config import LLM_URL
import requests
import json
import logging

__OK__ = 200
__INTERNAL_ERROR__ = 500
__NOT_FOUND__ = 404 


logger = logging.getLogger(__name__)

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
        try:
            response = requests.post(LLM_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'}, stream=True)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Cannot reach the LLM on {LLM_URL}. Is the LLM server started?")
            error_response = make_response('', __INTERNAL_ERROR__)
            error_response.status = f"{__INTERNAL_ERROR__} Sorry, could not reach the LLM server."
            return error_response

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