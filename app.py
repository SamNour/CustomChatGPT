import math
import random
import os
import streamlit as st
from streamlit_chat import message
import os
import json
from openai_wrapper import *


##Code added by Yeet for TUMONLINE

st.set_page_config(page_title="BotTUM Chat", page_icon="https://www.tum.de/favicon.ico", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        .stDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

##Code for TUMONLINE API by Yeet:
API_ENDPOINT = "https://campus.tum.de/tumonline/wbservicesbasic."

API_TOKENASK = "requestToken"
API_REQUEST_MONEY = "studienbeitragsstatus"
API_REQUEST_IDENTITY = "id"
API_REQUEST_EXAMS = "noten"

import requests
import os.path
from datetime import datetime
import re

def extract_token_info(text):
    pattern = r'<token>(.*?)</token>'
    matches = re.findall(pattern, text)
    return matches

def requestOrReturnCachedApi(studentID):
    #check if file studentID.json exists:
    #   if yes: return file
    #   if no: request API and save to file

    try:

        if(os.path.isfile(studentID+".json")):
            return open(studentID+".json", "r").read()
        else:
            r = requests.get(url = API_ENDPOINT+API_TOKENASK, params = "?pUsername="+studentID+"&pTokenName=botTUM")
            if(r.status_code != 200):
                print("Error: Request failed with status code "+str(r.status_code))
                return ''

            with open(studentID+".json", "w") as f:
                print(r.text)
                tokenOnly = extract_token_info(r.text)[0]
                print(tokenOnly)
                f.write(tokenOnly)
                f.close()
    
    except Exception as e:
        print("Error: Request failed with error: "+str(e))
        return ''
    return tokenOnly

def requestMoney(API_TOKEN):
    r = requests.get(url = API_ENDPOINT+API_REQUEST_MONEY, params = "?pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return None
        #<?xml version="1.0" encoding="utf-8"?>
        #<rowset>
        #    <row>
        #        <soll>102</soll>
        #        <frist>2024-02-15</frist>
        #        <semester_bezeichnung>Sommersemester 2024</semester_bezeichnung>
        #        <semester_id>24S</semester_id>
        #    </row>
        #</rowset>
    #return only money:102, due date:2024-02-15, semester:Sommersemester 2024
    try:
        parsed = r.text[r.text.index("<soll>")+6:r.text.index("</soll>")]+","+r.text[r.text.index("<frist>")+7:r.text.index("</frist>")]+","+r.text[r.text.index("<semester_bezeichnung>")+22:r.text.index("</semester_bezeichnung>")]
        #parse the date into a date object:
        parts = parsed.split(',')

        # Extract the components
        number = int(parts[0])
        date_str = parts[1]
        semester = parts[2]

        # Convert date string to date object
        date_object = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Create the tuple
        result_tuple = (number, date_object, semester)

        return result_tuple
    except Exception as e:
        print("Error: Parsing failed with error: "+str(e)+"\n"+r.text)
        return ''

def requestName(API_TOKEN):
    r = requests.get(url = API_ENDPOINT+API_REQUEST_IDENTITY, params = "pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return ''
    try:
        parsed = r.text[r.text.index("<vorname>")+9:r.text.index("</vorname>")]+" "+r.text[r.text.index("<familienname>")+14:r.text.index("</familienname>")]
        return ' ' + parsed
    except Exception as e:
        print("Error: Parsing failed")
        print(API_TOKEN)
        print(r.text)
        return ''
    

def requestLastExamResult(API_TOKEN):
    r = requests.get(url = API_ENDPOINT+API_REQUEST_EXAMS, params = "?pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return None
    try:
        parsed = r.text[r.text.index("<lv_titel>")+10:r.text.index("</lv_titel>")]+": "+r.text[r.text.index("<uninotenamekurz>")+17:r.text.index("</uninotenamekurz>")]
        return parsed
    except Exception as e:  
        print("Error: Parsing failed with error: "+str(e)+"  \n"+r.text)
        return None
    


#API_TOKEN = requestOrReturnCachedApi("ge00gok")
#print(requestMoney(API_TOKEN))
#print(requestName(API_TOKEN))
#print(requestLastExamResult(API_TOKEN))
#output:
#(102, datetime.date(2024, 2, 15), 'Sommersemester 2024')
#Max Mustermann
#Analysis 1: 1.0


##Yeet code end.
import requests
import pandas as pd

with st.sidebar:
    st.title('Login With TUMOnline')
    if(os.path.isfile("ge94gok.json")):
        hf_email = "ge94gok"
        hf_pass = requestOrReturnCachedApi(hf_email)
        st.success('Already Logged in with TUMOnline!  \n Welcome' + requestName(hf_pass) + '!', icon='✅')
    else:
        hf_email = st.text_input('Enter TUMID:', type='password')
        #hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email):# and hf_pass):
            st.warning('Please enter your TUMID!', icon='⚠️')
        else:
            check=False
            first=True
            while(check==False):
                #if ((len(hf_email) < 8) or (len(hf_email) > 8)):
                #st.warning('Please enter a valid TUMID!', icon='⚠️')
                #break
                hf_pass = requestOrReturnCachedApi(hf_email)
                if (first and (len(hf_pass) < 30 or len(hf_pass) > 35)):
                    st.warning('Please enter a valid TUMID!', icon='⚠️')
                    first=False
                else:
                    check=True
            st.success('welcome ' + requestName(hf_pass)  + '! You can now use your customized botTUM right after you give access to your API key through TUMOnline!', icon='👉')
    
    st.markdown('ⓘ Find out more about how your data is being treated by [Azure](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy)!')
    st.markdown('Logo used belongs to Technische Universität München.')

    languages = {"English": "en", "German": "de"}
    query_parameters = st.experimental_get_query_params()
    if "lang" not in query_parameters:
        st.experimental_set_query_params(lang="en")
        st.rerun()


    def set_language() -> None:
        if "selected_language" in st.session_state:
            st.experimental_set_query_params(
                lang=languages.get(st.session_state["selected_language"]))
            
    sel_lang = st.radio(
        "Language:",
        options=languages,
        horizontal=True,
        on_change=set_language,
        key="selected_language",
    )

    @st.cache_data(ttl=60*60*12)
    def fetch_emojis():
        resp = requests.get(
            'https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json')
        json = resp.json()
        codes, emojis = zip(*json.items())
        return pd.DataFrame({
            'Emojis': emojis,
            'Shortcodes': [f':{code}:' for code in codes],
        })

    '''
    # Emoji cheatsheet for emoji lovers:
    '''

    # emojis = fetch_emojis()

    # st.table(emojis)

## yeet code end.

#'''
#    Place for UI
#'''


#'''
# Welcome to your chat with BotTUM!
#'''



col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('https://www.tum.de/favicon.ico', width=60)
with col2:
    st.header('Welcome to your chat with BotTUM!')

#st.title("Welcome to your chat with BotTUM!")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "avatar" : 'https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png' , "content": "Hi, how may I help you with your questions about TUM?"}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    

#a tuple of 10 funny questions for TUM:
funny_questions = ("Tell me more about Bachelors in Information Engineering", "Tell me more about Bachelors in Management and Technology :briefcase:", "Tell me more about Bachelors in Mathematics :heavy_division_sign:", "Tell me more about Student Council services :snowman_without_snow:", "Tell me more about Bachelors in Chemistry :crystal_ball:", "Tell me more about Bachelors in Biology :microscope:", "Tell me more about Bachelors in Mechanical Engineering :mechanic:", "Tell me more about how I can apply to TUM :love_letter:", "Tell me more about Bachelors in Aerospace Engineering :gear:", "Tell me more about Bachelors in Civil Engineering :warning:")
picked_question = funny_questions[0]#[math.floor(random.random()*10)]

#st.markdown("***")
#!! Accept voice input
#rerun = st.button('Speak? :studio_microphone:',help="this button will allow you to speak instead of texting using your microphone")

# Accept user input
if prompt := st.chat_input(picked_question):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""


    for response in openai.ChatCompletion.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            deployment_id=deployment_id,
            dataSources=[  # camelCase is intentional, as this is the format the API expects
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "key": search_key,
                        "indexName": search_index_name,
                        "embeddingEndpoint": f"{openai.api_base}/openai/deployments/ada-tt/embeddings?api-version={openai.api_version}",
                        "embeddingKey": openai.api_key,
                        "queryType": "vectorSimpleHybrid",
                        "roleInformation": "Your name is botTUM. You are a helpful and kind assistant for students at the Technical University of Munich (Technische Universität München). Your job is to answer students’ queries about their studies. Be brief in your answers. You should answer only with the facts listed in the list of sources below. If there is not enough information below, say you don’t know. Do not generate answers that don’t use the sources below. If asking a clarifying question to the user would help, ask the question. Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, e.g. [info1.txt]. Don’t combine sources, list each source separately, e.g. [info1.txt][info2.pdf][info3.pptx][info4.docx]."
                    }
                }
            ],
            temperature=.4,
            stream=True
        ):
            print(response)
            full_response += (response["choices"][0]["delta"].get("content", None) or "")
            message_placeholder.markdown(full_response + "▌")
    else:
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

