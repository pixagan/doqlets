import React , {useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, Container, Card, Form, Button, ListGroup, OverlayTrigger, Popover, Tooltip, Carousel, InputGroup, FormControl, Table, Badge } from 'react-bootstrap'
import Meta from '../components/Meta'
import axios from 'axios'
import { DocConfig } from '../components/docchat/DocConfig'

import { useNavigate } from 'react-router-dom';

  
export const LandingScreen = ({match, history}) => {

   
    const dispatch = useDispatch()

    const navigate = useNavigate();

    const [viewMode, setViewMode] = useState("chat")  //chat, config

    const [sectionType, setSectionType] = useState("all") 
    const [documents, setDocuments] = useState([])
    const [query, setQuery] = useState('')
    const [chatHistory, setChatHistory] = useState([])
    const [docPages, setDocPages] = useState([])


    const [selectedFile, setSelectedFile] = useState(null)
    const [fileName, setFileName] = useState('')

    const handleFileChange = (e) => {
        const file = e.target.files?.[0]
        if (file) {
          setSelectedFile(file)
          setFileName(file.name)
        }
      }

    const uploadDocument = async () => {
        if (!selectedFile) return
        const formData = new FormData()
        formData.append('file', selectedFile)   // must be 'file' to match backend

        const response = await axios.post('/api/store', formData)

        if(response.status === 200){
            const responseD = await axios.get('/api/document')
            console.log("doc_pages ", responseD.data.doc_pages)
            setDocPages(responseD.data.doc_pages)
        }
        
    }

    const chatRequest = async () => {

        var config={
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const response = await axios.post('/api/chat', { query }, config)
        const answer = response.data.chat_response

        console.log("query ", query)
        console.log("answer ", answer)

        setChatHistory([{ query: query, response: answer }, ...chatHistory])
    }

    const loadHistory = async () => {
        const response = await axios.get('/api/history')
        const history = response.data.chats
        console.log("history ", history)
        setChatHistory(history)
    }

    


    useEffect(() => {
        


    }, [])



    return(
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', textAlign: 'center', margin:'5px', padding:'5px' }}>

         <Meta title={'Doqlets'} description={'Doqlets'}/>

         <ListGroup horizontal>
            <ListGroup.Item action onClick={()=>setViewMode("chat")}>Chat</ListGroup.Item>  
            <ListGroup.Item action onClick={()=>setViewMode("config")}>Config</ListGroup.Item>  
         </ListGroup>


         {viewMode === "chat" && (
            <>
            
            <Row>
                    <Col>
                    <p className='h4'>Document</p>
                    <div className="mt-3">
                    <Form.Group controlId="formFile">
                        <InputGroup>
                        
                        <Form.Control
                            type="file"
                            accept=".pdf,.doc,.docx,.txt"
                            onChange={handleFileChange}
                            className="mb-2"
                        />
                        <Button variant="primary" onClick={uploadDocument}>Upload</Button>
                        
                        </InputGroup>
                    
                        {fileName && (
                            <small className="text-muted d-block">
                            Selected: {fileName}
                            </small>
                        )}
                    
                        </Form.Group>
                    </div>

                    <hr />


                    <div style={{maxHeight: '95vh', overflow: 'scroll'}}>
                        <p className='h4'>Document Title</p>

                        {docPages.map((page, index)=>(
                            <div key={index}>
                                <p className='text-left'>{page.content}</p>
                            </div>
                        ))}

                    </div>
                    
                    </Col>
                    <Col style={{ maxHeight: '95vh', overflow: 'scroll' }}>
                    <p className='h4'>
                        <span style={{marginRight:'10px'}}>Chat</span>
                        <Badge bg='light' style={{paddingTop:'5px', paddingBottom:'5px'}} onClick={()=>loadHistory()}>Load History</Badge>
                    </p>
                    

                
                    <hr />

                    <InputGroup>
                        <Form.Control as="textarea" rows={5} placeholder="Enter your query" value={query} onChange={(e)=>setQuery(e.target.value)} className="mb-2"/>
                        <Button variant="primary" onClick={()=>chatRequest()}>Chat</Button>
                    </InputGroup>

                    

                    
                        
                    {chatHistory.map((item, index)=>(
                        <Card key={index}>
                            <Card.Header>
                            <p className='text-left h5'>{item.query && item.query.toString()}</p>
                            </Card.Header>
                        
                        <Card.Body>
                            {item.response && (
                                Object.values(item.response).map((value, index)=>(
                                    <p key={index} className='text-left'>{value}</p>
                                ))
                            )}
                        
                        </Card.Body>
                            
                        </Card>
                    ))}
                        
                    
                    
                    </Col>
                </Row>

            
            </>


            )}

            {viewMode === "config" && (
                <DocConfig />
            )}

      

           
        </div>
    )
}

export default LandingScreen