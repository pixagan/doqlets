from nodes.MongoNode import MongoNode
from laeyerz.utils.KeyManager import KeyManager

class UsageModel:

    def __init__(self):
        print("Usage Model")

        self.km            = KeyManager()

        self.db = MongoNode("DoqletsDB", config={"MONGO_URI": self.km["MONGO_URI"], "MONGO_DB": self.km["MONGO_DB"]})
        
        self.cost_table = {}


    def add(self, model, input_tokens, output_tokens):
        self.cost_table[model] = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }


    def update_usage(self, project_id, model, tokens):
      
        cost_model = self.db.load_documents("cost", {"project_id": project_id})

        if cost_model is not None:

            if cost_model["usage"][model] is not None:
                cost_model["usage"][model]["input_tokens"] += tokens["input_tokens"]
                cost_model["usage"][model]["output_tokens"] += tokens["output_tokens"]
            else:
                cost_model["usage"][model] = {
                    "input_tokens": tokens["input_tokens"],
                    "output_tokens": tokens["output_tokens"],
                }

            self.db.update_document_id("cost", str(cost_model["_id"]), cost_model)

        else:
            print("Cost model not found for project ", project_id)

        

    def get_costs(self, project_id):
        print("Load Cost Estimate")

        cost_model = self.db.load_documents("cost", {"project_id": project_id})

        cost_model["_id"] = str(cost_model["_id"])

        return cost_model
        

