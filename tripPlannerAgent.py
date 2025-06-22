from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState,StateGraph, END, START
import llm
from travelPlannerTools import tools
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from tripPlanner import TripPlanSummary
from typing import List
import json
from IPython.display import Image, display

parser = JsonOutputParser(pydantic_object=TripPlanSummary)

prompt_template=PromptTemplate(
    template = """
            You are a helpful Travel Assistant. 
            Provide attractions, hotels and their address, Price of Hotel and Current Weather, forecasted Weather for the Date of travel in Tabular Format.
            if forecasted weather is not available mentioned it as 'not known'. Provide multiple suggestions for hotel stay.
            Use available tools for providing information and calculation of total Hotel price.
            Format the final response as per the instruction :  {format_instruction}
""",
    partial_variables={"format_instruction":parser.get_format_instructions()},
)

prompt_template.format()

system_prompt  = SystemMessage(
            content="""You are a helpful Travel Assistant. 
            Provide attractions, hotels and their address, Price of Hotel and Current Weather, forecasted Weather for the Date of travel in Tabular Format.
            Suggest one hotel for each Day near the attraction.If forecasted weather is not available mentioned it as 'not known'. Provide multiple suggestions for hotel stay.
            Use available tools for providing information and calculation of total Hotel price.
            """
        )



print(tools)
llm_with_tools = llm.model.bind_tools(tools=tools)

def assistTravelPlan(state:MessagesState):
    user_question = state["messages"]
    input_question = [system_prompt] + user_question
    response = llm_with_tools.invoke(input_question)
    return {"messages": [response]}
    
    


graph=StateGraph(MessagesState)
graph.add_node("llm_decision_step",assistTravelPlan)

graph.add_node("tools",ToolNode(tools))
graph.add_edge(START,"llm_decision_step")


graph.add_conditional_edges(
    "llm_decision_step",
    tools_condition,
)

graph.add_edge("tools","llm_decision_step")
app=graph.compile()


png_graph = app.get_graph().draw_mermaid_png() 

# To display the image (optional, if you're in a Jupyter Notebook)
display(Image(png_graph))

# To save the PNG file
with open("travel_agent_graph.png", "wb") as f:
    f.write(png_graph)

try:
    message=[HumanMessage(content="Plan a tourist attactions for Chicago City around August 25th, 2025 for 5 days and plan a Hotel stay within price of  200 USD for each day. Also search weather for the city menrtioned and total price of the hotel stay" 
    )]
    
    #for output in app.stream({"messages":message}, {"recursion_limit": 20}):
    #    for key,value in output.items():
    #        print(f"Output from {key} Node")
    #        print("_______")
    #        print(value)
    #        print("\n")

    response = app.invoke({"messages":message}, {"recursion_limit": 20})
    
    
    print(response['messages'])

    data = response['messages'][-1].content # parses the string to dict
    
    with open("output1.md", "w", encoding='utf-8') as file:
        file.write(data)
        
        

except Exception as e:
    print(f"An unexpected error occurred: {e}")