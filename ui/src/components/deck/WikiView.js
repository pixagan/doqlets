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
import PageView from './PageView'
import AddWikiPage from './AddWikiPage'

const WikiView = ({ project_id }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)


    const [rightView, setRightView] = useState('wiki') //wiki. add

    const [pageTitle, setPageTitle] = useState('')

    const [sections, setSections] = useState([ ])

    const [cards, setCards] = useState([])

    const [pages, setPages] = useState([])

    const [page_id, setPageId] = useState(null)
    const [selectedPage, setSelectedPage] = useState(null)
    

    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }


    const setAddPageRequest = (page) => {
        setPages([...pages, page])
    }

    const addPage = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post('/api/wiki/pages', { title: pageTitle }, config)
        console.log("response ", response)
        setPages([...pages, response.data.page])
    }


    const loadPages = async () => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/wiki/pages`, config)
        console.log("response ", response)
        setPages(response.data.pages)
    }


    


    const selectPage = async (page_id, page_title) => {
        setPageId(page_id)
        //setPageTitle(page_title)
        setSelectedPage(page_id)
        setRightView('wiki')
    

        //loadPageCards(page_id)
    }



    useEffect(() => {
        
        loadPages()
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>

<Row>
            <Col xs={2} style={{maxHeight: '95vh', overflow: 'scroll'}}>

             {/* <p className='h4'>Project View</p> */}
             {/* <DataView project_id={project_id} /> */}

              <ListGroup>
                {/* <ListGroup.Item style={{padding:'1px'}}>
                    <InputGroup>
                    <Form.Control type="text" placeholder="Enter page title" value={pageTitle} onChange={(e)=>setPageTitle(e.target.value)} />
                    <Badge onClick={()=>addPage()}>+</Badge>
                    </InputGroup>
                </ListGroup.Item> */}

                <ListGroup.Item style={{padding:'5px', border:'None'}}>
                    <Button onClick={()=>setRightView('add')} style={{width:'90%', backgroundColor:'blue', borderRadius:'10px'}}>Add Page</Button>
                </ListGroup.Item>
                    

              {pages && pages.map((page, index)=>(
                <ListGroup.Item key={index} className='text-left' style={{fontWeight:'bold'}} onClick={()=>selectPage(page.uid, page.title)} active={page_id === page.uid}>
                {page.title}
                </ListGroup.Item>
             ))}
                
              </ListGroup>

              </Col>


              <Col>
              {rightView === "wiki" && (
              <PageView project_id={project_id} page_id={page_id} page_title={pageTitle} />
              )}
              {rightView === "add" && (
                <AddWikiPage project_id={project_id} setAddPageRequest={setAddPageRequest}/>
              )}
              </Col>
             
            
          

            </Row>
          
                
        </div>



    )
}



export default WikiView
