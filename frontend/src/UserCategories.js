
import React, {useContext, useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import Context from './Context'
import {postJSON, getJSON} from './helpers'
const inline = {
  display: 'inline'
}
function UserCategories({users, categories}){
    const dispatch = useContext(Context)
    const [user, setUser] = useState('');
    const [category, setCategory] = useState('');
    const [userCategories, setUserCategories] = useState('{}')
    const [loading, setLoading] = useState(false);
    async function getUserCategories(user){
      const categories = await getJSON(`/api/${user}/categories`);
    }
    async function addUser(user){
      setLoading(true)
      const data = await postJSON('/api/users', {username: user});
      console.log(data)
      if(data.error){
        console.log(data)
      }else{
        const users = data.map(user=> ({...user, loading:false}))
        dispatch({type: 'setUsers', payload: users});
      }
      setLoading(false)
    }
    async function addCategory(category){
      const data = await postJSON('/api/categories', category)
      dispatch({type: 'setCategories', payload: data})
    }
    
    useEffect(()=>{
      console.log(user)
      getUserCategories(user)
      
    }, [user])
      return(
      <div className='twitter-users'>        
        <h3>Categories</h3>
        <select name='categories' value={category} onChange={(e)=>setCategory(e.target.value)}>
                <option >----</option>
                {categories.map((cat)=>(
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
        </select>
        <CategoryUsers category={category} users={users}/>
        <p><stong>New Category</stong> <input type='text' value={category} onChange={(e)=>setCategory(e.target.value)}/></p>
        <button disabled={loading} onClick={()=>addCategory(category)} >{loading ? 'Loading...': 'Add Category'}</button>
      </div>
      
    )
}



function CategoryUsers({category, users}){
  const dispatch = useContext(Context)
  const [user, setUser] = useState('')
  const [categoryUsers, setUsers] = useState([])
  const [loading, setLoading] = useState(false);
  async function addToCategory(category, user){
    const users = await postJSON(`/api/category/${category}/users`,user)
    setUsers(users)
  }
  async function addNewUserToCat(user, cat_id){
    setLoading(true)
    const data = await postJSON('/api/users', {username: user, cat_id});
    setLoading(false)
    if(data.error){
      console.log(data)
    }else{
      const users = data.map(user=> ({...user, loading:false}))
      dispatch({type: 'setUsers', payload: users});
    }
    
    fetchCatUsers()
  }
  async function fetchCatUsers(){
    const users = await getJSON(`/api/category/${category}/users`)
    setUsers(users)
  }
  useEffect(()=>{
    fetchCatUsers();
  },[category]);
  
  return(
    <div>
    <ul>
      {categoryUsers.map((user)=>(
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
    <h4>Add user to category</h4>
        <p><select style={inline} value={user} name='user' onChange={(e)=>setUser(e.target.value)}>
                <option value=''>----</option>
                {users.map((user)=>(
                    <option key={user.id} value={user.username}>{user.username}</option>
                ))}
        </select>
        <button disabled={!(category && user) } style={inline} onClick={()=>addToCategory(category, user)}>Add</button></p>

        <input type='text' value={user} onChange={(e)=>setUser(e.target.value)}/>
        <button disabled={loading} onClick={()=>addNewUserToCat(user, category)}>{loading ? 'Loading...': 'Add User'}</button>
    </div>
    
  )
}



export default UserCategories