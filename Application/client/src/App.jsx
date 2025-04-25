import { useState, useEffect } from 'react'

import { Outlet } from 'react-router';
import { Link } from 'react-router';

import ForceGraph from 'react-force-graph-3d';

import { useFetch } from './hooks/useFetch';

function App() {
  const [count, setCount] = useState(0)

  async function logout() {
    const res = await fetch("/registration/logout/", {
      credentials: "same-origin", // TODO include cookies!
    });

    if (res.ok) {
      // TODO navigate away from the single page app!
      window.location = "/registration/sign_in/";
    } else {
      // TODO handle logout failed!
    }
  }

  const [hasError, setHasError] = useState(false);

  const [data, setData] = useState({ nodes: [], links: [] });

  const makeRequest = useFetch();

  async function getData() {


    const response = await makeRequest('/graph', "GET", '')

    if (response.ok) {
      const fetchedData = await response.json();

      setData(fetchedData.data);

    } else { 
      setHasError(true);
    }
  }

  useEffect(() => { 
      getData();
  }, []);


  const handleNodeClick = (node) => {
      console.log(node);
  };

  return (
    <>
      <nav className="Navigation">

        <div>
            <Link>New Note</Link>
        </div>
        
        <div>
          <Link>View Notes</Link>
        </div>

        
          <button onClick={logout}>Logout</button>

      </nav>


      <main>
        <Outlet>{ }</Outlet>
        <div>
                {
                    !hasError &&
                    (<ForceGraph
                        width={500}
                        height={600}
                        graphData={data}
                        nodeRelSize={6}
                        nodeAutoColorBy="id"
                        onNodeClick={handleNodeClick}
                        nodeLabel={"id"}
                    />)
                }
                {
                    hasError &&
                    <div className="error-popup">
                            An Error ocurred, please refresh
                    </div>
                }
        </div>
      </main>

    </>
  )
}

export default App;