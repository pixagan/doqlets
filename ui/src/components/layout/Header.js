import React, { useEffect } from 'react' 
import {  useNavigate} from 'react-router-dom'
import {Navbar, Nav } from 'react-bootstrap'

const Header = () => {

   
    const navigate = useNavigate();


    useEffect(() => {


    }, [])

    


    return (
        <header className="header" style={{border:'None', marginBottom:'0px', paddingBottom:'1px',borderLeft:'None', borderRight:'None', borderBottom:'1px solid #b861fb'}}>

            <Navbar expand="lg" collapseOnSelect style={{padding:'0px', borderColor:'#b861fb', marginTop:'0px', marginBottom:'0px', marginLeft:'10px'}}>
                
                <Navbar.Brand href="/">Doqlets</Navbar.Brand>
        </Navbar>

        </header>
    )
}

export default Header