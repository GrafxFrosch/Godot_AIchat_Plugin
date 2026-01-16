from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI  # Wir nutzen ChatOpenAI für den Key
import argparse


# ==============================================================================
# STATE DEFINITIONS
# ==============================================================================

class AgentState(TypedDict):
    """
    Der State hält alle Daten während der Ausführung des Graphen.
    """
    user_input: str
    history: str
    output: str  # Hier speichern wir das Ergebnis


# ==============================================================================
# GRAPH NODES
# ==============================================================================

def generate_response(state: AgentState):
    """
    Node: Generiert eine Antwort basierend auf dem Input.
    'model' muss global oder im Scope verfügbar sein.
    """
    prompt = f"""
    You are integrated in a Godot Project as a helpful AI assistant.
    History: {state["history"]}
    User Input: {state["user_input"]}
    """

    # Aufruf des Modells (model wird unten initialisiert)
    response = model.invoke(prompt)

    # Rückgabe des Updates für den State
    return {"output": response.content}


# ==============================================================================
# GRAPH CONSTRUCTION
# ==============================================================================

def create_graph():
    # Wir definieren den Graphen mit dem AgentState
    builder = StateGraph(AgentState)

    # Node hinzufügen
    builder.add_node("response_node", generate_response)

    # Ablauf definieren
    builder.add_edge(START, "response_node")
    builder.add_edge("response_node", END)

    return builder.compile()


# ==============================================================================
# INTERFACE FUNCTIONS
# ==============================================================================

def askChatter(user_query: str, history: str, compiled_graph) -> str:
    """
    Startet den Graphen mit den entsprechenden Inputs.
    """
    inputs = {
        "user_input": user_query,
        "history": history
    }
    result = compiled_graph.invoke(inputs)
    return result["output"]


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--history", nargs='?', default="")  # Das '?' erlaubt leere Werte
    parser.add_argument("--apikey", required=True)
    args = parser.parse_args()

    # 1. Modell initialisieren mit dem übergebenen Key
    # Hier kannst du 'gpt-4o' oder 'gpt-3.5-turbo' nutzen
    model = ChatOpenAI(openai_api_key=args.apikey, model="gpt-4o-mini")

    # 2. Graph erstellen
    graph = create_graph()

    # 3. Ausführen und Ergebnis drucken
    final_output = askChatter(args.prompt, args.history, graph)
    print(final_output)