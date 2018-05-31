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

$("#addEdge").click(function(){
    $addEdgeWindow.dialog();
    $addEdgeWindow.dialog("open");
});

$("#changeEdgeGain").click(function(){
    $changeEdgeWindow.dialog("open");
});