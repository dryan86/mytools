#target photoshop

// This script exports photoshop layers as individual images.
// It also write a JSON file that can be imported into Spine
// where the images will be displayed in the same positions.

// Settings.
var ignoreHiddenLayers = true;
var savePNGs = true;
var saveJSON = true;
var scaleFactor = 1;
showDialog();

function main () {
	// Output dir.
	var dir = app.activeDocument.path + "/images/";

	new Folder(dir).create();

	var name = decodeURI(app.activeDocument.name);
	name = name.substring(0, name.indexOf("."));

	app.activeDocument.duplicate();

	// Collect original layer visibility and hide all layers.
	var layers = [];
	getLayers(app.activeDocument, layers);

	var layerCount = layers.length;
	var layerVisibility = {};

    var exportLayers = [];
    var re = new RegExp("^[a-zA-Z0-9_.]+$"); 
	for (var i = layerCount - 1; i >= 0; i--) {
		var layer = layers[i];
		layerVisibility[layer] = layer.visible;
		layer.visible = false;

         if (re.test(layer.name)) {
             exportLayers.push(layer);
         }
	}

    var exportLayerCount = exportLayers.length;
    var docWidth = app.activeDocument.width.as("px") * scaleFactor;
	var docHeight = app.activeDocument.height.as("px") * scaleFactor;
            
	// Save JSON.
	if (saveJSON || savePNGs) {
		var json = "{\n";
		for (var i = exportLayerCount - 1; i >= 0; i--) {
			var layer = exportLayers[i];
			
			if (ignoreHiddenLayers && !layerVisibility[layer]) continue;
				
			var x = docWidth;
			var y = docHeight;
			
			layer.visible = true;
			if (!layer.isBackgroundLayer)
				app.activeDocument.trim(TrimType.TRANSPARENT, false, true, true, false);
			x -= app.activeDocument.width.as("px") * scaleFactor;
			y -= app.activeDocument.height.as("px") * scaleFactor;
			if (!layer.isBackgroundLayer)
				app.activeDocument.trim(TrimType.TRANSPARENT, true, false, false, true);
			var width = app.activeDocument.width.as("px") * scaleFactor;
			var height = app.activeDocument.height.as("px") * scaleFactor;

			// Save image.
			if (savePNGs) {
				if (scaleFactor != 1) scaleImage();

                  var tmpName =  trim(layer.name);

                // if png or jpg
                var fileExt = ".png"
                var index = tmpName.lastIndexOf(".");
                if (index != -1) {
                    var ext = tmpName.substr(index+1);
                    if (ext == "jpg"){
                        fileExt = ".jpg"
                    }
                }
            
                if (fileExt == ".png"){
                  tmpName = tmpName + fileExt;
                }
                  
				var file = File(dir + "/" + tmpName);
				if (file.exists) file.remove();

                // save png start
                if (fileExt == ".jpg"){
                    var jpgSaveOptions = new JPEGSaveOptions();
                    jpgSaveOptions.embedColorProfile = true;
                    jpgSaveOptions.formatOptions = FormatOptions.STANDARDBASELINE;
                    jpgSaveOptions.matte = MatteType.NONE;
                    jpgSaveOptions.quality = 9; //1-12
                    activeDocument.saveAs(file, jpgSaveOptions, true, Extension.LOWERCASE);
                }
            
                if (fileExt == ".png"){
                      var id6 = charIDToTypeID('Expr')
                      var desc3 = new ActionDescriptor()
                      var id7 = charIDToTypeID('Usng')
                      var desc4 = new ActionDescriptor()
                      var id8 = charIDToTypeID('Op  ')
                      var id9 = charIDToTypeID('SWOp')
                      var id10 = charIDToTypeID('OpSa')
                      desc4.putEnumerated(id8, id9, id10)
                      var id11 = charIDToTypeID('Fmt ')
                      var id12 = charIDToTypeID('IRFm')
                      var id13 = charIDToTypeID('PN24')
                      desc4.putEnumerated(id11, id12, id13)
                      var id14 = charIDToTypeID('Intr')
                      desc4.putBoolean(id14, true)
                      var id15 = charIDToTypeID('Trns')
                      desc4.putBoolean(id15, true)
                      var id16 = charIDToTypeID('Mtt ')
                      desc4.putBoolean(id16, true)
                      var id17 = charIDToTypeID('MttR')
                      desc4.putInteger(id17, 255)
                      var id18 = charIDToTypeID('MttG')
                      desc4.putInteger(id18, 255)
                      var id19 = charIDToTypeID('MttB')
                      desc4.putInteger(id19, 255)
                      var id20 = charIDToTypeID('SHTM')
                      desc4.putBoolean(id20, false)
                      var id21 = charIDToTypeID('SImg')
                      desc4.putBoolean(id21, true)
                      var id22 = charIDToTypeID('SSSO')
                      desc4.putBoolean(id22, false)
                      var id23 = charIDToTypeID('SSLt')
                      var list1 = new ActionList()
                      desc4.putList(id23, list1)
                      var id24 = charIDToTypeID('DIDr')
                      desc4.putBoolean(id24, false)
                      var id25 = charIDToTypeID('In  ')
                      desc4.putPath(id25, new File(dir + "/" + tmpName))
                      desc4.putBoolean(charIDToTypeID('EICC'), false)
                      var id26 = stringIDToTypeID('SaveForWeb')
                      desc3.putObject(id7, id26, desc4)
                      executeAction(id6, desc3, DialogModes.NO)
                }
                // save png end

				if (scaleFactor != 1) stepHistoryBack();
			}
			
			if (!layer.isBackgroundLayer) {
				stepHistoryBack();
				stepHistoryBack();
			}
			layer.visible = false;
			
			x += Math.round(width) / 2;
			y += Math.round(height) / 2;

              // convert to center
              //x -= docWidth / 2;
              //y -= docHeight / 2;
            
			json += "\"" + trim(layer.name) + "\":{\"x\":" + x + ",\"y\":" + y+ ",\"width\":" + Math.round(width) + ",\"height\":" + Math.round(height) + "}";
             if (i > 0) {
                json += ",\n";
             }
		}
		json += "\n}";

		if (saveJSON) {
			// Write file.
			var file = new File(dir + name + ".json");
			file.remove();
			file.open("a");
			file.lineFeed = "\n";
			file.write(json);
			file.close();
		}
	}

	activeDocument.close(SaveOptions.DONOTSAVECHANGES);
}

