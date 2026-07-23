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

const PageView = ({ page_id, page_title }) => {

    const dispatch = useDispatch()


    const [pageTitle, setPageTitle] = useState('Page')
    const [cards, setCards] = useState([])


    const loadPageCards = async (page_id) => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/pages/${page_id}`, config)
        console.log("response ", response.data)
        setCards(response.data.cards)
    }
    


    useEffect(() => {

        console.log("cards ", cards)
        loadPageCards(page_id)
    }, [page_id])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>


            {page_id == null && (
                <p className='h4'>Select a page from the Menu on the left</p>
            )}

             <p className='h4'>{page_title}</p>

             <br />


            {cards.map((card, index)=>(
                <ContentCard page_id={page_id} card={card} />
            
            ))}
               
                

                
        </div>



    )
}



export default PageView
