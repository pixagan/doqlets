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

import os

from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
from laeyerz.agent.Agent import Agent

from laeyerz.utils.KeyManager import KeyManager

from nodes.OpenAINode import OpenAINode as LLM 

from AgentTools import tools

from Skilllist import skillist


km = KeyManager()


class DoqletsAgentManager:
    def __init__(self):
        self.agent_runs = []
        self.agent = None
        self.skillist = skillist


    def setup(self):
        print("Setting up Doqlets Agent Manager")


    def create_agent(self, skill_instructions):

        agent_role = "You are a Doqlets Agent that is tasked with completing a task based using the tools provided. Use the skill instructions added below to complete the task."
        agent_instructions = skill_instructions

        data_instruction = """You must only use the data available in the databases for the task.
        You can use the tools provided to search and retrueve data. DO NOT MAKE UP ANY INFOMRATION.
        """

        response_format = """Respond in Markdown format unless otherwise specified by the user."""
        
        agent_instructions = agent_instructions + data_instruction

        llm_config={
            "api_key":km['OPENAI_API_KEY'], 
            "model":"gpt-5.1"
        }


        reasoner_llm =  LLM("DoqletsReasoner",  config=llm_config)

        doqlets_agent = Agent( name="DoqletsAgent", config = {
                "api_key_path":'.env',
                "reasoner":reasoner_llm, 
                "role":agent_role, 
                "instructions":agent_instructions, 
                "tools":{}
            }
        )

        doqlets_agent = self.load_tools(doqlets_agent)

        return doqlets_agent


    def reset_agent(self):
        print("Resetting agent")


    def load_tools(self, agent):

        for tool in tools:
            agent.add_tool(tool)

        return agent


    def load_skill(self, selected_skill):

        print("Skilllist: ", self.skillist)

        skill_file = None
        for skill in self.skillist:
            if skill["name"] == selected_skill:
                skill_file = skill["file"]
                break

        if skill_file is None:
            raise ValueError(f"Skill {selected_skill} not found")
            return None


        with open('./skills/' + skill_file, "r") as file:
            skill_instructions = file.read()

        return skill_instructions




    def run_task(self, skill, task, write_to_file=False):

        print("Loading Skill Instructions for ", skill)
        skill_instructions = self.load_skill(skill)

        print("Skill Instructions: ", skill_instructions)

        if skill_instructions is None:
            print("Skill Instructions not found for ", skill)
            raise ValueError(f"Skill {skill} not found")
            return None


        print("Creating Agent for ", skill)
        agent = self.create_agent(skill_instructions)

        print("Running Task for ", skill)
        task_response = agent.run_agent(task=task, write_to_file=write_to_file)
        print("Task Response for ", skill, task_response)

        return task_response



if __name__ == "__main__":
    agent_manager = DoqletsAgentManager()
    agent_manager.run_task(skill="SlideGenerator", task={"task":"Create a slide deck about the basics of Large Language Models", "collection_name":"doqlets", "n_results":5})