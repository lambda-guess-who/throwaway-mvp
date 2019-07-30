import React, {useReducer, useState, useEffect} from 'react';
import {} from './helpers'
function UserTweets({match}){
    const [user, setUser] = useState({});
    const [tweets, setTweets] = useState([]);
    async function fetchUser(user_id){
        console.log(match.params.id)
        const r = await fetch(`/api/user/${user_id}`);
        const data = await r.json();
        setUser(data);
        setTweets(data.tweets)
      }
    useEffect(()=>{
        fetchUser(match.params.id)
      }, [match.params.id])
    return(
        <div>
            <h1>{user.username}</h1>
            {tweets.map((tweet, idx)=>(
                <div key={idx} className='tweet'>
                    <p>{tweet}</p>
                </div>
                
            ))}
        </div>
    );
}
export default UserTweets