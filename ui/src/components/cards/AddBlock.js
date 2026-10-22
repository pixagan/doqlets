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


const AddBlock = ({ project_id, page_id, addBlockRequest }) => {

    const dispatch = useDispatch()

    const textareaRef1 = useRef(null)
    const textareaRef2 = useRef(null)
    const textareaRef3 = useRef(null)

    const [blockType, setBlockType] = useState('')
    const [blockTitle, setBlockTitle] = useState('')
    const [blockDefinition, setBlockDefinition] = useState('')
    const [blockRules, setBlockRules] = useState('')
    const [blocktypes, setBlockTypes] = useState(["paragraph", "table", "list"])
    const [blockContext, setBlockContext] = useState('')
   
    const createBlock = async() => {

        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }

        var newBlock = {
            "title":blockTitle,
            "block_type":blockType,
            "block_description":blockDefinition,
            "rules":blockRules,
            "context":blockContext,
        }

        const response = await axios.post(`/api/pages/blocks/${project_id}/${page_id}`, newBlock, config)
        console.log("response ", response.data)
        //addBlockRequest(response.data.block)
        
    }

    
    const resizeTextarea1 = () => {
        const textarea = textareaRef1.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }

    const resizeTextarea2 = () => {
        const textarea = textareaRef2.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }

    const resizeTextarea3 = () => {
        const textarea = textareaRef3.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }

    useEffect(() => {
        
    }, [])



    return (

        <>

            
            <Card style={{border:'None', margin:'5px', padding:'5px'}}>
                <Form.Control type="text" placeholder="Enter title (required)" value={blockTitle} onChange={(e) => setBlockTitle(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>

                 <Form.Select aria-label="Block Type" value={blockType} onChange={(e)=>setBlockType(e.target.value)} style={{marginBottom:'10px'}}>

                <option value="">Select Block type</option>
                {blocktypes.map((skill, index)=>(
                  <option key={index} value={skill}>{skill}</option>
                ))}
              </Form.Select>

                
                <Form.Control as="textarea" rows={5} placeholder="Block Instructions : Formatting requests, etc." value={blockRules} onChange={(e) => setBlockRules(e.target.value)} onInput={resizeTextarea1} ref={textareaRef1} style={{marginBottom:"10px"}}/>

                <Form.Control as="textarea" rows={5} placeholder="What is the block about?(Optional)" value={blockDefinition} onChange={(e) => setBlockDefinition(e.target.value)} onInput={resizeTextarea2} ref={textareaRef2} style={{marginBottom:"10px"}}/>

                <Form.Control as="textarea" rows={5} placeholder="Any context that might be required (Optional)" value={blockContext} onChange={(e) => setBlockContext(e.target.value)} onInput={resizeTextarea3} ref={textareaRef3} style={{marginBottom:"10px"}}/>

                <Button variant="primary" onClick={()=>createBlock()}>Create Block</Button>

            </Card>
                
        </>



    )
}



export default AddBlock
