#@+leo-ver=5-thin
#@+node:2014spring.20140508134612.2197: * @file cmsimply.py
'''
Copyright © 2014 Chiaming Yen

CMSimply is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CMSimply is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CMSimply. If not, see <http://www.gnu.org/licenses/>.

***********************************************************************
'''

#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:2014spring.20140508134612.2198: ** <<declarations>> (cmsimply.py)
import cherrypy
import re
import os
import math
import hashlib
from cherrypy.lib.static import serve_file
# use quote_plus() to generate URL
import urllib.parse
# use cgi.escape() to resemble php htmlspecialchars()
# use cgi.escape() or html.escape to generate data for textarea tag, otherwise Editor can not deal with some Javascript code.
import cgi

# get the current directory of the file
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
print("current dir:", _curdir)
import sys
sys.path.append(_curdir)

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    inOpenshift = True
else:
    inOpenshift = False

if inOpenshift:
    # while program is executed in OpenShift
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # while program is executed in localhost
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"
    print("data_dir:", data_dir)


#@-<<declarations>>
#@+others
#@+node:2014spring.20140508134612.2199: ** downloadlist_access_list
def downloadlist_access_list(files, starti, endi):
    # different extension files, associated links were provided
    # popup window to view images, video or STL files, other files can be downloaded directly
    # files are all the data to list, from starti to endi
    # add file size
    outstring = ""
    for index in range(int(starti)-1, int(endi)):
        fileName, fileExtension = os.path.splitext(files[index])
        fileExtension = fileExtension.lower()
        fileSize = sizeof_fmt(os.path.getsize(download_root_dir+"downloads/"+files[index]))
        # images files
        if fileExtension == ".png" or fileExtension == ".jpg" or fileExtension == ".gif":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # stl files
        elif fileExtension == ".stl":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/static/viewstl.html?src=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # flv files
        elif fileExtension == ".flv":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/flvplayer?filepath=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # direct download files
        else:
            outstring += "<input type='checkbox' name='filename' value='"+files[index]+"'><a href='download/?filepath="+download_root_dir.replace('\\', '/')+ \
            "downloads/"+files[index]+"'>"+files[index]+"</a> ("+str(fileSize)+")<br />"
    return outstring
#@+node:2014spring.20140508134612.2200: ** sizeof_fmt
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
#@+node:2014spring.20140508134612.2201: ** set_admin_css
# set_admin_css for administrator
def set_admin_css():
    outstring = '''<!doctype html><html><head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>CMSimply - Simple Cloud CMS in Python 3</title> \
<link rel="stylesheet" type="text/css" href="/static/cmsimply.css">
'''+syntaxhighlight()

    outstring += '''
<script src="/static/jquery.js"></script>
<script type="text/javascript">
$(function(){
    $("ul.topmenu> li:has(ul) > a").append('<div class="arrow-right"></div>');
    $("ul.topmenu > li ul li:has(ul) > a").append('<div class="arrow-right"></div>');
});
</script>
'''
    # SSL for OpenShift operation
    if inOpenshift:
        outstring += '''
<script type="text/javascript">
if ((location.href.search(/http:/) != -1) && (location.href.search(/login/) != -1)) \
window.location= 'https://' + location.host + location.pathname + location.search;
</script>
'''
    site_title, password = parse_config()
    outstring += '''
</head><header><h1>'''+site_title+'''</h1> \
<confmenu>
<ul>
<li><a href="">Home</a></li>
<li><a href="sitemap">SiteMap</a></li>
<li><a href="edit_page">Edit All</a></li>
<li><a href="'''+cherrypy.url(qs=cherrypy.request.query_string)+'''&edit=1">Edit</a></li>
<li><a href="edit_config">Config</a></li>
<li><a href="search_form">Search</a></li>
<li><a href="imageuploadform">Image Upload</a></li>
<li><a href="fileuploadform">File Upload</a></li>
<li><a href="download_list">File List</a></li>
<li><a href="logout">Logout</a></li>
'''
    outstring += '''
</ul>
</confmenu></header>
'''
    return outstring
#@+node:2014spring.20140508134612.2202: ** set_footer
def set_footer():
    # Extra consideration for cherrypy.url(qs=cherrypy.request.query_string) return no data
    return "<footer> \
        <a href='edit_page'>Edit All</a>| \
        <a href='"+cherrypy.url(qs=cherrypy.request.query_string)+"&edit=1'>Edit</a>| \
        <a href='edit_config'>Config</a> \
        <a href='login'>login</a>| \
        <a href='logout'>logout</a> \
        <br />Powered by <a href='http://cmsimple.cycu.org'>CMSimply</a> \
        </footer> \
        </body></html>"
#@+node:2014spring.20140508134612.2203: ** file_get_contents
def file_get_contents(filename):
    # open file in utf-8 and return file content
    with open(filename, encoding="utf-8") as file:
        return file.read()
#@+node:2014spring.20140508134612.2204: ** search_content
# use head title to search page content
def search_content(head, page, search):
    return page[head.index(search)]
#@+node:2014spring.20140508134612.2205: ** parse_content
def parse_content():
    if not os.path.isfile(data_dir+"content.htm"):
        # create content.htm if there is no content.htm
        File = open(data_dir+"content.htm", "w", encoding="utf-8")
        File.write("<h1>head 1</h1>content 1")
        File.close()
    subject = file_get_contents(data_dir+"content.htm")
    # deal with content without heading
    # replace subject content with special seperate string to avoid error 
    subject = re.sub('#@CMSIMPLY_SPLIT@#', '井@CMSIMPLY_SPLIT@井', subject)
    content_sep = '#@CMSIMPLY_SPLIT@#'
    head_level = 3
    # remove all attribute inside h1, h2 and h3 tags
    subject = re.sub('<(h1|h2|h3)[^>]*>', r'<\1>', subject, flags=re.I)
    content = re.split('</body>', subject)
    result = re.sub('<h[1-'+str(head_level)+']>', content_sep, content[0])
    # remove the first element contains html and body tags
    data = result.split(content_sep)[1:]
    head_list = []
    level_list = []
    page_list = []
    order = 1
    for index in range(len(data)):
        #page_data = re.sub('</h[1-'+str(head_level)+']>', content_sep, data[index])
        page_data = re.sub('</h', content_sep, data[index])
        head = page_data.split(content_sep)[0]
        order += 1
        head_list.append(head)
        # put level data into level variable
        level = page_data.split(content_sep)[1][0]
        level_list.append(level)
        # remove  1>,  2> or 3>
        page = page_data.split(content_sep)[1][2:]
        page_list.append(page)
    # send head to unique function to avoid duplicate heading
    #head_list = unique(head_list)
    return head_list, level_list, page_list
#@+node:2014spring.20140508134612.2206: ** render_menu
def render_menu(head, level, page, sitemap=0):
    directory = ""
    current_level = level[0]
    if sitemap:
        directory += "<ul>"
    else:
        directory += "<ul id='css3menu1' class='topmenu'>"
    for index in range(len(head)):
        if level[index] > current_level:
            directory += "<ul>"
            directory += "<li><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
        elif level[index] == current_level:
            if level[index] == 1:
                if sitemap:
                    directory += "<li><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
                else:
                    directory += "<li class='topmenu'><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
            else:
                directory += "<li><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
        else:
            directory += "</li>"*(int(current_level) - int(level[index]))
            directory += "</ul>"*(int(current_level) - int(level[index]))
            if level[index] == 1:
                if sitemap:
                    directory += "<li><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
                else:
                    directory += "<li class='topmenu'><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
            else:
                directory += "<li><a href='get_page?heading="+head[index]+"'>"+head[index]+"</a>"
        current_level = level[index]
    directory += "</li></ul>"
    return directory
#@+node:2014spring.20140508134612.2207: ** filebrowser
def filebrowser():
    return '''
<script type="text/javascript">
function wrFilebrowser (field_name, url, type, win) {
poppedUpWin = win;
inputField = field_name;
if (type == "file") {type = "downloads"};
// 請注意, 這裡要配合 application 中的 root.cmsimply 設為 cmsimply
var cmsURL = "/cmsimply/file_selector";    

if (cmsURL.indexOf("?") < 0) {
    cmsURL = cmsURL + "?type="+ type ;
}
else {
    cmsURL = cmsURL + "&type="+type ;
}

tinyMCE.activeEditor.windowManager.open(
    {
        file  : cmsURL,
        width : 800,
        height : 600,
        resizable : "yes",
        inline : "yes",
        close_previous : "no",
        popup_css : false,
        scrollbars : "yes"
      },
      {
        window : win,
        input : field_name
      }
);
return false;
}
'''
#@+node:2014spring.20140508134612.2208: ** syntaxhighlight
def syntaxhighlight():
    return '''
<script type="text/javascript" src="/static/syntaxhighlighter/shCore.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushJScript.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushJava.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushPython.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushSql.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushXml.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushPhp.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushCpp.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushCss.js"></script>
<script type="text/javascript" src="/static/syntaxhighlighter/shBrushCSharp.js"></script>
<link type="text/css" rel="stylesheet" href="/static/syntaxhighlighter/css/shCoreDefault.css"/>
<script type="text/javascript">SyntaxHighlighter.all();</script>
'''
#@+node:2014spring.20140508134612.2209: ** editorhead
def editorhead():
    return '''
<script language="javascript" type="text/javascript" src="/static/tinymce3/tiny_mce/tiny_mce.js"></script>
<script type="text/javascript" src="/static/tinymce3/init.js"></script>
'''
#@+node:2014spring.20140508134612.2210: ** tinymceinit
def tinymceinit():
    return '''
<script language="javascript" type="text/javascript">
function tinyMCE_initialize0() {
    tinyMCE_instantiateByClasses('simply-editor', {
// General options

theme : "advanced",
width : "800",
height : "600",
element_format : "html",
language : "en",
plugins : "autosave,pagebreak,style,layer,table,save,advimage,advlink,advhr,emotions,iespell,"
        + "insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,"
        + "noneditable,visualchars,nonbreaking,xhtmlxtras,template,wordcount,media,lists,syntaxhl",

// Theme options
theme_advanced_buttons1 : "save,|,fullscreen,code,formatselect,fontselect,fontsizeselect,styleselect,syntaxhl",
theme_advanced_buttons2 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,cut,copy,paste,pastetext,pasteword,|,bullist,numlist,outdent,indent,blockquote",
theme_advanced_buttons3 : "undo,redo,|,link,unlink,anchor,image,media,cleanup,|,hr,removeformat,visualaid,|,forecolor,backcolor,|,search,replace,|,charmap",
theme_advanced_buttons4 : "emotions,sub,sup,|,tablecontrols,insertdate,inserttime,help",
theme_advanced_toolbar_location : "top",
theme_advanced_toolbar_align : "left",
theme_advanced_statusbar_location : "bottom",
theme_advanced_resizing : true,
theme_advanced_blockformats : "h1,h2,h3,p,div,h4,h5,h6,blockquote,dt,dd,code",
theme_advanced_font_sizes : "8px=8px, 10px=10px,12px=12px, 14px=14px, 16px=16px, 18px=18px,20px=20px,24px=24px,36px=36px",

content_css : "/static/cmsimply.css",
//link and image list
external_image_list_url: "/static/tinymce3/cms_image_list.js",
external_link_list_url: "/static/tinymce3/cms_link_list.js",

// Extra
plugin_insertdate_dateFormat: "%d-%m-%Y",
plugin_insertdate_timeFormat: "%H:%M:%S",
inline_styles : true,
apply_source_formatting : true,
relative_urls : true,
convert_urls: false,
entity_encoding : "raw",

file_browser_callback: "wrFilebrowser" ,
fullscreen_new_window : false ,
fullscreen_settings : {
theme_advanced_buttons1: "save,|,fullscreen,code,|,formatselect,fontselect,fontsizeselect,styleselect,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,cut,copy,paste,pastetext,pasteword,|,bullist,numlist,outdent,indent,blockquote,|,undo,redo",
theme_advanced_buttons2 : "link,unlink,anchor,image,media,cleanup,|,hr,removeformat,visualaid,|,forecolor,backcolor,|,search,replace,|,charmap,emotions,|,sub,sup,tablecontrols,insertdate,inserttime,|,help",
theme_advanced_buttons3 : "",
theme_advanced_buttons4 : ""
}
});
}
</script>
'''
#@+node:2014spring.20140508134612.2211: ** editorfoot
def editorfoot():
    return '''<body id="body"  onload="tinyMCE_initialize0();">'''
