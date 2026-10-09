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

from nodes.OpenAINode import OpenAINode as LLM
from nodes.MongoNode import MongoNode


import simplejson as json


km = KeyManager()

llm_config={
    "api_key":km['OPENAI_API_KEY'], 
    "model":"gpt-5.1", 
}

db = MongoNode("DoqletsDB", config={"MONGO_URI": km["MONGO_URI"], "MONGO_DB": km["MONGO_DB"]})


relevantpage_llm = LLM('FinRelevantPage', config=llm_config)




def create_page_schema_llm(page_name, page_description, page_rules, required_blocks=[]):

  instructions = """You are responsible for creating LLM Pages.
  Given a page name, description, rules and selected blocks, reformat and convert it into a clean
  page model that can be used by an AI wiki manager to decide what content can and cannot be added to the page.
  Respond purely in the JSON response format provided. below

  Response format :
  {
    "page_name":
    "page_description":
    "page_rules":
 }
  """

  messages = [
    {
      "role": "system",
      "content": instructions
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"Page Name: {page_name}, Page Description: {page_description}, Page Rules: {page_rules}, Required blocks if any : {required_blocks}"
        }
      ]
    }
  ]

  response = relevantpage_llm.call_llm(messages)
  updated_page_schema = response['message'].content
  updated_page_schema_json = json.loads(updated_page_schema)
  return updated_page_schema_json




def create_block_schema_llm():
  pass