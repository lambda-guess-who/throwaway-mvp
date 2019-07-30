import React, {useEffect} from 'react';
import {getJSON} from './helpers'
import Login from './Login'

function Profile({user}){
    return(
        <div>
    {user.user_name && (
    <h2>Hi! {user.user_name},</h2>
    )}
    {!user.user_name&&(
        <Login/>
    )}
        </div>
    )
    
}
export default Profile;