#@+node:2014spring.20140508134612.2212: ** tinymce_editor
def tinymce_editor(menu_input=None, editor_content=None, page_order=None):
    files = os.listdir(download_root_dir+"downloads/")
    link_list = ""
    image_list = ""
    for index in range(len(files)):
        file_url = "download/?filepath="+download_root_dir.replace('\\', '/')+"downloads/"+files[index]
        link_list += "['"+files[index]+"', '"+file_url+"']"
        if index != len(files)-1:
            link_list += ","
    # deal with image link
    images = os.listdir(download_root_dir+"images/")
    for index in range(len(images)):
        image_url = "/images/"+images[index]
        image_list += "['"+images[index]+"', '"+image_url+"']"
        if index != len(images)-1:
            image_list += ","
    sitecontent =file_get_contents(data_dir+"content.htm")
    editor = set_admin_css()+editorhead()+filebrowser()+'''
var myImageList = new Array('''+image_list+''');
var myLinkList = new Array('''+link_list+''');
</script>'''+tinymceinit()+'''</head>'''+editorfoot()
    # edit all pages
    if page_order == None:
        outstring = editor + "<div class='container'><nav>"+ \
            menu_input+"</nav><section><form method='post' action='savePage'> \
     <textarea class='simply-editor' name='page_content' cols='50' rows='15'>"+editor_content+"</textarea> \
     <input type='submit' value='save'></form></section></body></html>"
    else:
        # add viewpage button wilie single page editing
        head, level, page = parse_content()
        outstring = editor + "<div class='container'><nav>"+ \
            menu_input+"</nav><section><form method='post' action='ssavePage'> \
     <textarea class='simply-editor' name='page_content' cols='50' rows='15'>"+editor_content+"</textarea> \
<input type='hidden' name='page_order' value='"+str(page_order)+"'> \
     <input type='submit' value='save'>"
        outstring += '''<input type=button onClick="location.href='get_page?heading='''+head[page_order]+ \
            ''''" value='viewpage'></form></section></body></html>'''
    return outstring
#@+node:2014spring.20140508134612.2213: ** parse_config
def parse_config():
    if not os.path.isfile(data_dir+"config"):
        # create config file if there is no config file
        file = open(data_dir+"config", "w", encoding="utf-8")
        # default password is admin
        password="admin"
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        file.write("siteTitle:CMSimply - Simple Cloud CMS in Python 3\npassword:"+hashed_password)
        file.close()
    config = file_get_contents(data_dir+"config")
    config_data = config.split("\n")
    site_title = config_data[0].split(":")[1]
    password = config_data[1].split(":")[1]
    return site_title, password
#@+node:2014spring.20140508134612.2214: ** file_selector_script
def file_selector_script():
    return '''
<script type="text/javascript" src="/static/tinymce3/tiny_mce/tiny_mce_popup.js"></script>
<script language="javascript" type="text/javascript">

var FileBrowserDialogue = {
    
    init : function () {
        // Nothing to do
    },

   
    submit : function (url) {
        var URL = url;
        var win = tinyMCEPopup.getWindowArg("window");
        var input = win.document.getElementById(tinyMCEPopup.getWindowArg("input"));
        win.document.getElementById(tinyMCEPopup.getWindowArg("input")).value = URL;

        input.value = URL;
        if (input.onchange) input.onchange();

        tinyMCEPopup.close();
    }
}

tinyMCEPopup.onInit.add(FileBrowserDialogue.init, FileBrowserDialogue);

function setLink(link){

    FileBrowserDialogue.submit(link);
    return true;
}
</script>
'''
#@+node:2014spring.20140508134612.2215: ** file_lister
def file_lister(directory, type=None, page=1, item_per_page=10):
    files = os.listdir(download_root_dir+directory)
    total_rows = len(files)
    totalpage = math.ceil(total_rows/int(item_per_page))
    starti = int(item_per_page) * (int(page) - 1) + 1
    endi = starti + int(item_per_page) - 1
    outstring = file_selector_script()
    notlast = False
    if total_rows > 0:
        outstring += "<br />"
        if (int(page) * int(item_per_page)) < total_rows:
            notlast = True
        if int(page) > 1:
            outstring += "<a href='"
            outstring += "file_selector?type="+type+"&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'><<</a> "
            page_num = int(page) - 1
            outstring += "<a href='"
            outstring += "file_selector?type="+type+"&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'>Previous</a> "
        span = 10
        for index in range(int(page)-span, int(page)+span):
        #for ($j=$page-$range;$j<$page+$range;$j++)
            if index>= 0 and index< totalpage:
                page_now = index + 1 
                if page_now == int(page):
                    outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                else:
                    outstring += "<a href='"
                    outstring += "file_selector?type="+type+"&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                    outstring += "'>"+str(page_now)+"</a> "

        if notlast == True:
            nextpage = int(page) + 1
            outstring += " <a href='"
            outstring += "file_selector?type="+type+"&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'>Next</a>"
            outstring += " <a href='"
            outstring += "file_selector?type="+type+"&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'>>></a><br /><br />"
        if (int(page) * int(item_per_page)) < total_rows:
            notlast = True
            if type == "downloads":
                outstring += downloadselect_access_list(files, starti, endi)+"<br />"
            else:
                outstring += imageselect_access_list(files, starti, endi)+"<br />"
        else:
            outstring += "<br /><br />"
            if type == "downloads":
                outstring += downloadselect_access_list(files, starti, total_rows)+"<br />"
            else:
                outstring += imageselect_access_list(files, starti, total_rows)+"<br />"
        if int(page) > 1:
            outstring += "<a href='"
            outstring += "file_selector?type="+type+"&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'><<</a> "
            page_num = int(page) - 1
            outstring += "<a href='"
            outstring += "file_selector?type="+type+"&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'>Previous</a> "
        span = 10
        for index in range(int(page)-span, int(page)+span):
        #for ($j=$page-$range;$j<$page+$range;$j++)
            if index >=0 and index < totalpage:
                page_now = index + 1
                if page_now == int(page):
                    outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                else:
                    outstring += "<a href='"
                    outstring += "file_selector?type="+type+"&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                    outstring += "'>"+str(page_now)+"</a> "
        if notlast == True:
            nextpage = int(page) + 1
            outstring += " <a href='"
            outstring += "file_selector?type="+type+"&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'>Next</a>"
            outstring += " <a href='"
            outstring += "file_selector?type="+type+"&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
            outstring += "'>>></a>"
    else:
        outstring += "no data!"

    if type == "downloads":
        return outstring+"<br /><br /><a href='/fileuploadform'>file upload</a>"
    else:
        return outstring+"<br /><br /><a href='/imageuploadform'>image upload</a>"
#@+node:2014spring.20140508134612.2216: ** downloadselect_access_list
def downloadselect_access_list(files, starti, endi):
    outstring = ""
    for index in range(int(starti)-1, int(endi)):
        fileName, fileExtension = os.path.splitext(files[index])
        fileSize = os.path.getsize(download_root_dir+"/downloads/"+files[index])
        outstring += '''<input type="checkbox" name="filename" value="'''+files[index]+'''"><a href="#" onclick='window.setLink("download/?filepath='''+ \
        download_root_dir.replace('\\', '/')+'''/downloads/'''+files[index]+'''",0); return false;'>'''+ \
        files[index]+'''</a> ('''+str(sizeof_fmt(fileSize))+''')<br />'''
    return outstring
#@+node:2014spring.20140508134612.2217: ** loadlist_access_list
def loadlist_access_list(files, starti, endi, filedir):
    # different extension files, associated links were provided
    # popup window to view images, video or STL files, other files can be downloaded directly
    # files are all the data to list, from starti to endi
    # add file size
    outstring = ""
    for index in range(int(starti)-1, int(endi)):
        fileName, fileExtension = os.path.splitext(files[index])
        fileExtension = fileExtension.lower()
        fileSize = sizeof_fmt(os.path.getsize(data_dir+filedir+"_programs/"+files[index]))
        # images files
        if fileExtension == ".png" or fileExtension == ".jpg" or fileExtension == ".gif":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # stl files
        elif fileExtension == ".stl":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/static/viewstl.html?src=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # flv files
        elif fileExtension == ".flv":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/flvplayer?filepath=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # py files
        elif fileExtension == ".py":
            outstring += '<input type="radio" name="filename" value="'+files[index]+'">'+files[index]+' ('+str(fileSize)+')<br />'
        # direct download files
        else:
            outstring += "<input type='checkbox' name='filename' value='"+files[index]+"'><a href='/"+filedir+"_programs/"+files[index]+"'>"+files[index]+"</a> ("+str(fileSize)+")<br />"
    return outstring
#@+node:2014spring.20140508134612.2218: ** imageselect_access_list
def imageselect_access_list(files, starti, endi):
    outstring = '''<head>
<style>
a.xhfbfile {padding: 0 2px 0 0; line-height: 1em;}
a.xhfbfile img{border: none; margin: 6px;}
a.xhfbfile span{display: none;}
a.xhfbfile:hover span{
    display: block;
    position: relative;
    left: 150px;
    border: #aaa 1px solid;
    padding: 2px;
    background-color: #ddd;
}
a.xhfbfile:hover{
    background-color: #ccc;
    opacity: .9;
    cursor:pointer;
}
</style>
</head>
'''
    for index in range(int(starti)-1, int(endi)):
        fileName, fileExtension = os.path.splitext(files[index])
        fileSize = os.path.getsize(download_root_dir+"/images/"+files[index])
        outstring += '''<a class="xhfbfile" href="#" onclick='window.setLink("download/?filepath='''+ \
        download_root_dir.replace('\\', '/')+'''/images/'''+files[index]+'''",0); return false;'>'''+ \
        files[index]+'''<span style="position: absolute; z-index: 4;"><br />
        <img src="download/?filepath='''+ \
        download_root_dir.replace('\\', '/')+'''/images/'''+files[index]+'''" width="150px"/></span></a> ('''+str(sizeof_fmt(fileSize))+''')<br />'''
    return outstring
