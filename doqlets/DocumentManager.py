from laeyerz.flow.Node import Node

from nodes.MongoNode import MongoNode


class DocumentManager(Node):

    def __init__(self):
        print("Document Manager")
        self.db = MongoNode("DoqletsDB", config={"MONGO_URI": self.km["MONGO_URI"], "MONGO_DB": self.km["MONGO_DB"]})


    def add_document(self, mode, title, data):
        print("Add Document")

    

    def add_text_document(self):
        print("Add Document")



    def add_document_db(self):
        print("Add Document Db")

        doc = {
                "title": title,
                "data": data,
            }

        created_document = self.db.create_document("document_data", doc)


    def add_document_file(self):
        print("Add Document File")


    def load_document_file(self):
        print("Load Document File")


    def load_document_db(self):
        print("Load Document DB")

        document = self.db.load_document_id("document_data", doc["doc_id"])
