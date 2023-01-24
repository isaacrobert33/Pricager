import './App.css';
import React from "react";
import { ChakraProvider } from '@chakra-ui/react';


function App() {
  return (
    <ChakraProvider resetCSS={false}>
      <div className='App'>
        <h2>Price manager</h2>
      </div>
    </ChakraProvider>
    
  );
}

export default App;
