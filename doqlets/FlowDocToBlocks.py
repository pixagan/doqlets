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






def extract_doc_search_criteron(cards):

    card_info = []
    card_dict = {}

    index = 0
    for card in cards:
        card_info.append({
            "card_id": str(card["_id"]),
            "card_type": card["card_type"],
            "card_keypoints": card["keypoints"]
        })

        card_dict[str(card["_id"])] = index
        index = index + 1


    return {
        "card_info": card_info,
        "card_dict": card_dict
    }

cardInfoExtractionNode = Node("CardInfoExtraction")

cardInfoExtractionNode_inputs = [
    {
        "name": "cards",
        "type": "array",
        "description": "The cards to be loaded",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

cardInfoExtractionNode_outputs = [
    {
        "name": "card_info", 
        "type": "array",
        "description": "The relevant card_details as an array"
    },
    {
        "name": "card_dict",
        "type": "dict",
        "description": "A dictionary of the card ids with the card index"
    }
]

cardInfoExtractionNode.set_function("card_info_extraction", extract_doc_search_criteron, {}, cardInfoExtractionNode_inputs, cardInfoExtractionNode_outputs)






def load_relevant_blocks():
    print("Load blocks ")

    #for page in page merge

    blocks_rules = db.load_documents("block_rules",{})
    for block in blocks_rules:
        block["_id"]= str(block["_id"])
    


    return {
        "block_rules": blocks_rules
    }



loadRelevantBlocksNode = Node("LoadRelevantBlocks")

loadRelevantBlocksNode_inputs = [
]

loadRelevantBlocksNode_outputs = [
    {
        "name": "block_rules", 
        "type": "array",
        "description": "The relevant blocks loaded from the database"
    }
]

loadRelevantBlocksNode.set_function("load_relevant_blocks", load_relevant_blocks, {}, loadRelevantBlocksNode_inputs, loadRelevantBlocksNode_outputs)




relevantpage_llm = LLM('FinRelevantPage', config=llm_config)
findrelevantblocks_llm = LLM('FindRelevantBlocks', config=llm_config)


def card_block_matching(cards, blocks):
    print("Check for new additions : ", cards)
    print("Blocks : ", blocks)

    messages = [
        {
            "role":"system",
            "content":"""You job is to check if content cards are relevant to smart blocks, which are extracted and processed information. 
            For this task, you are provided a list of the key points of each card with the card's id. You are also provided with a list of blocks wach containing the block's id and the block's rules telling you what each block is about.
            Compare the card's keypoints with the block's rules and determine which cards are relevant to which blocks.
            You will respond with relevant card for each block. You can have blocks that don't have a relevant card. 

            Respond in the json format as shown below.
            

            Respond purely in the JSON format :
            {
                "merge_requests": [
                {
                    "block": "block_id1",
                    "relevant_cards": ["card1_id", "card2_id", "card3_id"],
                },
                {
                    "block": "block_id3",
                    "relevant_cards": ["card1_id", "card2_id", "card3_id"],
                },
                ... for all block that require cards to be added
                ]
            }
            """
        },
        {
            "role":"user",
            "content":"The cards are: " + str(cards) 
        },
        {
            "role":"user",
            "content":"the blocks card already added to are: " + str(blocks)
        }
    ]

    response = findrelevantblocks_llm.call_llm(messages)
    content = response['message'].content
    merge_requests_json = json.loads(content)
    merge_requests = merge_requests_json["merge_requests"]

    #print("Merge Requests : ", merge_requests)

    return {
        "merge_requests": merge_requests
    }

cardBlockMatchingNode = Node("CardBlockMatching")

cardBlockMatchingNode_inputs = [
    {
        "name": "cards",
        "type": "array",
        "description": "The cards to be merged",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "blocks",
        "type": "array",
        "description": "The blocks card already added to",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

cardBlockMatchingNode_outputs = [
    {
        "name": "merge_requests",
        "type": "array",
        "description": "The merge requests to be added",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

cardBlockMatchingNode.set_function("card_block_matching", card_block_matching, {}, cardBlockMatchingNode_inputs, cardBlockMatchingNode_outputs)





merge_blocks_llm = LLM('MergeBlocks_LLM', config=llm_config_merge)

def merge_blocks(cards, card_dict, merge_requests):
    print("Merge blocks : ", merge_requests, len(merge_requests))
    print("Card Dict : ", card_dict)

    block_data = []

    #agent_response = block_update_agent.run_agent(input_data)

    merge_summary = []

    for req in merge_requests:

        rel_cards = []
        for cid in req["relevant_cards"]:
            ccard = {
                "content":cards[card_dict[cid]]["content"]
            }
            rel_cards.append(ccard)

            
        block_id = req["block"]
        cblock = db.load_document_id("blocks", block_id)

        merge_inputs = {
            "cards":rel_cards,
            "block":cblock
        }

        agent_response = block_update_agent.run_agent(merge_inputs)

        updated_block = agent_response["outputs"]["output"]

        updated_block = json.loads(updated_block)

        cblock["content"] = updated_block["content"]

        merge_summary.append({
            "block_id":block_id,
            "block_updated":updated_block["block_updated"],
            "changes_made":updated_block["changes_made"],
            "cards_merged":req["relevant_cards"]
        })

        db.update_document_id("blocks", block_id, cblock)


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
        "name":"card_dict",
        "type":"dict",
        "description":"A dictionary of card ids with index",
        "inputType": "source",
        "source":"",
        "value": None
    },
    {
        "name": "merge_requests",
        "type": "array",
        "description": "The merge requests to be merged",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

mergeBlocksNode_outputs = [
    {
        "name": "merged_blocks",
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

addToPagesFlow = Flow("AddToPagesFlow")

addToPagesFlow.add_node(cardInfoExtractionNode)
addToPagesFlow.add_node(loadRelevantBlocksNode)
addToPagesFlow.add_node(cardBlockMatchingNode)
addToPagesFlow.add_node(mergeBlocksNode)


addToPagesFlow.add_edge("START", "CardInfoExtraction|card_info_extraction")
addToPagesFlow.add_edge("CardInfoExtraction|card_info_extraction", "LoadRelevantBlocks|load_relevant_blocks")
addToPagesFlow.add_edge("LoadRelevantBlocks|load_relevant_blocks", "CardBlockMatching|card_block_matching")

#addToPagesFlow.add_edge("CardBlockMatching|card_block_matching", "END")

addToPagesFlow.add_edge("CardBlockMatching|card_block_matching", "MergeBlocks|merge_blocks")
addToPagesFlow.add_edge("MergeBlocks|merge_blocks", "END")



addToPagesFlow.add_data_source("CardInfoExtraction|card_info_extraction|cards", "INPUTS|cards")


addToPagesFlow.add_data_source("CardBlockMatching|card_block_matching|cards", "CardInfoExtraction|card_info_extraction|card_info")
addToPagesFlow.add_data_source("CardBlockMatching|card_block_matching|blocks", "LoadRelevantBlocks|load_relevant_blocks|block_rules")


addToPagesFlow.add_data_source("MergeBlocks|merge_blocks|cards", "INPUTS|cards")
addToPagesFlow.add_data_source("MergeBlocks|merge_blocks|card_dict", "CardInfoExtraction|card_info_extraction|card_dict")
addToPagesFlow.add_data_source("MergeBlocks|merge_blocks|merge_requests", "CardBlockMatching|card_block_matching|merge_requests")


#addToPagesFlow.set_outputs(["CardBlockMatching|card_block_matching|merge_requests"])

addToPagesFlow.set_outputs(["MergeBlocks|merge_blocks|merge_summary"])

