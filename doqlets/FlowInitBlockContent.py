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


from SampleCards import cards as sample_cards
from CardTypes import card_types

from nodes.OpenAINode import OpenAINode as LLM
from nodes.MongoNode import MongoNode as Mongo
from nodes.ChromaNode import ChromaNode

from AgentBlockUpdate import block_update_agent
from AgentBlockUpdate import block_search_related_agent

import simplejson as json

#from ttclient.FlowTracker import FlowTracker
#from ttclient.TaskTracker import TaskTracker



import simplejson as json


km = KeyManager()

llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1", 
}

llm_config_merge={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.5", 
}


db = Mongo("DoqletsDB", config={"MONGO_URI": km["MONGO_URI"], "MONGO_DB": km["MONGO_DB"]})




def load_block(block_id):
    block =  db.load_document_id("blocks", block_id)
    block_rules = db.load_document("block_rules", {"block_id": block_id})
    return {
        "block": block,
        "block_rules": block_rules
    }


loadBlocksNode = Node("LoadBlocks")

loadBlocksNode_inputs = [
    {
        "name": "block_id",
        "type": "string",
        "description": "The block id to find relevant block information for",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

loadBlocksNode_outputs = [
    {
        "name": "block", 
        "type": "dict",
        "description": "The block as a dictionary"
    },
    {
        "name": "block_rules", 
        "type": "dict",
        "description": "The block rules as a dictionary"
    }
]

loadBlocksNode.set_function("load_blocks", load_block, {}, loadBlocksNode_inputs, loadBlocksNode_outputs)




def find_relevant_cards(block_id, block, block_rules):

    vector_store_parameters = {
        "collection_name":"doqlets",
        "n_results":"5"
    }

    agent_response = block_search_related_agent.run_agent(task={
        "block_title": block_rules["title"],
        "block_instructions": block_rules["rules"],
        "vector_store_parameters": vector_store_parameters
    })

    relevant_cards = agent_response["outputs"]["output"]

    relevant_cards = json.loads(relevant_cards)

    relevant_cards = relevant_cards["relevant_cards"]

    print("Relevant cards : ", relevant_cards)


    return {
        "relevant_cards": relevant_cards   
    }

findRelevantCardsNode = Node("FindRelevantCards")

findRelevantCardsNode_inputs = [
    {
        "name": "block_id",
        "type": "string",
        "description": "The relevant block id",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "block",
        "type": "dict",
        "description": "The block as a dictionary",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "block_rules",
        "type": "dict",
        "description": "The block rules as a dictionary",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

findRelevantCardsNode_outputs = [
    {
        "name": "relevant_cards", 
        "type": "array",
        "description": "The relevant card ids as an array"
    }
]

findRelevantCardsNode.set_function("find_relevant_cards", find_relevant_cards, {}, findRelevantCardsNode_inputs, findRelevantCardsNode_outputs)






def load_relevant_cards(card_list):
    print("Load blocks ")

    #for page in page merge

    cards = db.load_documents("cards",{"_id": {"$in": card_list}})
    

    return {
        "cards": cards
    }



loadRelevantCardsNode = Node("LoadRelevantCards")

loadRelevantCardsNode_inputs = [
    {
        "name": "card_list",
        "type": "array",
        "description": "The list of card ids to load",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

loadRelevantCardsNode_outputs = [
    {
        "name": "cards", 
        "type": "array",
        "description": "The relevant blocks loaded from the database"
    }
]

loadRelevantCardsNode.set_function("load_relevant_cards", load_relevant_cards, {}, loadRelevantCardsNode_inputs, loadRelevantCardsNode_outputs)






merge_blocks_llm = LLM('MergeBlocks_LLM', config=llm_config_merge)

def merge_blocks(cards, block, block_rules):
    print("Merge blocks : ", cards, len(cards))

    merged_cards = []
   
    block_data = []

    merge_summary = []

    if(len(cards) > 0):

        merge_inputs = {
            "cards":cards,
            "block":block,
            "block_rules":block_rules
        }

        agent_response = block_update_agent.run_agent(task=merge_inputs, write_to_file=False)

        updated_block = agent_response["outputs"]["output"]

        updated_block = json.loads(updated_block)

        block["content"] = updated_block["content"]

        print("Updated block : ", block)

        db.update_document_id("blocks", str(block["_id"]), block)

        merge_summary.append({
            "block_id":str(block["_id"]),
            "block_updated":updated_block["block_updated"],
            "changes_made":updated_block["changes_made"],
            "cards_merged":merged_cards
        })


    return {
        "merge_summary": merge_summary
    }



mergeBlocksNode = Node("MergeBlocks")

mergeBlocksNode_inputs = [
    {
        "name": "cards",
        "type": "dict",
        "description": "The card to be merged",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name":"block",
        "type":"dict",
        "description":"The block to be merged into",
        "inputType": "source",
        "source":"",
        "value": None
    },
    {
        "name": "block_rules",
        "type": "array",
        "description": "The block rules to be provided",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

mergeBlocksNode_outputs = [
    {
        "name": "merge_summary",
        "type": "array",
        "description": "The merged blocks",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

mergeBlocksNode.set_function("merge_blocks", merge_blocks, {}, mergeBlocksNode_inputs, mergeBlocksNode_outputs)





#----------------- Flow 1 ---------------------------------------
# Data  -> Pages -> Blocks -> Merge Blocks -> Update Blocks to DB

dataToBlocksFlow = Flow("DataToBlocksFlow")

dataToBlocksFlow.add_node(loadBlocksNode)
dataToBlocksFlow.add_node(findRelevantCardsNode)
dataToBlocksFlow.add_node(loadRelevantCardsNode)
dataToBlocksFlow.add_node(mergeBlocksNode)


dataToBlocksFlow.add_edge("START", "LoadBlocks|load_blocks")
dataToBlocksFlow.add_edge("LoadBlocks|load_blocks", "FindRelevantCards|find_relevant_cards")
#dataToBlocksFlow.add_edge("FindRelevantCards|find_relevant_cards", "LoadRelevantCards|load_relevant_cards")
#dataToBlocksFlow.add_edge("LoadRelevantCards|load_relevant_cards", "MergeBlocks|merge_blocks")

dataToBlocksFlow.add_edge("FindRelevantCards|find_relevant_cards", "MergeBlocks|merge_blocks")


dataToBlocksFlow.add_edge("MergeBlocks|merge_blocks", "END")



dataToBlocksFlow.add_data_source("LoadBlocks|load_blocks|block_id", "INPUTS|block_id")


dataToBlocksFlow.add_data_source("FindRelevantCards|find_relevant_cards|block_id", "INPUTS|block_id")
dataToBlocksFlow.add_data_source("FindRelevantCards|find_relevant_cards|block", "LoadBlocks|load_blocks|block")
dataToBlocksFlow.add_data_source("FindRelevantCards|find_relevant_cards|block_rules", "LoadBlocks|load_blocks|block_rules")

#dataToBlocksFlow.add_data_source("LoadRelevantCards|load_relevant_cards|card_list", "FindRelevantCards|find_relevant_cards|relevant_cards")


#dataToBlocksFlow.add_data_source("MergeBlocks|merge_blocks|cards", "LoadRelevantCards|load_relevant_cards|cards")
dataToBlocksFlow.add_data_source("MergeBlocks|merge_blocks|cards", "FindRelevantCards|find_relevant_cards|relevant_cards")

dataToBlocksFlow.add_data_source("MergeBlocks|merge_blocks|block", "LoadBlocks|load_blocks|block")
dataToBlocksFlow.add_data_source("MergeBlocks|merge_blocks|block_rules", "LoadBlocks|load_blocks|block_rules")


dataToBlocksFlow.set_outputs(["MergeBlocks|merge_blocks|merge_summary"])
