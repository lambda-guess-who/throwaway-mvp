import React, {useState} from 'react';

function Predict({users}){
    const [user1, setUser1] = useState('')
    const [user2, setUser2] = useState('')
    const [tweet, setTweet] = useState('')
    const [prediction, setPrediction] = useState('')
    const [loading, setLoading] = useState(false);
    async function predictTweet(user1,user2,tweet){
        setLoading(true)
        const res = await fetch(`/api/predict/${user1}/${user2}?tweet=${encodeURIComponent(tweet)}`)
        const data = await res.json()
        setPrediction(data)
        setLoading(false)
    }
    return(
        <div>
            <p>User1</p>
            <select value={user1} name='user1' onChange={(e)=>setUser1(e.target.value)}>
                <option>----</option>
                {users.map((user)=>(
                    <option key={user.id} value={user.id}>{user.username}</option>
                ))}
            </select>
            <p>User2</p>
            <select value={user2} name='user2' onChange={(e)=>setUser2(e.target.value)}> 
                <option>----</option>
                {users.map((user)=>(
                    <option key={user.id} value={user.id}>{user.username}</option>
                ))}
            </select>
            <textarea value={tweet} onChange={(e)=>setTweet(e.target.value)}></textarea>
            <button disabled={loading | !(user1 & user2) } onClick={()=>predictTweet(user1,user2,tweet)}>
              {loading ? 'Loading...': 'Predict'}
            </button>
            {prediction && <p>{prediction}</p>}
        </div>
    )
    
}
export default Predict;