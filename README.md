# RAG_bot_mvp   

## Setting up the frontend
You can serve the frontend with docker.
For this purpose you have to install docker on your PC. Once this is done run (in the frontend dir)
```
docker build -t bot_mvp .
```
in the console. This sets up the docker container.
To run the docker container, simply run 
```
docker run -p 127.0.0.1:8000:80 bot_mvp
```


## Backend

The backend implements a RAG architecture for the information retrieval:
![RAG Architecture](https://huggingface.co/datasets/huggingface/cookbook-images/resolve/main/RAG_workflow.png)