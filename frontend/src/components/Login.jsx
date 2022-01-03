import React, {useState, useContext} from "react";

import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";

export const Login = () =>  {

    const [email, setEmail]=useState("");
    const [password, setPassword] = useState("");  
    const [errorMsg, setErrorMsg] = useState("");
    const [,setToken] = useContext(UserContext);


    const submitLogin = async () => {
        const requestOptions ={
            method: "POST",
            headers: {"Content-Type":"application/x-www-form-urlencoded"},
            body: JSON.stringify(`'grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret='`)
        }
        const response = await fetch("/api/token", requestOptions)
        const data = await response.json();

        if (!response.ok) {
            setErrorMsg(data.detail)
        } else {
            setToken(data.access_token)
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    }
    return (
        <>
               <div className="column">
            <form action="" className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centered">Login</h1>
                <div className="field">
                    <label className="label">Emaill Address</label>
                    <div className="control">
                        <input type="email" 
                            placeholder="Enter email" 
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            id="form-email" 
                            className="input"
                            required
                        />
                    </div>
                </div>    
                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input type="password" 
                            placeholder="Enter Password" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            id="form-pwd" 
                            className="input"
                            required
                        />
                    </div>
                </div>    
                <ErrorMessage message={errorMsg}/>
                <br />
                <button className="button is-primary" type="submit">Login</button>
            </form>
        </div>
        </>
    )
}