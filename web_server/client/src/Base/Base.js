import React, {PropTypes} from 'react';
import { Link } from 'react-router';
import Auth from '../Auth/Auth';
import './Base.css';

const Base = ({children}) => (
    <div>
        <nav className="nav">
            <div className="nav-wrapper">
                <a href="/" className="brand-logo">&nbsp;&nbsp;News Recommend</a>
                <ul id="nav-mobile" className="right">
                    {Auth.isUserAuthenticated() ?
                            (<div>
                                <li><Link to='/search'><i className="fa fa-search"></i> Search News</Link></li>
                                <li>{Auth.getEmail()}</li>
                                <li><a href="/logout">Log out</a></li>
                            </div>)
                            :
                            (
                                <div>
                                    <li><a href="/login">Login</a></li>
                                    <li><a href="/signup">Sign up</a></li>
                                </div>
                            )
                    }
                </ul>
            </div>
        </nav>
        <br/>
        {children}
    </div>
);

// Base.propTypes = {
//     children: PropTypes.object.isRequired
// };

export default Base;