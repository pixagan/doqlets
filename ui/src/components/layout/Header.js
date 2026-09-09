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

import React, { useEffect } from 'react' 
import {  useNavigate} from 'react-router-dom'
import {Navbar, Nav, Button} from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { Image } from 'react-bootstrap'

const Header = () => {

   
    const navigate = useNavigate();


    useEffect(() => {


    }, [])

    


    return (
        <header className="header" style={{border:'None', marginBottom:'0px', paddingBottom:'1px',borderLeft:'None', borderRight:'None', borderBottom:'1px solid #b861fb'}}>

            <Navbar expand="lg" collapseOnSelect style={{padding:'0px', borderColor:'#b861fb', marginTop:'0px', marginBottom:'0px', marginLeft:'10px'}}>
                
                <Navbar.Brand href="/">
                <Image src="/doqlets.png" alt="Doqlets" style={{width:'30px', height:'30px'}} /> Doqlets</Navbar.Brand>

                

                 


        </Navbar>

        </header>
    )
}

export default Header