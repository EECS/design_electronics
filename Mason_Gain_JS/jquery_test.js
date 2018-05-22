var startEdge;
var endEdge;
var edgeGain;
var startNode;
var endNode;

$addEdgeWindow = jQuery("#addEdgeDialog");
$changeEdgeWindow = jQuery("#changeEdgeDialog");

$addEdgeWindow.dialog({
    autoOpen: false,
    height: 350,
    width:400,
    modal:true,
    position: 'center',
    overlay: { opacity: 0.5, background: 'black'},
    buttons: { 
        Ok: function() {
            startEdge = $("#addEdgeStartEdge").val();
            endEdge = $("#addEdgeEndEdge").val();
            edgeGain = $("#addEdgeEdgeGain").val();
            addEdge(startEdge, endEdge, edgeGain)
            $(this).dialog("close");
       },
        Cancel: function () {
            $(this).dialog("close");
        }
    }
});

$changeEdgeWindow.dialog({
    autoOpen: false,
    height: 350,
    width:400,
    modal:true,
    position: 'center',
    overlay: { opacity: 0.5, background: 'black'},
    buttons: { 
        Ok: function() {
            startNode = $("#changeEdgeStartNode").val();
            endNode = $("#changeEdgeEndNode").val();
            edgeGain = $("#newEdgeGain").val();
            changeEdgeGain(startNode, endNode, edgeGain);
            $(this).dialog("close");
       },
        Cancel: function () {
            $(this).dialog("close");
        }
    }
});

var showDialog = function(dial){
    dial.dialog();
    dial.dialog("open");
};

$("#addEdge").click(function(){
    showDialog($addEdgeWindow);
});

$("#changeEdgeGain").click(function(){
    showDialog($changeEdgeWindow);
});