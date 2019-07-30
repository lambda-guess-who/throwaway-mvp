import React from 'react';
import {postJSON, devProdStr} from './helpers'
function createNonce(){
    /**
     * Only used for matching request tokens on the server since we are 
     * doing oath stateless.
     * Not Crypto secure random but not a very important key either.
     * An attacker cannot use this nonce to hijack an account.
     * You may still want to replace this later with a more secure random later.
     * 
     */
    let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let text = ''
    for (let i = 0; i < 50; i++){
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text
}


function Login(){
    async function create_login_url(){
        const nonce = createNonce()
        localStorage.setItem('loginNonce', nonce)
        const callback_url =  window.location.protocol + '//' + window.location.host + '/logged_in'
        const link = await postJSON('/api/auth/create_login_url', {nonce, callback_url})
        window.location.href = link['redirect_url']
    }
    return(
        <div>
            <button onClick={()=>create_login_url()}>Log in with Twitter</button>
            
        </div>
    )
}
export default Login;