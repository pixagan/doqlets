# Copyright 2025 Pixagan Technologies

from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node
from laeyerz.agent.Agent import Agent

from laeyerz.utils.KeyManager import KeyManager

from nodes.OpenAINode import OpenAINode as LLM
from nodes.MongoDBNode import MongoDBNode as MongoDB

class ProjectManager(Node):

    def __init__(self):
        print("PageManager initialized")


    def project_model(self, project_id):

        project_model = {
            "page_breakdown":""
        }


        new_page_logic = ""


    def add_page(self, title, description):
        #add a page to the database

        #check for any projeect plan

        page_sections = ""

        add_section_criterion = ""

        new_page = {
            "title":title,
            "description":description,
            "model":page_model

        }


    def determine_new_page_required(self, title, description):
        #determine if a new page is required
        #return the page model
        page_model = {
            "page_breakdown":""
        }
        return page_model


    def update_page_model(self, page_id, modifications):    

        page_model = {
            "page_breakdown":""
        }

    

    def create_page_section(self):
        print("Creating page section")



    def add_cards(self, cards):

        for card in cards:
            self.add_card(card)


    def add_card(self, card):

        #given card, check which pages, sections it is relevant to

        #check closest cards as well
        print("Adding card to project")






if __name__ == "__main__":
    project_manager = ProjectManager()
    project_manager.create_page_section()