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


const AddBlock = ({ page_id, addBlockRequest }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)

    const [blockType, setBlockType] = useState('')
    const [blockTitle, setBlockTitle] = useState('')
    const [blockDefinition, setBlockDefinition] = useState('')
    const [blockRules, setBlockRules] = useState('')

   
    const createBlock = () => {

      
        
    }

    
    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }


    useEffect(() => {
        
    }, [])



    return (

        <>

            
            <Card style={{border:'None', margin:'5px', padding:'5px'}}>
                <Form.Control type="text" placeholder="Enter title (required)" value={blockTitle} onChange={(e) => setBlockTitle(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>
                <Form.Control as="textarea" rows={20} placeholder="Block Definition : What the block should contain" value={blockDefinition} onChange={(e) => setBlockDefinition(e.target.value)} onInput={resizeTextarea} ref={textareaRef}/>
                <Form.Control as="textarea" rows={20} placeholder="Block Rules : Formatting requests, etc." value={blockRules} onChange={(e) => setBlockRules(e.target.value)} onInput={resizeTextarea} ref={textareaRef}/>
                <Button variant="primary" onClick={()=>createBlock()}>Create Block</Button>

            </Card>
                
        </>



    )
}



export default AddBlock
