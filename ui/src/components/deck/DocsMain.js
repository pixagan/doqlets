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
import DocView from './DocView'
import AddData from './AddData'


const DocsMain = ({ project_id }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)
    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }

    const [pageTitle, setPageTitle] = useState('')
    const [doc_id, setDocId] = useState(null)
    const [selectedPage, setSelectedPage] = useState(null)
    const [rightView, setRightView] = useState("view")  //view, add
    const [docs, setDocs] = useState([])

    const addDoc = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post('/api/pages', { title: pageTitle }, config)
        console.log("response ", response)
        setDocs([...docs, response.data.page])
    }

    const selectPage = async (page_id, page_title) => {
        setDocId(page_id)
        setSelectedPage({_id:page_id, title:page_title})
        setRightView("view")

    }


    const loadDocs = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/documents`, config)
        console.log("response ", response)
        setDocs(response.data.documents)
    }

    const callBackAddData = async (newDoc) => {
        setDocs([newDoc, ...docs])
        setDocId(newDoc._id)
        setRightView("view")
    }

    

    


    useEffect(() => {

        loadDocs()
        
    }, [])

    useEffect(() => {
        console.log("Update Doc View ", doc_id)
    }, [doc_id])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>


          <Row>
                <Col xs={2} style={{maxHeight: '95vh', overflow: 'scroll'}}>



                    
                    <ListGroup>
                        <ListGroup.Item style={{borderLeft:'None', borderRight:'None', borderTop:'None'}}>
                        <Button onClick={()=>setRightView("add")} style={{width:'80%'}}>Add Data</Button>
                        </ListGroup.Item>
                        <ListGroup.Item style={{padding:'1px'}}>
                            <InputGroup>
                            <Form.Control type="text" placeholder="Enter doc title" value={pageTitle} onChange={(e)=>setPageTitle(e.target.value)} />
                            <Badge onClick={()=>addDoc()}>+</Badge>
                            </InputGroup>
                        </ListGroup.Item>

                        {docs && docs.map((doc, index)=>(
                            <ListGroup.Item key={index} className='text-left' style={{fontWeight:'bold'}} onClick={()=>selectPage(doc._id, doc.title)} active={doc_id === doc._id}>
                            {doc.title}
                            </ListGroup.Item>
                        ))}

                    </ListGroup>


                    </Col>

                    {rightView == "view" && (
                        <Col>
                        <DocView project_id={project_id} doc_id={doc_id} />
                        </Col>
                    )}

                    {rightView == "add" && (
                        <Col>
                        <AddData project_id={project_id} callBackAddData={callBackAddData} />
                        </Col>
                    )}
                   

        </Row>





                
        </div>

    )
}



export default DocsMain
