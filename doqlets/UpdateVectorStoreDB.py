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

from laeyerz.utils.KeyManager import KeyManager

from nodes.ChromaNode import ChromaNode
from nodes.MongoNode import MongoNode as Mongo

km = KeyManager()

db = Mongo("DoqletsDB", config={"MONGO_URI": km["MONGO_URI"], "MONGO_DB": km["MONGO_DB"]})

# docs = ["""Neural networks learn by adjusting their weights to minimize prediction errors. Algorithms such as backpropagation compute how much each weight contributes to the overall error and update the weights accordingly. Through many iterations over the training data, the network gradually improves its performance on the target task.
# """,
# """Neurons in a neural network play different roles depending on their location. Input neurons receive raw data, such as pixel values in an image or words in a sentence. Hidden neurons, located in one or more intermediate layers, perform most of the computation by extracting increasingly abstract features from the input. Output neurons produce the final prediction, such as an object label in an image, a translated sentence, or the next word in a paragraph. Although all neurons use similar mathematical operations, their role depends on their position and the information they process.
# """
# ]

# metadata = [
#     {
#         "title": "Neural networks",
#     },
#     {
#         "title": "Neurons in a neural network",
#     }
# ]

cards = db.load_documents("cards", {})
docs = []
metadata = []
for card in cards:
    docs.append(card["content"])
    metadata.append({
        "uid": card["uid"],
        "title": card["title"],
    })



chroma_db = ChromaNode("ChromaDB", config={"db_path": km["CHROMA_PATH"]})

collection_name = "doqlets" #"test_collection"
#collection = chroma_db.create_get_collection(collection_name)


chroma_db.add_documents(collection_name, docs, metadata)


matches = chroma_db.search(collection_name, "Large Language Models")
print(matches)

#ids = ["5300bfcb-d8e1-4115-b546-3df1b9018b3b", "7b3ba74b-7561-4c1b-9795-073ce545a749"]
#chroma_db.delete_documents(collection_name, ids)