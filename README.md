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

  a.  LLM will generate teh result and end the process.

else
  a. LLM will determine the tools required and pass the arguments required for the tool.
  b. call will be transferred to Tool. 
  c. Tool will do the required processing and pass the response to the LLM
  d. LLM will check if all the necessary info is available and generate teh result end the process.
