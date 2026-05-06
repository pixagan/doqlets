import { combineReducers, applyMiddleware } from 'redux'

import { configureStore } from '@reduxjs/toolkit';




const reducer = combineReducers({


})



const initialState = {

   
} 

const store = configureStore({reducer:reducer, initialState}); 


export default store