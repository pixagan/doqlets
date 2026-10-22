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

#Page Manager Agent

from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
from laeyerz.utils.KeyManager import KeyManager

from laeyerz.agent.Agent import Agent

from nodes.OpenAINode import OpenAINode as LLM
from nodes.MongoNode import MongoNode as Mongo
from nodes.ChromaNode import ChromaNode

import simplejson as json

km = KeyManager()

reasoner_llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1", 
}

llm_config_merge={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5-mini", 
}


db = Mongo("DoqletsDB", config={"MONGO_URI": km["MONGO_URI"], "MONGO_DB": km["MONGO_DB"]})

vector_store = ChromaNode("ChromaNode", config={"db_path": km["CHROMA_PATH"]})



#check page for blocks
#add to existing or create new block

block_search_related_instructions = """You are a relevant content finder for a document inteligence app.

You are given a spec for the content block including what information is required for the block a nd how it needs to be merged with the block's content along with any relevant context.
You will be given content block along with a summary, keypoints of the content.

You need to find any relevant content cards stored in the knowledge store and pass on the relevant card information as shown below including the card's id, document(which is the card's content), uid and distance.

For that use the semantic_search tool to search the knowledge store for the relevant content.
Do not pass in any project ids into the vector store search as in input query.

Respond purely in the JSON format :
    {
        "relevant_cards": [
            {
                "id": "card1_id",
                "document": "card1_document",
                "uid": "card1_uid",
                "distance": "card1_distance"
            },
            ...
        ],
    }

The following tools are available to you:
- semantic search - 

Do not try to update the block's content or perform any merge, just find the relevant content.


"""


reasoner_llm = LLM("BlockManagerAgent",config=reasoner_llm_config)
block_search_related_agent = Agent( name="CardMergeAgent", config = {
        "reasoner":reasoner_llm, 
        "role":"You are a Page Manager Agent for an AI Managed Wiki", 
        "instructions":block_search_related_instructions, 
        "tools":[]
    }
)


# ---------------------Tools -----------------------------


#keyword search
block_search_related_agent.add_tool({
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










# ------------------------------------Block Update Agent----------------------

block_update_agent_instructions = """Given a block and content including its summary and metadata,
- Determine from the block's metadata what the block's content is, what format the content is in, and any required processing.
- Next extract from the provided content any relevant information to the block.
- Based on the block's style, format and rules, convert the content into the block's format.
- Next Merge the formatted mew content into the block's existing content content, in line with the block's rules.

Inputs Passed In:
- block: The block content to update
- block_rules: The block rules, instructionss about what to be extract from the information provided as cards, how it is to be formatted and updated to the block.
- cards: The content to update the block with passed in as Content Cards
Optional Inputs that might or not passed in:
- block_description: The block description, a short description of the block's purpose and content. This might not be provided.
- content : Any additional context that has been provided that is relevant to the block update. This might not be provided.

Response format :  If the block is updated, respond with the updating information as shwon below, else with confirmation of no update
{
  "block_id": "block_id", 
  "block_updated": "Yes/No",
  "changes_made": "A 20 word keypoint summary of the changes",
  "content": "The updated block content"
}
"""


block_update_agent = Agent( name="BlockUpdateAgent", config = {
        "reasoner":reasoner_llm, 
        "role":"Block Update Agent", 
        "instructions":block_update_agent_instructions, 
        "tools":[]
    }
)