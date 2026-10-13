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

import { Settings, Workflow, Tag, Pencil } from 'lucide-react'


import { MarkdownView } from '../cards/MarkdownView'



const BlockSettingsView = ({ project_id, page_id, title, card_id}) => {

    const dispatch = useDispatch()

    const [viewMode, setViewMode] = useState('rules') // rules, edit, tags, connections

    const [cardDetail, setCardDetail] = useState({})
    const [tags, setTags] = useState('')
    const [connections, setConnections] = useState('')

     const [blockType, setBlockType] = useState('')
    const [blockTitle, setBlockTitle] = useState('')
    const [blockDefinition, setBlockDefinition] = useState('')
    const [blockRules, setBlockRules] = useState('')
    const [blocktypes, setBlockTypes] = useState(["paragraph", "table", "list"])
    

    const toggleViewMode = (mode_in) => {

        if(mode_in == viewMode){
            setViewMode('rules')
        }
        else{
            setViewMode(mode_in)
        }
    }

    const [settingsView, setSettingsView] = useState('')
    const updateSettingsView = (view) => {

        if(view === settingsView){
            setSettingsView('')
        }else{
            setSettingsView(view)
        }
        
    }

    const loadBlockSettings = async() => {

        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/pages/blocks/${project_id}/${card_id}`, config)
        console.log("response ", response.data)
        setCardDetail(response.data.block)

        setBlockTitle(response.data.block.title)
        setBlockRules(response.data.block.rules)
        setBlockType(response.data.block.type)




    }

    const updateBlockRequest = async() => {

    }

     
    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }

    const textareaRef = useRef(null)


    useEffect(() => {

        loadBlockSettings()
        
    }, [card_id])



    return (

        <>

            <p className='h3'><Settings /> <span>Block Settings</span>  </p>

            <hr />
            
            <Card style={{border:'None', margin:'2px', padding:'5px'}}>
                <Card.Header style={{border:'None', textAlign:'left', fontWeight:'bold'}}>
                    {title}
                </Card.Header>
                <Card.Body>
                    <InputGroup>
                        <Badge bg='light' onClick={()=>toggleViewMode("rules")}><Settings size={16}/></Badge>
                        <Badge bg='light' onClick={()=>toggleViewMode("edit")}><Pencil size={16}/></Badge>
                        <Badge bg='light' onClick={()=>toggleViewMode("connections")}><Workflow size={16}/></Badge>
                        <Badge bg='light' onClick={()=>toggleViewMode("tags")}><Tag size={16}/></Badge>
                        
                    </InputGroup>
                </Card.Body>

               {viewMode == 'rules' && (
                    <Card.Body style={{border:'None', textAlign:'left'}}>
                     

                        {cardDetail && cardDetail.title && (
                            <p><span className='h5' style={{backgroundColor:'#e4ebf7', marginRight:'10px'}}>Title : </span><span>{cardDetail.title}</span></p>
                        )}

                        {cardDetail && cardDetail.type && (
                            <p><span className='h5' style={{backgroundColor:'#e4ebf7', marginRight:'10px'}}>Type : </span><span>{cardDetail.type}</span></p>
                        )}


                        {cardDetail && cardDetail.rules && (
                            <p><span className='h5' style={{backgroundColor:'#e4ebf7', marginRight:'10px'}}>Rules : </span><span>{cardDetail.rules}</span></p>
                        )}


                    </Card.Body>
               )}

               {viewMode == 'edit' && (
                <>
                    <Card.Body style={{border:'None', margin:'5px', padding:'5px'}}>
                        <Form.Control type="text" placeholder="Enter title (required)" value={blockTitle} onChange={(e) => setBlockTitle(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>

                        <Form.Select aria-label="Block Type" value={blockType} onChange={(e)=>setBlockType(e.target.value)} style={{marginBottom:'10px'}}>

                        <option value="">Select Block type</option>
                        {blocktypes.map((skill, index)=>(
                        <option key={index} value={skill}>{skill}</option>
                        ))}
                    </Form.Select>


                    <Form.Control as="textarea" rows={5} placeholder="Block Definition : What the block should contain" value={blockDefinition} onChange={(e) => setBlockDefinition(e.target.value)} onInput={resizeTextarea} ref={textareaRef} style={{marginBottom:"10px"}}/>
                        
                        <Form.Control as="textarea" rows={5} placeholder="Block Rules : Formatting requests, etc." value={blockRules} onChange={(e) => setBlockRules(e.target.value)} onInput={resizeTextarea} ref={textareaRef} style={{marginBottom:"10px"}}/>

                        <Button variant="primary" onClick={()=>updateBlockRequest()}>Update Block</Button>

                    </Card.Body>

                </>
               )}
                    
               
                
        


            {viewMode === 'tags' && (
                <Card.Body>
                    <p style={{textAlign:'left'}}>Tags</p>
                    
                    {/*{tags.map((tag, index)=>(
                        <Badge bg='light' key={index} variant="primary">{tag}</Badge>
                    ))} */}

                </Card.Body>
            )}

            {viewMode === 'connections' && (
                <Card.Body>
                    <p style={{textAlign:'left'}}>Connections</p>
                  {/*}  {connections.map((connection, index)=>(
                        <Badge bg='light' key={index} variant="primary">{connection}</Badge>
                    ))} */}
                </Card.Body>
            )}

                 
                    


                    
                 
                 

            </Card>
                
        </>



    )
}



export default BlockSettingsView
