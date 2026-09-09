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

from laeyerz.utils.KeyManager import KeyManager
from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node



from laeyerz_nodes.llm.OpenAINode import OpenAINode as LLM
from laeyerz_nodes.fileloaders.PdfLoader import PdfLoader
from laeyerz_nodes.dataprocessors.TextProcessor import TextProcessorNode
from laeyerz_nodes.embeddings.SentenceTransformerNode import SentenceTransformerNode as Embeddings
from laeyerz_nodes.vectorstores.FaissNode import FaissNode as VectorStore

from laeyerz.nodes.llm.PromptNode import PromptNode

from nodes.ChromaNode import ChromaNode

from CardTypes import card_types


km = KeyManager()


# pdf_loader    = PdfLoader("PdfLoader")


# #Combine text into a single string
# combine_text  = TextProcessorNode("CombinePages")

# #Split Text
# split_text     = TextProcessorNode("SplitText")

chroma_node = ChromaNode("ChromaNode", config={"db_path": km["CHROMA_PATH"]})


#llm chunking model

llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5-mini", 
}

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
                    "card_topic":"What the card is about. This helps figure out which page the card should be added to and where to add new data."
                    "content":"The content of the card",
                },
                {
                    "card_type":"image",
                    "title":"The header of the card",
                    "uid":"title with spaces replaced with underscores and specical character if any removed in lower case ",
                    "content":"A description of the image",
                    "card_topic":"What the card is about",
                    "image_url":"The url of the image"
                },
                {
                    "card_type":"table",
                    "title":"The header of the card",
                    "uid":"title with spaces replaced with underscores and specical character if any removed in lower case",
                    "content":"A description of the table",
                    "card_topic":"What the card is about",
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





#-----Creating thh Flow
docloader_flow = Flow("DocumentStore")

#-----adding nodes
docloader_flow.add_node(dataToCardsNode)
docloader_flow.add_node(prepVectorstoreCardsNode)
docloader_flow.add_node(chroma_node)

#adding edges
docloader_flow.add_edge("START", "DataToCards|data_to_cards")
docloader_flow.add_edge("DataToCards|data_to_cards", "PrepVectorstoreCards|prep_vectorstore_cards")
docloader_flow.add_edge("PrepVectorstoreCards|prep_vectorstore_cards", "ChromaNode|add_documents")
docloader_flow.add_edge("ChromaNode|add_documents", "END")


#adding data sources
docloader_flow.add_data_source("DataToCards|data_to_cards|data", "INPUTS|data")

docloader_flow.add_data_source("PrepVectorstoreCards|prep_vectorstore_cards|cards", "DataToCards|data_to_cards|cards")

docloader_flow.add_data_source("ChromaNode|add_documents|documents", "PrepVectorstoreCards|prep_vectorstore_cards|documents")
docloader_flow.add_data_source("ChromaNode|add_documents|metadata", "PrepVectorstoreCards|prep_vectorstore_cards|metadatas")
docloader_flow.set_node_input("ChromaNode|add_documents|collection_name", "doqlets")

#dataToCardsFlow.set_outputs(["MergeCardsToTags|merge_cards_to_tags|merged_cards"])

docloader_flow.finalize()



# store_flow.add_node(pdf_loader)
# store_flow.add_node(combine_text)
# store_flow.add_node(split_text)
# store_flow.add_node(embedding_model)
# store_flow.add_node(vector_store)

# #-----adding edges
# store_flow.add_edge("START", "PdfLoader|extract_pdf_text")
# store_flow.add_edge("PdfLoader|extract_pdf_text", "CombinePages|combine_pages")
# store_flow.add_edge("CombinePages|combine_pages", "SplitText|split_text")
# store_flow.add_edge("SplitText|split_text", "Embeddings|encode")
# store_flow.add_edge("Embeddings|encode", "DocumentStore|store")
# store_flow.add_edge("DocumentStore|store", "END")


# #---adding data sources
# store_flow.add_data_source("PdfLoader|extract_pdf_text|loaded_file", "INPUTS|file")
# store_flow.add_data_source("CombinePages|combine_pages|pages", "PdfLoader|extract_pdf_text|doc_pages")
# store_flow.add_data_source("SplitText|split_text|text", "CombinePages|combine_pages|text")
# store_flow.add_data_source("Embeddings|encode|sentences", "SplitText|split_text|chunks")
# store_flow.add_data_source("DocumentStore|store|vectors", "Embeddings|encode|embeddings")
# store_flow.add_data_source("DocumentStore|store|metadata", "SplitText|split_text|chunks")

