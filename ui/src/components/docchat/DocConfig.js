import axios from 'axios'
import React , { useState, useEffect,} from 'react'
import { Card, Badge, InputGroup, Button, Table, Form, Row, Col, ListGroup } from 'react-bootstrap'
import { ArrowBigDown } from 'lucide-react'

import { useDispatch, useSelector } from 'react-redux'

import { useRef } from 'react'


export const DocConfig = ({selectedEdge}) => {


    const dispatch = useDispatch()

    const textareaRef = useRef(null)

    const [source, setSource] = useState('')
   

    useEffect(() => {

        
    }, [])
   
 

    return (

        <div style={{padding:'10px', backgroundColor:'white', borderRadius:'10px'}}>


            <p>LLM</p>

            <p>Data Reader</p>

            <p>Data Processor</p>

            <p>Vector Store</p>

            
           
        
        </div>

    )
}


export default DocConfig
