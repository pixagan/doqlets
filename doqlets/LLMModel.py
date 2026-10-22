from laeyerz.flow.Node import Node

from OpenAINode import OpenAINode
from CostModel import UsageModel


class LLMModel(Node):

    def __init__(self):
        print("LLM Model")
        self.models = {}
        self.model_vendor_map = {}
        self.usage_model = UsageModel()


    def setup(self, vendors=["OPENAI"], api_keys={}):
        print("Setup")

        for vendor in vendors:

            if(vendor == "OPENAI"):
                llm_config={
                    "api_key":km['OPENAI_API_KEY'], 
                }
                self.models["OPENAI"] = OpenAINode("OpenAILLM", config=llm_config)


    def determine_vendor(self, model):

        vendor = self.model_vendor_map["model"]

        return vendor


    def check_model_allowed(self, model):
        print("Check Model Allowed")



    def call_llm(self, model, messages, tools=[]):
        print("Calling LLM")

        vendor = self.determine_vendor(model)

        response = self.models[vendor].call_llm(model, messages)

        tokens = response["tokens"]

        self.usage_model.add(tokens["model"], tokens["prompt_tokens"], tokens["completion_tokens"])

        return response





        



        