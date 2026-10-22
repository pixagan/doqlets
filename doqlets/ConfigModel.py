class ConfigModel:

    def __init__(self):
        print("Config Model")

        self.config = {
            "block_llm":"gpt-5.1",
            "workflow_llm":"gpt-5.1",
            "card_matching_llm":"gpt-5.5",
            "agent_llm":"gpt-5.1"
        }

    def load_config(self):

        return self.config


    def update_config(self):
        print("Update Config")