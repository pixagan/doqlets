import './App.css';

import React from 'react'

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


import LandingScreen from './screens/LandingScreen'

import Header from './components/layout/Header'
import Footer from './components/layout/Footer'



const App = () => {

  return (

    <Router>

      <Header />
    

      <main style={{margin:'0px', padding:'0px'}}>

        <Routes>

          <Route path='/' element={<LandingScreen />} exact />

        </Routes>

      </main>

      <Footer />

    </Router>

  );
}

export default App;



