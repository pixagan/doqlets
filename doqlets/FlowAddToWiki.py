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

#from ttclient.FlowTracker import FlowTracker
#from ttclient.TaskTracker import TaskTracker



import simplejson as json


km = KeyManager()

llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1", 
}


db = Mongo("DoqletsDB", config={"MONGO_URI": km["MONGO_URI"], "MONGO_DB": km["MONGO_DB"]})
vector_store = ChromaNode("ChromaNode", config={"db_path": km["CHROMA_PATH"]})


cleanup_llm = LLM('Cleanup_LLM', config=llm_config)



def find_relevant_pages(page_ids):
    print("Load page")

    cpages = db.load_documents("pages", {"_id": {"$in": page_ids}})

    pages = []
    for cpage in cpages:
        pages.append({
            "id": str(cpage["_id"]),
            "description": cpage["description"],
            "sections": cpage["sections"],
            "rules": cpage["rules"]
        })

    page_description = cpage["description"]
    sections = cpage["sections"]

    #page rules, page sections

    return {
        "page_description":page_description,
        "sections":sections
    }

loadPageNode = Node("LoadPage")

loadPageNode_inputs = [
    {
        "name": "page_id",
        "type": "string",
        "description": "The id of the page to be loaded",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

loadPageNode_outputs = [
    {
        "name": "section_list", 
        "type": "array",
        "description": "The list of sections in the page"
    },
    {
        "name": "page_description",
        "type": "string",
        "description": "The description of the page",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

loadPageNode.set_function("load_page", load_page, {}, loadPageNode_inputs, loadPageNode_outputs)






classify_llm = LLM('Classify_LLM', config=llm_config)

def merge_sections(cards, pages):
    print("Classify cards")

    messages = [
        {
            "role":"system",
            "content":"""You are a Wiki Manager. Given the content cards, you need to figure out which pages they will show up in.
            Ideally, a card should show up only in one page. Use the pages provided to figure out which page the card belongs to.
            If the card has dependencies to other cards, then use the connections field to link the cards to the other cards.
            Use the uid field of the cards provided to link the cards to the other cards.
            Also populate the tags field with any relevant tags for the card's content so a search engine can find relevant cards.
            
            """
            + str(pages)

            + """ Respond in the JSON format below, with the card title and the tage. Do not write out the content of the card.
            {
            "cards":{
                "card_title":{
                    "card_uid":"The uid of the card",
                    "page":"The uid of the page the card should be added to",
                    "connections":[
                        "uid1",
                        "uid2",
                        "uid3"
                    ],
                    "tags":[
                        "tag1",
                        "tag2",
                        "tag3"
                    ]
                }
              }
            }
            """
        },
        {
            "role":"user",
            "content":"The cards to be classified are: " + str(cards)
        }
    ]


    response = classify_llm.call_llm(messages)

    content = response['message'].content

    content = json.loads(content)

    cards = content['cards']

    print("Cards : ", cards)

    return {
        "tag_cards":cards
    }



mergeSectionsNode = Node("TagCards")

mergeSectionsNode_inputs = [
    {
        "name": "cards",
        "type": "array",
        "description": "The cards to be tagged",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "pages",
        "type": "array",
        "description": "The pages to be tagged",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

mergeSectionsNode_outputs = [
    {
        "name": "tag_cards", 
        "type": "dict", 
        "description": "The cards tagged"
    },
    
]

mergeSectionsNode.set_function("merge_sections", merge_sections, {}, mergeSectionsNode_inputs, mergeSectionsNode_outputs)






def update_sections_to_db(sections):
    print("Push cards to db")
    print(cards)

    card_id_maps = {}

    card_ids = []
    for card in cards:
        created_card = db.create_document("cards", card)
        card_ids.append({
            "id": str(created_card.inserted_id),
            "title": card["title"],
            "uid": card["uid"],
            "page_id": page_id,
        })

        card_id_maps[card["uid"]] = {
            "id": str(created_card.inserted_id),
            "title": card["title"],
        }

    return {
        "card_ids":card_ids,
        "card_id_maps":card_id_maps
    }

pushCardsToDBNode = Node("PushCardsToDB")

pushCardsToDBNode_inputs = [
    {
        "name": "cards",
        "type": "array",
        "description": "The cards to be pushed to the database",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

pushCardsToDBNode_outputs = [
    {
        "name": "card_ids", 
        "type": "array", 
        "description": "The ids of the cards pushed to the database"
    },
    {
        "name": "card_id_maps",
        "type": "dict",
        "description": "The maps of the cards pushed to the database"
    }
]

pushCardsToDBNode.set_function("push_cards_to_db", push_cards_to_db, {}, pushCardsToDBNode_inputs, pushCardsToDBNode_outputs)








#----------------- Flow 1 ---------------------------------------
# Data -> Cards -> Tag -> Duplication Pipeline -> Old/New Cards -> Old Cards removal Pipeline -> New Cards Add Pipeline

addToWikiFlow = Flow("AddToWikiFlow")

addToWikiFlow.add_node(loadPageNode)
addToWikiFlow.add_node(mergeSectionsNode)
addToWikiFlow.add_node(pushCardsToDBNode)
addToWikiFlow.add_node(prepVectorstoreCardsNode)
addToWikiFlow.add_node(vector_store)


addToWikiFlow.add_edge("START", "LoadPages|load_pages")
addToWikiFlow.add_edge("LoadPages|load_pages", "MergeSections|merge_sections")
addToWikiFlow.add_edge("MergeSections|merge_sections", "PushCardsToDB|push_cards_to_db")
addToWikiFlow.add_edge("PushCardsToDB|push_cards_to_db", "PrepVectorstoreCards|prep_vectorstore_cards")
addToWikiFlow.add_edge("PrepVectorstoreCards|prep_vectorstore_cards", "ChromaNode|add_documents")
addToWikiFlow.add_edge("ChromaNode|add_documents", "END")

dataToCardsFlow.add_edge("PushCardsToDB|push_cards_to_db", "PrepVectorstoreCards|prep_vectorstore_cards")
dataToCardsFlow.add_edge("PrepVectorstoreCards|prep_vectorstore_cards", "ChromaNode|add_documents")
dataToCardsFlow.add_edge("ChromaNode|add_documents", "END")



dataToCardsFlow.add_data_source("DataToCards|data_to_cards|data", "INPUTS|data")

dataToCardsFlow.add_data_source("TagCards|tag_cards|cards", "DataToCards|data_to_cards|cards")
dataToCardsFlow.add_data_source("TagCards|tag_cards|pages", "LoadPages|load_pages|pages")

dataToCardsFlow.add_data_source("MergeCardsToTags|merge_cards_to_tags|cards", "DataToCards|data_to_cards|cards")
dataToCardsFlow.add_data_source("MergeCardsToTags|merge_cards_to_tags|tag_cards", "TagCards|tag_cards|tag_cards")

dataToCardsFlow.add_data_source("PushCardsToDB|push_cards_to_db|cards", "MergeCardsToTags|merge_cards_to_tags|merged_cards")


dataToCardsFlow.add_data_source("PrepVectorstoreCards|prep_vectorstore_cards|cards", "MergeCardsToTags|merge_cards_to_tags|merged_cards")

dataToCardsFlow.add_data_source("ChromaNode|add_documents|documents", "PrepVectorstoreCards|prep_vectorstore_cards|documents")
dataToCardsFlow.add_data_source("ChromaNode|add_documents|metadata", "PrepVectorstoreCards|prep_vectorstore_cards|metadatas")
dataToCardsFlow.set_node_input("ChromaNode|add_documents|collection_name", "doqlets")

dataToCardsFlow.set_outputs(["MergeCardsToTags|merge_cards_to_tags|merged_cards"])

