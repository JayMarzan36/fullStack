import {
  SimulationNodeDatum,
  SimulationLinkDatum,
} from "d3-force";

import { FC, Memo } from "react"

// Following https://medium.com/@qdangdo/visualizing-connections-a-guide-to-react-d3-force-graphs-typescript-74b7af728c90 for making my graph
// TODO fix
interface CustomNode extends SimulationNodeDatum {
        id: String;
        name: String;
}

interface CustomLink extends SimulationLinkDatum { 
    strength: Number
}

export function Graph() {
    //TODO figure out how to use d3 to represent the notes data for graph
    
    


    return (
        <>
            <h1>View Graph</h1>
        </>
    )
}