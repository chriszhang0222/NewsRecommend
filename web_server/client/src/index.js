import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import {browserHistory, Router} from 'react-router';
import routers from './routes';

ReactDOM.render(
    <Router history={browserHistory} routes={routers}/>,
    document.getElementById('root')
)