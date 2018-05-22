var cy = cytoscape({

    container: document.getElementById('cy'), // container to render in
    
    elements: [ // list of graph elements to start with
    ],
    
    style: [ // the stylesheet for the graph
        {
        selector: 'node',
        style: {
            'background-color': '#666',
            'content': "data(id)"
        }
        },
    
        {
        selector: 'edge',
        style: {
            'width': 3,
            'label': 'data(gain)',
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier'
        }
        }
    ],
    
    layout: {
        name: 'grid',
        rows: 1
    },

});