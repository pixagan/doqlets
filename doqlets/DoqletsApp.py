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

from Skilllist import skillist
from ActionLog import ActionLog

#Data Loaders
from DataLoader import DataLoader
from FlowAddData import dataToCardsFlow
from DocumentLoaderFlow import docloader_flow
#from FileLoaderFlow import fileloader_flow

#Search and Chat
from FlowSearch import searchFlow
from FlowChat import chatFlow

#Agents
from DoqletsAgentManager import DoqletsAgentManager




class ChatInput(BaseModel):
    query: str

class DataInput(BaseModel):
    title: str
    data: str

class PageCreate(BaseModel):
    title: str

class SearchInput(BaseModel):
    query: str

class AgentInput(BaseModel):
    skill: str
    task: str


class DoqletsApp:

    def __init__(self):

        self.store_flow    = None
        self.retrieve_flow = None

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


        self.d2c_flow        = dataToCardsFlow
        self.doc_loader_flow = docloader_flow
        #self.file_loader_flow = fileloader_flow

        self.data_loader = DataLoader()

        self.search_flow = searchFlow
        self.chat_flow   = chatFlow

        self.action_log = ActionLog()
        self.agent_manager = DoqletsAgentManager()

        self.setup_components()
        self.setup_flow()
        self.setup_routes()


    def setup_components(self):
        print("Setting up components")



    def setup_flow(self):
        print("Setting up store flow")


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




    #--------------------Documents -------------------------------------------------

        @self.api.get("/api/documents")
        async def load_documents():

            documents = self.db.load_documents("documents", {})
            for document in documents:
                document["_id"] = str(document["_id"])
            return {"documents": documents}



        @self.api.get("/api/documents/{doc_id}")
        async def load_document(doc_id: str):

            doc      = self.db.load_document_id("documents", doc_id)

            print("doc ", doc)

            document = self.db.load_document_id("document_data", doc["doc_id"])
            
            print("document ", document)

            

            document["_id"] = str(document["_id"])

            return {"document": document}


        @self.api.post("/api/documents/text")
        async def add_data(data_in:DataInput):

            data  = data_in.data
            title = data_in.title

            doc = {
                "title": title,
                "data": data,
            }

            created_document = self.db.create_document("document_data", doc)


            new_document = {
                "project_id":"",
                "title": title,
                "source": "db",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }


            created_doc = self.db.create_document("documents", new_document)


            #flow_response = self.doc_loader_flow.run({"data": data})

            flow_response = self.d2c_flow.run({"data": data})

            cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            card_ids = [card["_id"] for card in cards]

            self.action_log.add_item("adding_data", "Adding data as text directly to database", {"card_ids": card_ids})



            return_doc = {
                "project_id":"",
                "title": title,
                "source": "db",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }


            # flow_response = self.d2c_flow.run({"data": data})

            # cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            # card_ids = [card["_id"] for card in cards]

            # self.action_log.add_item("adding_data", "Adding data as text directly to database", {"card_ids": card_ids})

            return {"document": return_doc}


        @self.api.post("/api/documents/file")
        async def store_pdf(file: UploadFile = File(...)):

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
                "project_id":"",
                "title": title,
                "source": "file",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }

            created_doc = self.db.create_document("documents", new_document)

            flow_response = self.d2c_flow.run({"data": data})

            print("Done with Flow")

            cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            card_ids = [card["_id"] for card in cards]


    
            #flow_response = self.doc_loader_flow.run({"data": data})
            
            return {"document": new_document}



        @self.api.put("/api/documents/file")
        async def update_doc(file: UploadFile = File(...)):

            file_content = await file.read()
            #self.store_flow.run({"file": file_content})

            data = self.data_loader.load_pdf(file_content)

            new_document = {
                "project_id":"",
                "title": title,
                "source": "file",   #db, file, cloud, web.
                "doc_id": str(created_document.inserted_id),
            }

            created_doc = self.db.create_document("documents", new_document)

            flow_response = self.doc_loader_flow.run({"data": data})
            
            return {"message": "PDF stored successfully"}

        



        #--------------------Wiki -------------------------------------------------

        @self.api.post("/api/wiki/store/text")
        async def add_data(data_in:DataInput):

            data = data_in.data

            flow_response = self.d2c_flow.run({"data": data})

            cards = flow_response["outputs"]["MergeCardsToTags|merge_cards_to_tags|merged_cards"]

            card_ids = [card["_id"] for card in cards]

            self.action_log.add_item("adding_data", "Adding data as text directly to database", {"card_ids": card_ids})

            return {"cards": merged_cards}



        @self.api.get("/api/wiki/pages")
        async def load_pages():

            pages = self.db.load_documents("pages", {})
            for page in pages:
                page["_id"] = str(page["_id"])
            return {"pages": pages}


        @self.api.post("/api/wiki/pages")
        async def add_page(page_create:PageCreate):

            title = page_create.title

            uid = title.strip().replace(" ", "_").lower()

            created_page = self.db.create_document("pages", {"title": title})

            page_rules = {
                "page_id": str(created_page.inserted_id),
                "description": "",
                "rules": []
            }


            new_page = {
                "_id": str(created_page.inserted_id),
                "title": title,
                "page_description": page_description,
                "uid": uid
            }

            self.action_log.add_item("add_page", "Adding page to database", {"title": title})

            return {"page": new_page}


        @self.api.get("/api/wiki/pages/{page_uid}")
        async def load_page(page_uid: str):
            cards = self.db.load_documents("cards", {"page":page_uid})
            for card in cards:  
                card["_id"] = str(card["_id"])


            page_model = self.db.load_document("pages", {"uid":page_uid})
            page_model["_id"] = str(page_model["_id"])
            return {"cards": cards, "page_model": page_model}




       #--------------------Search  / RAG -------------------------------------------------


        @self.api.post("/api/search")
        async def search_pages(search_in:SearchInput):

            query = search_in.query
            search_response = self.search_flow.run({"query": query})
            #print("search_results ", search_response)

            search_results = search_response["outputs"]["MergeSearchResults|merge_search_results|merged_results"]
            print("search_results ", search_results)

            self.action_log.add_item("search", "Searching for relevant data from database", {})

            return {"search_results": search_results}


        @self.api.post("/api/chat")
        async def chat_pages(search_in:SearchInput):

            query = search_in.query
            chat_response = self.chat_flow.run({"query": query})
            #print("search_results ", search_response)

            answer = chat_response["outputs"]["AnswerQuery|answer_query|answer"]
            print("chat answer ", answer)

            chat_id = self.action_log.add_chat_item(query, answer)

            return {"answer": answer}


        @self.api.get("/api/chat")
        async def load_chat_history():

            chats = self.db.load_documents("chat", {})
            for chat in chats:
                chat["_id"] = str(chat["_id"])

            return {"chats": chats}


        #--------------- Tasks -------------------------------------------

        @self.api.post("/api/agents")
        async def run_task(task_in:AgentInput):

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

            task_response = self.agent_manager.run_task(skill, task_request)
            #print("search_results ", search_response)
            print("task_response ", task_response)

            task_id = self.action_log.add_task_item(task_description, skill, task_response["outputs"])


            task_response["task"] = task_description
            task_response["skill"] = skill
            task_response["_id"] = str(task_id)
            task_response["keypoints"] = task_response["outputs"]["task_keypoints"]
            task_response["response"] = task_response["outputs"]["output"]

            return {"task_response": task_response}


        @self.api.get("/api/agents")
        async def get_agent_runs():

            tasks = self.db.load_documents("task", {})
            for task in tasks:
                task["_id"] = str(task["_id"])
            return {"tasks": tasks}



        @self.api.get("/api/skills")
        async def get_skills():

            skills = skillist

            return {"skills": skills}


        #------------------------------------------------------------------

    def run(self):
        uvicorn.run(self.api, host="0.0.0.0", port=6070)


if __name__ == "__main__":
    app = DoqletsApp()
    app.run()