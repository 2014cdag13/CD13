<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo (http://webpages.charter.net/edreamleo/front.html) -->
<?xml-stylesheet ekr_test?>
<leo_file xmlns:leo="http://www.leo-editor.org/2011/leo" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="course-mde-tw.20140417093332.1998"><vh>@settings</vh>
<v t="course-mde-tw.20140417093332.1999"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="course-mde-tw.20140417093332.2000"><vh>@string initial_split_orientation = horizontal</vh></v>
<v t="course-mde-tw.20140417093332.2001"><vh>@string rst3_write_intermediate_extension = .rst</vh></v>
</v>
<v t="course-mde-tw.20140417093332.2063"><vh>協同產品設計實習</vh></v>
<v t="2014pythonE.20140422152422.1669"><vh>電子郵箱管理</vh></v>
<v t="2014pythonE.20140422152422.1671"><vh>Github 帳號管理</vh></v>
<v t="2014pythonE.20140422152422.1670"><vh>OpenShift 權限管理</vh></v>
<v t="course-mde-tw.20140422171455.1745"><vh>Github 倉儲與 OpenShift 同步</vh></v>
<v t="course-mde-tw.20140417093332.2027" a="E"><vh>@path wsgi</vh>
<v t="course-mde-tw.20140417093332.2028" a="E"
expanded="course-mde-tw.20140417093332.2030,"><vh>@file application</vh></v>
</v>
<v t="course-mde-tw.20140417093332.2058" a="E"><vh>利用 pandoc 進行格式轉換</vh>
<v t="course-mde-tw.20140422221207.1747"><vh>注意事項</vh></v>
<v t="course-mde-tw.20140417093332.2059"><vh>@button pandoc</vh></v>
<v t="course-mde-tw.20140417093332.2060" a="E"><vh>@path wsgi/doc</vh>
<v t="course-mde-tw.20140417093332.2061"><vh>@edit title.txt</vh></v>
</v>
</v>
<v t="course-mde-tw.20140417093332.2047" a="E"><vh>分組協同報告區</vh>
<v t="course-mde-tw.20140417093332.2048" a="E"><vh>@path wsgi/doc</vh>
<v t="course-mde-tw.20140417093332.2049" a="E"><vh>@path 2ag1</vh>
<v t="course-mde-tw.20140417093332.2050"><vh>@edit doc.txt</vh></v>
</v>
<v t="course-mde-tw.20140417093332.2051" a="E"><vh>@path 2ag2</vh>
<v t="course-mde-tw.20140417093332.2052"><vh>@edit doc.txt</vh></v>
</v>
<v t="2014pythonE.20140429104126.1755"><vh>@path 2ag3</vh>
<v t="2014pythonE.20140429104126.1756"><vh>@edit doc.txt</vh></v>
</v>
<v t="kmolII_lite.20140430001511.1599" a="E"><vh>@path 2ag5</vh>
<v t="kmolII_lite.20140430001511.1600"><vh>@edit doc.txt</vh></v>
</v>
<v t="2014pythonE.20140429160432.1843" a="E"><vh>@path 2ag7</vh>
<v t="2014pythonE.20140429160432.1844"><vh>@edit doc.txt</vh></v>
</v>
<v t="2014pythonE.20140429160432.1847" a="E"><vh>@path 2ag16</vh>
<v t="2014pythonE.20140429160432.1848"><vh>@edit doc.txt</vh></v>
</v>
<v t="2014pythonE.20140424070658.1679" a="E"><vh>@path coursemdetw</vh>
<v t="2014pythonE.20140424070658.1680"><vh>@auto doc.txt</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="2014pythonE.20140422152422.1669">配合 2014cda 專案

2014cdaproject@gmail.com

正好可以有三個  Python 3.3 應用程式, 用於 

2014cda, 2014cdb, 2014c2 等三個專案使用</t>
<t tx="2014pythonE.20140422152422.1670">puttygen.exe 導入 private key 後, 以 Conversions-&gt;Export OpenSSH key

將資料存入 V:\home\.ssh\id_rsa 檔案中

當使用者利用  git clone OpenShift 平台上專案時, Git 將會利用 id_rsa 私鑰與 OpenShift settings 設定所儲存的 public key 進行配對, 若通過驗證才能更新或擷取 OpenShift 平台上的程式碼.</t>
<t tx="2014pythonE.20140422152422.1671">course-mde-tw on Github 使用 coursemdetw@gmail.com 登記

couorsemdetw on Github 使用 course@mde.tw 登記

2014cda, 2014cdb, 2014c2 Github 專案登記在 coursemdetw 名下

course-mde-tw 為協同人員

</t>
<t tx="2014pythonE.20140424070658.1679"></t>
<t tx="2014pythonE.20140429104126.1755"></t>
<t tx="2014pythonE.20140429160432.1843"></t>
<t tx="2014pythonE.20140429160432.1847"></t>
<t tx="course-mde-tw.20140417093332.1998"></t>
<t tx="course-mde-tw.20140417093332.1999">QSplitter::handle {
    background-color: #CAE1FF; /* lightSteelBlue1 */
}

QStackedWidget {
    /* background-color:lightpink; */
    border-color: red;
    padding: 0px;
    /* border-width: 0px; */
    /* background-color: yellow; */
}

QSplitter {
    border-color: white;
    background-color: white;
    border-style: solid;
}

QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    /*font-family: DejaVu Sans Mono;*/    
    font-family:YaHei Mono;
    /* 沒有特別對應字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: #f2fdff;
    selection-color: red;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* log font 大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: #fdf5f5; /* A kind of pink. */
    selection-color: white;
    selection-background-color: red;
    /*font-family: DejaVu Sans Mono;*/
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* 內文字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="course-mde-tw.20140417093332.2000">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="course-mde-tw.20140417093332.2001"></t>
<t tx="course-mde-tw.20140417093332.2027"></t>
<t tx="course-mde-tw.20140417093332.2047">各組的報告統一放在 doc 目錄下, 並且按照分組編號作為目錄名稱

最後希望能夠利用程式整合各分組報告內容, 統一處理成為 pdf 與 html 檔案

目錄架構:

doc 
    2ag1
        doc.txt
    2ag2
        doc.txt</t>
<t tx="course-mde-tw.20140417093332.2048"></t>
<t tx="course-mde-tw.20140417093332.2049"></t>
<t tx="course-mde-tw.20140417093332.2051"></t>
<t tx="course-mde-tw.20140417093332.2058">@language latex

% 中文內容設定

\usepackage{xeCJK}    % 中英文字行分開設置
\usepackage[T1]{fontspec}    %設定字體用
\usepackage{graphicx}
\usepackage{fancyvrb} % for frame on Verbatim
% 新細明體
% 文鼎ＰＬ新宋
\setCJKmainfont{新細明體}</t>
<t tx="course-mde-tw.20140417093332.2059">@language python
import os
'''
c is the commander of the outline containing the script.
g is Leo's leo.core.leoGlobals module.
p is the presently selected position, the same as c.p.
'''
d = c.scanAllDirectives(p)
#g.es(d)
# d 為 commander 由目前所在目錄進行指令設定掃描
# d 資料格式為 dictionary
''' 
實際操作下, d 為 
{'tabwidth': -4, 'lineending': None, 'language': 'python', 'encoding': None, 'pluginsList': [], 'pagewidth': 70, 'wrap': True, 'path': 'D:\\github\\mdeCourse\\2013spring', 'delims': ('#', '', '')}
'''
#在處理 pandoc 之前,  將協同人員上傳的 file1.txt 與 file2.txt 結合為 demo.txt
# 應該以 walkdir 走進各目錄取檔案名稱後, 然後依照字串排序決定先後次序
filenames = ['title.txt', '2ag1/doc.txt', '2ag2/doc.txt', '2ag3/doc.txt', '2ag5/doc.txt', 'coursemdetw/doc.txt']
directory = "V:/project/2014cda/wsgi/doc/"
with open('V:/project/2014cda/wsgi/pandoc/result.txt', 'w', encoding="utf-8") as outfile:
    for fname in filenames:
        fname = directory+fname
        with open(fname, encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)
            outfile.write("\n\n")

# 將目錄指到 pandoc
mandir = d.get('path') + "/wsgi/pandoc"
g.es(mandir)
os.chdir(mandir)
# 先轉一份 html 
os.system("V:\\apps\\pandoc\\pandoc.exe -s result.txt -o result.html")
# 利用 pandoc 將 demo.txt 轉為 demo.tex, 在此決定是否要有 toc
os.system("V:\\apps\\pandoc\\pandoc.exe -s result.txt --toc -o result.tex")
# 中文設定必須要放在 begin document 之前
setup = ''' 
\\usepackage{xeCJK}    % 中英文字行分開設置 
\\usepackage[T1]{fontspec}    %設定字體用 
\\usepackage{graphicx} 
\\usepackage{fancyvrb} % for frame on Verbatim 
\\setCJKmainfont{新細明體}
'''
# 在 demo.tex 最前頭加上"中文設定"
file = open("result.tex", "r", encoding="utf-8")
lines = file.read().splitlines()
file.close()
file = open("result.tex", "w", encoding="utf-8")
for i in range(len(lines)):
    # 設法將中文設定放在文件開始之前, 以便蓋掉之前的設定
    if "\\begin{document}" in lines[i]:
        file.write(setup+lines[i]+"\n")
    else:
        file.write(lines[i]+"\n")
file.close()
target_name = "result"
filename = target_name+".tex"
os.system("V:\\apps\\portableLatex\\MiKTeX\\texmf\\miktex\\bin\\xelatex.exe -no-pdf -interaction=nonstopmode "+filename)
os.system("V:\\apps\\portableLatex\\MiKTeX\\texmf\\miktex\\bin\\xelatex.exe -no-pdf -interaction=nonstopmode "+filename)
filename = target_name+".xdv"
os.system("V:\\apps\\portableLatex\\MiKTeX\\texmf\\miktex\\bin\\xdvipdfmx.exe -vv -E "+filename)

filename = target_name+".pdf"
os.system(filename)</t>
<t tx="course-mde-tw.20140417093332.2060"></t>
<t tx="course-mde-tw.20140417093332.2063">@language md
"# This is my README" 

同步規劃:

Bitbucket: https://bitbucket.org/cmsimply/public_cmsimply

Bitbucket 免費帳號特性:

可以自由將倉儲轉為 public 或 private, 沒有限制

每一倉儲最多只能有 5 個 collaborators

OpenShift: http://cdproject-coursemdetw.rhcloud.com/

OpenShift 免費帳號特性:

支援各種網際程式雲端部署, 但是每一帳號至多只能建 3 個應用程式

接下來要加上與 Github 的全班協同倉儲進行同步

Github 免費帳號特性:

免費帳號只能使用 public 倉儲

沒有限制 collaborators 個數, 適合多協同人員執行開放專案使用
</t>
<t tx="course-mde-tw.20140422171455.1745">在 Github 倉儲中將 OpenShift 倉儲設為 remote 倉儲

git remote add openshift ssh://5356315e4382ec2b3f000557@2014cda-mdenfu.rhcloud.com/~/git/2014cda.git/

利用 git pull 拉下目前位於 OpenShift 對應倉儲上的程式碼

git pull 的目的在設法讓 OpenShift 與 Github 中的 git 專案合併

若與 Github 近端倉儲中的資料沒有產生衝突, 則可以在內容修改後, 同時 push 到 Github 與 OpenShift

目前 OpenShift 網站: http://2014cda-mdenfu.rhcloud.com/

Github 倉儲則為: https://github.com/coursemdetw/2014cda

目前的規劃是讓參與協同者可以自由更新 Github 倉儲內容

並且將 Github 倉儲與各組可以控制的 OpenShift 網站同步</t>
<t tx="course-mde-tw.20140422221207.1747">mathspec.sty 檔案必須放在 pandoc 目錄中, 與文書處理原始檔案放在一起.</t>
<t tx="kmolII_lite.20140430001511.1599"></t>
</tnodes>
</leo_file>
