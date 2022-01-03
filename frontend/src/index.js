import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import "bulma/css/bulma.min.css";

import { UserProvider } from "./context/UserContext"

ReactDOM.render(
  <UserProvider>
    <App />
  </UserProvider>,
  document.getElementById('root')
);
