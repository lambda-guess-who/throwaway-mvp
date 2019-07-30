import React, {useState} from 'react'
import {Link} from 'react-router-dom'

export default function GameMenu({categories, history}){
    const [category, setCategory] = useState(1)
    const [count, setCount] = useState(5)
    return (
        <div>
            <h2>Guess Who?</h2>
            <h3>Play a quick game: </h3>
            <div>
            <p>Select a category: </p>
            <select value={category} onChange={(e)=>setCategory(e.target.value)}>
                {categories.map((category, idx)=>(
                    <option key={idx} value={category.id}>{category.name}</option>
                ))}
            </select>
            <p>Select number of tweets to guess: </p>
            <select value={count} onChange={(e)=>setCount(e.target.value)}>
                <option value='5'>5</option>
                <option value='10'>10</option>
                <option value='15'>15</option>
                <option value='20'>20</option>
            </select>
            </div>
            <button onClick={()=>history.push(`/quickgame/${category}/${count}`)}>Start Guessing!</button>
        </div>)
}