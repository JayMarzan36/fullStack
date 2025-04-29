import { useState, useEffect } from 'react'

import { Outlet } from 'react-router';
import { Link } from 'react-router';
import { Graph } from './components/Graph';



function App() {

  async function logout() {
    const res = await fetch("/registration/logout/", {
      credentials: "same-origin",
    });

    if (res.ok) {
      window.location = "/registration/sign_in/";
    }
  }


  

  return (
    <>
      <title>Link Notes</title>
      <nav className="Navigation">

        <div>
              <Link to={"/"}>View Graph</Link>
          </div>

        <div>
            <Link to={"/newnote"}>New Note</Link>
        </div>
        
        <div>
          <Link to={"/viewnote"}>View Notes</Link>
        </div>

          <button onClick={logout}>Logout</button>

      </nav>


      <main>

        <Outlet>{ }</Outlet>

      </main>

    </>
  )
}

export default App;