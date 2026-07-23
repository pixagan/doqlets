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

  import PageView from '../components/deck/PageView'
  import DataView from '../components/deck/DataView'
  import AddData from '../components/deck/AddData'
  import ChatCard from '../components/deck/ChatCard'
  import SearchCard from '../components/deck/SearchCard'
  import AgentCard from '../components/deck/AgentCard'

  
export const WikiScreen = ({match, history}) => {

    const dispatch = useDispatch()

    const navigate = useNavigate();

    const [pageTitle, setPageTitle] = useState('')

    const [sectionType, setSectionType] = useState("all") 
    const [documents, setDocuments] = useState([])

    const [rightView, setRightView] = useState("pages") // chat, add, view
    const [query, setQuery] = useState('')
    const [chatHistory, setChatHistory] = useState([])
    const [docPages, setDocPages] = useState([])

    const [project_id, setProjectId] = useState(null)
    const [page_id, setPageId] = useState(null)
    const [selectedPage, setSelectedPage] = useState(null)

    const [cards, setCards] = useState([])

    const [pages, setPages] = useState([])


    const [chatView, setChatView] = useState("chat") //search, chat

    
    const addPage = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post('/api/pages', { title: pageTitle }, config)
        console.log("response ", response)
        setPages([...pages, response.data.page])
    }


    const loadPages = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/pages`, config)
        console.log("response ", response)
        setPages(response.data.pages)
    }


    


    const selectPage = async (page_id, page_title) => {
        setPageId(page_id)
        //setPageTitle(page_title)
        setSelectedPage(page_id)
        setRightView("pages")

        //loadPageCards(page_id)
    }


    useEffect(() => {
        
        loadPages()

    }, [])



    return(
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', textAlign: 'center', margin:'5px', padding:'5px' }}>

         <Meta title={'Doqlets'} description={'Doqlets'}/>
    
         <Row>
            <Col xs={2} style={{maxHeight: '95vh', overflow: 'scroll'}}>

             {/* <p className='h4'>Project View</p> */}
             {/* <DataView project_id={project_id} /> */}

              <ListGroup>
                <ListGroup.Item style={{padding:'1px'}}>
                    <InputGroup>
                    <Form.Control type="text" placeholder="Enter page title" value={pageTitle} onChange={(e)=>setPageTitle(e.target.value)} />
                    <Badge onClick={()=>addPage()}>+</Badge>
                    </InputGroup>
                </ListGroup.Item>

              {pages && pages.map((page, index)=>(
                <ListGroup.Item key={index} className='text-left' style={{fontWeight:'bold'}} onClick={()=>selectPage(page.uid, page.title)} active={page_id === page.uid}>
                {page.title}
                </ListGroup.Item>
             ))}
                
              </ListGroup>
             
            
            </Col>


            <Col style={{ maxHeight: '95vh', overflow: 'scroll'}}>

            <ListGroup horizontal>
                <ListGroup.Item onClick={()=>setRightView("pages")} active={rightView === "pages"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    View
                </ListGroup.Item>
                <ListGroup.Item onClick={()=>setRightView("add")} active={rightView === "add"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Add Data
                </ListGroup.Item>
                <ListGroup.Item onClick={()=>setRightView("chat")} active={rightView === "chat"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Chat
                </ListGroup.Item>
                <ListGroup.Item onClick={()=>setRightView("agents")} active={rightView === "agents"} style={{paddingTop:'5px', paddingBottom:'5px'}}>
                    Agents
                </ListGroup.Item>
            </ListGroup>

            <br />


            {rightView === "pages" && (
                <div>
                     <PageView project_id={project_id} page_id={page_id} page_title={pageTitle} />

                </div>
            )}


            
            {rightView === "add" && (
                <div>

                    <AddData project_id={project_id} />
                
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



            
            
            </Col>
         </Row>


           
        </div>
    )
}

export default WikiScreen