import './App.css';
import React, { useEffect } from "react";
import { ChakraProvider } from '@chakra-ui/react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import favicon from "./favicon.ico"
import Search from './Search';
import DynamicProducts from './DynamicProducts';

function App() {
  
  return (
    <Router>
        <ChakraProvider resetCSS={false}>
        <div className='App'>
          <div className='header'>
            <img width={"42px"} height={"42px"} src={favicon} alt={"logo"}></img>
            <h2>Price manager</h2>
            <div className='tabs'>
              <Link id='search-tab' to={"/search"} >Search</Link>
              <Link id='products-tab' to={"/products"} >Dynamic Products & Price variants</Link>
            </div>
          </div>
          <Routes>
            <Route exact path='/search' element={<Search />}></Route>
            <Route exact path='/products' element={<DynamicProducts />}></Route>
          </Routes>
        </div>
      </ChakraProvider>
    </Router>
    
    
  );
}

export default App;
