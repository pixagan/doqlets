from laeyerz.utils.KeyManager import KeyManager
from laeyerz.flow.Flow import Flow
from laeyerz.flow.Node import Node

from laeyerz_nodes.llm.OpenAINode import OpenAINode as LLM
from laeyerz_nodes.fileloaders.PdfLoader import PdfLoader
from laeyerz_nodes.dataprocessors.TextProcessor import TextProcessorNode
from laeyerz_nodes.embeddings.SentenceTransformerNode import SentenceTransformerNode as Embeddings
from laeyerz_nodes.vectorstores.FaissNode import FaissNode as VectorStore

from laeyerz.nodes.llm.PromptNode import PromptNode

from nodes.ChromaNode import ChromaNode


km = KeyManager()


pdf_loader    = PdfLoader("PdfLoader")

#Combine text into a single string
combine_text  = TextProcessorNode("CombinePages")

#Split Text
split_text     = TextProcessorNode("SplitText")

#Text to Embeddings
embedding_model  = Embeddings("Embeddings")
embedding_model2 = Embeddings("Embeddings2")

#Create Vector Store
vector_store = VectorStore("DocumentStore")

api_key = km.get('OPENAI_API_KEY')
llm_node = LLM("LLM", config={"api_key": api_key, "model":"gpt-5-mini"})


prompt_template = {
"roles": {
        "instructions":"developer",
        "context":"user",
        "query":"user",
}
}

promptNode = PromptNode("Prompt", config={}, template=prompt_template)
promptNode.add_prompt_inputs(
    [
        {"name": "instructions", "type": "str"},
        {"name": "context", "type": "list"},
        {"name": "query", "type": "str"}
    ]
)
promptNode = promptNode






#-----Creating thh Flow
store_flow = Flow("DocumentStore")

#-----adding nodes
store_flow.add_node(pdf_loader)
store_flow.add_node(combine_text)
store_flow.add_node(split_text)
store_flow.add_node(embedding_model)
store_flow.add_node(vector_store)

#-----adding edges
store_flow.add_edge("START", "PdfLoader|extract_pdf_text")
store_flow.add_edge("PdfLoader|extract_pdf_text", "CombinePages|combine_pages")
store_flow.add_edge("CombinePages|combine_pages", "SplitText|split_text")
store_flow.add_edge("SplitText|split_text", "Embeddings|encode")
store_flow.add_edge("Embeddings|encode", "DocumentStore|store")
store_flow.add_edge("DocumentStore|store", "END")


#---adding data sources
store_flow.add_data_source("PdfLoader|extract_pdf_text|loaded_file", "INPUTS|file")
store_flow.add_data_source("CombinePages|combine_pages|pages", "PdfLoader|extract_pdf_text|doc_pages")
store_flow.add_data_source("SplitText|split_text|text", "CombinePages|combine_pages|text")
store_flow.add_data_source("Embeddings|encode|sentences", "SplitText|split_text|chunks")
store_flow.add_data_source("DocumentStore|store|vectors", "Embeddings|encode|embeddings")
store_flow.add_data_source("DocumentStore|store|metadata", "SplitText|split_text|chunks")

store_flow.finalize()
