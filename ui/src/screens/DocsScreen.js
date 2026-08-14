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


import React , {useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, Container, Card, Form, Button, ListGroup, OverlayTrigger, Popover, Tooltip, Carousel, InputGroup, FormControl, Table, Badge } from 'react-bootstrap'
import Meta from '../components/Meta'
import axios from 'axios'

import {
    BrowserView,
    MobileView,
    isBrowser,
    isMobile,
    deviceDetect
  } from "react-device-detect";

  import { useNavigate } from 'react-router-dom';

  
export const DocsScreen = ({match, history}) => {

   
    const dispatch = useDispatch()

    const navigate = useNavigate();

    const [projects, setProjects] = useState([]) 
    const [projectName, setProjectName] = useState('')
   
 
    


    useEffect(() => {
        
      

    }, [])



    return(
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', textAlign: 'center', margin:'0px' }}>


         <section>
            <p>RAG is one of the most powerful AI applications</p>
         </section>

         <section>
            <p>Pick your architecture and connectors and deploy without coding</p>
         </section>



         
           
        </div>
    )
}

export default DocsScreen