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

import './App.css';

import React from 'react'

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


import WikiScreen from './screens/WikiScreen'
import ProjectsScreen from './screens/ProjectsScreen'



import Header from './components/layout/Header'
import Footer from './components/layout/Footer'



const App = () => {

  return (

    <Router>

      <Header />
    

      <main style={{margin:'0px', padding:'0px'}}>

        <Routes>

          <Route path='/' element={<WikiScreen />} exact />
          <Route path='/projects' element={<ProjectsScreen />} exact />
          <Route path='/doqlets/:project_id' element={<WikiScreen />} exact />
      
         
        </Routes>

      </main>

      <Footer />

    </Router>

  );
}

export default App;



