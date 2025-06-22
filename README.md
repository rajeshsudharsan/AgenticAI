Agent example using Langgraph
==============================

Used Following Tools
  1) Google SERP API For Searching Hotels
  2) Google Places API for Searching Attractions
  3) Open Weather map for Finding Weather for current Date and Travel Date
  4) Custom tool for Calculating the Total hotel price
What you need to run the Code:

Google SERP API KEY
Google Places API KEY
OPEN WeatherMap API KEY



LLM Will interact with tools mentioned above if the prompt is related to Searching Hotels or Attractions or weather or caluating the total price.

If the question is generic

  1)  LLM will generate the result and end the process.

else
  1) LLM will determine the tools required and pass the arguments required for the tool.
  2) call will be transferred to Tool. 
  3) Tool will do the required processing and pass the response to the LLM
  4) LLM will check if all the necessary info is available and generate the result end the process.
  5) if necessary info is not available LLM will either generate the response on its own or again try to call the tools repaeatedly
