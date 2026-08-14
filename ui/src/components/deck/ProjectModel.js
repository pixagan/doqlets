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

const ProjectModel = ({ project_id }) => {

    const dispatch = useDispatch()


    const [projectModel, setProjectModel] = useState({})


    const loadProjectModel = async (page_id) => {
        var config = {
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.get(`/api/pages/${page_id}`, config)
        console.log("response ", response.data)
        setProjectModel(response.data.project_model)
    }
    


    useEffect(() => {

      
        
    }, [])

    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh', maxHeight:'95vh', overflow:'scroll', border:'None'}}>


            <p className='h4'>Project Description</p>

            <hr />


            <p className='h4'>Page Creation Strategy</p>

            <hr />
   

           <p className='h4'>Page Sections Requirements</p>

           #how to break the page into sections


                
        </div>


    )
}



export default ProjectModel
