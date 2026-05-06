import React from 'react'
import {  Row, Col } from 'react-bootstrap'
import {Nav  } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { Container} from 'react-bootstrap'


const Footer = () => {
    return (

        <>
        
        <footer className="footer">
        

        <Container>

        <hr/>

      
        <hr/>

        <Row>
          <Col className='text-center py-3 mt-0'>
          <span> &copy; 2025-, Pixagan Technologies Pvt Limited. All rights reserved. | </span>
          </Col>
        </Row>

        <hr />

        </Container>





        </footer>
        
        </>


        )
    }
    
    export default Footer