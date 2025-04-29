import { useEffect, useState } from "react";
import { useFetch } from "./useFetch";

export function updateGraph() {

    const [hasError, setHasError] = useState(false);
    
    const [data, setData] = useState({ nodes: [], links: [] });

    const makeRequest = useFetch();

    async function getData() {
        const response = await makeRequest('/graph', "GET", '');

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

    return [data, hasError];
}
