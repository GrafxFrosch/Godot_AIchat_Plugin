from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI


# Initialize the Azure model from the local AzurChat module



# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def getAzure(endpoint:str,apikey:str):
    return AzureChatOpenAI(
        azure_endpoint=endpoint,
        model="gpt-4o-mini",
        api_key= apikey,
        api_version="2024-08-01-preview",
    )

def ask_model(prompt: str) -> str:
    """
    Queries the Azure model and returns the cleaned text response.
    """
    response = model.invoke(prompt)

    # Check if response contains a message object with a content attribute
    if hasattr(response, "content"):
        return response.content.strip()
    return str(response).strip()


# ==============================================================================
# STATE DEFINITIONS (TypedDicts)
# ==============================================================================

class InputState(TypedDict):
    """Defines the structure for input data passed to the graph."""
    user_input: str
    history: str


class OutputState(TypedDict):
    """Defines the structure for output data produced by the graph."""
    output: TypedDict


# ==============================================================================
# GRAPH NODES
# ==============================================================================

def generate_response(state: InputState) -> dict:
    """
    Node 1: Generates a response based on the user input and conversation history.
    """
    prompt =  f"""
    You are Integrated in a Godot Project as an helpful AI assistant you execute the following prompt:
    {state["user_input"]}
    """
    # Invoke model with user input combined with the system prompt instructions
    response = ask_model(state["user_input"] + " Your task:" + prompt)
    return {"output": response}


# ==============================================================================
# GRAPH CONSTRUCTION
# ==============================================================================

# Initialize the StateGraph with the defined state schemas
builder = StateGraph(
    state_schema=OutputState,
    input_schema=InputState,
    output_schema=OutputState
)

# Add nodes to the graph
builder.add_node("response", generate_response)

# Define the workflow edges
builder.add_edge(START, "response")
builder.add_edge("response", END)

# Compile the graph into an executable state machine
graph = builder.compile()


# ==============================================================================
# INTERFACE FUNCTIONS (Exported)
# ==============================================================================

def askChatter(input: str, history: str) -> str:
    """
    Main interface to interact with the chatter agent.
    Invokes the graph logic and returns the resulting dictionary.
    """
    result = graph.invoke({"user_input": input, "history": history})
    return result


# ==============================================================================
# MAIN EXECUTION (Entry Point)
# ==============================================================================
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--history", default="")
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--apikey", required=True)
    args = parser.parse_args()

    model = getAzure(args.endpoint, args.apikey)
    print(askChatter(args.prompt, args.history))