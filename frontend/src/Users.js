import React from 'react'
import {Link} from 'react-router-dom'

export default function Users({users}){
    return (
        <div>
            <h3>Tweeter Users</h3>
            <div>
            {users.map((user)=>(
                <Link  key={user.id} to={`/user/${user.id}`}>
                    <li>{user.username}</li>
                </Link>
            ))}
            </div>
        </div>)
}