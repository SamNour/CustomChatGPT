import openai
from promptflow import tool
import requests


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

setup_byod(deployment_id)
print("I was here")

def make_query()