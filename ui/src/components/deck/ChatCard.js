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

import React, { useState, useEffect, Fragment, useRef } from 'react'
import PropTypes from 'prop-types'
import {Alert} from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, Image, ListGroup, Card, Button, Form, Table, InputGroup, Badge } from 'react-bootstrap'
import axios from 'axios'



const ChatCard = ({ project_id }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)

    const [chatHistory, setChatHistory] = useState([])
    const [query, setQuery] = useState('')

    const [searchResults, setSearchResults] = useState([])
    

    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }

    const chatRequest = async () => {

        var config={
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post('/api/chat', { query }, config)
        const answer = response.data.answer

        //console.log("query ", query)
        console.log("answer ", answer)

        setChatHistory([{ query: query, answer: answer }, ...chatHistory])

    }


    const loadHistory = async () => {
        const response = await axios.get('/api/chat')
        const history = response.data.chats
        console.log("history ", history)
        setChatHistory(history)
    }


    useEffect(() => {
        loadHistory()
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>

            
              <div>
                   

                   <p className='h4'>
                <span style={{marginRight:'10px'}}>Chat</span>
                {/* <Badge bg='light' style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>loadHistory()}>Load History</Badge> */}
            </p>
            

           
            <hr />

            <InputGroup>
                <Form.Control as="textarea" rows={5} placeholder="Enter your query" value={query} onChange={(e)=>setQuery(e.target.value)} className="mb-2"/>
                <Button variant="primary" onClick={()=>chatRequest()}>Chat</Button>
            </InputGroup>
            
                
            {chatHistory.map((item, index)=>(
                <Card key={index}>
                    <Card.Header>
                    <p className='text-left h5'>{item.query && item.query.toString()}</p>
                    </Card.Header>
                   
                   <Card.Body style={{maxHeight:'40vh', overflow:'scroll'}}>
                    <p className='text-left'>{item.answer && item.answer.toString()}</p>
                    {/* <MarkdownView content={item.answer} /> */}
                   </Card.Body>
                    
                </Card>
            ))}






                </div>
                

                
        </div>



    )
}



export default ChatCard
