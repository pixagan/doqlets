# Doqlets - Turn your documents into living intelligence, build intelligent pages block by block. Agents that handle RAG and other relevant tasks built in to work on the data.

Built on the Laeyerz Library (https://github.com/pixagan/Laeyerz)

## License

Doqlets is licensed under the [Apache License 2.0](LICENSE).

This means you are free to use, modify, and distribute this software in
source or binary form, provided you comply with the terms of the license.
See the [NOTICE](NOTICE) file for attribution requirements.


## Installing Doqlets

### Install Backend
Navigate to the doqlets folder
`pip install -e .`

Run `python DoqletsApp.py` to start the server

### Install Frontend
Navigate to the ui folder
Run an `npm install`
Run `npm start` to start the frontend 



#### Dependencies
- Laeyerz  - Workflow and Agents
- Open AI LLM
- Chroma DB
- Mongo DB



## How it works
Currently Doqlets allows you to add text and pdfs.


## Creating Pages
Create a Page using the Pages View.

Add Smart Blocks to the Page. For the Smart Block define what the block handles.

## Agents
Laeyerz Agents are plugged in to the knowledge store. You can use them along with tools provided for tasks. You can customize the code to add custom tools, skills to perform tasks not pre built.

## RAG
All documnts you add, unless explicitly specified are indexed and stored. You can ask questions about any of them and get the relevant responses. The Agent handles RAG.


