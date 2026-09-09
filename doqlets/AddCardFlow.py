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

from ProjectManager import ProjectManager



pm = ProjectManager()


def get_card_meta(card):
    #get the meta data for the card

    return {
        "title": card["title"],
        "description": card["description"],
    }



def get_relevant_pages(card_meta):
    #get the relevant pages for the card

    #relevant pages, relevant sections

    return {
        "relevant_pages": [],
        "relevant_sections": [],
    }



def get_related_cards(card_meta):
    #get the related cards for the card

    return {
        "related_cards": [],
    }



def determine_merge(card, card_meta, relevant_pages, relevant_sections, related_cards):
    #determine if the card should be merged with an existing card


    #get relevant cards in sections

    #determine which sections the card should be added to

    return {
        "merge_requests": []
    }



def finalize_merge(card, card_meta, relevant_pages, relevant_sections, related_cards):
    
    #based on the merge request, make the relevant llm calls to update specified cards

    #new cards to be added
    #cards to be updated
    #cards to be deleted
    return {
        "update_requests": [],
    }






addCardFlow = Flow("AddCardFlow")


addCardFlow.add_edges("START", "GetCardMeta|get_card_meta")
addCardFlow.add_edges("GetCardMeta|get_card_meta", "GetRelevantPages|get_relevant_pages")
addCardFlow.add_edges("GetRelevantPages|get_relevant_pages", "GetRelatedCards|get_related_cards")
addCardFlow.add_edges("GetRelatedCards|get_related_cards". "DetermineMerge|determine_merge")
addCardFlow.add_edges("DetermineMerge|determine_merge", "FinalizeMerge|finalize_merge")
addCardFlow.add_edges("FinalizeMerge|finalize_merge", "UpdateExistingCards|update_existing_cards")
addCardFlow.add_edges("UpdateExistingCards|update_existing_cards", "AddNewCards|add_new_cards")
addCardFlow.add_edges("AddNewCards|add_new_cards", "RemoveDuplicates|remove_duplicates")
addCardFlow.add_edges("RemoveDuplicates|remove_duplicates", "END")


