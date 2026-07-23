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

from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
from laeyerz.utils.KeyManager import KeyManager
from nodes.ChromaNode import ChromaNode
from nodes.OpenAINode import OpenAINode as LLM


km = KeyManager()


llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1", 
}



vector_store = ChromaNode("ChromaNode", config={"db_path": km["CHROMA_PATH"]})

chatFlow = Flow("ChatFlow")

#semantic search
def semantic_search(query: str):

    collection_name = "doqlets"

    matches = vector_store.search(collection_name, query)

    return {
        "results": matches
    }

semanticSearchNode = Node("SemanticSearch")
semanticSearchNode_inputs = [
    {
        "name": "query",
        "type": "text",
        "description": "The query to search the vector store for",
        "inputType": "source",
        "source": "",
        "value": None

    }
]
semanticSearchNode_outputs = [
    {
        "name": "results",
        "type": "array",
        "description": "The results of the semantic search"
    }
]
semanticSearchNode.set_function("semantic_search", semantic_search, {}, semanticSearchNode_inputs, semanticSearchNode_outputs)





def merge_search_results(results: list):
    #print("results ", results)
    merged_results = []
    for result in results:
        merged_results.append({
            "title": result["metadata"]["title"],
            "content": result["document"],
            "uid": result["metadata"]["uid"],
            "score": result["distance"],
        })
    return {
        "merged_results": merged_results
    }

mergeSearchResultsNode = Node("MergeSearchResults")
mergeSearchResultsNode_inputs = [
    {
        "name": "results",
        "type": "array",
        "description": "The results of the semantic search",
        "inputType": "source",
        "source": "",
        "value": None
    }
]
mergeSearchResultsNode_outputs = [
    {
        "name": "merged_results",
        "type": "array",
        "description": "The results of the semantic search"
    }
]
mergeSearchResultsNode.set_function("merge_search_results", merge_search_results, {}, mergeSearchResultsNode_inputs, mergeSearchResultsNode_outputs)




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

    context_string = ""
    for item in context:
        context_string += item["content"] + "\n"


    messages = [
        {
            "role": "developer",
            "content": instructions
        },
        {
            "role": "user",
            "content": "Query " + query
        },
        {
            "role": "user",
            "content": "Context: " + context_string
        }
    ]
    output = query_responder_llm.call_llm(messages)
    answer = output['message'].content
    return {
        "answer": answer
    }


answerQueryNode = Node("AnswerQuery")
answerQueryNode_inputs = [
    {
        "name": "query",
        "type": "text",
        "description": "The query to answer",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "context",
        "type": "array",
        "description": "The context to answer the query",
        "inputType": "source",
        "source": "",
        "value": None
    }
]
answerQueryNode_outputs = [
    {
        "name": "answer",
        "type": "text",
        "description": "The answer to the query"
    }
]

answerQueryNode.set_function("answer_query", answer_query, {}, answerQueryNode_inputs, answerQueryNode_outputs)



chatFlow.add_node(semanticSearchNode)
chatFlow.add_node(mergeSearchResultsNode)
chatFlow.add_node(answerQueryNode)

chatFlow.add_edge("START","SemanticSearch|semantic_search")
chatFlow.add_edge("SemanticSearch|semantic_search","MergeSearchResults|merge_search_results")
chatFlow.add_edge("MergeSearchResults|merge_search_results","AnswerQuery|answer_query")
chatFlow.add_edge("AnswerQuery|answer_query","END")

chatFlow.add_data_source("SemanticSearch|semantic_search|query", "INPUTS|query")

chatFlow.add_data_source("MergeSearchResults|merge_search_results|results", "SemanticSearch|semantic_search|results")

chatFlow.add_data_source("AnswerQuery|answer_query|query", "INPUTS|query")
chatFlow.add_data_source("AnswerQuery|answer_query|context", "MergeSearchResults|merge_search_results|merged_results")

chatFlow.set_outputs(["MergeSearchResults|merge_search_results|merged_results", "AnswerQuery|answer_query|answer"])



# output = chatFlow.run({"query": "What are LLMs?"})
# outputs = output["outputs"]
# for key, value in outputs.items():
#     print(key, value)
