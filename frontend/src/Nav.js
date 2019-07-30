import React from 'react';
import {Link} from 'react-router-dom'
import {inlineBlock} from './styles'
function Nav(){
    return(
        <nav className='main-nav'>
            <p style={inlineBlock}> <Link to='/'>Home </Link></p>
            <p style={inlineBlock}> <Link to='/categories'>Categories </Link></p>
            <p style={inlineBlock}> <Link to='/users'>Users </Link></p>
        </nav>
    )
}
export default Nav;