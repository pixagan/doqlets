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


const AddData = ({ project_id, callBackAddData }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)


    const [selectedType, setSelectedType] = useState('text')


    const [title, setTitle] = useState('')

    const [text, setText] = useState('')

    const [addMode, setAddMode] = useState('all') // all vs page

    const [selectedPage, setSelectedPage] = useState(null)
    const [pagelist, setPagelist] = useState([])

    const loadPages = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/wiki/pages`, config)
        console.log("response ", response)
        setPagelist(response.data.pages)
    }


    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }


    const uploadText = async () => {
        if (!text) return
        const response = await axios.post('/api/documents/text', {title:title, data:text})
        console.log("response ", response.data)
        callBackAddData(response.data.document)
    }


    const [selectedFile, setSelectedFile] = useState(null)
    const [fileName, setFileName] = useState('')

    const uploadDocument = async () => {
        if (!selectedFile) return
        const formData = new FormData()
        formData.append('file', selectedFile)   // must be 'file' to match backend

        const response = await axios.post('/api/documents/file', formData)
        console.log("response ", response.data)

        callBackAddData(response.data.document)

        // if(response.status === 200){
        //     const responseD = await axios.get('/api/document')
        //     console.log("doc_pages ", responseD.data.doc_pages)
        //     //setDocPages(responseD.data.doc_pages)
        // }
        
    }

    const handleFileChange = (e) => {
        const file = e.target.files?.[0]
        if (file) {
          setSelectedFile(file)
          setFileName(file.name)
        }
      }



    useEffect(() => {
        
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>

            
            <ListGroup horizontal>
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>setSelectedType('text')} active={selectedType === 'text'}>
                    Text
                </ListGroup.Item>
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>setSelectedType('file')} active={selectedType === 'file'}>
                    File
                </ListGroup.Item>
            </ListGroup>


             <InputGroup>
                <Form.Select addMode={addMode} value={addMode} onChange={(e) => setAddMode(e.target.value)}>
                    <option value="all">All</option>
                    <option value="page">Page</option>
                </Form.Select>

                <Form.Select value={selectedPage} value={addMode === 'page' ? selectedPage : null} onChange={(e) => setSelectedPage(e.target.value)}>
                    {pagelist.map((page, index) => (
                        <option key={index} value={page._id}>{page.title}</option>
                    ))}
                </Form.Select>
             </InputGroup>
             


            {selectedType === 'text' && (
                <div>
                    
                    <Form.Control type="text" placeholder="Enter title" value={title} onChange={(e) => setTitle(e.target.value)} style={{marginBottom:'10px', marginTop:'10px'}}/>
                    <Form.Control as="textarea" rows={20} placeholder="Enter text" value={text} onChange={(e) => setText(e.target.value)} onInput={resizeTextarea} ref={textareaRef}/>
                    <Button variant="primary" onClick={()=>uploadText()}>Upload</Button>
                </div>
            )}


            {selectedType === 'file' && (
                <div>
                    <div className="mt-3">
             <Form.Group controlId="formFile">
                <InputGroup>
                
                <Form.Control
                    type="file"
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileChange}
                    className="mb-2"
                />
                 <Button variant="primary" onClick={uploadDocument}>Upload</Button>
                
                </InputGroup>
              
                {fileName && (
                    <small className="text-muted d-block">
                    Selected: {fileName}
                    </small>
                )}
               
                </Form.Group>
            </div>
                </div>
            )}
                

                
        </div>



    )
}



export default AddData
