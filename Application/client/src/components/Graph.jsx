import { GraphCanvas } from 'reagraph';

export function Graph() {
    //For graph https://github.com/reaviz/reagraph

    //TODO request server to get graph relations and put into the graph element

    return (
        <>
            <GraphCanvas
                nodes={[
                    {
                        id: 'n',
                        label: '1'
                    },
                    {
                        id: 'n2',
                        label: '2'
                    }
                ]}
                edges={[
                    {
                        id: '1->2',
                        source: 'n',
                        target: 'n2',
                        label: 'Edge'
                    }
                ]}
            />
        </>
    )
}