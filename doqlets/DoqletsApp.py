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
# Created: Anil Variyar
# Copyright: Anil Variyar

import os
import sys
from pathlib import Path
import uuid
from datetime import datetime
import csv
from io import StringIO
from io import BytesIO
from typing import Dict


from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from dotenv import load_dotenv, find_dotenv
load_dotenv()

from laeyerz.utils.KeyManager import KeyManager
from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node

from nodes.MongoNode import MongoNode
from nodes.ChromaNode import ChromaNode

from Skilllist import skillist
from ActionLog import ActionLog

#Data Loaders
from DataLoader import DataLoader
from FlowAddData import dataToCardsFlow
#from FlowDocumentLoader import docloader_flow
#from FileLoaderFlow import fileloader_flow

from FlowDocToBlocks import addToPagesFlow
from FlowDocToCards import docToCardsFlow

#Search and Chat
from FlowSearch import searchFlow
from FlowChat import chatFlow

#Agents
from DoqletsAgentManager import DoqletsAgentManager


class ProjectCreate(BaseModel):
    name: str

class ChatInput(BaseModel):
    query: str

class DataInput(BaseModel):
    title: str
    data: str

class PageCreate(BaseModel):
    title: str
    description: str
    pageRules: str

class SearchInput(BaseModel):
    query: str

class AgentInput(BaseModel):
    skill: str
    task: str

class BlockCreate(BaseModel):
    title: str
    block_type: str
    rules: str
    context: str


