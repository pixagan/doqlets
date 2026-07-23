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

from nodes.MongoNode import MongoNode
from laeyerz.utils.KeyManager import KeyManager


class ActionLog:

    def __init__(self):
        self.logs = []
        self.chat_logs = []
        self.agent_logs = []
        self.km = KeyManager()
        self.db =  MongoNode("DoqletsDB", config={"MONGO_URI": self.km["MONGO_URI"], "MONGO_DB": self.km["MONGO_DB"]})


    def add_item(self, action_type, action_description, metadata=None):

        new_item = {
            "action_type": action_type,
            "action_description": action_description,
            "metadata": metadata
        }
        #self.items.append(new_item)

        self.db.create_document("action_log", new_item)


    def get_items(self):
        return self.items


    def clear_items(self):
        self.items = []


    def add_chat_item(self, query, answer):

        new_chat = {
            "query": query,
            "answer": answer,
        }

        new_chat = self.db.create_document("chat", new_chat)

        self.add_item("chat", "Chat with the agent", {"chat_id": str(new_chat.inserted_id)})



    def add_task_item(self, task, skill, agent_response): 

        new_task = {
            "task": task,
            "skill": skill,
            "agent_response": agent_response,
        } 

        new_task = self.db.create_document("task", new_task)

        self.add_item("task", "Task run with Agent", {"task_id": str(new_task.inserted_id), "skill": skill})

