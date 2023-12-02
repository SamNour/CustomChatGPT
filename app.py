import openai
import os
import streamlit as st
from streamlit_chat import message
import os, requests

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

#API_TOKEN = "38082AA281635080C59ED8BCFE0B91F1"#meh forgot to remove so will cancel this put anyways

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
                tokenOnly = extract_token_info(r.text)[0]
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
    r = requests.get(url = API_ENDPOINT+API_REQUEST_IDENTITY, params = "?pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return ''
    try:
        parsed = r.text[r.text.index("<vorname>")+9:r.text.index("</vorname>")]+" "+r.text[r.text.index("<familienname>")+14:r.text.index("</familienname>")]
        return parsed
    except Exception as e:
        print("Error: Parsing failed")
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
        print("Error: Parsing failed with error: "+str(e)+"\n"+r.text)
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
        st.success('Already Logged in with TUMOnline!', icon='✅')
        hf_email = "ge94gok"
        hf_pass = requestOrReturnCachedApi(hf_email)
        st.info('Welcome ' + requestName(hf_email))
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
                st.warning('Please enter a valid TUMID!', icon='⚠️')
                #break
                hf_pass = requestOrReturnCachedApi(hf_email)
                if (first and (len(hf_pass) < 30 or len(hf_pass) > 35)):
                    st.warning('Please enter a valid TUMID!', icon='⚠️')
                    first=False
                else:
                    check=True
            st.success('welcome ' + requestName(hf_pass)  + '! You can now use your customized botTUM right after you give access to your API key through TUMOnline!', icon='👉')
    
    st.markdown('ⓘ Find out more about how your data is being treated by [Azure](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy)!')
    st.markdown('Logo used belong to Technische Universität München.')

    languages = {"English": "en", "German": "de"}

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
    # Streamlit emoji shortcodes

    Below are all the emoji shortcodes supported by Streamlit.

    Shortcodes are a way to enter emojis using pure ASCII. So you can type this `:smile:` to show this
    :smile:.

    (Keep in mind you can also enter emojis directly as Unicode in your Python strings too — you don't
    *have to* use a shortcode)
    '''

    emojis = fetch_emojis()

    st.table(emojis)

    query_parameters = st.experimental_get_query_params()
    if "lang" not in query_parameters:
        st.experimental_set_query_params(lang="en")
        st.experimental_rerun()


    def set_language() -> None:
        if "selected_language" in st.session_state:
            st.experimental_set_query_params(
                lang=languages.get(st.session_state["selected_language"]))

    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')

    sel_lang = st.radio(
        "Language",
        options=languages,
        horizontal=True,
        on_change=set_language,
        key="selected_language",
    )


## yeet code end.



#'''
#    Place for the AI keys and stuff
#'''
openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup
openai.api_base = "https://openai-bottum-france.openai.azure.com/" # Add your endpoint here
openai.api_key = os.getenv("OPENAI_API_KEY") # Add your OpenAI API key here
deployment_id = "gpt-4-tt" # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://azureaisearch-bottum.search.windows.net"; # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY"); # Add your Azure AI Search admin key here
search_index_name = "michelle2"; # Add your Azure AI Search index name here


def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(deployment_id)

#'''
#    Place for UI
#'''



st.title("Welcome to your chat with BotTUM!")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "avatar" : 'https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png' , "content": "Hi, how may I help you with your questions about TUM?"}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    

# Accept user input
if prompt := st.chat_input("Tell me more about Bachelors in Information Engineering"):
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
                    }
                }
            ],
            stream=True
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
    else:
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})




