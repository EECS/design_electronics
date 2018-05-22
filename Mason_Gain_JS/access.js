document.getElementById('addNode').onclick = addNode;
//document.getElementById('addEdge').onclick = addEdge;
document.getElementById('removeNode').onclick = removeNode;
document.getElementById('centerGraph').onclick = centerGraph;
document.getElementById('calculateAdjNodes').onclick = calculateAdjNodes;
document.getElementById('getNodeNumber').onclick = getNodeNumber;
document.getElementById('exportJson').onclick = exportJson;

var totalNodes = 0;

function addNode(){
    var nodeId = prompt("Please enter name for the node to be added.");

    if(nodeId != null && cy.$("#"+nodeId).length == 0){
        cy.add({
            group:"nodes", 
            data: {id: nodeId, nodeNumber: totalNodes},
            position : {x : (cy.width()/2), y: (cy.height()/2)}
        });
        totalNodes += 1;
    }else{
        console.log("Node already in graph or invalid input.");
    }
    
};

function removeNode(){
    var nodeId = prompt("Please enter name for the node to be removed.");
    nodeId = protectInput(nodeId);
    
    if(nodeId != null && cy.$("#"+nodeId).length > 0){
        var removedNodeNumber = cy.$("#"+nodeId).data("nodeNumber");
        cy.$("#"+nodeId).remove();
        
        cy.nodes().map(function(ele, i){
            //Decrease all nodes with a node number greater than the removed node
            //number by one as the total number of nodes in the graph has decreased by one.
            if(ele.data("nodeNumber")>removedNodeNumber){
                ele.data("nodeNumber", ele.data("nodeNumber")-1);
            }
        });
        
        totalNodes -= 1;
    }else{
        console.log("Node not in graph.");
    }
    
};

function addEdge(startEdge, endEdge, edgeGain){
    if(cy.$("#"+startEdge+endEdge).length == 0){
        cy.add({
            group:"edges", 
            data: {id: startEdge+endEdge, source: startEdge, target: endEdge, gain: edgeGain}
        });
    }
};

function changeEdgeGain(startNode, endNode, edgeGain){
    startNode = protectInput(startNode);
    endNode = protectInput(endNode);
    edgeGain = protectInput(edgeGain);
    if(startNode != null && endNode != null && edgeGain != null){
        var edge = cy.$("#"+startNode+endNode);
        if(edge.length != 0){
            edge.data("gain", edgeGain);
        }else{
            console.log("Edge not in graph.");
        }
    }else{
        console.log("Invalid input.");
    }
    
};

function removeEdge(startEdge, endEdge){
    startEdge = protectInput(startEdge);
    endEdge = protectInput(endEdge);
    
    if(startEdge != null && endEdge != null && cy.$("#"+startEdge+endEdge).length > 0){
        cy.$("#"+startEdge+endEdge).remove();
    }else{
        console.log("One or both edges not in graph.");
    }

};

function centerGraph(){
    cy.fit();
};

function calculateAdjNodes(){
    //Sort all nodes in increasing nodeNumber order.
    var sortedNodes = cy.nodes().sort(function(a, b){
        return a.data("nodeNumber")-b.data("nodeNumber");
    });
    
    var adjNodes = [];
    var adjGains = [];
    
    //Creates 2D array of out going nodes from nodes in graph.
    for(var i = 0; i < sortedNodes.length; i++){
        //Get outgoing elements from current node. 
        var outgoingEles = sortedNodes[i].outgoers();
        
        currentAdjNodes = [];
        currentNodeGains = []
        
        //Loop through outgoing nodes list, creating a python list with
        //all nodeIds of next nodes from current nodes in the list.
        for(var j = 0; j < outgoingEles.length; j++){
            var currentEle = outgoingEles[j];
            if(currentEle.isNode()){
                //Add node number to current adjacent node list.
                currentAdjNodes.push(currentEle.data("nodeNumber"));
            }else{
                currentNodeGains.push("'("+currentEle.data("gain")+")'");
            }
        }
        
        adjNodes.push("["+currentAdjNodes+"]");
        adjGains.push("["+currentNodeGains+"]");
        //adjNodes.push(currentAdjNode.toString());
    }

    console.log("Adjacent nodes are: \n");
    console.log("["+adjNodes+"]");
    console.log("Adjacent gains are: \n");
    console.log("["+adjGains+"]");
   
};

function getNodeNumber(){
    var nodeId = prompt("Please enter name for the node for which the number is wanted.");
    nodeId = protectInput(nodeId);
    
    if(nodeId != null){
        var node = cy.$("#"+nodeId);
        if(node.length != 0){
            console.log(node.data("nodeNumber"));
        }else{
            console.log("Node not in graph.");
        }
    }else{
        console.log("Node not in graph.");
    }
};

function exportJson(){
    console.log(cy.json());
};

function protectInput(input){
    if(input != null){
        return input.trim();
    }else{
        return null;
    }
};

