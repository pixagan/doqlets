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
import { MarkdownView } from '../cards/MarkdownView'


const TaskView = ({ task_card }) => {

    const dispatch = useDispatch()

    const [chatHistory, setChatHistory] = useState([])

    const [viewMode, setViewMode] = useState('output') //summary
   

    useEffect(() => {
        
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px',maxHeight:'95vh', overflow:'scroll', border:'None'}}>

            <Card>
                <Card.Header>
                    <Card.Title style={{textAlign:'left'}}>{task_card.task} | <Badge bg="light">{task_card.skill}</Badge></Card.Title>
                </Card.Header>
                <Card.Body>
                    <ListGroup horizontal style={{marginBottom:'15px'}}>
                        <ListGroup.Item onClick={()=>setViewMode('output')} active={viewMode === 'output'} style={{paddingTop:'5px', paddingBottom:'5px'}}>Outputs</ListGroup.Item>
                        <ListGroup.Item onClick={()=>setViewMode('summary')} active={viewMode === 'summary'} style={{paddingTop:'5px', paddingBottom:'5px'}}>Summary</ListGroup.Item>
                    </ListGroup>

                    {viewMode === 'output' && (
                        <>
                       
                        {/* <p>{task_card.response}</p> */}
                        <MarkdownView content={task_card.response} />
                    
                    
                        </>
                    
                    )}

                    {viewMode === 'summary' && (
                        <>
                    {/* <p className='h5' style={{textAlign:'left'}}>Summary</p> */}
                    <ul style={{"textAlign":"left"}}>

                    {task_card && task_card.keypoints && task_card.keypoints.map((item, index) => (
                        <li key={index}>{item}</li>
                    ))}
                    </ul>
                    </>
                    )}

                </Card.Body>

            </Card>
                
        </div>



    )
}



export default TaskView
