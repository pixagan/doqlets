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


const TaskView = ({ task_card }) => {

    const dispatch = useDispatch()

    const [chatHistory, setChatHistory] = useState([])

    const [viewMode, setViewMode] = useState('output') //summary
   

    useEffect(() => {
        
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>

            <Card>
                <Card.Header>
                    <Card.Title style={{textAlign:'left'}}>{task_card.task} | <Badge bg="light">{task_card.skill}</Badge></Card.Title>
                </Card.Header>
                <Card.Body>
                    <ListGroup horizontal>
                        <ListGroup.Item onClick={()=>setViewMode('output')} active={viewMode === 'output'} style={{paddingTop:'5px', paddingBottom:'5px'}}>Outputs</ListGroup.Item>
                        <ListGroup.Item onClick={()=>setViewMode('summary')} active={viewMode === 'summary'} style={{paddingTop:'5px', paddingBottom:'5px'}}>Summary</ListGroup.Item>
                    </ListGroup>

                    {viewMode === 'output' && (
                        <>
                        <p className='h5'>Outputs</p>
                    {task_card && task_card.agent_response && task_card.agent_response.output && Object.keys(task_card.agent_response.output).map((key, index) => (
                        <p key={index} style={{"textAlign":"left"}}><span style={{"fontWeight":"bold"}}>{key}:</span> <span style={{"fontWeight":"normal"}}>{task_card.agent_response.output[key]}</span></p>
                    ))}
                        </>
                    
                    )}

                    {viewMode === 'summary' && (
                        <>
                    <p className='h5'>Summary</p>
                    <ul style={{"textAlign":"left"}}>

                    {task_card && task_card.agent_response && task_card.agent_response.task_keypoints && task_card.agent_response.task_keypoints.map((item, index) => (
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
