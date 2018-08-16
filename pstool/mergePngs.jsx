#target photoshop
$.evalFile ( "C:/jslib/json2.js" ); 

var canvasWidth = 2742;
var canvasHeight = 3514;

if (app.documents.length > 0) 
{
    var myDocument = app.activeDocument;
    var thePath = myDocument.path;
	var docName = decodeURI(app.activeDocument.name);
	docName = docName.substring(0, docName.indexOf("."));

    // modify doc size
    myDocument.resizeCanvas (canvasWidth, canvasHeight, AnchorPosition.TOPLEFT);
        
    var jsonInfo = getJsonData(thePath + "/" + docName + ".json");
    
    function fixImages()
    {
        var layerLen = myDocument.artLayers.length;
         // work through the array;
         for (var m = 0; m < layerLen; m++) 
         {
            // open smart object; in active document
            var getLayerToChange = app.activeDocument.artLayers[m];
            app.activeDocument.activeLayer = getLayerToChange;
   
            var tmpName = getLayerToChange.name;
            tmpName = tmpName.substring(0, tmpName.indexOf("."));
            var slotInfo = jsonInfo.skins["default"][tmpName][tmpName];
            
            var fixx = slotInfo.x - Math.round(slotInfo.width)/2;
            var fixy = canvasHeight - (slotInfo.y + Math.round(slotInfo.height)/2);
            getLayerToChange.translate (fixx, fixy);
         };  
    };

    function fixDrawOrder()
    {
        var layerLen = myDocument.artLayers.length;

        var allLayers = {};
        
         // work through the array;
         for (var m = 0; m < layerLen; m++) 
         {
            // open smart object; in active document
            var getLayerToChange = app.activeDocument.artLayers[m];
   
            var tmpName = getLayerToChange.name;
            tmpName = tmpName.substring(0, tmpName.indexOf("."));
            allLayers[tmpName] = getLayerToChange;
         }; 

        var preLayer = null;
         for (var m in allLayers) 
         {
             var layer = allLayers[m];
             if (preLayer != null){
                 layer.move (preLayer, ElementPlacement.PLACEBEFORE);
             }
             preLayer = layer;
         }
    };
};

function getJsonData(filePath){
    var file = new File(filePath);  
    file.open("r", "TEXT"); 
    
    var fileString = "";  
    while (!file.eof){  
        var line = file.readln();  
        if (fileString.indexOf(line) == -1){  
            fileString += line;  
        }  
    }  
    
    var obj;
    try{  
        obj = JSON.parse(fileString); // Exception:SyntaxError: Unexpected token '  
    } catch(e) {  
        alert("Exception:" + e + "\nCould not run JSON.parse()");  
    }  

    return obj; 
}

fixImages();
fixDrawOrder();