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

def data_to_cards(data):
    print("Convert data into cards")

    print(data)

    messages = [
        {
            "role":"system",
            "content":"""Your job is to clean up the information provided and convert into structured content cards.
            The different types of cards are shown below. Breaking the information into cards is to break large documents or pieces of information into
            smaller pieces of information.

            The different card types are : """ +  str(card_types) + """

            Respond in the JSON format shown below: 
            {"cards":[
                {
                    "card_type":"text",
                    "title":"The header of the card",
                    "uid":"title with spaces replaced with underscores and specical character if any removed in lower case",
                    "content":"The content of the card",
                },
                {
                    "card_type":"image",
                    "title":"The header of the card",
                    "uid":"title with spaces replaced with underscores and specical character if any removed in lower case ",
                    "content":"A description of the image",
                    "image_url":"The url of the image"
                },
                {
                    "card_type":"table",
                    "title":"The header of the card",
                    "uid":"title with spaces replaced with underscores and specical character if any removed in lower case",
                    "content":"A description of the table",
                    "data":"the data of the table in csv format"
                }
            ]}
            """
        },
        {
            "role":"user",
            "content":"The information to be converted into cards is: " + str(data)
        }
    ]

    response = cleanup_llm.call_llm(messages)

    content = response['message'].content

    print("Cards : ", content)

    content = json.loads(content)

    cards = content['cards']

    return {
        "cards":cards
    }
    
dataToCardsNode = Node("DataToCards")

dataToCardsNode_inputs = [  
    {
        "name": "data",
        "type": "text",
        "description": "The data to be converted into cards",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

dataToCardsNode_outputs = [
    {
        "name": "cards", 
        "type": "array",
        "description": "The cards converted from the data"
    }
]

dataToCardsNode.set_function("data_to_cards", data_to_cards, {}, dataToCardsNode_inputs, dataToCardsNode_outputs)






def load_pages():
    print("Load sections")

    pages = db.load_documents("pages", {})

    pagelist = []

    for page in pages:
        new_sections = {
            "name": page["title"],
            "uid": page["uid"]
        }
        pagelist.append(new_sections)


    return {
        "pages":pagelist
    }

loadPagesNode = Node("LoadPages")

loadPagesNode_inputs = []

loadPagesNode_outputs = [
    {
        "name": "pages", 
        "type": "array",
        "description": "The pages loaded from the database"
    }
]

loadPagesNode.set_function("load_pages", load_pages, {}, loadPagesNode_inputs, loadPagesNode_outputs)




classify_llm = LLM('Classify_LLM', config=llm_config)

def tag_cards(cards, pages):
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



tagCardsNode = Node("TagCards")

tagCardsNode_inputs = [
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

tagCardsNode_outputs = [
    {
        "name": "tag_cards", 
        "type": "dict", 
        "description": "The cards tagged"
    },
    
]

tagCardsNode.set_function("tag_cards", tag_cards, {}, tagCardsNode_inputs, tagCardsNode_outputs)



def merge_cards_to_tags(cards, tag_cards):
    print("Merge cards to pages")

    for card in cards:
        card_title = card["title"]
        page = tag_cards[card_title]["page"]
        tags = tag_cards[card_title]["tags"]
        connections = tag_cards[card_title]["connections"]

        card["page"] = page
        card["tags"] = tags
        card["connections"] = connections

    return {
        "merged_cards":cards
    }

mergeCardsToTagsNode = Node("MergeCardsToTags")

mergeCardsToTagsNode_inputs = [
    {
        "name": "cards",
        "type": "array",
        "description": "The cards to be merged to pages",
        "inputType": "source",
        "source": "",
        "value": None
    },
    {
        "name": "tag_cards",
        "type": "dict",
        "description": "The tags of the cards",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

mergeCardsToTagsNode_outputs = [
    {
        "name": "merged_cards", 
        "type": "array", 
        "description": "The cards merged to pages"
    },
]

mergeCardsToTagsNode.set_function("merge_cards_to_tags", merge_cards_to_tags, {}, mergeCardsToTagsNode_inputs, mergeCardsToTagsNode_outputs)




def push_cards_to_db(cards):
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




def prep_vectorstore_cards(cards):

    print("Vectorize cards")

    documents = []
    metadatas = []

    for card in cards:
        documents.append(card["content"])
        metadatas.append({
            "uid": card["uid"],
            "title": card["title"],
        })

    return {
        "documents":documents,
        "metadatas":metadatas
    }

prepVectorstoreCardsNode = Node("PrepVectorstoreCards")

prepVectorstoreCardsNode_inputs = [
    {
        "name": "cards",
        "type": "array",
        "description": "The cards to be vectorized",
        "inputType": "source",
        "source": "",
        "value": None
    }
]

prepVectorstoreCardsNode_outputs = [
    {
        "name": "documents", 
        "type": "array", 
        "description": "The documents to be vectorized"
    },
    {
        "name": "metadatas",
        "type": "array",
        "description": "The metadatas to be vectorized"
    }
]

prepVectorstoreCardsNode.set_function("prep_vectorstore_cards", prep_vectorstore_cards, {}, prepVectorstoreCardsNode_inputs, prepVectorstoreCardsNode_outputs)





#----------------- Flow 1 ---------------------------------------
# Data -> Cards -> Tag -> Duplication Pipeline -> Old/New Cards -> Old Cards removal Pipeline -> New Cards Add Pipeline

dataToCardsFlow = Flow("DataToCardsFlow")


dataToCardsFlow.add_node(dataToCardsNode)
dataToCardsFlow.add_node(tagCardsNode)
dataToCardsFlow.add_node(pushCardsToDBNode)
dataToCardsFlow.add_node(loadPagesNode)
dataToCardsFlow.add_node(mergeCardsToTagsNode)
dataToCardsFlow.add_node(prepVectorstoreCardsNode)
dataToCardsFlow.add_node(vector_store)


dataToCardsFlow.add_edge("START", "LoadPages|load_pages")
dataToCardsFlow.add_edge("LoadPages|load_pages", "DataToCards|data_to_cards")
dataToCardsFlow.add_edge("DataToCards|data_to_cards", "TagCards|tag_cards")
dataToCardsFlow.add_edge("TagCards|tag_cards", "MergeCardsToTags|merge_cards_to_tags")
dataToCardsFlow.add_edge("MergeCardsToTags|merge_cards_to_tags", "PushCardsToDB|push_cards_to_db")

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

