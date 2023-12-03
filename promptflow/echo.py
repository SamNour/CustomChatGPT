from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def collect_responses(input1: str, input2: str, input3: str,
input4: str, input5: str, input6: str, input1: str) -> str:
    return 'hello ' + input1