#@+node:2014spring.20140508134612.2219: ** sizeof_fmt
def sizeof_fmt(num):
    for x in ['bytes','kb','mb','gb']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'tb')
#@+node:2014spring.20140508134612.2220: ** unique
def unique(items):
    found = set([])
    keep = []
    count = {}
    for item in items:
        if item not in found:
            count[item] = 0
            found.add(item)
            keep.append(item)
        else:
            count[item] += 1
            keep.append(str(item)+"_"+str(count[item]))
    return keep
#@+node:2014spring.20140508134612.2221: ** class CMSimply
class CMSimply(object):
    _cp_config = {
    # if there is no utf-8 encoding, no Chinese input available
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session timeout is 60 minutes
    'tools.sessions.timeout' : 60
    }
    
    #@+others
    #@+node:2014spring.20140508134612.2222: *3* __init__
    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(download_root_dir+"downloads"):
            try:
                os.makedirs(download_root_dir+"downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"images"):
            try:
                os.makedirs(download_root_dir+"images")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"tmp"):
            try:
                os.makedirs(download_root_dir+"tmp")
            except:
                print("mkdir error")
        if not os.path.isdir(data_dir+"brython_programs"):
            try:
                os.makedirs(data_dir+"brython_programs")
            except:
                print("mkdir error")
        if not os.path.isdir(data_dir+"calc_programs"):
            try:
                os.makedirs(data_dir+"calc_programs")
            except:
                print("mkdir error")

    #@+node:2014spring.20140508134612.2223: *3* index
    @cherrypy.expose
    def index(self, heading=None, *args, **kwargs):
        head, level, page = parse_content()
        raise cherrypy.HTTPRedirect("get_page?heading=")
        # the following will never execute
        directory = render_menu(head, level, page)
        if heading == None:
            heading = head[0]
        page_order = head.index(heading)
        if page_order == 0:
            last_page = ""
        else:
            last_page = head[page_order-1]+" << <a href='get_page?heading="+head[page_order-1]+"'>Previous</a>"
        if page_order == len(head) - 1:
            # no next page
            next_page = ""
        else:
            next_page = "<a href='get_page?heading="+head[page_order+1]+"'>Next</a> >> "+ head[page_order+1]
        if heading == None:
            #  while there is no content in content.htm
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section>"+last_page+" "+next_page+"<br /><h1>"+head[0]+"</h1>"+search_content(head, page, head[0])+"<br />"+last_page+" "+next_page+"</section></div></body></html>"
        else:
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section>"+last_page+" "+next_page+"<br /><h1>"+heading+"</h1>"+search_content(head, page, heading)+"<br />"+last_page+" "+next_page+"</section></div></body></html>"


    #@+node:2014spring.20140508134612.2224: *3* default
    # default method, if there is no corresponding method, cherrypy will redirect to default method
    # need *args and **kwargs as input variables for all possible URL links
    @cherrypy.expose
    def default_void(self, attr='default', *args, **kwargs):
        raise cherrypy.HTTPRedirect("/")
    #@+node:2014spring.20140508134612.2225: *3* error_log
    @cherrypy.expose
    def error_log(self, info="Error"):
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        return self.set_css()+"<div class='container'><nav>"+ \
        directory+"</nav><section><h1>ERROR</h1>"+info+"</section></div></body></html>"
    #@+node:2014spring.20140508134612.2226: *3* login
    @cherrypy.expose
    def login(self):
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        if not self.isAdmin():
            return self.set_css()+"<div class='container'><nav>"+ \
        directory+"</nav><section><h1>Login</h1><form method='post' action='checkLogin'> \
        Password:<input type='password' name='password'> \
        <input type='submit' value='login'></form> \
        </section></div></body></html>"
        else:
            raise cherrypy.HTTPRedirect("/edit_page")
    #@+node:2014spring.20140508134612.2227: *3* logout
    @cherrypy.expose
    def logout(self):
        cherrypy.session.delete()
        raise cherrypy.HTTPRedirect("/")
    #@+node:2014spring.20140508134612.2228: *3* checkLogin
    @cherrypy.expose
    def checkLogin(self, password=None):
        site_title, saved_password = parse_config()
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        if hashed_password == saved_password:
            cherrypy.session['admin'] = 1
            raise cherrypy.HTTPRedirect("edit_page")
        raise cherrypy.HTTPRedirect("/")
    #@+node:2014spring.20140508134612.2229: *3* get_page
    # seperate page need heading and edit variables, if edit=1, system will enter edit mode
    # single page edit will use ssavePage to save content, it means seperate save page
    @cherrypy.expose
    def get_page(self, heading=None, edit=0, *args, **kwargs):
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        try:
            pagecontent = search_content(head, page, heading)
            page_order = head.index(heading)
        except:
            heading = head[0]
            pagecontent = page[0]
            page_order = 0
        if page_order == 0:
            # no last page
            last_page = ""
        else:
            last_page = head[page_order-1] + " << <a href='get_page?heading="+head[page_order-1]+"'>Previous</a>"
        if page_order == len(head) - 1:
            # no next page
            next_page = ""
        else:
            next_page = "<a href='get_page?heading="+head[page_order+1]+"'>Next</a> >> "+ head[page_order+1]
        
        # edit=0 for viewpage
        if edit == 0:
            if heading == None:
                return page[0]
            else:
                return self.set_css()+"<div class='container'><nav>"+ \
                directory+"</nav><section>"+last_page+" "+next_page+"<br /><h1>"+heading+"</h1>"+pagecontent+"<br />"+last_page+" "+next_page+"</section></div></body></html>"
        # enter edit mode
        else:
            # check if administrator
            if not self.isAdmin():
                raise cherrypy.HTTPRedirect("login")
            else:
                pagedata = "<h"+level[page_order]+">"+heading+"</h"+level[page_order]+">"+search_content(head, page, heading)
                outstring = last_page+" "+next_page+"<br />"+ tinymce_editor(directory, cgi.escape(pagedata), page_order)
                return outstring
    #@+node:2014spring.20140508134612.2230: *3* isAdmin
    def isAdmin(self):
        if cherrypy.session.get('admin') == 1:
                return True
        else:
            return False
    #@+node:2014spring.20140508134612.2231: *3* edit_page
    # edit all page content
    @cherrypy.expose
    def edit_page(self):
        # check if administrator
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:
            head, level, page = parse_content()
            directory = render_menu(head, level, page)
            pagedata =file_get_contents(data_dir+"content.htm")
            outstring = tinymce_editor(directory, cgi.escape(pagedata))
            return outstring
    #@+node:2014spring.20140508134612.2232: *3* savePage
    @cherrypy.expose
    def savePage(self, page_content=None):
        # check if administrator
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        if page_content == None:
            return self.error_log("no content to save!")
        # we need to check if page heading is duplicated
        file = open(data_dir+"content.htm", "w", encoding="utf-8")
        # in Windows client operator, to avoid textarea add extra \n
        page_content = page_content.replace("\n","")
        file.write(page_content)
        file.close()
        '''
        # need to parse_content() to eliminate duplicate heading
        head, level, page = parse_content()
        file = open(data_dir+"content.htm", "w", encoding="utf-8")
        for index in range(len(head)):
            file.write("<h"+str(level[index])+">"+str(head[index])+"</h"+str(level[index])+">"+str(page[index]))
        file.close()
        '''
        raise cherrypy.HTTPRedirect("edit_page")
    #@+node:2014spring.20140508134612.2233: *3* ssavePage
    # seperate save page
    @cherrypy.expose
    def ssavePage(self, page_content=None, page_order=None):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        if page_content == None:
            return self.error_log("no content to save!")
        page_content = page_content.replace("\n","")
        head, level, page = parse_content()
        file = open(data_dir+"content.htm", "w", encoding="utf-8")
        for index in range(len(head)):
            if index == int(page_order):
                file.write(page_content)
            else:
                file.write("<h"+str(level[index])+">"+str(head[index])+"</h"+str(level[index])+">"+str(page[index]))
        file.close()
        '''
        # need to parse_content() to eliminate duplicate heading
        head, level, page = parse_content()
        file = open(data_dir+"content.htm", "w", encoding="utf-8")
        for index in range(len(head)):
            file.write("<h"+str(level[index])+">"+str(head[index])+"</h"+str(level[index])+">"+str(page[index]))
        file.close()
        '''
        # go back to origin edit status
        edit_url = "get_page?heading="+urllib.parse.quote_plus(head[int(page_order)])+"&edit=1"
        raise cherrypy.HTTPRedirect(edit_url)
    #@+node:2014spring.20140508134612.2234: *3* save_program
    @cherrypy.expose
    def save_program(self, filename=None, editor=None, overwrite=0, delete1=0, delete2=0):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:
            if overwrite == "1" or not os.path.isfile(data_dir+"/brython_programs/"+filename):
                # open file in wt will use Windows \r\n for new line
                # use replace method to remove extra lines for Windows environment
                with open(data_dir+"/brython_programs/"+filename, "wt", encoding="utf-8") as out_file:
                    data = editor.replace("\r\n", "\n")
                    out_file.write(data)
                return str(filename)+" saved!<br />"
            else:  
                return str(filename)+" exists! editor content not saved yet!<br />"

    #@+node:2014spring.20140508134612.2235: *3* save_calcprogram
    @cherrypy.expose
    def save_calcprogram(self, filename=None, sheet_content=None, overwrite=0, delete1=0, delete2=0):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:
            if overwrite == "1" or not os.path.isfile(data_dir+"/calc_programs/"+filename):
                # open file in wt will use Windows \r\n for new line
                # use replace method to remove extra lines for Windows environment
                with open(data_dir+"/calc_programs/"+filename, "wt", encoding="utf-8") as out_file:
                    data = sheet_content.replace("\r\n", "\n")
                    out_file.write(data)
                return str(filename)+" saved!<br />"
            else:  
                return str(filename)+" exists! editor content not saved yet!<br />"

     





    #@+node:2014spring.20140508134612.2236: *3* delete_program
    @cherrypy.expose
    def delete_program(self, filename=None, editor=None, overwrite=0, delete1=0, delete2=0):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:       
            if delete1 == "1" and delete2 == "1" and os.path.isfile(data_dir+"/brython_programs/"+filename):
                os.remove(data_dir+"/brython_programs/"+filename)
                return str(filename)+" deleted!<br />"
            elif not os.path.isfile(data_dir+"/brython_programs/"+filename):
                return str(filename)+" does not exist!<br />"
            else:
                return "can not delete "+str(filename)+"!"
                
    #@+node:2014spring.20140508134612.2237: *3* delete_calcprogram
    @cherrypy.expose
    def delete_calcprogram(self, filename=None, sheet_content=None, overwrite=0, delete1=0, delete2=0):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:       
            if delete1 == "1" and delete2 == "1" and os.path.isfile(data_dir+"/calc_programs/"+filename):
                os.remove(data_dir+"/calc_programs/"+filename)
                return str(filename)+" deleted!<br />"
            elif not os.path.isfile(data_dir+"/calc_programs/"+filename):
                return str(filename)+" does not exist!<br />"
            else:
                return "can not delete "+str(filename)+"!"
                
    #@+node:2014spring.20140508134612.2238: *3* fileuploadform
    @cherrypy.expose
    def fileuploadform(self):
        if self.isAdmin():
            head, level, page = parse_content()
            directory = render_menu(head, level, page)
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>file upload</h1>"+'''
<script src="/static/jquery.js" type="text/javascript"></script>
<script src="/static/axuploader.js" type="text/javascript"></script>
<script>
$(document).ready(function(){
$('.prova').axuploader({url:'fileaxupload', allowExt:['jpg','png','gif','7z','pdf','zip','flv','stl','swf'],
finish:function(x,files)
        {
            alert('All files have been uploaded: '+files);
        },
enable:true,
remotePath:function(){
  return 'downloads/';
}
});
});
</script>
<div class="prova"></div>
<input type="button" onclick="$('.prova').axuploader('disable')" value="asd" />
<input type="button" onclick="$('.prova').axuploader('enable')" value="ok" />
</section></body></html>
'''
        else:
            raise cherrypy.HTTPRedirect("login")
    #@+node:2014spring.20140508134612.2239: *3* fileaxupload
    @cherrypy.expose
    def fileaxupload(self, *args, **kwargs):
        # need to consider if the uploaded filename already existed.
        # right now all existed files will be replaced with the new files
        if self.isAdmin():
            filename = kwargs["ax-file-name"]
            flag = kwargs["start"]
            if flag == "0":
                file = open(download_root_dir+"downloads/"+filename, "wb")
            else:
                file = open(download_root_dir+"downloads/"+filename, "ab")
            file.write(cherrypy.request.body.read())
            file.close()
            return "files uploaded!"
        else:
            raise cherrypy.HTTPRedirect("login")
    #@+node:2014spring.20140508134612.2240: *3* flvplayer
    @cherrypy.expose
    def flvplayer(self, filepath=None):
        outstring = '''
    <object type="application/x-shockwave-flash" data="/static/player_flv_multi.swf" width="320" height="240">
         <param name="movie" value="player_flv_multi.swf" />
         <param name="allowFullScreen" value="true" />
         <param name="FlashVars" value="flv='''+filepath+'''&amp;width=320&amp;height=240&amp;showstop=1&amp;showvolume=1&amp;showtime=1
         &amp;startimage=/static/startimage_en.jpg&amp;showfullscreen=1&amp;bgcolor1=189ca8&amp;bgcolor2=085c68
         &amp;playercolor=085c68" />
    </object>
    '''
        return outstring
    #@+node:2014spring.20140508134612.2241: *3* imageuploadform
    @cherrypy.expose
    def imageuploadform(self):
        if self.isAdmin():
            head, level, page = parse_content()
            directory = render_menu(head, level, page)
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>image upload</h1>"+'''
<script src="/static/jquery.js" type="text/javascript"></script>
<script src="/static/axuploader.js" type="text/javascript"></script>
<script>
$(document).ready(function(){
$('.prova').axuploader({url:'imageaxupload', allowExt:['jpg','png','gif'],
finish:function(x,files)
        {
            alert('All files have been uploaded: '+files);
        },
enable:true,
remotePath:function(){
  return 'images/';
}
});
});
</script>
<div class="prova"></div>
<input type="button" onclick="$('.prova').axuploader('disable')" value="asd" />
<input type="button" onclick="$('.prova').axuploader('enable')" value="ok" />
'''
        else:
            raise cherrypy.HTTPRedirect("login")
    #@+node:2014spring.20140508134612.2242: *3* imageaxupload
    @cherrypy.expose
    def imageaxupload(self, *args, **kwargs):
        if self.isAdmin():
            filename = kwargs["ax-file-name"]
            flag = kwargs["start"]
            if flag == 0:
                file = open(download_root_dir+"images/"+filename, "wb")
            else:
                file = open(download_root_dir+"images/"+filename, "ab")
            file.write(cherrypy.request.body.read())
            file.close()
            return "image files uploaded!"
        else:
            raise cherrypy.HTTPRedirect("login")
    #@+node:2014spring.20140508134612.2243: *3* file_selector
    @cherrypy.expose
    def file_selector(self, type=None, page=1, item_per_page=10, keyword=None):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:
            if type == "downloads":
                #return downloads_file_selector()
                return file_lister("downloads", type, page, item_per_page)
            elif type == "image":
                #return images_file_selector()
                return file_lister("images", type, page, item_per_page)
    #@+node:2014spring.20140508134612.2244: *3* download_list
    @cherrypy.expose
    def download_list(self, item_per_page=5, page=1, keyword=None, *args, **kwargs):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        # cherrypy.session['admin'] = 1
        # cherrypy.session.get('admin')
        files = os.listdir(download_root_dir+"downloads/")
        total_rows = len(files)
        totalpage = math.ceil(total_rows/int(item_per_page))
        starti = int(item_per_page) * (int(page) - 1) + 1
        endi = starti + int(item_per_page) - 1
        outstring = "<form method='post' action='delete_file'>"
        notlast = False
        if total_rows > 0:
            outstring += "<br />"
            if (int(page) * int(item_per_page)) < total_rows:
                notlast = True
            if int(page) > 1:
                outstring += "<a href='"
                outstring += "download_list?&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'><<</a> "
                page_num = int(page) - 1
                outstring += "<a href='"
                outstring += "download_list?&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Previous</a> "
            span = 10
            for index in range(int(page)-span, int(page)+span):
                if index>= 0 and index< totalpage:
                    page_now = index + 1 
                    if page_now == int(page):
                        outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                    else:
                        outstring += "<a href='"
                        outstring += "download_list?&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                        outstring += "'>"+str(page_now)+"</a> "

            if notlast == True:
                nextpage = int(page) + 1
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Next</a>"
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>>></a><br /><br />"
            if (int(page) * int(item_per_page)) < total_rows:
                notlast = True
                outstring += downloadlist_access_list(files, starti, endi)+"<br />"
            else:
                outstring += "<br /><br />"
                outstring += downloadlist_access_list(files, starti, total_rows)+"<br />"
            
            if int(page) > 1:
                outstring += "<a href='"
                outstring += "download_list?&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'><<</a> "
                page_num = int(page) - 1
                outstring += "<a href='"
                outstring += "download_list?&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Previous</a> "
            span = 10
            for index in range(int(page)-span, int(page)+span):
            #for ($j=$page-$range;$j<$page+$range;$j++)
                if index >=0 and index < totalpage:
                    page_now = index + 1
                    if page_now == int(page):
                        outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                    else:
                        outstring += "<a href='"
                        outstring += "download_list?&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                        outstring += "'>"+str(page_now)+"</a> "
            if notlast == True:
                nextpage = int(page) + 1
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Next</a>"
                outstring += " <a href='"
                outstring += "download_list?&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>>></a>"
        else:
            outstring += "no data!"
        outstring += "<br /><br /><input type='submit' value='delete'><input type='reset' value='reset'></form>"

        head, level, page = parse_content()
        directory = render_menu(head, level, page)

        return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>Download List</h1>"+outstring+"<br/><br /></body></html>"
    #@+node:2014spring.20140508134612.2245: *3* load_list
    @cherrypy.expose
    def load_list(self, item_per_page=5, page=1, filedir=None, keyword=None, *args, **kwargs):
        '''
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        '''
        # cherrypy.session['admin'] = 1
        # cherrypy.session.get('admin')
        files = os.listdir(data_dir+filedir+"_programs/")
        total_rows = len(files)
        totalpage = math.ceil(total_rows/int(item_per_page))
        starti = int(item_per_page) * (int(page) - 1) + 1
        endi = starti + int(item_per_page) - 1
        #outstring = "<form name='filelist' method='post' action='load_program'>"
        outstring = "<form name='filelist' method='post' action=''>"
        notlast = False
        if total_rows > 0:
            # turn off the page selector on top
            '''
            outstring += "<br />"
            if (int(page) * int(item_per_page)) < total_rows:
                notlast = True
            if int(page) > 1:
                outstring += "<a href='"
                outstring += "brython?&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>{{</a> "
                page_num = int(page) - 1
                outstring += "<a href='"
                outstring += "brython?&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Previous</a> "
            span = 10
            for index in range(int(page)-span, int(page)+span):
                if index>= 0 and index< totalpage:
                    page_now = index + 1 
                    if page_now == int(page):
                        outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                    else:
                        outstring += "<a href='"
                        outstring += "brython?&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                        outstring += "'>"+str(page_now)+"</a> "

            if notlast == True:
                nextpage = int(page) + 1
                outstring += " <a href='"
                outstring += "brython?&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Next</a>"
                outstring += " <a href='"
                outstring += "brython?&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>}}</a><br /><br />"
            '''
            if (int(page) * int(item_per_page)) < total_rows:
                notlast = True
                outstring += loadlist_access_list(files, starti, endi, filedir)+"<br />"
            else:
                outstring += "<br /><br />"
                outstring += loadlist_access_list(files, starti, total_rows, filedir)+"<br />"
            
            if int(page) > 1:
                outstring += "<a href='"
                outstring += "/"+filedir+"?&amp;page=1&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>{{</a> "
                page_num = int(page) - 1
                outstring += "<a href='"
                outstring += "/"+filedir+"?&amp;page="+str(page_num)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Previous</a> "
            span = 10
            for index in range(int(page)-span, int(page)+span):
            #for ($j=$page-$range;$j<$page+$range;$j++)
                if index >=0 and index < totalpage:
                    page_now = index + 1
                    if page_now == int(page):
                        outstring += "<font size='+1' color='red'>"+str(page)+" </font>"
                    else:
                        outstring += "<a href='"
                        outstring += "/"+filedir+"?&amp;page="+str(page_now)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                        outstring += "'>"+str(page_now)+"</a> "
            if notlast == True:
                nextpage = int(page) + 1
                outstring += " <a href='"
                outstring += "/"+filedir+"?&amp;page="+str(nextpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>Next</a>"
                outstring += " <a href='"
                outstring += "/"+filedir+"?&amp;page="+str(totalpage)+"&amp;item_per_page="+str(item_per_page)+"&amp;keyword="+str(cherrypy.session.get('download_keyword'))
                outstring += "'>}}</a>"
        else:
            outstring += "no data!"
        #outstring += "<br /><br /><input type='submit' value='load'><input type='reset' value='reset'></form>"
        outstring += "<br /><br /></form>"

        return outstring
    #@+node:2014spring.20140508134612.2246: *3* delete_file
    @cherrypy.expose
    def delete_file(self, filename=None):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        if filename == None:
            outstring = "no file selected!"
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>Delete Error</h1>"+outstring+"<br/><br /></body></html>"
        outstring = "delete all these files?<br /><br />"
        outstring += "<form method='post' action='doDelete'>"
        # only one file is selected
        if isinstance(filename, str):
            outstring += filename+"<input type='hidden' name='filename' value='"+filename+"'><br />"
        else:
            # multiple files selected
            for index in range(len(filename)):
                outstring += filename[index]+"<input type='hidden' name='filename' value='"+filename[index]+"'><br />"
        outstring += "<br /><input type='submit' value='delete'></form>"

        return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>Download List</h1>"+outstring+"<br/><br /></body></html>"
    #@+node:2014spring.20140508134612.2247: *3* doDelete
    @cherrypy.expose
    def doDelete(self, filename=None):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        # delete files
        outstring = "all these files will be deleted:<br /><br />"
        # only select one file
        if isinstance(filename, str):
            try:
                os.remove(download_root_dir+"downloads/"+filename)
                outstring += filename+" deleted!"
            except:
                outstring += filename+"Error, can not delete files!<br />"
        else:
            # multiple files selected
            for index in range(len(filename)):
                try:
                    os.remove(download_root_dir+"downloads/"+filename[index])
                    outstring += filename[index]+" deleted!<br />"
                except:
                    outstring += filename[index]+"Error, can not delete files!<br />"

        head, level, page = parse_content()
        directory = render_menu(head, level, page)

        return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>Download List</h1>"+outstring+"<br/><br /></body></html>"
    #@+node:2014spring.20140508134612.2248: *3* creo_getvolume
    @cherrypy.expose
    def creo_getvolume(self, *args, **kwargs):
        return '''
