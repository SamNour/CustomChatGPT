import openai, os, requests

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


message_text = [{"role": "user", "content": "What are the differences between Azure Machine Learning and Azure AI services?"}]
# message_text = [{"role": "user", "content": message_text}]
completion = openai.ChatCompletion.create(
        messages=message_text,
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
        ]
    )
print(completion)