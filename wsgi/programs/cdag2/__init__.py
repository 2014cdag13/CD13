import cherrypy

# 這是 CDAG2 類別的定義
class CDAG2(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
這是 2014CDA 協同專案下的 cdag2 分組程式開發網頁, 以下為 W12 的任務執行內容.<br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="cube1">cdag1 正方體參數繪圖</a>(尺寸變數 a, b, c)<br /><br />
<a href="fourbar1">四連桿組立</a><br /><br />
請確定下列連桿位於 V:/home/fourbar 目錄中, 且開啟空白 Creo 組立檔案.<br />
<a href="/static/fourbar.7z">fourbar.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />
'''
        return outstring

    ''' 
    假如採用下列規畫
    
    import programs.cdag2 as cdag2
    root.cdag2 = cdag2.CDAG2()
    
    則程式啟動後, 可以利用 /cdag2/cube1 呼叫函式執行
    '''
    @cherrypy.expose
    def cube1(self, *args, **kwargs):
        '''
    // 假如要自行打開特定零件檔案
    // 若第三輸入為 false, 表示僅載入 session, 但是不顯示
    // ret 為 model open return
    var ret = document.pwl.pwlMdlOpen("axle_5.prt", "v:/tmp", false);
    if (!ret.Status) {
        alert("pwlMdlOpen failed (" + ret.ErrorCode + ")");
    }
    //將 ProE 執行階段設為變數 session
    var session = pfcGetProESession();
    // 在視窗中打開零件檔案, 並且顯示出來
    var window = session.OpenFile(pfcCreate("pfcModelDescriptor").CreateFromFileName("axle_5.prt"));
    var solid = session.GetModel("axle_5.prt",pfcCreate("pfcModelType").MDL_PART);
        '''
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcParameterExamples.js"></script>
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcComponentFeatExamples.js"></script>
    </head>
    <body>
    <script type="text/javascript">
var session = pfcGetProESession ();

// 以目前所開啟的檔案為 solid model
// for volume
var solid = session.CurrentModel;

var a, b, c, i, j, aValue, bValue, cValue, volume, count;
// 將模型檔中的 a 變數設為 javascript 中的 a 變數
a = solid.GetParam("a");
b = solid.GetParam("b");
c = solid.GetParam("c");
volume=0;
count=0;
try
{
    for(i=0;i<5;i++)
    {
        myf = 100;
        myn = myf + i*10;
        // 設定變數值, 利用 ModelItem 中的 CreateDoubleParamValue 轉換成 Pro/Web.Link 所需要的浮點數值
    aValue = pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myn);
    bValue = pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myn);
    // 將處理好的變數值, 指定給對應的零件變數
    a.Value = aValue;
    b.Value = bValue;
    //零件尺寸重新設定後, 呼叫 Regenerate 更新模型
    solid.Regenerate(void null);
    //利用 GetMassProperty 取得模型的質量相關物件
    properties = solid.GetMassProperty(void null);
    volume = properties.Volume;
    count = count + 1;
    alert("執行第"+count+"次,零件總體積:"+volume);
    // 將零件存為新檔案
    //var newfile = document.pwl.pwlMdlSaveAs("filename.prt", "v:/tmp", "filename_5_"+count+".prt");
    // 測試  stl 轉檔
    //var stl_csys = "PRT_CSYS_DEF";
    //var stl_instrs = new pfcCreate ("pfcSTLASCIIExportInstructions").Create(stl_csys);
    //stl_instrs.SetQuality(10);  
    //solid.Export("v:/tmp/filename_5_"+count+".stl", stl_instrs); 
    // 結束測試轉檔
    //if (!newfile.Status) {
            //alert("pwlMdlSaveAs failed (" + newfile.ErrorCode + ")");
        //}
    } // for loop
}
catch (err)
{
    alert ("Exception occurred: "+pfcGetExceptionType (err));
}
    </script>
    </body>
    </html>
    '''
        return outstring
        
    @cherrypy.expose
    def fourbar1(self, *args, **kwargs):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    </head>
    <body>
<script type="text/javascript">
if (!pfcIsWindows())
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
var session = pfcGetProESession();
// 設定 config option
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣
var identityMatrix = pfcCreate ("pfcMatrix3D");
for (var x = 0; x < 4; x++)
	for (var y = 0; y < 4; y++)
	{
		if (x == y)
			identityMatrix.Set (x, y, 1.0);
		else
			identityMatrix.Set (x, y, 0.0);
	}
var transf = pfcCreate ("pfcTransform3D").Create (identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件
if (model == void null || model.Type != pfcCreate ("pfcModelType").MDL_ASSEMBLY)
throw new Error (0, "Current model is not an assembly.");
var assembly = model;

/**----------------------------------------------- link0 -------------------------------------------------------------**/
    //檔案目錄，建議將圖檔放置工作目錄下較方便使用
	var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link0.prt");
	// 若 link1.prt 在 session 則直接取用
	var componentModel = session.GetModelFromDescr (descr);
	//若 link1.prt 不在 session 則從工作目錄中載入 session
	var componentModel = session.RetrieveModel(descr);
	//若 link1.prt 已經在 session 則放入組立檔中
	if (componentModel != void null)
	{
		//注意這個 asmcomp 即為設定約束條件的本體
		//asmcomp 為特徵物件,直接將零件, 以 transf 座標轉換放入組立檔案中
		var asmcomp = assembly.AssembleComponent (componentModel, transf);
	}

// 建立約束條件變數
var constrs = pfcCreate ("pfcComponentConstraints");
//設定組立檔中的三個定位面, 注意內定名稱與 Pro/E WF 中的 ASM_D_FRONT 不同, 而是 ASM_FRONT
var asmDatums = new Array ("ASM_FRONT", "ASM_TOP", "ASM_RIGHT");
//設定零件檔中的三個定位面, 名稱與 Pro/E WF 中相同
var compDatums = new Array ("FRONT", "TOP", "RIGHT");
	//建立 ids 變數, intseq 為 sequence of integers 為資料類別, 使用者可以經由整數索引擷取此資料類別的元件, 第一個索引為 0
	var ids = pfcCreate ("intseq");
	//建立路徑變數
	var path = pfcCreate ("MpfcAssembly").CreateComponentPath (assembly, ids);
	//採用互動式設定相關的變數
	var MpfcSelect = pfcCreate ("MpfcSelect");
//利用迴圈分別約束組立與零件檔中的三個定位平面
for (var i = 0; i < 3; i++)
{
	//設定組立參考面
	var asmItem = assembly.GetItemByName (pfcCreate ("pfcModelItemType").ITEM_SURFACE, asmDatums [i]);
	//若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
	if (asmItem == void null)
	{
		interactFlag = true;
		continue;
	}
	//設定零件參考面
	var compItem = componentModel.GetItemByName (pfcCreate ("pfcModelItemType").ITEM_SURFACE, compDatums [i]);
	//若無對應的零件參考面, 則啟用互動式平面選擇表單 flag
	if (compItem == void null)
	{
		interactFlag = true;
		continue;
	}
	var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, path);
	var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
	var constr = pfcCreate ("pfcComponentConstraint").Create (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
	constr.AssemblyReference = asmSel;
	constr.ComponentReference = compSel;
	constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (false, false);
	//將互動選擇相關資料, 附加在程式約束變數之後
	constrs.Append (constr);
}

//設定組立約束條件
asmcomp.SetConstraints (constrs, void null);
/**-------------------------------------------------------------------------------------------------------------------**/

/**----------------------------------------------- link1 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link1.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
var featID = components.Item(0).Id;

ids.Append(featID);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_1", "TOP", "ASM_TOP");
var compDatums = new Array ("A_1", "TOP", "TOP");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

	
/**-------------------------------------------------------------------------------------------------------------------**/

/**----------------------------------------------- link2 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link2.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate ("intseq");
ids.Append(featID+1);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2", "TOP", "ASM_TOP");
var compDatums = new Array ("A_1", "TOP", "TOP");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

	
/**-------------------------------------------------------------------------------------------------------------------**/


/**----------------------------------------------- link3 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link3.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");

var ids = pfcCreate ("intseq");
ids.Append(featID+2);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2");
var compDatums = new Array ("A_1");
for (var i = 0; i < 1; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);


var ids = pfcCreate ("intseq");

ids.Append(featID);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2", "TOP");
var compDatums = new Array ("A_2", "BOTTON");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, true);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

/**-------------------------------------------------------------------------------------------------------------------**/

var session = pfcGetProESession ();
var solid = session.CurrentModel;

properties = solid.GetMassProperty(void null);
var COG = properties.GravityCenter;
document.write("MassProperty:<br />");
document.write("Mass:"+(properties.Mass.toFixed(2))+"       pound<br />");
document.write("Average Density:"+(properties.Density.toFixed(2))+"       pound/inch^3<br />");
document.write("Surface area:"+(properties.SurfaceArea.toFixed(2))+"           inch^2<br />");
document.write("Volume:"+(properties.Volume.toFixed(2))+"   inch^3<br />");
document.write("COG_X:"+COG.Item(0).toFixed(2)+"<br />");
document.write("COG_Y:"+COG.Item(1).toFixed(2)+"<br />");
document.write("COG_Z:"+COG.Item(2).toFixed(2)+"<br />");

try
{
document.write("Current Directory:<br />"+currentDir);
}
catch (err)
{
alert ("Exception occurred: "+pfcGetExceptionType (err));
}
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();
</script>
    </body>
    </html>
    '''
        return outstring

