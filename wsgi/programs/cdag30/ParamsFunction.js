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
	
	var Wind=oSession.CurrentWindow;	
	Wind.Repaint();
}


// Function lists and then reports the parameters from the current model.
function ListParams()
{
	ResultDIV.innerHTML="";
	
	var Output="<TABLE>"+
				"<TR>"+
				"<TD><STRONG>Item</STRONG></TD>"+
				"<TD><STRONG>Name</STRONG></TD>"+
				"<TD><STRONG>Value</STRONG></TD>"+
				"</TR>";
	
	// Get Session, Model.
	mGlob = pfcCreate("MpfcCOMGlobal");
	var oSession = mGlob.GetProESession();
	var CurModel = oSession.CurrentModel;
	
	// List the Parameters.
	var lParams = CurModel.ListParams();
	
	for (i=0;i<lParams.Count;i++)
	{
		var CurParam = lParams.Item(i);
		var CurParamValue = CurParam.Value;
		var CurParamType = CurParamValue.discr;
				
		Output=Output+"<TR><TD>"+(i+1)+"</TD><TD>"+CurParam.Name+"</TD><TD>"
		
		if (CurParamType == pfcCreate("pfcParamValueType").PARAM_STRING)
		{
			Output=Output+CurParamValue.StringValue+"</TD></TR>";
		}
		
		else if (CurParamType == pfcCreate("pfcParamValueType").PARAM_INTEGER)
		{
			Output=Output+CurParamValue.IntValue+"</TD></TR>";
		}
		
		else if (CurParamType == pfcCreate("pfcParamValueType").PARAM_BOOLEAN)
		{
			Output=Output+CurParamValue.BoolValue+"</TD></TR>";
		}
		
		else if (CurParamType == pfcCreate("pfcParamValueType").PARAM_DOUBLE)
		{
			Output=Output+CurParamValue.DoubleValue+"</TD></TR>";
		}
		
		else if (CurParamType == pfcCreate("pfcParamValueType").PARAM_NOTE)
		{
			Output=Output+"Note with ID of "+CurParamValue.NoteID+"</TD></TR>";
		}
	
		else
		{
			Output=Output+"Unknown"+"</TD></TR>";
		}
	}
	
	Output=Output+"</TABLE>";
	ResultDIV.innerHTML=Output;
}


// Function demonstrates how a parameter's value can be modified.
function ChangeParam()
{
	//ToValue = ParamValue.value;
	//ResultDIV.innerHTML="";
	
	// Get Session, Window and Model.
	mGlob = pfcCreate("MpfcCOMGlobal");
	var oSession = mGlob.GetProESession();
	var CurWind = oSession.CurrentWindow;
	var CurModel = oSession.CurrentModel;
	
	// Get the HYD_LENGTH parameter.
	var CurParam = CurModel.GetParam("HYD_LENGTH");
	
	var CurParamValue = CurParam.Value;
	var CurParamType = CurParamValue.discr;
	
	//make value ToValue.
	//CurParamValue.DoubleValue = ToValue;
	//CurParam.Value = CurParamValue;
	
	// Update the model
	CurModel.Regenerate(null);
	CurWind.Repaint();
	
	// Explanation.
	ResultDIV.innerHTML="Parameter Value adjusted to "+codart+
						"<BR>Then Model Regenerated.</BR>";
}


// Function brings up the entry form for new parameter creation.
function CreateParam()
{
	ResultDIV.innerHTML="Fill out the following information:<BR>"+
						"Parameter Name: <INPUT TYPE='TEXT' NAME='NewParamName' VALUE='Example' SIZE=10><BR>"+
						"Parameter Value:<INPUT TYPE='TEXT' NAME='NewParamValue' VALUE='String' SIZE=10><BR>"+
						"<BR>"+
						"<INPUT TYPE='BUTTON' VALUE='CREATE PARAMETER' onClick='AssignParam()'>";
}


// This function creates a parameter based on the values from the parameter creation form.
function AssignParam()
{
	// Code takes the values from the entry boxes and assigns them to Variables.
	var TargetParamName=NewParamName.value;
	var TargetParamValue=NewParamValue.value;
	
	// Get Session, Model.
	mGlob = pfcCreate("MpfcCOMGlobal");
	var oSession = mGlob.GetProESession();
	var CurModel = oSession.CurrentModel;
	
	// Define a Parameter Value Object.
	var ParamValue = pfcCreate ("MpfcModelItem").CreateStringParamValue(TargetParamValue);
	
	// This is how you create a model parameter.
	CurModel.CreateParam(TargetParamName, ParamValue);
	
	// Re-Run the list of parameters function.
	ListParams();
}