class DoqletsApp:

    def __init__(self):



        self.api =  FastAPI(
                                title="Doqlets API for App",
                                description="The API for the Doqlets App",
                                version="1.0.0"
                            )

        self.api.add_middleware(
                                    CORSMiddleware,
                                    allow_origins=["http://localhost:3070"],  # Add your React app's URL here
                                    allow_credentials=True,
                                    allow_methods=["*"],  # Allows all methods
                                    allow_headers=["*"],  # Allows all headers
                                )


        self.km            = KeyManager()


        self.db = MongoNode("DoqletsDB", config={"MONGO_URI": self.km["MONGO_URI"], "MONGO_DB": self.km["MONGO_DB"]})

        self.vstore = ChromaNode("ChromaNode", config={"db_path": self.km["CHROMA_PATH"]})


        #self.store_flow    = None
        #self.retrieve_flow = None


        self.d2c_flow        = dataToCardsFlow
        #self.doc_loader_flow = docloader_flow
        #self.file_loader_flow = fileloader_flow

        self.data_loader = DataLoader()

        self.search_flow = searchFlow
        self.chat_flow   = chatFlow

        self.addToBlockFlow = addToPagesFlow
        self.docToCardsFlow = docToCardsFlow

        self.action_log = ActionLog()
        self.agent_manager = DoqletsAgentManager()


        self.setup_routes()




    def setup_routes(self):

        @self.api.get("/")
        async def load_index():
            return {"message": "Welcome to Doqlets API"}


        @self.api.get("/api/projects")
        async def load_projects():

            projects = self.db.load_documents("projects", {})
            for project in projects:
                project["_id"] = str(project["_id"])
            return {"projects": projects}


        @self.api.post("/api/projects")
        async def create_project(project_create:ProjectCreate):

            project_name = project_create.name.strip().lower()
            collection_name = "dq" + "_" + project_name

            created_project = self.db.create_document("projects", {"name": project_create.name, "collection_name":collection_name})


            self.vstore.create_get_collection(collection_name)


            new_project = {
                "name": project_create.name,
                "_id": str(created_project.inserted_id),
            }


            return {"project": new_project}


        @self.api.get("/api/projects/{project_id}")
        async def load_projects_id(project_id: str):

            cproject = self.db.load_document_id("projects", project_id)
            cproject["_id"] = str(cproject["_id"])
            return {"project": cproject}


    #--------------------Documents -------------------------------------------------

        @self.api.get("/api/documents/{project_id}")
        async def load_documents(project_id: str):

            documents = self.db.load_documents("documents", {"project_id":project_id})
            for document in documents:
                document["_id"] = str(document["_id"])
            return {"documents": documents}



        @self.api.get("/api/documents/{project_id}/{doc_id}")
        async def load_document(project_id: str, doc_id: str):

            doc      = self.db.load_document_id("documents", doc_id)

            print("doc ", doc)

            document = self.db.load_document_id("document_data", doc["doc_id"])
            
            print("document ", document)

            

            document["_id"] = str(document["_id"])

            return {"document": document}


        @self.api.get("/api/documents/cards/{project_id}/{page_uid}")
        async def load_page_cards(project_id: str, page_uid: str):
            cards = self.db.load_documents("cards", {"page":page_uid})
            for card in cards:  
                card["_id"] = str(card["_id"])


            page_model = self.db.load_document("pages", {"uid":page_uid})
            page_model["_id"] = str(page_model["_id"])
            return {"cards": cards, "page_model": page_model}



        @self.api.post("/api/documents/text/{project_id}")
        async def add_data(project_id: str, data_in:DataInput):

            data  = data_in.data
            title = data_in.title

            doc = {
                "title": title,
                "data": data,
            }

            created_document = self.db.create_document("document_data", doc)


            new_document = {
                "project_id":project_id,
                "title": title,
                "source": "db",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }


            created_doc = self.db.create_document("documents", new_document)

            doc_id = str(created_doc.inserted_id)


            #flow_response = self.doc_loader_flow.run({"data": data})

            #flow_response = self.d2c_flow.run({"data": data, "project_id": project_id, "document_id":doc_id})

            flow_response = self.docToCardsFlow.run({
                "data": data,
                "project_id": project_id,
                "document_id": doc_id
            })

            cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            card_ids = [card["_id"] for card in cards]




            self.action_log.add_item("adding_data", "Adding data as text directly to database", {"card_ids": card_ids})

            inputs = {
                "cards": cards
            }

            flow_res = addToPagesFlow.run(inputs)
            print("Flow Res : ", flow_res)

            merge_requests = flow_res["outputs"]["MergeBlocks|merge_blocks|merge_summary"]



            return_doc = {
                "project_id":project_id,
                "title": title,
                "source": "db",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }


            # flow_response = self.d2c_flow.run({"data": data})

            # cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            # card_ids = [card["_id"] for card in cards]

            # self.action_log.add_item("adding_data", "Adding data as text directly to database", {"card_ids": card_ids})

            return {"document": return_doc}


        @self.api.post("/api/documents/file/{project_id}")
        async def store_pdf(project_id: str, file: UploadFile = File(...)):

            file_content = await file.read()
            #self.store_flow.run({"file": file_content})

            title = file.filename
            

            data = self.data_loader.load_pdf(file_content)
            doc = {
                "title": title,
                "data": data,
            }
            created_document = self.db.create_document("document_data", doc)

            new_document = {
                "project_id":project_id,
                "title": title,
                "source": "file",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }

            created_doc = self.db.create_document("documents", new_document)

            #flow_response = self.d2c_flow.run({"data": data})

            flow_response = self.docToCardsFlow.run({
                "data": data,
                "project_id": project_id,
                "document_id": doc_id
            })

            print("Done with Flow")

            cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            card_ids = [card["_id"] for card in cards]

            inputs = {
                "cards": cards
            }

            flow_res = addToPagesFlow.run(inputs)
            print("Flow Res : ", flow_res)

            merge_requests = flow_res["outputs"]["MergeBlocks|merge_blocks|merge_summary"]



    
            #flow_response = self.doc_loader_flow.run({"data": data})
            
            return {"document": new_document}



        @self.api.put("/api/documents/file/{project_id}")
        async def update_doc(project_id:str, file: UploadFile = File(...)):

            file_content = await file.read()
            #self.store_flow.run({"file": file_content})

            data = self.data_loader.load_pdf(file_content)

            new_document = {
                "project_id":project_id,
                "title": title,
                "source": "file",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }

            created_doc = self.db.create_document("documents", new_document)

            flow_response = self.doc_loader_flow.run({"data": data})
            
            return {"message": "PDF stored successfully"}

        


        # --- Pages --------

        @self.api.get("/api/pages/{project_id}")
        async def load_pages(project_id: str):

            pages = self.db.load_documents("pages", {"project_id":project_id})
            for page in pages:
                page["_id"] = str(page["_id"])
            return {"pages": pages}


        @self.api.post("/api/pages/{project_id}")
        async def add_page(project_id: str, page_create:PageCreate):

            title = page_create.title
            description = page_create.description
            page_rules = page_create.pageRules

            uid = title.strip().replace(" ", "_").lower()

            created_page = self.db.create_document("pages", {"project_id":project_id, "title": title})

            page_rules = {
                "project_id": project_id,
                "page_id": str(created_page.inserted_id),
                "description": description,
                "rules": page_rules,
                "sections": []
            }

            created_page_rules = self.db.create_document("page_rules", page_rules)


            new_page = {
                "_id": str(created_page.inserted_id),
                "title": title,
                "page_description": description,
                "uid": uid
            }

            self.action_log.add_item("add_page", "Adding page to database", {"title": title})

            return {"page": new_page}


        @self.api.get("/api/pages/{project_id}/{page_uid}")
        async def load_page(project_id: str, page_uid: str):
            cards = self.db.load_documents("blocks", {"page_id":page_uid})
            for card in cards:  
                card["_id"] = str(card["_id"])

            print("cards ", cards)


            page_model = self.db.load_document_id("pages", page_uid)
            print("page_model ", page_model)
            page_model["_id"] = str(page_model["_id"])
            return {"cards": cards, "page_model": page_model}



        # --- Blocks --------

        @self.api.post("/api/pages/blocks/{project_id}/{page_id}")
        async def add_block(project_id: str, page_id: str, block_create:BlockCreate):

            title = block_create.title
            block_type = block_create.block_type
            rules = block_create.rules
            context = block_create.context

            print("New Block ", title, block_type, rules, context)

            newBlock = {
                "project_id":project_id,
                "page_id":page_id,
                "title":title,
                "block_type":block_type,
                "position":0,
                "uid":"",
                "content":"",
                "connections":[],
                "tags":[]
            }
            created_block = self.db.create_document("blocks", newBlock)

            newBlockRules = {
                "project_id": project_id,
                "title":title,
                "block_id":str(created_block.inserted_id),
                "rules":rules,
                "type":block_type,
                "instructions":rules,
                "context": context,
            }

            created_rules = self.db.create_document("block_rules", newBlockRules)

            newBlock["_id"] = str(created_block.inserted_id)
            return {"block": newBlock}





        @self.api.put("/api/pages/blocks/{project_id}/{page_uid}/block_id")
        async def update_block(project_id: str, page_uid: str):

            cblock = self.db.load_document_id("blocks", block_id)

            return {"block": cblock}


        @self.api.get("/api/pages/blocks/{project_id}/{block_id}")
        async def load_block_meta(project_id: str, block_id: str):

            cblock_meta = self.db.load_document("block_rules", {"block_id":block_id})

            print("Block ", cblock_meta)

            cblock_meta["_id"] = str(cblock_meta["_id"])

            return {"block": cblock_meta}



        #--------------- Tasks -------------------------------------------

        @self.api.post("/api/agents/{project_id}")
        async def run_task(project_id:str, task_in:AgentInput):

            task_description  = task_in.task
            skill = task_in.skill

            print("task_description ", task_description)
            print("skill ", skill)

            task_request = {
                "task":task_description,
                "vector_store_parameters":{
                    "collection_name":"doqlets",
                    "n_results":"5"
                }
            }

            print("running task ", skill, task_request)

            task_response = self.agent_manager.run_task(skill, task_request, project_id)
            #print("search_results ", search_response)
            print("task_response ", task_response)

            task_id = self.action_log.add_task_item(project_id, task_description, skill, task_response["outputs"])


            task_response["task"] = task_description
            task_response["skill"] = skill
            task_response["_id"] = str(task_id)
            task_response["keypoints"] = task_response["outputs"]["task_keypoints"]
            task_response["response"] = task_response["outputs"]["output"]

            return {"task_response": task_response}


        @self.api.get("/api/agents/{project_id}")
        async def get_agent_runs(project_id: str):

            tasks = self.db.load_documents("task", {"project_id": project_id})
            for task in tasks:
                task["_id"] = str(task["_id"])
            return {"tasks": tasks}



        @self.api.get("/api/skills")
        async def get_skills():

            skills = skillist

            return {"skills": skills}


        #---------------------------------- Usage -------------------

        @self.api.get("/api/usage/{project_id}")
        async def load_usage(project_id: str):

            usage = self.db.load_documents("usage", {"project_id":project_id})

            return {"usage": usage}



       #--------------------Search  / RAG (now depreciated)-------------------------------------------------

        @self.api.post("/api/search/{project_id}")
        async def search_pages(project_id:str, search_in:SearchInput):

            query = search_in.query
            search_response = self.search_flow.run({"query": query, "project_id": project_id})

            search_results = search_response["outputs"]["MergeSearchResults|merge_search_results|merged_results"]
            print("search_results ", search_results)

            self.action_log.add_item("search", "Searching for relevant data from database", {})

            return {"search_results": search_results}


        @self.api.post("/api/chat/{project_id}")
        async def chat_pages(project_id:str, search_in:SearchInput):

            query = search_in.query
            chat_response = self.chat_flow.run({"query": query, "project_id": project_id})
            #print("search_results ", search_response)

            answer = chat_response["outputs"]["AnswerQuery|answer_query|answer"]
            print("chat answer ", answer)

            chat_id = self.action_log.add_chat_item(query, answer)

            return {"answer": answer}


        @self.api.get("/api/chat/{project_id}")
        async def load_chat_history(project_id: str):

            chats = self.db.load_documents("chat", {"project_id":project_id})
            for chat in chats:
                chat["_id"] = str(chat["_id"])

            return {"chats": chats}



    def run(self):
        uvicorn.run(self.api, host="0.0.0.0", port=6070)


if __name__ == "__main__":
    app = DoqletsApp()
    app.run()