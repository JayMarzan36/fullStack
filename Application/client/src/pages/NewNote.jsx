import { useEffect, useState } from "react"
import { useFetch } from "../hooks/useFetch";
import { useLocation, useNavigate } from "react-router";

export function NewNote() { 

    const [hasError, setHasError] = useState(false);

    const [title, setTitle] = useState('');

    const [oldTitle, setOldTitle] = useState('');
    
    const [content, setContent] = useState('');

    const [updateStatus, setUpdateStatus] = useState(false);

    const navigate = useNavigate();

    const location = useLocation();

    const [data, setData] = useState([]);

    async function handleSubmit(e, action) { 
        e.preventDefault();

        const makeRequest = useFetch();

        let response;

        if (action === "submit") {
            if (updateStatus) {
                response = await makeRequest("/notes/", "PATCH", {
                    oldTitle,
                    title,
                    content
                });
            } else {

                response = await makeRequest("/notes/", "POST", {
                    title,
                    content
                });

                
            }
        } else if (action === "delete") {
            response = await makeRequest("/notes/", "DELETE", {
                title:data["note name"],
                content
            });
        }
        
        if (response.ok) {
            setHasError(false);
            navigate("/");
        } else { 
            setHasError(true);
        }
    }



    useEffect(() => {
        if (location.state && location.state.data) {
            const { data } = location.state;

            if (data) { 
                setUpdateStatus(true);

                setOldTitle(data["note name"]);
                
                setTitle(data["note name"]);
                
                setContent(data["note content"]);
            }

            setData(data);
        } else { 
            setUpdateStatus(false);

            setOldTitle('');
                
            setTitle('');
                
            setContent('');
            
        }
    }, [location]);

    return (
        <>
            <div className="mainNotes">

            {hasError && (<div className="hasError">An Error Occurred, please refresh</div>)}
            {updateStatus ? (<h1>Edit Note</h1>) : (<h1>New Note</h1>)}
            <form>
                <label>
                    <div>Title</div>
                    <input type="text" name="title" value={title} onChange={e => setTitle(e.target.value)}/>
                </label>
                <br />
                <button type="submit" onClick={(event) => handleSubmit(event, 'submit')}>Save</button>
                <button type="delete" onClick={(event) => handleSubmit(event, "delete")}>Delete</button>
                <br />
                <textarea rows="100" cols="80" name="content" onChange={e => setContent(e.target.value)} value={content} />

            </form>
            </div>
        </>
    )
}