<script src="/static/weblink/pfcUtils.js">
</script><script  src="/static/weblink/pfcParameterExamples.js"></script><script  src="/static/weblink/pfcComponentFeatExamples.js">
 document.writeln ("Error loading script!");
</script><script language="JavaScript">
    if (!pfcIsWindows())
        netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
  var session = pfcGetProESession ();
// for volume
  var solid = session.CurrentModel;
    try
        {
            createParametersFromArguments ();
            solid.Regenerate(void null);   
            properties = solid.GetMassProperty(void null);
            alert("part volume:"+properties.Volume);
        }
    catch (err)
        {
            alert ("Exception occurred: "+pfcGetExceptionType (err));
       }
</script>
'''
    #@+node:2014spring.20140508134612.2249: *3* anglebracket
    @cherrypy.expose
    def anglebracket(self, *args, **kwargs):
        return '''
<script src="/static/weblink/pfcUtils.js">
</script><script src="/static/weblink/wl_header.js">
document.writeln ("Error loading Pro/Web.Link header!");
</script><script language="JavaScript">
if (!pfcIsWindows()) netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
// if the third input is false, it means use session, but will not be displayed
// ret is the model open return
 var ret = document.pwl.pwlMdlOpen("angle_bracket_creo.prt", "c:/tmp", false);
