import { useEffect, useState } from 'react'

import ForceGraph from 'react-force-graph-3d';

import { updateGraph } from '../hooks/updateGraph';

export function Graph() {

    const [data, hasError] = updateGraph();

    const handleNodeClick = (node) => {
      console.log(node);
    };

    return (
        <>
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
        </>
    )
}