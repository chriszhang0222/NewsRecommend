import React, { Component } from 'react';
import logo from '../logo.png';
import './App.css';
import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';

class App extends Component {
  render() {
    return (
      <div>
          <img className='logo' src={logo} alt='logo'/>
          <div className='container'>

          </div>
      </div>
    );
  }
}

export default App;
