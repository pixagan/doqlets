# {
#     "models":{
#         "GPT-5.1":{
#             "model":"GPT-5.1",
#             "inputs":"200",
#             "outputs":"10"
#         }
#     }
# }


class CostModel:

    def __init__(self):
        print("Cost Model")
        self.cost_table = {}

    def load_cost_table(self):
        print("Load Cost Table")

    def estimate_cost(self, model, token_count):
        print("Estimate Cost")

        model_costs = self.cost_table[model]

        input_cost = model_costs["input"]
        output_cost = model_costs["output"]

        token_run_cost = token_count["input"]*model_costs["input"] + token_count["output"]*model_costs["output"]

        return token_run_cost


    def update_cost_model(self):
        print("Estimate Cost Model")

        cost_model = self.db.load_document(
            "cost_model":{}
        )

    def get_costs(self):
        print("Load Cost Estimate")