if (!ret.Status) {
    alert("pwlMdlOpen failed (" + ret.ErrorCode + ")");
}
    var session = pfcGetProESession();
    var window = session.OpenFile(pfcCreate("pfcModelDescriptor").CreateFromFileName("angle_bracket_creo.prt"));
    var solid = session.GetModel("angle_bracket_creo.prt",pfcCreate("pfcModelType").MDL_PART);
    var d1,d2,myf,myn,i,j,volume,count,d1Value,d2Value;
    d1 = solid.GetParam("len1");
    //d2 = solid.GetParam("width");
    //myf=20;
    //myn=20;
    volume=0;
    count=0;
    try
    {
            //createParametersFromArguments ();
            for(i=0;i<=3;i++)
            {
                //for(j=0;j<=2;j++)
                //{
                    myf=180+i;
                    //myn=100+i*10;
         d1Value = pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myf);
         d2Value = pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myn);
                    d1.Value = d1Value;
                    //d2.Value = d2Value;
                    solid.Regenerate(void null);
                    properties = solid.GetMassProperty(void null);
                    //volume = volume + properties.Volume;
volume = properties.Volume;
                    count = count + 1;
alert("execute no: "+count+", part volume:"+volume);
var newfile = document.pwl.pwlMdlSaveAs("angle_bracket_creo.prt", "c:/tmp", "cadp_w12_py_"+count+".prt");
if (!newfile.Status) {
    alert("pwlMdlSaveAs failed (" + newfile.ErrorCode + ")");
//}
                }
            }
            //alert("totally execute:"+count+"times, part volume:"+volume);
            //alert("part volume:"+properties.Volume);
            //alert("part volume to integer:"+Math.round(properties.Volume));
        }
    catch(err)
        {
            alert ("Exception occurred: "+pfcGetExceptionType (err));
        }
