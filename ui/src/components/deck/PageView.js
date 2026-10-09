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
import ContentCard from '../cards/ContentCard'
import AddBlock from '../cards/AddBlock'
import PageSettingsView from './PageSettingsView'
import BlockView from '../cards/BlockView'

const PageView = ({ page_id, page_title }) => {

    const dispatch = useDispatch()


    const [pageTitle, setPageTitle] = useState('Page')
    const [pageModel, setPageModel] = useState({})
    const [cards, setCards] = useState([])

    const [viewMode, setViewMode] = useState('wiki') // content, addblock, pagesettings, blocksettings


    const loadPageBlocks = async (page_id) => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/pages/${page_id}`, config)
        console.log("response ", response.data)
        setCards(response.data.cards)
        setPageModel(response.data.page_model)
    }


    const addBlockRequest = async (page_id) => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post(`/api/pages/blocks/${page_id}`, config)
        console.log("response ", response.data)
    }
    


    useEffect(() => {

        console.log("cards ", cards)
        if (page_id != null) {
            loadPageBlocks(page_id)
        }
    }, [page_id])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>


            {page_id == null ? (
                <>
                 <p className='h4'>Select a page from the Menu on the left</p>
                 <p className='h4'>To add data, click the Docs Tab and use the Add Data Form.</p>
                </>
               
            ): (
                <>
                
            <ListGroup horizontal>
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>setViewMode('content')}>Content</ListGroup.Item>
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>setViewMode('addblock')}>Add Block</ListGroup.Item>
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>setViewMode('pagesettings')}>Page Settings</ListGroup.Item>
                
            </ListGroup>

            <Row>
                <Col>

                <p className='h4'>{pageModel && pageModel.title}</p>

                    <br />


                    {cards.map((card, index)=>(
                    <BlockView page_id={page_id} card={card} />

                    ))}
                
                </Col>

                {viewMode == "addblock" && (
                    <Col>
                        <AddBlock page_id={page_id} addBlockRequest={addBlockRequest} />
                                    
                            
                    </Col>
                )}

                {viewMode == "pagesettings" && (
                    <Col>
                            <PageSettingsView project_id={""} page_id={page_id} page_title={page_title} />
                                    
                            
                    </Col>
                )}
               
            </Row>

           



          
                
                </>
            )}

        

                
        </div>



    )
}



export default PageView
