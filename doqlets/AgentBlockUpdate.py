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


#check page for blocks
#add to existing or create new block

block_manager_agent_instructions = """You are a Smart Block Update Agent for a wiki. 
You will be given content block along with a summary, keypoints of the content.

First load page metadata using the load_page tool.
Compare the card's keypoints and summary with the page's keypoints to check if the card's content is relevant to the page.

Once you have the relevant pages, load the blocks in the page using the load_relevant_blocks tool.

Next check the block's metadata with the content's metadat to determine if the content is relevant to the block, if so
use the block_update_agent tool to update the block's content.


Response Format: The Agent's final response in JSON format as shown below:
{
  "content_added": "Yes/No",
  "blocks_created": "Yes/No",
  "updated_blocks": [block_id1, block_id2, ...], #the blocks created or updated
}

The following tools are available to you:
- Load Page - load_page
- Load Relevant Blocks - load_page_block
- Update Block - update_page_block
"""


reasoner_llm = LLM("BlockManagerAgent",config=reasoner_llm_config)
block_manager_agent = Agent( name="CardMergeAgent", config = {
        "reasoner":reasoner_llm, 
        "role":"You are a Page Manager Agent for an AI Managed Wiki", 
        "instructions":block_manager_agent_instructions, 
        "tools":[]
    }
)



# ---------------------Tools -----------------------------

def load_page(page_id):
    page_template = db.load_document('page_rules', {"page_id": str(page_id)})
    page_schema = db.load_document('page_schema', {"page_id": str(page_id)})
    return {"page_rules": page_template, "page_schema": page_schema}


block_manager_agent.add_tool({
    "name": "load_page",
    "description": "Load Page",
    "inputs": [
        {
            "name": "page_id",
            "type": "string",
            "description": "The page id to load"
        }
    ],
    "outputs": [
        {
            "name": "page_rules",
            "type": "dict",
            "description": "The page template"
        },
        {
            "name": "page_schema",
            "type": "dict",
            "description": "The page schema"
        }
    ],
    "function": load_page
})






def load_relevant_blocks(block_id):

    block_content = db.load_document_id("blocks", block["block_id"])

    return {"block_content": block_content}


block_manager_agent.add_tool({
    "name": "load_page_block",
    "description": "Load Page Block",
    "inputs": [
        {
            "name": "block_id",
            "type": "string",
            "description": "The block id to load"
        }
    ],
    "outputs": [
        {
            "name": "block_content",
            "type": "dict",
            "description": "The block content"
        }
    ],
    "function": load_relevant_blocks
})




def update_page_block(block_id, block_content):

    cblock = db.load_document_id("blocks", block["uid"])
    cblock["content"] = block["content"]
    db.update_document_id("blocks", block_id, cblock)


block_manager_agent.add_tool({
    "name": "update_page_block",
    "description": "Update Page Block",
    "inputs": [
        {
            "name": "block_id",
            "type": "string",
            "description": "The block id to load"
        },
        {
            "name": "block_content",
            "type": "dict",
            "description": "The block content to update"
        }
    ],
    "outputs": [
        {
            "name": "isUpdated",
            "type": "boolean",
            "description": "The status of the block update : True or False"
        }
    ],
    "function": update_page_block
})


# --------------------------------------------------------------------------

block_update_agent_instructions = """Given a block and content including its summary and metadata,
- Determine from the block's metadata what the block's content is, what format the content is in, and any required processing.
- Next extract from the provided content any relevant information to the block.
- Based on the block's style, format and rules, convret the content into the block's format.
- Next Merge the formatted mew content into the block's existing content content, in line with the block's rules.

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