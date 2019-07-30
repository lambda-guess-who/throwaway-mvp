import React, {useEffect, useContext} from 'react';
import {postJSON, getJSON} from './helpers'
import queryString from 'query-string'
import Context from './Context'

function LoginRedirect({location, history}){
    const dispatch = useContext(Context)
    async function verfyLogin(nonce, verifier){
        const data = await postJSON('/api/auth/verify_login', {nonce, verifier})
        localStorage.removeItem('loginNonce');
        localStorage.setItem('jwt', data['jwt'])
        const user = await getJSON('/api/user_profile')
        console.log(user.user_name)
        dispatch({type: 'setUser', payload: user})
        history.push('/')

    }
    useEffect(()=>{
        const qs = queryString.parse(location.search)
        const verifier = qs.oauth_verifier
        const nonce = localStorage.getItem('loginNonce')
        verfyLogin(nonce, verifier)
    }, [])
    return(
        <div>
            <h1>Loading ... </h1>
        </div>
    )
}
export default LoginRedirect;