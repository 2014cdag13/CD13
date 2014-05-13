//var codart;
//var locate = window.location

// Function to create the activeX objects that are the interface to Web.Link.
function pfcCreate (className)
{
	if (navigator.appName.indexOf ("Microsoft") != -1)
		return new ActiveXObject ("pfc."+className);
	else
		alert ("Only only Internet Explorer is supported for Pro/ENGINEER Wildfire");
}

// This function just clears the results div.
function Clear ()
{
	ResultDIV.innerHTML="";
	mGlob = pfcCreate("MpfcCOMGlobal");
	var oSession = mGlob.GetProESession();
}

// function ListComponents()
function ListComponents()
{
	// Get Session, Model.
	mGlob = pfcCreate("MpfcCOMGlobal");
	var session = mGlob.GetProESession();
	var assembly = session.CurrentModel;
	var comp, p, p_value;
	if (assembly.Type != pfcCreate ("pfcModelType").MDL_ASSEMBLY)
	throw new Error (0, "Modello corrente non e un assieme");

	/*--------------------------------------------------------------------*\
	Visit the assembly components
	\*--------------------------------------------------------------------*/
	var components = assembly.ListFeaturesByType (false,
	pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);

	var assem = components.Item(0);
	var assem_type = assembly.MdlType;
	
//	alert("Complessivo");
	var complessivo = assembly.InstanceName;
//	alert(complessivo);
		p = assembly.GetParam("CODICE");
		p_value = p.Value;
		
		var str = p.Value.StringValue;
		point = str.indexOf(" ");
		if (point > 1) {
			nomeFile = str.substring(0, point);
		} else {
			nomeFile = str;
		}
	alert(complessivo + " - " + nomeFile);
		
//		alert(p.Name);
//		alert(p.Value.StringValue);
	
	// apertura file 
	var fileName = "G:\\SCOUT\\" + nomeFile + ".db";
	var fso = new ActiveXObject("Scripting.FileSystemObject");
	var s = fso.CreateTextFile(fileName, true);
	
    //document.get_deps.ModelNameExts.value = "";

	
	for (ii = 0; ii < components.Count; ii++)
	{
		var component = components.Item(ii);
		var desc = component.ModelDescr;
		var name = component.GetName();
		var type = component.CompType;		
		
//		alert(desc.InstanceName);
//		alert(desc.Type);
		if (desc.type == 0) {
			comp = session.GetModel(desc.InstanceName, pfcCreate("pfcModelType").MDL_ASSEMBLY);
		} else {
			comp = session.GetModel(desc.InstanceName, pfcCreate("pfcModelType").MDL_PART);
		}
		p = comp.GetParam("CODICE");
		p_value = p.Value;
//		alert(p.Name);
//		alert(p.Value.StringValue);

	// scrittura riga
        s.WriteLine(p.Value.StringValue + ";1;");
		//document.get_deps.ModelNameExts.value += p.Value.StringValue + "\n";
	}
	
	// chiusura file
	s.Close();
}
