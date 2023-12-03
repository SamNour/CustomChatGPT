#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 0.28.1 or lower.
import os
import openai
import requests

openai.api_type = "azure"
openai.api_base = "https://openai-bottum-france.openai.azure.com/"
openai.api_version = "2023-08-01-preview"
openai.api_key = '13f668bdda354088ba9c441486d90c57'
deployment_id = "gpt-4-tt"

message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."}]


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

inp = {'messages': [
    {'role': 'assistant', 'content': '\nsystem:\nYou are an AI model that can detect intention from provided unstructured data.\nYou can categorize intents for every question you get from the user. Your answers are based on the intent specification and the guidelines. If the specific intent specifications are provided for the identified intent, then add this information to the general guidelines.\nAlways specify the detected intent(s) and output their names.\nA user question can have exactly one intent. \nPlease calculate the certainty with which you classified this intent as a value from 0 (lowest)to 1 (highest).\nIf the certainty is higher than 0.9 output the chosen category otherwise change it to "Program Manager, custom study plan or other".\nOnly output the name of the final intent. Do not output anything else.\n\nThe intentions you can detect are:\n\n"Emotional, Personal or Sensitive",\n\n"Engineering and Natural Sciences",\n\n"Modules and Courses",\n\n"Thesis",\n\n"Bachelor\'s Thesis",\n\n"Master\'s Thesis",\n\n"Documents",\n\n"Grade Management",\n\n"Application",\n\n"Certificates, Credit transfers, Transcript of records, Project studies",\n\n"Course Schedules",\n\n"Registration Problems",\n\n"Examination board Applications",\n\n"Going Abroad",\n\n"Incoming Exchange Students",\n\n"International Partners",\n\n"Doctoral Program",\n\n"Orientation and Getting started",\n\n"Program Manager, custom study plan or other". \n\n'},
    {'role': 'user', 'content': 'd'}], 'engine': 'gpt-4-tt', 'temperature': 0.4
}

completion = openai.ChatCompletion.create(
  **inp
)
print(completion)