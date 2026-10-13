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

const PageSettingsView = ({ project_id, page_id, page_title }) => {

    const dispatch = useDispatch()


    const [pageTitle, setPageTitle] = useState('Page')
    const [pageModel, setPageModel] = useState({})
    const [cards, setCards] = useState([])

    const [viewMode, setViewMode] = useState('wiki') // wiki, pagemodel


    const loadPageSettings = async (page_id) => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/wiki/pages/settings/${page_id}`, config)
        console.log("response ", response.data)
       
    }


    


    useEffect(() => {
        
        //loadPageSettings(page_id)
        
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None', margin:'2px'}}>

           <p className='h4'>Page Description</p>

           <p className='h4'>Page Rules</p>

                
        </div>



    )
}



export default PageSettingsView
