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


import chromadb
import uuid
from laeyerz.utils.KeyManager import KeyManager
from laeyerz.flow.Node import Node


class ChromaNode(Node):
    
    def __init__(self, name, config={}):
        print(f"Initializing ChromaNode {name}")
        super().__init__(name, config)

        self.db_path = config["db_path"]

        self.client = chromadb.PersistentClient(
            path=str(self.db_path)
        )
        print(f"ChromaClient initialized at {self.db_path}")

        self.add_actions()
        

    def create_get_collection(self, name):
        collection = self.client.get_or_create_collection(name=name)
        return collection



    def add_documents(self, collection_name, documents, metadata=[]):
        
        collection = self.create_get_collection(collection_name)
        
        ids = [str(uuid.uuid4()) for _ in documents]
        
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadata
        )

        return ids


    def update_documents(self, collection_name, ids, documents, metadata=[]):
        collection = self.create_get_collection(collection_name)
        collection.update(
            ids=ids,
            documents=documents,
            metadatas=metadata
        )
        return ids


    def search(self, collection_name, query, n_results=5):

        collection = self.create_get_collection(collection_name)

        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

        matches = []

        for index, document in enumerate(results["documents"][0]):
            matches.append(
                {
                    "id": results["ids"][0][index],
                    "document": document,
                    "metadata": results["metadatas"][0][index],
                    "distance": results["distances"][0][index],
                }
            )



        return matches



    def delete_documents(self, collection_name, ids):
        collection = self.create_get_collection(collection_name)
        collection.delete(
            ids=ids
        )
        return ids


    def delete_collection(self, collection_name):
        collection = self.create_get_collection(collection_name)
        collection.delete()
        return collection_name
   

    def get_chroma_client(self):
        return self.chroma_client


    def add_actions(self):

        add_documents_inputs = [
            {
                "name":"collection_name",
                "type":"name",
                "description":"The name of the collection to add the documents to",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"documents",
                "type":"list",
                "description":"The documents to add to the collection",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"metadata",  
                "type":"list",
                "description":"The metadata to add to the documents",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        add_documents_outputs = [
            {
                "name":"ids",
                "type":"list",
                "description":"The ids of the documents added to the collection",
                "inputType":"output",
                "source":"",
                "value":None
            }
        ]

        self.add_action(action_name="add_documents", 
        function=self.add_documents, 
        parameters={}, 
        inputs=add_documents_inputs, 
        outputs=add_documents_outputs, 
        isDefault=False, 
        description="Add documents to the collection")



        update_documents_inputs = [
            {
                "name":"collection_name",
                "type":"name",
                "description":"The name of the collection to update the documents in",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"ids",
                "type":"list",
                "description":"The ids of the documents to update in the collection",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"documents",
                "type":"list",
                "description":"The documents to update in the collection",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"metadata",
                "type":"list",
                "description":"The metadata to update the documents with",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        update_documents_outputs = [
            {
                "name":"ids",
                "type":"list",
                "description":"The ids of the documents updated in the collection",
                "inputType":"output",
                "source":"",
                "value":None
            }
        ]

        
        self.add_action(action_name="update_documents", 
        function=self.update_documents, 
        parameters={}, 
        inputs=update_documents_inputs, 
        outputs=update_documents_outputs, 
        isDefault=False, 
        description="Update documents in the collection")
        


        search_inputs = [
            {
                "name":"collection_name",
                "type":"name",
                "description":"The name of the collection to search in",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"query",
                "type":"string",
                "description":"The query to search for in the collection",
                "inputType":"input",
                "source":"",
                "value":None
            },
            {
                "name":"n_results",
                "type":"int",
                "description":"The number of results to return",
                "inputType":"input",
                "source":"",
                "value":None
            }
        ]
        search_outputs = [
            {
                "name":"matches",
                "type":"list",
                "description":"The matches found in the collection",
                "inputType":"output",
                "source":"",
                "value":None
            }   
        ]


        self.add_action(action_name="search", 
        function=self.search, 
        parameters={}, 
        inputs=search_inputs, 
        outputs=search_outputs, 
        isDefault=False, 
        description="Search the collection")



        delete_documents_inputs = [
            {
                "name":"collection_name",
                "type":"name",
                "description":"The name of the collection to delete the documents from",
                "inputType":"input",
                "source":"",
                "value":None
            },
        ]
        delete_documents_outputs = [
            {
                "name":"ids",
                "type":"list",
                "description":"The ids of the documents deleted from the collection",
                "inputType":"output",
                "source":"",
                "value":None
            }
        ]


        # self.add_action(action_name="delete_documents", 
        # function=self.delete_documents, 
        # parameters={}, 
        # inputs=delete_documents_inputs, 
        # outputs=delete_documents_outputs, 
        # isDefault=False, 
        # description="Delete documents from the collection")
        