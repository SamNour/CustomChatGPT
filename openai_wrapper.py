import openai
from promptflow import tool
import requests
from typing import Optional


# Place for the AI keys and stuff
openai.api_type = "azure"
openai.api_version = "2023-08-01-preview"
openai.api_base = "https://openai-bottum-france.openai.azure.com/"
openai.api_key = '13f668bdda354088ba9c441486d90c57'
deployment_id = "gpt-4-tt"

search_endpoint = "https://azureaisearch-bottum.search.windows.net"
search_key = 'NElngw2d8eVnBatvpiJlfcAT3l6FrfmFQGINybEenIAzSeD4xiue'
search_index_name = "index-tt11"

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

def disable_byod():
    openai.requestssession = None


def make_query(
        messages,
        stream: bool,
        use_search: bool,
        system_prompt: str = 
            """system:
Your name is botTUM. You are:
- a helpful and kind assistant for students at the Technical University of Munich (Technische Universität München). Your job is to answer students’ queries about their studies and student life. If the student asks you to write an email or write a todo list, do it. You always strive to give answers specific to the student and personalize them as much as you can. Be brief in your answers.
- a good friend to the students at the Technical University of Munich (Technische Universität München). You have to be able to detect the sentiment of the student (happy/sad/anxious/worried/angry) and respond accordingly. End your responses with a suitable emoji.

You should answer only with the facts listed in the list of sources below. If there is not enough information below, admit you don't know or. If asking a clarifying question to the student would help, ask the question.
Do not generate answers that don’t use the sources below.

If you know which study program the student belongs to and are asked about something related about the study program that you don't know about, tell the student that their inquiry can be answered by the corresponding TUM program manager.
Advise the student to contact the the program manager for a personal consultation or more information by giving them all contact information you have on their program manager.
Include in your output an additional link to the resource with all contacts here: https://www.mgt.tum.de/programs/bachelor-management-technology/munich/for-current-students#c1771

If it is unknown which study program the student belongs to, inform them that they can also send in a request form to the student council with the following link:
https://www.mgt.tum.de/forms/contact-for-further-topics.

Also give the resources on the general student advisory to the student for legal, mental health or stress management consultation. 

Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, e.g. [info1.txt]. Don’t combine sources, list each source separately, e.g. [info1.txt][info2.pdf][info3.pptx][info4.docx].
            """,
        tool_prompt: Optional[str] = None):
    if tool_prompt:
        system_prompt += "\n" + tool_prompt
    if not use_search:
        messages = [{
            "role": "assistant",
            "content": system_prompt
        }] + messages
    else:
        setup_byod(deployment_id)
    
    inp = {
        "messages": messages,
        **({"deployment_id": deployment_id,
            "dataSources": [  # camelCase is intentional, as this is the format the API expects
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": search_endpoint,
                    "key": search_key,
                    "indexName": search_index_name,
                    "embeddingEndpoint": f"{openai.api_base}/openai/deployments/ada-tt/embeddings?api-version={openai.api_version}",
                    "embeddingKey": openai.api_key,
                    "queryType": "vectorSimpleHybrid",
                    "roleInformation": system_prompt
                }
            }
        ]} if use_search else {
            "engine": deployment_id
        }),
        "temperature": .4,
        **({"stream": stream} if stream else {})
    }
    try:
        return openai.ChatCompletion.create(**inp)
    finally:
        disable_byod()



def main_process(messages, use_old: bool):
    if not messages:
        return []
    
    if use_old:
        return make_query(
            messages,
            True, True
        )

    # Detecting an intent
    with open("./prompts/chat.txt", "r") as file:
        res = make_query(messages, False, False, "", file.read())
    
    categories = {
        "Emotional, Personal or Sensitive": "./refer_to_manager.txt",
        "Modules and Courses": "./ground_courses.txt",
        "Thesis": "./group_thesis.txt",
        "Bachelor's Thesis": "./ground_bachelor.txt",
        "Master's Thesis": "./ground_masters.txt",
        "Documents": "./ground_documents.txt",
        "Grade Management": "./ground_grade.txt",
        "Application": "./ground_application.txt",
        "Certificates, Credit transfers, Transcript of records, Project studies":  "./ground_certificates.txt",
        "Course Schedules": "./ground_schedules.txt",
        "Registration Problems": "./ground_registration.txt",
        "Examination board Applications": "./ground_examination_board.txt",
        "Going Abroad": "./ground_going_abroad.txt",
        "Incoming Exchange Students": "./ground_incoming_exchange.txt",
        "International Partners": "./ground_international_pa"
    }