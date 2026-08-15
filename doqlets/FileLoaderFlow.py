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

from nodes.PdfLoader import PdfLoader
from nodes.TextProcessor import TextProcessorNode


pdf_loader = PdfLoader("PdfLoader")

#Combine text into a single string
combine_text  = TextProcessorNode("CombinePages")

#Split Text
split_text     = TextProcessorNode("SplitText")


 #-----Creating thh Flow
fileloader_flow = Flow("FileLoaderFlow")

#-----adding nodes
fileloader_flow.add_node(pdf_loader)
fileloader_flow.add_node(combine_text)
fileloader_flow.add_node(split_text)

#-----adding edges
fileloader_flow.add_edge("START", "PdfLoader|extract_pdf_text")
fileloader_flow.add_edge("PdfLoader|extract_pdf_text", "CombinePages|combine_pages")
fileloader_flow.add_edge("CombinePages|combine_pages", "SplitText|split_text")
fileloader_flow.add_edge("SplitText|split_text", "END")


#---adding data sources
fileloader_flow.add_data_source("PdfLoader|extract_pdf_text|loaded_file", "INPUTS|file")
fileloader_flow.add_data_source("CombinePages|combine_pages|pages", "PdfLoader|extract_pdf_text|doc_pages")
fileloader_flow.add_data_source("SplitText|split_text|text", "CombinePages|combine_pages|text")

fileloader_flow.finalize()