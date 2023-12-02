import openai, os, requests

openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
# openai.api_version = "2023-10-01-preview"

# Azure OpenAI setup
api_base = "https://openai-bottum-france.openai.azure.com/" # Add your endpoint here
# openai.api_key = os.getenv("OPENAI_API_KEY") # Add your OpenAI API key here
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
            request.url = f"{api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(deployment_id)


message_text = [{"role": "user", "content": "What are the differences between Azure Machine Learning and Azure AI services?"}]

client = openai.AzureOpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    azure_endpoint=api_base,
    api_version="2023-07-01-preview"
)

completion = client.chat.completions.create(
    messages=message_text,
    model=deployment_id,
    extra_body={"dataSources": [  # camelCase is intentional, as this is the format the API expects
        {
            "type": "AzureCognitiveSearch",
            "parameters": {
                "endpoint": search_endpoint,
                "key": search_key,
                "indexName": search_index_name,
                # "accessToken": "c8yQH07JcPuFIhVg38bdbKGTTqjUGMw1f8EnLgfhVAAzSeCZqqcK"
            }
        }
    ]}
)
print(completion)