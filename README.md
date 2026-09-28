# Doqlets - Turn your documents into living knowldge, build custom pages/views, RAG and Agents built in
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

Currently Doqlets allows devs to add text and pds.
Those are broken down into cards which are added to the relevant sections.

## Creating Pages
Create a Page using the Pages View. 
Add a Page and Define its rules, what it is about and what content should show up.

Then as you keep adding documents to a Project, any relevant Pages get updated in realtime.

When to create a Page, when you want clear visual info that can be seen without constantly asking RAG.

## RAG
All documnts you add, unless explicitly specified are indexed and stored. You can ask questions about any of them and get the relevant responses.


## Agents
Laeyerz Agents are plugged in to the knowledge store. You can use them along with tools provided for tasks. You can customize the code to add custom tools, skills to perform tasks not pre built.