// Unfinished!
function hasLayerSets (layerset) {
	layerset = layerset.layerSets;
	for (var i = 0; i < layerset.length; i++)
		if (layerset[i].layerSets.length > 0) hasLayerSets(layerset[i]);
}

function scaleImage() {
	var imageSize = app.activeDocument.width.as("px");
	app.activeDocument.resizeImage(UnitValue(imageSize * scaleFactor, "px"), undefined, 72, ResampleMethod.BICUBICSHARPER);
}

function stepHistoryBack () {
	var desc = new ActionDescriptor();
	var ref = new ActionReference();
	ref.putEnumerated( charIDToTypeID( "HstS" ), charIDToTypeID( "Ordn" ), charIDToTypeID( "Prvs" ));
	desc.putReference(charIDToTypeID( "null" ), ref);
	executeAction( charIDToTypeID( "slct" ), desc, DialogModes.NO );
}

function getLayers (layer, collect) {
	if (!layer.layers || layer.layers.length == 0) return layer;
	for (var i = 0, n = layer.layers.length; i < n; i++) {
		// For checking if its an adjustment layer, but it also excludes
		// LayerSets so we need to find the different types needed.
		//if (layer.layers[i].kind == LayerKind.NORMAL) {
			var child = getLayers(layer.layers[i], collect)
			if (child) collect.push(child);
		//}
	}
}

function trim (value) {
	return value.replace(/^\s+|\s+$/g, "");
}

function hasFilePath() {
	var ref = new ActionReference();
	ref.putEnumerated( charIDToTypeID("Dcmn"), charIDToTypeID("Ordn"), charIDToTypeID("Trgt") ); 
	return executeActionGet(ref).hasKey(stringIDToTypeID('fileReference'));
}

function showDialog () {
	if (!hasFilePath()) {
		alert("File path not found.\nYou need to save the document before continuing.");
		return;
	}

	var dialog = new Window("dialog", "Export Layers");

	dialog.savePNGs = dialog.add("checkbox", undefined, "Save PNGs"); 
	dialog.savePNGs.value = savePNGs;
	dialog.savePNGs.alignment = "left";

	dialog.saveJSON = dialog.add("checkbox", undefined, "Save JSON");
	dialog.saveJSON.alignment = "left";
	dialog.saveJSON.value = saveJSON;

	dialog.ignoreHiddenLayers = dialog.add("checkbox", undefined, "Ignore hidden layers");
	dialog.ignoreHiddenLayers.alignment = "left";
	dialog.ignoreHiddenLayers.value = ignoreHiddenLayers;

	var scaleGroup = dialog.add("panel", [0, 0, 180, 50], "Image Scale");
	var scaleText = scaleGroup.add("edittext", [10,10,40,30], scaleFactor * 100); 
	scaleGroup.add("statictext", [45, 12, 100, 20], "%");
	var scaleSlider = scaleGroup.add("slider", [60, 10,165,20], scaleFactor * 100, 1, 100);
	scaleText.onChanging = function() {
		scaleSlider.value = scaleText.text;
		if (scaleText.text < 1 || scaleText.text > 100) {
			alert("Valid numbers are 1-100.");
			scaleText.text = scaleFactor * 100;
			scaleSlider.value = scaleFactor * 100;
		}
	};
	scaleSlider.onChanging = function() { scaleText.text = Math.round(scaleSlider.value); };

	var confirmGroup = dialog.add("group", [0, 0, 180, 50]);
	var runButton = confirmGroup.add("button", [10, 10, 80, 35], "Ok");
	var cancelButton = confirmGroup.add("button", [90, 10, 170, 35], "Cancel");
	cancelButton.onClick = function() { dialog.close(0); return; };
	runButton.onClick = function() {
		savePNGs = dialog.savePNGs.value;
		saveJSON = dialog.saveJSON.value;
		ignoreHiddenLayers = dialog.ignoreHiddenLayers.value;
		scaleFactor = scaleSlider.value / 100;
		main();
		dialog.close(0);
	};

	dialog.orientation = "column";
	dialog.center();
	dialog.show();
}