</script>
'''
    #@+node:2014spring.20140508134612.2250: *3* search_form
    @cherrypy.expose
    def search_form(self):
        if self.isAdmin():
            head, level, page = parse_content()
            directory = render_menu(head, level, page)
            return self.set_css()+"<div class='container'><nav>"+ \
        directory+"</nav><section><h1>Search</h1><form method='post' action='doSearch'> \
        keywords:<input type='text' name='keyword'> \
        <input type='submit' value='search'></form> \
        </section></div></body></html>"
        else:
            raise cherrypy.HTTPRedirect("login")
    #@+node:2014spring.20140508134612.2251: *3* doSearch
    @cherrypy.expose
    def doSearch(self, keyword=None):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        else:
            head, level, page = parse_content()
            directory = render_menu(head, level, page)
            match = ""
            for index in range(len(head)):
                if keyword != "" and (keyword.lower() in page[index].lower() or \
                keyword.lower() in head[index].lower()): \
                    match += "<a href='get_page?heading="+head[index]+"'>"+head[index]+"</a><br />"
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>Search Result</h1>keyword: "+ \
            keyword.lower()+"<br /><br />in the following pages:<br /><br />"+ \
            match+" \
         </section></div></body></html>"
    #@+node:2014spring.20140508134612.2252: *3* set_css
    def set_css(self):
        outstring = '''<!doctype html><html><head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>CMSimply - Simple Cloud CMS in Python 3</title> \
    <link rel="stylesheet" type="text/css" href="/static/cmsimply.css">
    '''+syntaxhighlight()

        outstring += '''
    <script src="/static/jquery.js"></script>
    <script type="text/javascript">
    $(function(){
        $("ul.topmenu> li:has(ul) > a").append('<div class="arrow-right"></div>');
        $("ul.topmenu > li ul li:has(ul) > a").append('<div class="arrow-right"></div>');
    });
    </script>
    '''
        if inOpenshift:
            outstring += '''
    <script type="text/javascript">
    if ((location.href.search(/http:/) != -1) && (location.href.search(/login/) != -1)) \
    window.location= 'https://' + location.host + location.pathname + location.search;
    </script>
    '''
        site_title, password = parse_config()
        outstring += '''
    </head><header><h1>'''+site_title+'''</h1> \
    <confmenu>
    <ul>
    <li><a href="">Home</a></li>
    <li><a href="sitemap">Site Map</a></li>
    '''
        if self.isAdmin():
            outstring += '''
    <li><a href="edit_page">Edit All</a></li>
    <li><a href="'''+cherrypy.url(qs=cherrypy.request.query_string)+'''&edit=1">Edit</a></li>
    <li><a href="edit_config">Config</a></li>
    <li><a href="search_form">Search</a></li>
    <li><a href="imageuploadform">image upload</a></li>
    <li><a href="fileuploadform">file upload</a></li>
    <li><a href="download_list">file list</a></li>
    <li><a href="logout">logout</a></li>
    '''
        else:
            outstring += '''
    <li><a href="login">login</a></li>
    '''
        outstring += '''
    </ul>
    </confmenu></header>
    '''
        return outstring
    #@+node:2014spring.20140508134612.2253: *3* edit_config
    @cherrypy.expose
    def edit_config(self):
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        if not self.isAdmin():
            return self.set_css()+"<div class='container'><nav>"+ \
        directory+"</nav><section><h1>Login</h1><form method='post' action='checkLogin'> \
        Password:<input type='password' name='password'> \
        <input type='submit' value='login'></form> \
        </section></div></body></html>"
        else:
            site_title, password = parse_config()
            # edit config file
            return self.set_css()+"<div class='container'><nav>"+ \
        directory+"</nav><section><h1>Edit Config</h1><form method='post' action='saveConfig'> \
        Site Title:<input type='text' name='site_title' value='"+site_title+"' size='50'><br /> \
        Password:<input type='text' name='password' value='"+password+"' size='50'><br /> \
     <input type='hidden' name='password2' value='"+password+"'> \
        <input type='submit' value='send'></form> \
        </section></div></body></html>"
    #@+node:2014spring.20140508134612.2254: *3* saveConfig
    @cherrypy.expose
    def saveConfig(self, site_title=None, password=None, password2=None):
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
        if site_title == None or password == None:
            return self.error_log("no content to save!")
        old_site_title, old_password = parse_config()
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        if site_title == None or password == None or password2 != old_password or password == '':
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>Error!</h1><a href='/'>Home</a></body></html>"
        else:
            if password == password2 and password == old_password:
                hashed_password = old_password
            else:
                hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
            file = open(data_dir+"config", "w", encoding="utf-8")
            file.write("siteTitle:"+site_title+"\npassword:"+hashed_password)
            file.close()
            return self.set_css()+"<div class='container'><nav>"+ \
            directory+"</nav><section><h1>config file saved</h1><a href='/'>Home</a></body></html>"
    #@+node:2014spring.20140508134612.2255: *3* listdir
    # use to check directory variable data
    @cherrypy.expose
    def listdir(self):
        return download_root_dir +","+data_dir
    #@+node:2014spring.20140508134612.2256: *3* sitemap
    @cherrypy.expose
    def sitemap(self):
        head, level, page = parse_content()
        directory = render_menu(head, level, page)
        sitemap = render_menu(head, level, page, sitemap=1)

        return self.set_css()+"<div class='container'><nav>"+ \
        directory+"</nav><section><h1>Site Map</h1>"+sitemap+"</section></div></body></html>"
    #@+node:2014spring.20140508134612.2257: *3* brython
    @cherrypy.expose
    def brython(self, item_per_page=5, page=1, keyword=None, filename=None, *args, **kwargs):
        part1 =  '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <link rel="stylesheet" type="text/css" href="/static/console.css">
    <link rel="stylesheet" type="text/css" href="/static/brython.css">
    <script type="text/javascript" src="/static/Brython2.1.0-20140419-113919/brython.js"></script>
    <script src="https://togetherjs.com/togetherjs-min.js"></script>
    <script src="https://d1n0x3qji82z53.cloudfront.net/src-min-noconflict/ace.js" type="text/javascript">
    </script>
    <script src="/static/Cango2D.js" type="text/javascript">
    </script>
    <script src="/static/yen_fourbar.js" type="text/javascript">
    </script>
    <script src="/static/gearUtils-04.js" type="text/javascript">
    </script>
    <script src="/static/jsc3d.js" type="text/javascript">
    </script>
    <script src="/static/stlviewer.js" type="text/javascript">
    </script>
    <script src="/static/threejs/three.min.js" type="text/javascript">
    </script>
    <script src="/static/threejs/Coordinates.js" type="text/javascript">
    </script>
    <script src="/static/threejs/dat.gui.min.js" type="text/javascript">
    </script>
    <script src="/static/threejs/Detector.js" type="text/javascript">
    </script>
    <script src="/static/threejs/OrbitAndPanControls.js" type="text/javascript">
    </script>
    <script type="text/javascript" >
    function getradio(tagname){
    var radios = document.getElementsByName(tagname);
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            // do whatever you want with the checked radio
            return radios[i].value;
            // only one radio can be logically checked, don't check the rest
            break;
          }
       }
    }

    function run_js(){
        var cons = document.getElementById("console")
        var jscode = cons.value
        var t0 = (new Date()).getTime()
        eval(jscode)
        var t1 = (new Date()).getTime()
        console.log("Javascript code run in "+(t1-t0)+" ms")
    }
    </script>
    <script type="text/python3" src="/static/editor.py"></script>

    <script type="text/python3">
    from browser import doc

    overwrite = 0
    # add delete_program 1/7, seven steps to complete the ajax task, the last step is to add delete_program function on server
    # delete1 and delete2 parameters are also added into save_program function.
    delete1 = 0
    delete2 = 0

    def set_debug(ev):
        if ev.target.checked:
            __BRYTHON__.debug = 1
        else:
            __BRYTHON__.debug = 0
            
    def set_overwrite(ev):
        global overwrite
        if ev.target.checked:
            overwrite = 1
        else:
            overwrite = 0

    # add delete_program 2/7, client side add set_delete1 and set_delete2 functions.
    def set_delete1(ev):
        global delete1
        if ev.target.checked:
            delete1 = 1
        else:
            delete1 = 0

    def set_delete2(ev):
        global delete2
        if ev.target.checked:
            delete2 = 1
        else:
            delete2 = 0

    #### ajax process
    from browser import ajax,doc

    def on_complete(req):
        print(req.readyState)
        print('status',req.status)
        if req.status==200 or req.status==0:
            # show request text on id=result division
            doc["result"].html = req.text
        else:
            doc["result"].html = "error "+req.text

    def err_msg():
        doc["result"].html = "server didn't reply after %s seconds" %timeout

    timeout = 4

    def go(url):
        req = ajax.ajax()
        req.bind('complete', on_complete)
        req.set_timeout(timeout, err_msg)
        req.open('GET', url, True)
        req.send()

    def post(url):
        req = ajax.ajax()
        req.bind('complete', on_complete)
        req.set_timeout(timeout, err_msg)
        req.open('POST', url, True)
        req.set_header('content-type','application/x-www-form-urlencoded')
        # doc["filename"].value is the id=filename input field's value
        # editor.getValue() is the content on editor, need to send dictionary format data
        # while post url, need to save editor content into local_storage to use the previous load javascripts
        storage["py_src"] = editor.getValue()
        # add delete_program 3/7, two parameters added, this will also affect save_program function on server.
        req.send({'filename':doc["filename"].value, 'editor':editor.getValue(), 'overwrite':overwrite, 'delete1':delete1, 'delete2':delete2})
        
    # get program from server
    def get_prog(ev):
        # ajax can only read data from server
        _name = '/brython_programs/'+doc["filename"].value
        try:
            editor.setValue(open(_name, encoding="utf-8").read())
            doc["result"].html = doc["filename"].value+" loaded!"
        except:
            doc["result"].html = "can not get "+doc["filename"].value+"!"
        editor.scrollToRow(0)
        editor.gotoLine(0)
        reset_theme()
        
    def get_radio(ev):
        from javascript import JSObject
        filename = JSObject(getradio)("filename")
        # ajax can only read data from server
        doc["filename"].value = filename
        _name = '/brython_programs/'+filename
        editor.setValue(open(_name, encoding="utf-8").read())
        doc["result"].html = filename+" loaded!"
        editor.scrollToRow(0)
        editor.gotoLine(0)
        reset_theme()
        
    # bindings
    doc['run_js'].bind('click',run_js)
    doc['set_debug'].bind('change',set_debug)
    '''
        adm1 = '''
    doc['set_overwrite'].bind('change',set_overwrite)
    # add delete_program 4/7, two associated binds added
    doc['set_delete1'].bind('change',set_delete1)
    doc['set_delete2'].bind('change',set_delete2)
    '''
        part2 = '''
    # next functions are defined in editor.py
    doc['show_js'].bind('click',show_js)
    doc['run'].bind('click',run)
    doc['show_console'].bind('click',show_console)
    # get_prog and get _radio (working)
    doc['get_prog'].bind('click', get_prog)
    doc['get_radio'].bind('click', get_radio)
    # reset_the_src and clear_console (working)
    doc['reset_the_src'].bind('click',reset_the_src)
    doc['clear_console'].bind('click',clear_console)
    # clear_canvas and clear_src
    doc['clear_canvas'].bind('click',clear_canvas)
    doc['clear_src'].bind('click',clear_src)
    # only admin can save program to server
    '''
        adm2 = '''
    doc['save_program'].bind('click',lambda ev:post('save_program'))
    # add delete_program 5/7, delete_program button bind to execute delete_program on server.
    doc['delete_program'].bind('click',lambda ev:post('/delete_program'))
    '''
        # if load program through url
        if filename != None:
            load_program = '''
    _name = '/brython_programs/'''+filename+''''
    try:
        editor.setValue(open(_name, encoding="utf-8").read())
        doc["filename"].value = "'''+filename+'''"
        doc["result"].html = "'''+filename+''' loaded!"
    except:
        doc["result"].html = "can not get '''+filename+'''!"
    editor.scrollToRow(0)
    editor.gotoLine(0)
    reset_theme()
    '''
        else:
            load_program = ""

        part3 = '''
    </script>
    </head>
    <body onload="brython({debug:1, cache:'version'})">
    <table id="banner" cellpadding=0 cellspacing=0>
    <tr id="banner_row">
    <td style="width:80px"></td>
    <td class="alnleft">
    '''
        part4 = '''
    </td>
    <td class="alnleft">
                <button id="reset_the_src">reset the_src</button>
                <button id="clear_src">clear src</button>
                <button id="clear_console">clear console</button>
                <button id="clear_canvas">clear canvas</button>
                <button onclick="TogetherJS(this); return false;">Start TogetherJS</button>
                <br />filename: <input id="filename">
    '''
        adm3 = '''
                <button id="save_program">save program</button>
                overwrite<input type="checkbox" id="set_overwrite">
                <br /><!-- add delete_program button and two double checkboxs 6/7 -->
                <button id="delete_program">delete program</button>
                sure to delete1<input type="checkbox" id="set_delete1">
                sure to delete2<input type="checkbox" id="set_delete2">
    '''
        part5 = '''
                <div id="result">(empty)</div>
                <button id="get_radio">load selected program</button>
                <button onClick="window.location.reload()">reload page</button>
                <button id="get_prog">get prog file</button>
    </td>
    </tr>
    </table>
    <!--
    <div style="text-align:center">
    <br>Brython version: <span id="version"></span>
    </div>
    -->
    <div id="container">
    <div id="left-div">
    <div style="padding: 3px 3px 3px 3px;">
    Theme: <select id="ace_theme">
    <optgroup label="Bright">
    <option value="ace/theme/chrome">Chrome</option>
    <option value="ace/theme/crimson_editor">Crimson Editor</option>
    <option value="ace/theme/eclipse">Eclipse</option>
    <option value="ace/theme/github">GitHub</option>
    </optgroup>
    <optgroup label="Dark">
    <option value="ace/theme/cobalt">Cobalt</option>
    <option value="ace/theme/idle_fingers">idleFingers</option>
    <option value="ace/theme/monokai">Monokai</option>
    <option value="ace/theme/pastel_on_dark">Pastel on dark</option>
    <option value="ace/theme/vibrant_ink">Vibrant Ink</option>
    </optgroup>
    </select> 
    </div>
      <div id="editor"></div>
    </div>

    <div id="right-div">
    <div style="padding: 3px 3px 3px 3px;">
      <div style="float:left">
        <button id="run">run</button>
        <button id="run_js">run Javascript</button>
        debug<input type="checkbox" id="set_debug" checked>
      </div>

      <div style="float:right">
        <button id="show_console">Console</button>
        <button id="show_js">Javascript</button>
      </div>
    </div>
    <div style="width:100%;height:100%;">
    <textarea id="console"></textarea>
    </div>
    </div>

    <div style="float:left;margin-top:50px;">
    <canvas id="plotarea" width="800" height="600"></canvas>
    </div>
    </body>
    </html>
    '''
        if not self.isAdmin():
            return part1+part2+load_program+part3+self.load_list(item_per_page, page, "brython")+part4+part5
        else:
            return part1+adm1+part2+adm2+load_program+part3+self.load_list(item_per_page, page, "brython")+part4+adm3+part5
    #@+node:2014spring.20140508134612.2258: *3* ethercalc
    @cherrypy.expose
    def ethercalc(self, filename=None, *args, **kwargs):
        part1 = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/Brython2.1.0-20140419-113919/brython.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcconstants.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalc-3.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalctableeditor.js"></script>
    <script type="text/javascript" src="/static/socialcalc/formatnumber2.js"></script>
    <script type="text/javascript" src="/static/socialcalc/formula1.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcpopup.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcspreadsheetcontrol.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcviewer.js"></script>
    </head>
    <body onload="brython({debug:1, cache:'version'})">
    <div id="tableeditor" style="margin:8px 0px 10px 0px;">editor goes here</div>
    </div>
    <div id="msg" onclick="this.innerHTML='&nbsp;';"></div>

    <script id="ascript" type="text/python">
    from browser import ajax, doc, alert, websocket
    from javascript import JSConstructor

    spreadsheet =  JSConstructor(SocialCalc.SpreadsheetControl)()
    savestr = ""
    spreadsheet.InitializeSpreadsheetControl("tableeditor")
    spreadsheet.ExecuteCommand('redisplay', '')

    def on_complete(req):
        print(req.readyState)
        print('status',req.status)
        if req.status==200 or req.status==0:
            doc["result"].html = req.text
        else:
            doc["result"].html = "error "+req.text

    def err_msg():
        doc["result"].html = "server didn't reply after %s seconds" %timeout

    timeout = 4

    def go(url):
        req = ajax.ajax()
        req.bind('complete',on_complete)
        req.set_timeout(timeout,err_msg)
        req.open('GET',url,True)
        req.send()

    def post(url):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        req = ajax.ajax()
        req.bind('complete',on_complete)
        req.set_timeout(timeout,err_msg)
        req.open('POST',url,True)
        req.set_header('content-type','application/x-www-form-urlencoded')
        req.send({'filename':doc["filename"].value, 'sheet_content':sheet_content})

    def show_save(ev):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        print(sheet_content)
        
    def doreload(ev):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
        if (parts):
            if (parts.sheet):
                spreadsheet.sheet.ResetSheet()
                spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
            if (parts.edit):
                spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])

        #if (spreadsheet.editor.context.sheetobj.attribs.recalc=="off"):
            #spreadsheet.ExecuteCommand('redisplay', '')
        #else:
        spreadsheet.ExecuteCommand('recalc', '')
        alert("reload done")

    # get program from server
    def get_prog(ev):
        # ajax can only read data from server
        _name = '/calc_programs/'+doc["filename"].value
        try:
            sheet_content = open(_name, encoding="utf-8").read()
            parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
            if (parts):
                if (parts.sheet):
                    spreadsheet.sheet.ResetSheet()
                    spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
                if (parts.edit):
                    spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])
            spreadsheet.ExecuteCommand('recalc', '')
            doc["result"].html = doc["filename"].value+" loaded!"
        except:
            doc["result"].html = "can not get "+doc["filename"].value+"!"

    # for built-in websocket
    def on_open(evt):
        doc['send_button'].disabled = False
        doc['closebtn'].disabled = False
        doc['openbtn'].disabled = True

    def on_message(evt):
        # message reeived from server
        alert("Message received : %s" %evt.data)

    def on_close(evt):
        # websocket is closed
        alert("Connection is closed")
        doc['openbtn'].disabled = False
        doc['closebtn'].disabled = True
        doc['send_button'].disabled = True

    ws = None
    def _open(evt):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        if not __BRYTHON__.has_websocket:
            alert("WebSocket is not supported by your browser")
            return
        global ws
        # open a web socket
        ws = websocket.websocket("wss://localhost:8000")
        # bind functions to web socket events
        ws.bind('open',on_open)
        ws.bind(sheet_content,on_message)
        ws.bind('close',on_close)

    def send(evt):
        data = doc["data"].value
        if data:
            ws.send(data)

    def close_connection(evt):
        ws.close()
        doc['openbtn'].disabled = False

    # bindings
    #doc['timeout'].bind('click',lambda ev:go('/ajax.py'))
    doc['save_program'].bind('click',lambda ev:post('save_calcprogram'))
    doc['get_prog'].bind('click', get_prog)
    doc['show_save'].bind('click', show_save)
    doc['doreload'].bind('click', doreload)
    doc['openbtn'].bind('click', _open)
    '''
        # if load program through url
        if filename != None:
            load_program = '''
    # ajax can only read data from server
    _name = '/calc_programs/'''+filename+''''
    try:
        sheet_content = open(_name, encoding="utf-8").read()
        parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
        if (parts):
            if (parts.sheet):
                spreadsheet.sheet.ResetSheet()
                spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
            if (parts.edit):
                spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])
        spreadsheet.ExecuteCommand('recalc', '')
        doc["filename"].value = "'''+filename+'''"
        doc["result"].html = "'''+filename+''' loaded!"
    except:
        doc["result"].html = "can not get '''+filename+'''!"
    '''
        else:
            load_program = ""

        part2 = '''
    </script>
    <button id="show_save">顯示內容</button>
    <button id="doreload">do reload</button>
    <button onClick=exec_command();>exec command</button>
    <button id="save_program";>save program</button>
    filename: <input id="filename">
    <button id="get_prog">get prog file</button><br />
    <div id="result">(empty)</div><br />
    <button id="openbtn">Open connection</button> 
    <input id="data">
    <button id="send_button" disabled onclick="send()">Send</button>
    <button id="closebtn" disabled onclick="close_connection()">Close connection</button>
    </body>
    </html>
    '''
        return part1+load_program+part2

    #@+node:2014spring.20140508134612.2259: *3* calc
    @cherrypy.expose
    def calc(self, item_per_page=5, page=1, keyword=None, filename=None, *args, **kwargs):
        part1 = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/Brython2.1.0-20140419-113919/brython.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcconstants.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalc-3.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalctableeditor.js"></script>
    <script type="text/javascript" src="/static/socialcalc/formatnumber2.js"></script>
    <script type="text/javascript" src="/static/socialcalc/formula1.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcpopup.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcspreadsheetcontrol.js"></script>
    <script type="text/javascript" src="/static/socialcalc/socialcalcviewer.js"></script>
    <script type="text/javascript">
    function getradio(tagname){
    var radios = document.getElementsByName(tagname);
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            // do whatever you want with the checked radio
            return radios[i].value;
            // only one radio can be logically checked, don't check the rest
            break;
          }
       }
    }
    </script>
    </head>
    <body onload="brython({debug:1, cache:'version'})">
    <div id="tableeditor" style="margin:8px 0px 10px 0px;">editor goes here</div>
    <div id="msg" onclick="this.innerHTML='&nbsp;';"></div>

    <script id="ascript" type="text/python">
    from browser import ajax, doc, alert, websocket
    from javascript import JSConstructor

    spreadsheet =  JSConstructor(SocialCalc.SpreadsheetControl)()
    savestr = ""
    spreadsheet.InitializeSpreadsheetControl("tableeditor")
    spreadsheet.ExecuteCommand('redisplay', '')

    overwrite = 0
    # add delete_program 1/7, seven steps to complete the ajax task, the last step is to add delete_program function on server
    # delete1 and delete2 parameters are also added into save_program function.
    delete1 = 0
    delete2 = 0

    def set_overwrite(ev):
        global overwrite
        if ev.target.checked:
            overwrite = 1
        else:
            overwrite = 0

    # add delete_program 2/7, client side add set_delete1 and set_delete2 functions.
    def set_delete1(ev):
        global delete1
        if ev.target.checked:
            delete1 = 1
        else:
            delete1 = 0

    def set_delete2(ev):
        global delete2
        if ev.target.checked:
            delete2 = 1
        else:
            delete2 = 0

    def on_complete(req):
        print(req.readyState)
        print('status',req.status)
        if req.status==200 or req.status==0:
            doc["result"].html = req.text
        else:
            doc["result"].html = "error "+req.text

    def err_msg():
        doc["result"].html = "server didn't reply after %s seconds" %timeout

    timeout = 4

    def go(url):
        req = ajax.ajax()
        req.bind('complete',on_complete)
        req.set_timeout(timeout,err_msg)
        req.open('GET',url,True)
        req.send()

    def post(url):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        req = ajax.ajax()
        req.bind('complete',on_complete)
        req.set_timeout(timeout,err_msg)
        req.open('POST',url,True)
        req.set_header('content-type','application/x-www-form-urlencoded')
        # add delete_program 3/7, two parameters added, this will also affect save_program function on server.
        req.send({'filename':doc["filename"].value, 'sheet_content':sheet_content, 'overwrite':overwrite, 'delete1':delete1, 'delete2':delete2})

    def show_save(ev):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        print(sheet_content)
        
    def doreload(ev):
        global spreadsheet
        sheet_content = spreadsheet.CreateSpreadsheetSave()
        parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
        if (parts):
            if (parts.sheet):
                spreadsheet.sheet.ResetSheet()
                spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
            if (parts.edit):
                spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])

        #if (spreadsheet.editor.context.sheetobj.attribs.recalc=="off"):
            #spreadsheet.ExecuteCommand('redisplay', '')
        #else:
        spreadsheet.ExecuteCommand('recalc', '')
        alert("reload done")

    # get program from server
    def get_prog(ev):
        # ajax can only read data from server
        _name = '/calc_programs/'+doc["filename"].value
        try:
            sheet_content = open(_name, encoding="utf-8").read()
            parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
            if (parts):
                if (parts.sheet):
                    spreadsheet.sheet.ResetSheet()
                    spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
                if (parts.edit):
                    spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])
            spreadsheet.ExecuteCommand('recalc', '')
            doc["result"].html = doc["filename"].value+" loaded!"
        except:
            doc["result"].html = "can not get "+doc["filename"].value+"!"

    def get_radio(ev):
        from javascript import JSObject
        filename = JSObject(getradio)("filename")
        # ajax can only read data from server
        doc["filename"].value = filename
        _name = '/calc_programs/'+filename
        try:
            sheet_content = open(_name, encoding="utf-8").read()
            parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
            if (parts):
                if (parts.sheet):
                    spreadsheet.sheet.ResetSheet()
                    spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
                if (parts.edit):
                    spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])
            spreadsheet.ExecuteCommand('recalc', '')
            doc["result"].html = doc["filename"].value+" loaded!"
        except:
            doc["result"].html = "can not get "+doc["filename"].value+"!"

    # bindings
    doc['get_prog'].bind('click', get_prog)
    doc['get_radio'].bind('click', get_radio)
    doc['doreload'].bind('click', doreload)
    '''
        adm1 = '''
    doc['save_program'].bind('click',lambda ev:post('save_calcprogram'))
    # add delete_program 5/7, delete_program button bind to execute delete_program on server.
    doc['delete_program'].bind('click',lambda ev:post('/delete_calcprogram'))
    doc['show_save'].bind('click', show_save)
    doc['set_overwrite'].bind('change',set_overwrite)
    # add delete_program 4/7, two associated binds added
    doc['set_delete1'].bind('change',set_delete1)
    doc['set_delete2'].bind('change',set_delete2)
    '''
        # if load program through url
        if filename != None:
            load_program = '''
    # ajax can only read data from server
    _name = '/calc_programs/'''+filename+''''
    try:
        sheet_content = open(_name, encoding="utf-8").read()
        parts = spreadsheet.DecodeSpreadsheetSave(sheet_content)
        if (parts):
            if (parts.sheet):
                spreadsheet.sheet.ResetSheet()
                spreadsheet.ParseSheetSave(sheet_content[parts.sheet.start:parts.sheet.end])
            if (parts.edit):
                spreadsheet.editor.LoadEditorSettings(sheet_content[parts.edit.start:parts.edit.end])
        spreadsheet.ExecuteCommand('recalc', '')
        doc["filename"].value = "'''+filename+'''"
        doc["result"].html = "'''+filename+''' loaded!"
    except:
        doc["result"].html = "can not get '''+filename+'''!"
    '''
        else:
            load_program = ""

        part2 = '''
    </script>
    filename: <input id="filename">
    <button id="get_prog">get prog file</button><br />
    <div id="result">(empty)</div><br />
    <button id="doreload">do reload</button>
    <button id="get_radio">load selected program</button><br />
    '''
        adm2 = '''
    <button id="show_save">顯示內容</button>
    <button id="save_program";>save program</button>
    overwrite<input type="checkbox" id="set_overwrite">
    <br /><!-- add delete_program button and two double checkboxs 6/7 -->
    <button id="delete_program">delete program</button>
    sure to delete1<input type="checkbox" id="set_delete1">
    sure to delete2<input type="checkbox" id="set_delete2"><br />
    '''
        part3 = '''
    </body>
    </html>
    '''
        # only admin can view and edit calc, we still need to find a way to protect programs on calc_programs
        if not self.isAdmin():
            raise cherrypy.HTTPRedirect("login")
            # for not admin
            #return part1+load_program+part2+self.load_list(item_per_page, page, "calc")+part3
        else:
            # for admin
            return part1+adm1+load_program+part2+adm2+self.load_list(item_per_page, page, "calc")+part3

    #@+node:2014spring.20140508134612.2260: *3* openjscad
    @cherrypy.expose
    def openjscad(self, *args, **kwargs):
        return '''
    <!DOCTYPE html>
    <html><head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
    <title>OpenJSCAD.org</title>
    <link rel="stylesheet" href="/jquery/themes/base/jquery-ui.css" />
    <script src="/jquery/jquery-1.9.1.js"></script>
    <script src="/jquery/jquery-ui.js"></script>
    <script src="/jquery/jquery.hammer.js"></script>
    <link rel="stylesheet" href="/style.css" type="text/css">
    <link rel="stylesheet" href="/openjscad.css" type="text/css">
    </head>
    <body onload="onload()">
    <style>
    /* we choose chrome theme for ace, and make sure line number is transparent too */
    /* this has to stay in the body (not head) otherwise does not take effect */
    .ace-chrome .ace_gutter { 
       border-left: 2px dashed rgba(200,200,200,0.2);
       background: none;
    }
    .ace-chrome {
       font-size: 10pt;     // -- not 'px', but 'pt' for high dpi screens
    }
    </style>
    <script src="/lightgl.js"></script>
    <script src="/csg.js"></script>
    <script src="/openjscad.js"></script>
    <script src="/openscad.js"></script>
    <script src="/underscore.js"></script>
    <script src="/openscad-openjscad-translator.js"></script>
    <script lang=JavaScript>
    var version = '0.017 (2014/02/14)';
    var me = document.location.toString().match(/^file:/)?'web-offline':'web-online'; // me: {cli, web-offline, web-online}
    var browser = 'unknown';
    if(navigator.userAgent.match(/(opera|chrome|safari|firefox|msie)/i))
       browser = RegExp.$1.toLowerCase();

    $(document).ready(function() {
       $("#viewer").height($(window).height());

       $(window).resize(function() {                // adjust the relevant divs
          $("#viewer").width($(window).width());
          $("#viewer").height($(window).height());
       });


    });   
    </script>
    <div id="editor">// -- OpenJSCAD.org logo
    function main(params)
    {
      // Main entry point; here we construct our solid: 
      var gear = involuteGear(
        params.numTeeth,
        params.circularPitch,
        params.pressureAngle,
        params.clearance,
        params.thickness
      );
      if(params.centerholeradius > 0)
      {
        var centerhole = CSG.cylinder({start: [0,0,-params.thickness], end: [0,0,params.thickness], radius: params.centerholeradius, resolution: 16});
        gear = gear.subtract(centerhole);
      }
      return gear;
    }

    // Here we define the user editable parameters: 
    function getParameterDefinitions() {
      return [
        { name: 'numTeeth', caption: 'Number of teeth:', type: 'int', default: 15 },
        { name: 'circularPitch', caption: 'Circular pitch:', type: 'float', default: 10 },
        { name: 'pressureAngle', caption: 'Pressure angle:', type: 'float', default: 20 },
        { name: 'clearance', caption: 'Clearance:', type: 'float', default: 0 },
        { name: 'thickness', caption: 'Thickness:', type: 'float', default: 5 },
        { name: 'centerholeradius', caption: 'Radius of center hole (0 for no hole):', type: 'float', default: 2 },
      ];
    }

    /*
      For gear terminology see: 
        http://www.astronomiainumbria.org/advanced_internet_files/meccanica/easyweb.easynet.co.uk/_chrish/geardata.htm
      Algorithm based on:
        http://www.cartertools.com/involute.html

      circularPitch: The distance between adjacent teeth measured at the pitch circle
    */ 
    function involuteGear(numTeeth, circularPitch, pressureAngle, clearance, thickness)
    {
      // default values:
      if(arguments.length < 3) pressureAngle = 20;
      if(arguments.length < 4) clearance = 0;
      if(arguments.length < 4) thickness = 1;
      
      var addendum = circularPitch / Math.PI;
      var dedendum = addendum + clearance;
      
      // radiuses of the 4 circles:
      var pitchRadius = numTeeth * circularPitch / (2 * Math.PI);
      var baseRadius = pitchRadius * Math.cos(Math.PI * pressureAngle / 180);
      var outerRadius = pitchRadius + addendum;
      var rootRadius = pitchRadius - dedendum;

      var maxtanlength = Math.sqrt(outerRadius*outerRadius - baseRadius*baseRadius);
      var maxangle = maxtanlength / baseRadius;

      var tl_at_pitchcircle = Math.sqrt(pitchRadius*pitchRadius - baseRadius*baseRadius);
      var angle_at_pitchcircle = tl_at_pitchcircle / baseRadius;
      var diffangle = angle_at_pitchcircle - Math.atan(angle_at_pitchcircle);
      var angularToothWidthAtBase = Math.PI / numTeeth + 2*diffangle;

      // build a single 2d tooth in the 'points' array:
      var resolution = 5;
      var points = [new CSG.Vector2D(0,0)];
      for(var i = 0; i <= resolution; i++)
      {
        // first side of the tooth:
        var angle = maxangle * i / resolution;
        var tanlength = angle * baseRadius;
        var radvector = CSG.Vector2D.fromAngle(angle);    
        var tanvector = radvector.normal();
        var p = radvector.times(baseRadius).plus(tanvector.times(tanlength));
        points[i+1] = p;
        
        // opposite side of the tooth:
        radvector = CSG.Vector2D.fromAngle(angularToothWidthAtBase - angle);    
        tanvector = radvector.normal().negated();
        p = radvector.times(baseRadius).plus(tanvector.times(tanlength));
        points[2 * resolution + 2 - i] = p;
      }

      // create the polygon and extrude into 3D:
      var tooth3d = new CSG.Polygon2D(points).extrude({offset: [0, 0, thickness]});

      var allteeth = new CSG();
      for(var i = 0; i < numTeeth; i++)
      {
        var angle = i*360/numTeeth;
        var rotatedtooth = tooth3d.rotateZ(angle);
        allteeth = allteeth.unionForNonIntersecting(rotatedtooth);
      }

      // build the root circle:  
      points = [];
      var toothAngle = 2 * Math.PI / numTeeth;
      var toothCenterAngle = 0.5 * angularToothWidthAtBase; 
      for(var i = 0; i < numTeeth; i++)
      {
        var angle = toothCenterAngle + i * toothAngle;
        var p = CSG.Vector2D.fromAngle(angle).times(rootRadius);
        points.push(p);
      }

      // create the polygon and extrude into 3D:
      var rootcircle = new CSG.Polygon2D(points).extrude({offset: [0, 0, thickness]});

      var result = rootcircle.union(allteeth);

      // center at origin:
      result = result.translate([0, 0, -thickness/2]);

      return result;
    }
    </div>

    <div oncontextmenu="return false;" id="viewer"></div> <!-- avoiding popup when right mouse is clicked -->

    <div id="parametersdiv"></div>
    <div id="tail">
    <div id="statusdiv"></div>
    <div id="errordiv"></div>
    </div>
    <!--<script src="/ace/ace.js" type="text/javascript" charset="utf-8"></script>-->
    <script src="https://d1n0x3qji82z53.cloudfront.net/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
    <script>
    var gProcessor = null;
    var editor = null;
    var _includePath = "/";

    function onload() {
       // -- http://ace.ajax.org/#nav=howto
       editor = ace.edit("editor");
       editor.setTheme("ace/theme/chrome");
       //document.getElementById('ace_gutter').style.background = 'none';
       editor.getSession().setMode("ace/mode/javascript");
       editor.getSession().on('change', function(e) {});               
       ['Shift-Return'].forEach(function(key) {
          editor.commands.addCommand({
             name: 'myCommand',
             bindKey: { win: key, mac: key },
             exec: function(editor) {
                var src = editor.getValue();
                if(src.match(/^\/\/\!OpenSCAD/i)) {
                   editor.getSession().setMode("ace/mode/scad");
                   src = openscadOpenJscadParser.parse(src);
                } else {
                   editor.getSession().setMode("ace/mode/javascript");
                }
                gMemFs = [];
                gProcessor.setJsCad(src);
             },
          });
       });
       
       gProcessor = new OpenJsCad.Processor(document.getElementById("viewer"));

       //gProcessor.setDebugging(debugging); 
       if(me=='web-online') {    // we are online, fetch first example
          gProcessor.setJsCad(editor.getValue());
       }
    }

    // Show all exceptions to the user:
    OpenJsCad.AlertUserOfUncaughtExceptions();
    </script>
    </body></html> 
    '''
    #@+node:2014spring.20140508134612.2261: *3* ucrobot
    @cherrypy.expose
    def ucrobot(self):
        return '''
    <html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            </head>
    	<body style="overflow:auto; margin:0; padding:0;position:relative">
    		<div id="container" onclick="this.focus();"></div>
    		<div id="grading"></div>
    <script type="text/javascript" src="/static/threejs/Detector.js"></script>
    		<script type="text/javascript">
    		if ( ! Detector.webgl ) { 
    				Detector.addGetWebGLMessage();
    		}
    		</script>
    		<script type="text/javascript" src="/static/threejs/three.min.js"></script>
              <script type="text/javascript" src="/static/threejs/Coordinates.js"></script>
    		<script type="text/javascript" src="/static/threejs/OrbitAndPanControls.js"></script>
    		<script type="text/javascript" src="/static/threejs/dat.gui.min.js"></script>
    		<script type="text/javascript" src="/static/threejs/demo.js"></script>

    </body></html>
    '''
    #@-others
#@+node:2014spring.20140508134612.2262: ** class Download
class Download:
    #@+others
    #@+node:2014spring.20140508134612.2263: *3* index
    @cherrypy.expose
    def index(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")
    #@-others
#@-others

root = CMSimply()
root.download = Download()


# setup static, images and downloads directories
application_conf = {
        '/static':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': _curdir+"/static"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/brython_programs':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/brython_programs"},
        '/calc_programs':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/calc_programs"},
        '/':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': _curdir+"/static/openjscad"}
    }

# if inOpenshift ('OPENSHIFT_REPO_DIR' exists in environment variables) or not inOpenshift
if __name__ == '__main__':
    if inOpenshift:
        # operate in OpenShift
        application = cherrypy.Application(root, config = application_conf)
    else:
        # operate in localhost
        cherrypy.quickstart(root, config = application_conf)
#@-leo
