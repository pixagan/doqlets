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


const AddWikiPage = ({ project_id, callBackAddData, setAddPageRequest }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)


    const [selectedType, setSelectedType] = useState('text')
    const [selectPage, setSelectPage] = useState(null)

    const [title, setTitle] = useState('')

    const [description, setDescription] = useState('')

    const [pageRules, setPageRules] = useState('')

    const [addMode, setAddMode] = useState('all') // all vs page


    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }


    const addPage = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post('/api/wiki/pages', { title: title, description:description, pageRules:pageRules }, config)
        console.log("response ", response)
        //setPages([...pages, response.data.page])

        setAddPageRequest(response.data.page)
    }


    const [selectedFile, setSelectedFile] = useState(null)
    const [fileName, setFileName] = useState('')

    
    

    useEffect(() => {
        
    }, [])

    return (

            <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>

                <Button style={{textAlign:'left'}}>Add Page</Button>
        
                <Form.Control type="text" placeholder="Enter title" value={title} onChange={(e) => setTitle(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>
                <Form.Control as="textarea" rows={5} placeholder="Page Rules" value={pageRules} onChange={(e) => setPageRules(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>
                <Form.Control as="textarea" rows={5} placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>
            
            </div>
        )
    }



export default AddWikiPage
