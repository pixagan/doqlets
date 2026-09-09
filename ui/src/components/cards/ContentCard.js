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


const ContentCard = ({ page_id, card}) => {

    const dispatch = useDispatch()

    const [viewSettings, setViewSettings] = useState(false)
    const toggleViewSettings = () => {
        setViewSettings(!viewSettings)
    }

    const [settingsView, setSettingsView] = useState('')
    const updateSettingsView = (view) => {

        if(view === settingsView){
            setSettingsView('')
        }else{
            setSettingsView(view)
        }
        
    }

    const textareaRef = useRef(null)


    useEffect(() => {
        
    }, [])



    return (

        <>

            
            <Card style={{border:'None', margin:'5px', padding:'5px'}}>
                <Card.Header style={{border:'None', textAlign:'left', fontWeight:'bold'}} onClick={()=>toggleViewSettings()}>
                    {card.title}
                </Card.Header>
                 <Card.Body style={{border:'None', textAlign:'left'}}>
                    {card.content}
                 </Card.Body>

                 {viewSettings && (
                    <div>
                        <InputGroup>
                            <Button style={{paddingTop:'2px', paddingBottom:'2px'}} onClick={()=>updateSettingsView('tags')}>Tags</Button>
                            <Button style={{paddingTop:'2px', paddingBottom:'2px'}} onClick={()=>updateSettingsView('connections')}>Connections</Button>
                        </InputGroup>


                        {settingsView === 'tags' && (
                            <div>
                                <p style={{textAlign:'left'}}>Tags</p>
                                {card.tags.map((tag, index)=>(
                                    <Badge bg='light' key={index} variant="primary">{tag}</Badge>
                                ))}

                            </div>
                        )}

                        {settingsView === 'connections' && (
                            <div>
                                <p style={{textAlign:'left'}}>Connections</p>
                                {card.connections.map((connection, index)=>(
                                    <Badge bg='light' key={index} variant="primary">{connection}</Badge>
                                ))}
                            </div>
                        )}
                    </div>
                 )}

            </Card>
                
        </>



    )
}



export default ContentCard
