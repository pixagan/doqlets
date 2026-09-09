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


const AddFiles = ({ project_id }) => {

    const dispatch = useDispatch()

    const textareaRef = useRef(null)

    const [chatHistory, setChatHistory] = useState([])
    const [query, setQuery] = useState('')
    const [skillList, setSkillList] = useState([
        {
            "name": "SlideGenerator",
            "description": "Generate a slide deck based on the input data",
            "file":"skills/PresentationGenerator.md",
        },
    ])

    const [selectedSkill, setSelectedSkill] = useState('')

    const [searchResults, setSearchResults] = useState([])
    

    const resizeTextarea = () => {
        const textarea = textareaRef.current
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
    }


    const loadSkills = async () => {
        const response = await axios.get('/api/skills')
        const skills = response.data.skills
        console.log("skills ", skills)
        setSkillList(skills)
    }

    const chatRequest = async () => {

        var config={
            headers: {
                'Content-Type': 'application/json'
            }
        }

        console.log("selectedSkill ", selectedSkill)
        //console.log("selectedSkill['name'] ", selectedSkill["name"])
        console.log("query ", query)
        const response = await axios.post('/api/agents', { skill: selectedSkill, task: query }, config)
        const answer = response.data.task_response

        console.log("response ", answer.toString())

        setChatHistory([{ query: query, response: answer }, ...chatHistory])

    }


    const loadHistory = async () => {
        const response = await axios.get('/api/agents')
        const history = response.data.tasks
        console.log("history ", history)
        setChatHistory(history)
    }


    useEffect(() => {
        loadSkills()
        loadHistory()
    }, [])



    return (

        <div style={{backgroundColor:'white', padding:'1px', minHeight:'95vh',  border:'None'}}>

            
              <div>
                   

            <p className='h4'>
                <span style={{marginRight:'10px'}}>Tasks</span>
            </p>
            

           
            <hr />
            <InputGroup>
            
            <Form.Select aria-label="Default select example" value={selectedSkill} onChange={(e)=>setSelectedSkill(e.target.value)}>
              <option value="">Select an Agent</option>
              {skillList.map((skill, index)=>(
                <option key={index} value={skill.name}>{skill.name}</option>
              ))}
            </Form.Select>
            <Button variant="primary" onClick={()=>chatRequest()} style={{textAlign:'left'}}>Run</Button>
          </InputGroup>

            <Form.Control as="textarea" rows={5} placeholder="Task Data" value={query} onChange={(e)=>setQuery(e.target.value)} className="mb-2"/>
            

            <hr />

            <p className='h5'>Add Documents/Files</p>
           
            <hr />


                </div>
                

                
        </div>



    )
}



export default AddFiles
