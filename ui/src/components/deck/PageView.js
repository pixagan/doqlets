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
import BlockSettingsView from '../cards/BlockSettingsView'

const PageView = ({ project_id, page_id, page_title }) => {

    const dispatch = useDispatch()


    const [pageTitle, setPageTitle] = useState('Page')
    const [pageModel, setPageModel] = useState({})
    const [cards, setCards] = useState([])
    const [selectedCard, setSelectedCard] = useState("")
    const [selectedCardTitle, setSelectedCardTitle] = useState("")

    const [viewMode, setViewMode] = useState('content') // content, addblock, pagesettings, blocksettings

    const toggleViewMode = (mode_in) => {

        if(mode_in == viewMode){
            setViewMode('content')
        }else{
            setViewMode(mode_in)
        }

    }

    const toggleBlockSettingsView = (card_id, title) => {
 
        setSelectedCard(card_id)
        setSelectedCardTitle(title)
        toggleViewMode('blocksettings')

    }


    const loadPageBlocks = async (page_id) => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/pages/${project_id}/${page_id}`, config)
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
        const response = await axios.post(`/api/pages/blocks/${project_id}/${page_id}`, config)
        console.log("response ", response.data)
    }

    const updatePageBlockList = (newCard) => {
        setCards([newCard, ...cards])
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
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>toggleViewMode('content')}>Content</ListGroup.Item>
                <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>toggleViewMode('addblock')}>Add Block</ListGroup.Item>
               {/*} <ListGroup.Item style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>toggleViewMode('pagesettings')}>Page Settings</ListGroup.Item> */}
                
            </ListGroup>

            <Row>
                <Col style={{"overflow-x":'scroll', minHeight:'95vh'}}>

                <hr />

                <p className='h4'>{pageModel && pageModel.title}</p>

                    


                    {cards.map((card, index)=>(
                    <BlockView project_id={project_id} page_id={page_id} card={card} blockSettingsView={toggleBlockSettingsView}/>

                    ))}
                
                </Col>

                {viewMode == "addblock" && (
                    <Col>
                        <AddBlock project_id={project_id} page_id={page_id} addBlockRequest={updatePageBlockList} />
                                    
                            
                    </Col>
                )}

                {viewMode == "pagesettings" && (
                    <Col>
                            <PageSettingsView project_id={project_id} page_id={page_id} page_title={page_title} />
                                    
                            
                    </Col>
                )}

                {viewMode == "blocksettings" && (
                    <Col>
                            

                            <BlockSettingsView project_id={project_id} card_id={selectedCard} title={selectedCardTitle} page_id={page_id}/>
                                    
                            
                    </Col>
                )}
               
            </Row>

           



          
                
                </>
            )}

        

                
        </div>



    )
}



export default PageView
