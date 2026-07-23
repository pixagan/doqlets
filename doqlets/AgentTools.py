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


from nodes.MongoNode import MongoNode as Mongo
from nodes.ChromaNode import ChromaNode
from nodes.OpenAINode import OpenAINode as LLM 

from laeyerz.utils.KeyManager import KeyManager

#Tools
#Semantic Search Tool
#Keyword Search Tool
#LLM tool
#Slide Planner
#Report Planner Tool

km = KeyManager()

llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1"
}



db = Mongo("DoqletsDB", config={"MONGO_URI": km["MONGO_URI"], "MONGO_DB": km["MONGO_DB"]})

vector_store = ChromaNode("ChromaNode", config={"db_path": km["CHROMA_PATH"]})



tools = []

#keyword search
tools.append({
    "name": "semantic_search",
    "description": "Run a search on the vector store database",
    "inputs": [
        {
            "name": "collection_name",
            "type": "string",
            "description": "The name of the collection to search in"
        },
        {
            "name": "query",
            "type": "string",
            "description": "The query to search for"
        },
        {
            "name": "n_results",
            "type": "number",
            "description": "The number of results to return"
        }
    ],
    "outputs": [
        {
            "name": "matches",
            "type": "array",
            "description": "The matches found in the collection"
        }
    ],
    "function": vector_store.search
})




query_responder_llm = LLM("LLM", config=llm_config)
def answer_query(query: str, context: list):

    instructions = """
    You are a helpful assistant that can answer questions about the documents.
    You will be given a query and context chunks.
    You need to answer the query based on the context.
    DO NOT SPECULATE OR MAKE UP INFORMATION, USE ONLY THE INFORMATION PROVIDED TO ANSWER THE QUERY.
    IF NO CONTEXT IS PROVIDED, OR THE CONTEXT PROVIDED DOES NOT ANSWER THE QUERY, RESPOND WITH 'COULD NOT FIND RELEVANT INFORMATION.'
    RESPOND ONLY WITH THE ANSWER NOTING ELSE.
    """
    messages = [
        {
            "role": "developer",
            "content": instructions
        },
        {
            "role": "user",
            "content": f"Query: {query}\nContext: {context}"
        }
    ]
    output = query_responder_llm.call_llm(messages)
    answer = output['message'].content
    return {
        "answer": answer
    }



tools.append({
    "name": "answer_query",
    "description": "Answer a query based on the context",
    "inputs": [
        {
            "name": "query",
            "type": "string",
            "description": "The query to answer"
        },
        {
            "name": "context",
            "type": "array",
            "description": "The context to answer the query"
        }
    ],
    "outputs": [
        {
            "name": "answer",
            "type": "string",
            "description": "The answer to the query"
        }
    ],
    "function": answer_query
})
