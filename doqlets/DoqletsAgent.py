# Copyright 2025 Pixagan Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
from laeyerz.agent.Agent import Agent

from laeyerz.utils.KeyManager import KeyManager

from nodes.OpenAINode import OpenAINode as LLM

from AgentTools import tools


#--------------------------- Storage Flow ----------------------------
#API key path
km = KeyManager()


llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1"
}


api_key = km.get('OPENAI_API_KEY')

reasoner_llm =  LLM("DoqletsAgent",  config=llm_config)
agent_role = "You are a RAG agent that answers questions about the documents."
agent_instructions = """You will be given a query by the user.

You need to find and retrieve the most relevant chunks of information from the databases.
Then based on the retrieved information, generate a response to the user's query.

Retrieval Approach :

Start by using the vector store to retrieve via semantic search the most relevant chunks based on the user's original query.
If the semantic search returns relevant chunks and the answer looks complete, use the Answer Drafter to draft the answer.

If semantic search does not return relevant chunks or the answer looks incomplete, use the BM25 keyword search tool to find matching chunks via keyword search.

If semantic search and BM25 keyword search both fail to get relevant chunks, try rewording the query and use semantic search one last time. 

If despite the above steps, an answer is not found, respond with 'COULD NOT FIND RELEVANT INFORMATION'.

Check the drafted answer, and return it as the response. DO NOT MODIFY OR CHANGE ANY PART OF THE ANSWER RETURNED BY THE ANSWER DRAFTER.
Do not make up any information to answer a query, make sure the responses are based on the chunks retrieved.



Tools Provided:
Semantic Search Tool - queries a vector store
BM25 Keyword Search Tool - queries a BM25 database
LLM Tool - Rewording the user query to imporve Semantic Search Hits
Slide Planner Tool - Generating the answer based on the query and the chunks
Report Planner Tool - Generating the answer based on the query and the chunks
"""


doqlets_agent = Agent( name="DoqletsAgent", config = {
        "api_key_path":'.env',
        "reasoner":reasoner_llm, 
        "role":agent_role, 
        "instructions":agent_instructions, 
        "tools":{}
    }
)


#------------ Adding all available tools to the agent
for tool in tools:
    doqlets_agent.add_tool(tool)


#-------------- Run Agent ------------------------------

agent_response = doqlets_agent.run_agent({
    "task_description": "What is ChatGPT?",
    "task_context":""
})
