import React, {useEffect, useReducer, useState, createContext, useContext} from 'react';
import {postJSON, getJSON, appReducer} from './helpers'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import UserCategories from './UserCategories'
import Context from './Context'
import UserTweets from './UserTweets'
import Nav from './Nav'
import Users from './Users'
import LoginRedirect from './LoginRedirect'
import Profile from './Profile'
import QuickGame from './QuickGame'
import GameMenu from './GameMenu'
import './App.css';

function App() {
  const [state, dispatch] = useReducer(appReducer, {users: [], user: {}, categories: []})
  const fetchTweeterUsers = async()=>{
    const response = await fetch('/api/users');
    const data = await response.json();
    const users = data.map(user=> ({...user, loading:false}))
    dispatch({type: 'setUsers', payload: users});
  }
  async function fetchUser(){
    const payload = await getJSON('/api/user_profile')
    dispatch({type: 'setUser', payload})
  }
  async function fetchCategories(){
    const payload = await getJSON('/api/categories')
    dispatch({type: 'setCategories', payload})
  }
  
  useEffect(()=>{
    fetchTweeterUsers();
    fetchUser();
    fetchCategories();
  },[])
  return (
    <Router>
      <Context.Provider value={dispatch}>
        <Nav/>
        <Profile user={state.user}/>
        <Route  path="/categories" exact render={
          (props)=> (
          <div className="home-content">
            <UserCategories {...props} users={state.users} categories={state.categories}/>
          </div>
          )
        }/>
        <Route  path="/users" exact render={
          (props)=> (
            <Users{...props} users={state.users}/>
          )
        }/>
        <Route  path="/" exact render={
          (props)=> (
            <GameMenu {...props} categories={state.categories}/>
          )
        }/>
        <Route path="/user/:id" component={UserTweets}/>
        <Route path="/quickgame/:cat_id/:count" component={QuickGame}/>
        <Route path="/logged_in/" component={LoginRedirect}/>
      </Context.Provider>
    </Router>
    
  );
}


export default App;
