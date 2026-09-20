// Copyright 2026 Pixagan Technologies
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


import React , {useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, Container, Card, Form, Button, ListGroup, OverlayTrigger, Popover, Tooltip, Carousel, InputGroup, FormControl, Table, Badge } from 'react-bootstrap'
import Meta from '../components/Meta'
import axios from 'axios'

import {
    BrowserView,
    MobileView,
    isBrowser,
    isMobile,
    deviceDetect
  } from "react-device-detect";

  import { useNavigate } from 'react-router-dom';

//   import PageView from '../components/deck/PageView'
  import WikiView from '../components/deck/WikiView'
//   import DataView from '../components/deck/DataView'
//   import AddData from '../components/deck/AddData'
  import ChatCard from '../components/deck/ChatCard'
  import SearchCard from '../components/deck/SearchCard'
  import AgentCard from '../components/deck/AgentCard'
//   import ProjectModel from '../components/deck/ProjectModel'
//   import DocView from '../components/deck/DocView'
  import DocsMain from '../components/deck/DocsMain'
  
export const WikiScreen = ({match, history}) => {

    const dispatch = useDispatch()

    const navigate = useNavigate();

    const [pageTitle, setPageTitle] = useState('')

    const [sectionType, setSectionType] = useState("all") 
    const [documents, setDocuments] = useState([])

    const [rightView, setRightView] = useState("wiki") // chat, add, view
    const [query, setQuery] = useState('')
    const [chatHistory, setChatHistory] = useState([])
    const [docPages, setDocPages] = useState([])

    const [project_id, setProjectId] = useState(null)
    
    

    const [cards, setCards] = useState([])


    


    const [chatView, setChatView] = useState("chat") //search, chat

    
   


    useEffect(() => {
        
     

    }, [])



    return(
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', textAlign: 'center', margin:'5px', padding:'5px' }}>

         <Meta title={'Doqlets'} description={'Doqlets'}/>

         <ListGroup horizontal>
                <ListGroup.Item onClick={()=>setRightView("wiki")} active={rightView === "wiki"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Wiki
                </ListGroup.Item>
                <ListGroup.Item onClick={()=>setRightView("docs")} active={rightView === "docs"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Docs
                </ListGroup.Item>
                <ListGroup.Item onClick={()=>setRightView("chat")} active={rightView === "chat"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Chat
                </ListGroup.Item>
                <ListGroup.Item onClick={()=>setRightView("agents")} active={rightView === "agents"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Agents
                </ListGroup.Item>
               
               
               
            </ListGroup>

            <br />
    
        


            {rightView === "wiki" && (
                <div>
                    <WikiView project_id={project_id} />
                   

                </div>
            )}


        


            {rightView === "chat" && (
                <div>
                    
                    <ListGroup horizontal>
                        <ListGroup.Item onClick={()=>setChatView("chat")} active={chatView === "chat"} style={{paddingTop:'5px', paddingBottom:'5px'}}>Chat</ListGroup.Item>
                        <ListGroup.Item onClick={()=>setChatView("search")} active={chatView === "search"} style={{paddingTop:'5px', paddingBottom:'5px'}}>Search</ListGroup.Item>
                        
                    </ListGroup>

                    {chatView === "search" && (
                        <SearchCard project_id={project_id} />
                    )}

                    {chatView === "chat" && (
                        <ChatCard project_id={project_id} />
                    )}

                

                  
                   

                </div>
            )}


            {rightView === "agents" && (
                <div>
                    
                    <AgentCard project_id={project_id} />
                 
                   
                </div>
            )}




            {rightView === "docs" && (
                <DocsMain project_id={project_id} />
              
            )}




           
        </div>
    )
}

export default WikiScreen