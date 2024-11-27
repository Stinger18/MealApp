from typing import Annotated, Literal, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool, BaseTool
# Langgraph imports
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph # Used for typing
from langgraph.checkpoint.memory import MemorySaver
# Project file imports
try:
    from app import crud, models
except ImportError:
    import crud, models
    from database import SessionLocal

from colorama import Fore, Style
from dotenv import load_dotenv
import os
import time
import sys


# Load environment variables
load_dotenv()

# Get tavily search api key
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

class SousChef:
    def __init__(self, tools: list[BaseTool], userInfo: (models.User | None) = None):
        self.tools = tools
        self.tool_node = ToolNode(self.tools)
        self.model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("GPT_API_KEY")).bind_tools(self.tools)
        self.user = userInfo

    # Define the function that determines whether to continue or not
    def should_continue(self, state: MessagesState) -> Literal["tools", END]: # type: ignore
        messages = state['messages']
        last_message = messages[-1]
        # print(last_message)
        # If the LLM makes a tool call, then we route to the "tools" node
        if last_message.tool_calls:
            return "tools"
        # Otherwise, we stop (reply to the user)
        return END
        
    # Define the function that calls the model
    def call_model(self, state: MessagesState):
        messages = state['messages']
        response = self.model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}
    
    def process_user_info(self, state: MessagesState):
        '''Pass initial user data and instructions into the agent'''
        message = state['messages'][-1].content
        if self.user:
            initial_message = [SystemMessage(content=f"You are a personal sous-chef assistant named Sous-Chef."
                                                    f"Use the user's information below to recommend recipes, manage their pantry, and answer any cooking questions. "
                                                    f"My Info: {self.user}"),
                                HumanMessage(content=message)]
        else:
            initial_message = [SystemMessage(content="You are a personal sous-chef assistant named Sous-Chef. Help users find recipes, manage their pantry, and answer cooking questions."),
                                HumanMessage(content=message)]
        
        # Invoke model with the initial system message
        response = self.model.invoke(initial_message)
        return {"messages": [response]}

    
    def ceate_agent(self):
        # Define a new graph
        workflow = StateGraph(MessagesState)
        # Add the nodes
        workflow.add_node('process_user_info', self.process_user_info)
        workflow.add_node('agent', self.call_model)
        workflow.add_node('tools', self.tool_node)

        # Set the entrypoint as `process_user_info`
        # This means that this node is the first one called
        workflow.add_edge(START, 'process_user_info')
        # Next call the agent and get ready
        # workflow.add_edge('process_user_info', 'agent')

        # We now add a conditional edge
        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "process_user_info",
            # Next, we pass in the function that will determine which node is called next.
            self.should_continue,
        )

        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        workflow.add_edge("tools", 'agent')

        # Initialize memory to persist state between graph runs
        checkpointer = MemorySaver()

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        # meaning you can use it as you would any other runnable.
        # Note that we're (optionally) passing the memory when compiling the graph
        sousChef = workflow.compile(checkpointer=checkpointer)
        return sousChef

## Build the Agents tools
@tool
def searchWeb(query: str): # Travily Search
    '''Search the web to return new recipes to the human '''
    search = TavilySearchResults(max_results=3)
    return search.invoke(query)

@tool
def get_all_recipes(recipeID: str) -> list[dict]: # Database Search
    '''Return all the recipe titles the human already has by using recipeID'''
    # print('tool called')
    # print(recipeID)
    try:
        recipes: models.Recipe = crud.get_all_recipes(db=SessionLocal(), userRecipeId=recipeID)
        # Format the recipes for the agent
        formatted_recipes = [
            {"name": recipe.title}
            for recipe in recipes
        ]
        return formatted_recipes
    except Exception as e:
        print('error happend:', e)
        return {
            "error": f"An error occurred while retrieving the recipes: {e}"
        }
    # return [{'name': 'Creamy Tuscan Chicken', 'ingredients': 'chicken, garlic, spinach, sun-dried tomatoes, heavy cream, parmesan cheese', 'instructions': '1. Season the chicken with salt and pepper. 2. Heat the oil in a large skillet over medium-high heat. 3. Add the chicken and cook until golden brown on both sides. 4. Remove the chicken from the skillet and set aside. 5. Add the garlic to the skillet and cook until fragrant. 6. Add the spinach and sun-dried tomatoes and cook until the spinach is wilted. 7. Add the heavy cream and parmesan cheese and bring to a simmer. 8. Return the chicken to the skillet and cook until the sauce has thickened. 9. Serve the chicken with the sauce.'}]

# @tool
# def add_recipe_to_db():
#     '''Add the recipe the human likes to the database'''
#     return f'Recipe was added to the database.'

@tool
def get_pantry(pantryID: str) -> list[dict]: # Pantry Search
    '''Return pantry for ingredients the human already has by using pantryID'''
    try:
        pantry: models.Pantry = crud.get_pantry(db=SessionLocal(), userPantryId=pantryID)
        # Format the pantry for the agent
        formatted_pantry = [
            {"item": ingredient.item, "quantity": ingredient.quantity}
            for ingredient in pantry
        ]
        return formatted_pantry
    except Exception as e:
        print('error happend:', e)
        return {
            "error": f"An error occurred while retrieving the pantry: {e}"
        }

# @tool
# def add_to_pantry(ingredients: list):
#     '''Add ingredients to the pantry'''
#     return f'{ingredients} were added to the pantry.'

# @tool
# def remove_from_pantry(ingredients: list):
#     '''Remove ingredients from the pantry'''
#     return f'{ingredients} were removed from the pantry.'

tools = [searchWeb, get_all_recipes]
# add_recipe_to_db, get_pantry, add_to_pantry, remove_from_pantry

# Can build with these tools or call SousChef(tools) outside of this file to make a new agent with different tools
def buildSousChef(userInfo: models.User = None) -> CompiledStateGraph:
    sousChef = SousChef(tools, userInfo).ceate_agent()
    return sousChef

# Function to print text with typing effect
def typing_effect(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the text is printed

def main():
    ''' Setup the agent when ran locally '''
    db = SessionLocal()
    user: (models.User | None) = crud.get_user_by_id(db=db, userId=1)
    print(user)
    sousChef: CompiledStateGraph = buildSousChef(userInfo=user)
    print(Fore.GREEN + "Sous-Chef here! What can I help you with today? ")
    while True:
        print(Fore.RED + 'Enter "q" to quit.')
        query = input(Fore.GREEN + "Ask Sous-Chef: " + Style.RESET_ALL)
        if query == 'q':
            break
        # Use the Runnable
        final_state = sousChef.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": 42}}
        )
        print(Fore.LIGHTBLUE_EX, end=" ")
        typing_effect(final_state["messages"][-1].content)
        print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
