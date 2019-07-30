
 export function postJSON(url, data){
    const token = localStorage.getItem('jwt')
    const bearer = token ? `Bearer ${token}` : '' 
    return fetch(url,{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': bearer
      },
      body: JSON.stringify(data)
    }).then(response => {
      if (response.status === 401){
        console.log(response)
        alert('Login Required!')
      }
      return response.json()
    })
  
  }

  export function getJSON(url){
    const token = localStorage.getItem('jwt')
    const bearer = token ? `Bearer ${token}` : '' 
    return fetch(url,{
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': bearer
      }
    }).then(response => {
      if (response.status === 401){
        console.log(response)
        
        //alert('Login Required!')
      }
      return response.json()
    }
      
    
    )
  
  }


export function devProdStr(dev,prod){
  if (process.env.NODE_ENV !== 'production') {
    return dev
  }
  return prod
}

export function appReducer (state, action){
  switch(action.type){
    case 'setUsers': return {
      ...state,
      users: action.payload
    }
    case 'setCategories': return {
      ...state,
      categories: action.payload
    }
    case 'setUser': return {
      ...state,
      user: action.payload
    }
    default:
      return state;
  }
}