// This function demonstrates how parameters can just as easily be deleted.
function DeleteParam()
{
	ResultDIV.innerHTML="";
	
	// Get Session and Model.
	mGlob = pfcCreate("MpfcCOMGlobal");
	var oSession = mGlob.GetProESession();
	var CurModel = oSession.CurrentModel;
	
	// Get list of Parameters.
	var lParams = CurModel.ListParams();
	
	// We're going to delete the last parameter so we can find it by using the lists' Count property.
 	var nParams = lParams.Count;
	
	// The function will only allow the user to delete up to the last two parameters (to avoid screw-ups)
	if (nParams>2)
	{
		var LastParam = lParams(nParams-1);
		ResultDIV.innerHTML="Parameter "+LastParam.Name+" was deleted.";
		LastParam.Delete();
	}
	else
	{
		ResultDIV.innerHTML="You are not allowed to delete the last two parameters.";
	}
}


/*====================================================================*\
FUNCTION: createParametersFromArguments
PURPOSE:  Create/modify parameters in the model based on name-value pairs 
			in the page URL
\*====================================================================*/
function createParametersFromArguments ()  
{
	var propValue;
  	var propsfile = "params.properties";
  	var p;
 
  	var args = getArgs (); // See Function getArgs
  
	//Use the current model as the parameter owner.
	var session = pfcCreate ("MpfcCOMGlobal").GetProESession ();
  	var pOwner = session.CurrentModel;
 
  	if (pOwner == void null)
		throw new Error (0, "No current model.");

	//Process each name/value pair as a Pro/E parameter.
	for (var i = 0; i < args.length; i++)
  	{
		var pName = args[i].Name;
     	var pv = createParamValueFromString(args[i].Value); // See function createParamValueFromString
     	p = pOwner.GetParam(pName);

		//GetParam returns null if it can't find the param.  Create it.
		if (p == void null) 
       	{
  			pOwner.CreateParam (pName, pv);
       	}
     	else
       	{
         	p.Value = pv;
       	}
   	}
   	// This macro just brings up the parameters box so we can see the results.
	session.RunMacro ("~ Select `main_dlg_cur` `MenuBar1` `Utilities`;~ Close `main_dlg_cur` `MenuBar1`;~ Activate `main_dlg_cur` `Utilities.psh_params`");
}


/*====================================================================*\
FUNCTION: getArgs
PURPOSE:  Parse arguments passed via the URL
\*====================================================================*/
function getArgs ()
{
	var args = new Array ();

	var query = location.search.substring (1);
	
	var pairs = query.split ("&");
	for (var i = 0; i < pairs.length; i++)
	{	
		var pos = pairs [i].indexOf ('=');
		if (pos == -1) continue;
		var argname = pairs[i].substring (0, pos);
		var value = pairs[i].substring (pos+1);
		var argPair = new Object ();
		argPair.Name = argname;
		argPair.Value = unescape (value);
		args.push (argPair);
	}
	
	return args;
}


/*====================================================================*\
FUNCTION: createParamValueFromString
PURPOSE:  Parses a string into a pfcParamValue object, checking for most 
		restrictive possible type to use.
\*====================================================================*/	
function createParamValueFromString (s /* string */)
{
	if (s.indexOf (".") == -1)
	{
		var i = parseInt (s);
		if (!isNaN(i))
			return pfcCreate ("MpfcModelItem").CreateIntParamValue(i);
	}
	else
	{
		var d = parseFloat (s);
		if (!isNaN(d))
			return pfcCreate ("MpfcModelItem").CreateDoubleParamValue(d);
	}
    if (s.toUpperCase() == "Y" || s.toUpperCase ()== "TRUE")
	  return pfcCreate ("MpfcModelItem").CreateBoolParamValue(true);
			
	if (s.toUpperCase() == "N" || s.toUpperCase ()== "FALSE")
	  return pfcCreate ("MpfcModelItem").CreateBoolParamValue(false);
			
	return pfcCreate ("MpfcModelItem").CreateStringParamValue(s);
}
