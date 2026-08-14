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


import simplejson as json

from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
from laeyerz.utils.KeyManager import KeyManager


from SampleCards import cards as sample_cards
from CardTypes import card_types

from nodes.OpenAINode import OpenAINode as LLM
from nodes.MongoNode import MongoNode as Mongo
from nodes.ChromaNode import ChromaNode

km = KeyManager()


vector_store = ChromaNode("ChromaNode", config={"db_path": km["CHROMA_PATH"]})

#for card, get the closest matches in the db
def get_closest_matches(text):
    #get the closest matches in the db
    matches = vector_store.search(collection_name, query)
    return {
        "matches": matches,
    }
getClosestMatchesNode = Node("GetClosestMatches")

getClosestMatchesNode_inputs = [  
    {
        "name": "text",
        "type": "text",
        "description": "The data to be converted into cards",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

getClosestMatchesNode_outputs = [
    {
        "name": "cards", 
        "type": "array",
        "description": "The cards converted from the data"
    }
]

getClosestMatchesNode.set_function("get_closest_matches", get_closest_matches, {}, getClosestMatchesNode_inputs, getClosestMatchesNode_outputs)




#then check if the card fits into an existing one or requires a new card

def check_merge(card, matches):

    closest_match = 0
    closest_distance = matches[0]["distance"]

    for iC in range(len(matches)):
        if matches[iC]["distance"] < closest_distance:
            closest_distance = matches[iC]["distance"]
            closest_match = iC

    return {
        "closest_match": matches[closest_match],
        "closest_distance": closest_distance
    }

    #add to closest match
checkMergeNode = Node("CheckMerge")

checkMergeNode_inputs = [  
    {
        "name": "card",
        "type": "dict",
        "description": "The card to be checked for merging",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "matches",
        "type": "array",
        "description": "The closest matches to the card",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

checkMergeNode_outputs = [
    {
        "name": "closest_match", 
        "type": "array",
        "description": "The cards converted from the data"
    },
    {
        "name": "closest_distance", 
        "type": "float",
        "description": "The distance between the card and the closest match",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

checkMergeNode.set_function("check_merge", check_merge, {}, checkMergeNode_inputs, checkMergeNode_outputs)






llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1", 
}

merge_llm = LLM('Merge_LLM', config=llm_config)

def finalize_merge(text, match):
    #merge the card into the match
    #return the merged card

    messages = [
        {
            "role":"system",
            "content":"""Check if the text provided and the existing card are very similary
            If they are merge the content into one card. If they are not similar and are better off as separate cards, return the text as is.
            Respond in the JSON format :
            {
                "merge": true/false,
                "reason": "reason for the merge/not merge"
                "merged_text": "the merged text"
            }
            """
        },
        {
            "role":"user",
            "content":"""Merge the two pieces of text into a single card.
            """
        }
    ]

  
    
    response = merge_llm.call_llm(messages)

    json_response = json.loads(response['message'].content)
    

    return {
        "merge_request": json_response
    }

finalizeMergeNode = Node("FinalizeMerge")

finalizeMergeNode_inputs = [  
    {
        "name": "text",
        "type": "dict",
        "description": "The card to be checked for merging",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "match",
        "type": "array",
        "description": "The closest matches to the card",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

checkMergeNode_outputs = [
    {
        "name": "merge_request", 
        "type": "dict",
        "description": "The merge request"
    }
]

getClosestMatchesNode.set_function("get_closest_matches", get_closest_matches, {}, getClosestMatchesNode_inputs, getClosestMatchesNode_outputs)







#if fits in an existing one, then perform a merge

#else create a new card


addCardToPageFlow = Flow("AddCardToPageFlow")

addCardToPageFlow.add_node(getClosestMatchesNode)
addCardToPageFlow.add_node(checkMergeNode)
addCardToPageFlow.add_node(mergeCardsNode)
addCardToPageFlow.add_node(addCardToPageNode)

addCardToPageFlow.add_edge("START", "GetClosestMatches|get_closest_matches")
addCardToPageFlow.add_edge("GetClosestMatches|get_closest_matches", "CheckMerge|check_merge")
addCardToPageFlow.add_edge("CheckMerge|check_merge", "MergeCards|merge_cards")
addCardToPageFlow.add_edge("MergeCards|merge_cards", "AddCardToPage|add_card_to_page")

addCardToPageFlow.add_data_source("GetClosestMatches|get_closest_matches", "INPUTS|text")

addCardToPageFlow.add_data_source("CheckMerge|check_merge|matches", "GetClosestMatches|get_closest_matches|cards")
addCardToPageFlow.add_data_source("CheckMerge|check_merge|card", "INPUTS|card")

addCardToPageFlow.add_data_source("FinalizeMerge|finalize_merge|text", "CheckMerge|check_merge|card")
addCardToPageFlow.add_data_source("FinalizeMerge|finalize_merge|match", "CheckMerge|check_merge|matches")

addCardToPageFlow.set_outputs("FinalizeMerge|finalize_merge|merge_request", "CheckMerge|check_merge|merge_request")



