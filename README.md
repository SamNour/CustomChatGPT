# UI for BotTUM Custom AI bot for TUM students and possible TUM students

The initial UI elements have been forked from https://github.com/MG-Microsoft/CustomChatGPT[original]

### What is this?
This is a UI implementation done with Python that contacts Azure OpenAI servers with custom API to retrieve responds to questions with LLM specifically curated for people interested in TUM questions.

It was implemented in the Hackathon between TUM and Microsoft.
### How to run it?

after cloning the repo,
with python 3.10+ in Windows:
```python
pip install -p .\requirements.txt
```
with python 3.10+ in Linux:
```python
pip install -p requirements.txt
```
after installing requirements, you can initialize the Streamlit GUI using:
```python
streamlit run app.py --server.port=8082 --server.address=0.0.0.0
```
after that, in Windows, the server will run on localhost:8082 and on 0.0.0.0:8082 in Linux.
