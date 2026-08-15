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


const DocView = ({ project_id, doc_id }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)

    const [selectedSection, setSelectedSection] = useState('')
    const [doc, setDoc] = useState(null)

    const [sections, setSections] = useState([ ])


    const loadDoc = async () => {
        if (!doc_id) return
        const response = await axios.get(`/api/documents/${doc_id}`)
        console.log("response ", response)
        setDoc(response.data.document)
    }
    

    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }


    useEffect(() => {

        loadDoc()
        
    }, [doc_id])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>

            {doc && (
                <div>
                    <p className='h5'>{doc.title}</p>
                    <p style={{textAlign:'left'}}>{doc.data}</p>
                </div>
            )}
          

                
        </div>



    )
}



export default DocView
