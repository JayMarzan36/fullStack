import { useState } from "react"
import { useFetch } from "../hooks/useFetch";
import { useNavigate } from "react-router";
import { updateGraph } from "../hooks/updateGraph";

export function NewNote() { 


    const [title, setTitle] = useState('');
    
    const [content, setContent] = useState('');

    const navigate = useNavigate();

    async function handleSubmit(e) { 
        e.preventDefault();

        const makeRequest = useFetch();

        const response = await makeRequest("/notes/", "POST", {
            title,
            content
        });

        if (response.ok) {
            navigate("/");
        }
    }

    return (
        <>
            <h1>New Note</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Note Title
                    <input type="text" name="title" value={title} onChange={e => setTitle(e.target.value)}/>
                </label>
                <br />
                <button type="submit">Save</button>
                <br />
                <label>
                    <textarea rows="100" cols="80" name="content" onChange={e => setContent(e.target.value)} value={content} />
                </label>
                
            </form>
        </>
    )
}