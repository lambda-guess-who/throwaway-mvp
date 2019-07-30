import React, {useEffect, useState} from 'react';
import {getJSON} from './helpers'
import Login from './Login'
import {noDisplay} from './styles'
function QuickGame({match, history}){
    const cat_id = match.params.cat_id
    const count = match.params.count
    const [tweets, setTweets] = useState([])
    const [page, setPage] = useState(0)
    const [score, setScore] = useState(0)
    async function getGame(){
        const tweets = await getJSON(`/api/quickgame/${cat_id}/${count}`)
        setTweets(tweets)
        setPage(0)
        setScore(0)
    }
    useEffect(()=>{
        getGame()
    },[count, cat_id])
    function checkAnswer(user){
        if (user.real){
            setScore(score+1)
        }
        if (page+1<count){
            setPage(page+1);
        }
        else{
            
            setPage(page+1);
        }
        
    }
    return(
        <div>
        {tweets.map((tweet, idx)=>(
        <div>
            
            <div key={idx} style={idx==page ? {} : noDisplay } skey={idx}>
                <h2>Guess Who?</h2>
                <h3>Your Score: {score}/{page}</h3>
                <div className='tweet'>{tweet.tweet}</div>
                <div className='options'>
                {tweet.options.map((user, idx2)=>(
                    <div key={idx2} className='profile-container' onClick={()=>{checkAnswer(user)}}>
                        <img src={user.photo}></img>
                    <div>@{user.handle}</div>
                    </div>
                ))}
                </div>
                
            </div>
            
        </div>
        
        ))}
        <div style={page==count ? {} : noDisplay }>
                <h2>Final Score: {score}/{page}</h2>
                <button onClick={()=>getGame()}>Try Again</button>
            </div>
        </div>
    )
    
}
export default QuickGame;