import { useState, useEffect } from "react";
import { useFetch } from "../hooks/useFetch"
import { redirect, useNavigate } from "react-router";

export function ViewNotes() {

    const [hasError, setHasError] = useState(false);
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

    function handleClick(dataPoint) { 
        navigate("/newnote", { state: { data : dataPoint } });
    }

    return (
        <>
            
            <div className="mainNotes">
                <h1>View Notes</h1>

                <div className="noteList">
                    {titleData.map((data) => 
                        data.userNotes.map((dataPoint, index) => (
                            <div className="noteCard" key={index}>
                                <p onClick={() => handleClick(dataPoint)}>
                                    {dataPoint["note name"]}
                                </p>
                            </div>
                        ))
                    )}
                </div>
            </div>

        </>
    )
}