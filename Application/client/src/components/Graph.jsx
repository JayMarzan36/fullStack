import { useEffect, useState } from 'react'

import ForceGraph from 'react-force-graph-3d';

import { updateGraph } from '../hooks/updateGraph';
import { useNavigate } from 'react-router';
import { useFetch } from '../hooks/useFetch';

export function Graph() {

    const [data, hasError] = updateGraph();

    const [titleData, setTitleData] = useState([])
    const navigate = useNavigate();

    async function getNotes() { 
        const makeRequest = useFetch();

        const response = await makeRequest("/getnotes/", "GET", '');

        if (response.ok) {
            const fetchedData = await response.json();
            setTitleData(oldData => [...oldData, fetchedData]);
        } else { 
            setHasError(true);
        }
    }

    useEffect(() => { 
        getNotes();
    }, []);

    const handleNodeClick = (node) => {
        let dataPoint;

        for (let i = 0; i < titleData[0].userNotes.length; i++) { ;
            const note = titleData[0].userNotes[i];
            if (note["note name"] === node.id) { 
                dataPoint = note;
                break;
            }
        }

        if (dataPoint) { 
            navigate("/newnote", { state: { data : dataPoint } });
        }

    };

    return (
        <>
            <div className="graph">
                {
                    !hasError &&
                    (<ForceGraph
                        width={1700}
                        height={900}
                        graphData={data}
                        nodeRelSize={6}
                        nodeAutoColorBy="id"
                        onNodeClick={handleNodeClick}
                        nodeLabel={"id"}
                        backgroundColor='#1c448e'
                    />)
                }
                {
                    hasError &&
                    <div className="error-popup">
                            An Error ocurred, please refresh
                    </div>
                }
        </div>
        </>
    )
}