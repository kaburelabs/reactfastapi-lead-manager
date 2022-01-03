import React, {useState, useContext} from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
    const [email, setEmail]=useState("");
    const [password, setPassword] = useState("");   
    // const [confirmationPwd, setConfirmationPwd] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
    const [tok, setToken] = useContext(UserContext);

    const submitRegistration = async () => {
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body:JSON.stringify({email:email, hashed_password:password})
        }
        const response = await fetch("/api/users", requestOptions)
        const data = await response.json()

        if (!response.ok) {
            setErrorMsg(data.detail); 
        } else {
            setToken(data.access_token)
        }
    }
    
    const handleSubmit = (e) => {
        e.preventDefault();
        if (password.length > 2) {
            submitRegistration();
        } else {
            setErrorMsg("Ensure that hte password match and are greater than 5 characters.")
        }
    }

    return (
        <div className="column">
            <form action="" className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centered">Register</h1>
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
                <button className="button is-primary" type="submit">Register</button>
            </form>
        </div>
    )
}

export default Register