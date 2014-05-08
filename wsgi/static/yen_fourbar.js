// Yen fourbar javascript
// Point function object, use JSConstructor to convert into Brython object
// under Brython, point = JSConstructor(Point) to convert Javascript's Point into Brython's point object
var Point = function Point(x,y){
    this.x=x;
    this.y=y;
}
// 附加 drawMe() 方法, 以繪製出點位置
Point.prototype.drawMe = function drawMe(g,r){
    this.g = g;
    this.r = r;
    this.g.save();
    this.g.moveTo(this.x,this.y);
    this.g.beginPath();
    // draw a radius=4 circle
    this.g.arc(this.x, this.y, this.r, 0, 2 * Math.PI, true);
    this.g.moveTo(this.x,this.y);
    this.g.lineTo(this.x+this.r, this.y);
    this.g.moveTo(this.x, this.y);
    this.g.lineTo(this.x-this.r, this.y);
    this.g.moveTo(this.x, this.y);
    this.g.lineTo(this.x, this.y+this.r);
    this.g.moveTo(this.x, this.y);
    this.g.lineTo(this.x, this.y-this.r);
    this.g.restore();
    this.g.stroke();
}
// 加入 Eq 方法
Point.prototype.Eq = function Eq(pt){
    this.x = pt.x;
    this.y = pt.y;
}
// 加入 setPoint 方法
Point.prototype.setPoint = function setPoint(px,py){
    this.x = px;
    this.y = py;
}
// 加上 distance(pt) 方法, 計算點到 pt 的距離
Point.prototype.distance = function distance(pt){
    this.pt = pt;
    return Math.sqrt(Math.pow(this.x-this.pt.x,2)+Math.pow(this.y-this.pt.y,2));
}
// Line 函式物件
// Line function object, use JSConstructor to convert into Brython object
// under Brython, line = JSConstructor(Line) to convert Javascript's Line into Brython's line object
var Line = function Line(p1,p2){
    this.p1 = p1;
    this.p2 = p2;
    this.Tail = this.p1;
    this.Head = this.p2;
    this.length = Math.sqrt(Math.pow(this.p2.x-this.p1.x, 2)+Math.pow(this.p2.y-this.p1.y,2));
}
// setPP 方法 for Line
Line.prototype.setPP = function setPP(p1,p2){
    this.p1 = p1;
    this.p2 = p2;
    this.Tail = this.p1;
    this.Head = this.p2;
    this.length = Math.sqrt(Math.pow(this.p2.x-this.p1.x, 2)+Math.pow(this.p2.y-this.p1.y,2));
}
// setRT 方法 for Line, 應該已經確定 Tail 點, 然後以 r, t 作為設定 Head 的參考
Line.prototype.setRT = function setRT(r,t){
    this.r = r;
    this.t = t;
    var x = this.r * Math.cos(this.t);
    var y = this.r * Math.sin(this.t);
    this.Tail.Eq(this.p1);
    this.Head.setPoint(this.Tail.x + x,this.Tail.y + y);
}
// getR 方法 for Line
Line.prototype.getR = function getR(){
    // x 分量與 y 分量
    var x = this.p1.x - this.p2.x;
    var y = this.p1.y - this.p2.y;
    return Math.sqrt(x * x + y * y);
}
// 根據定義 atan2(y,x), 表示 (x,y) 與 正 x 軸之間的夾角, 介於 PI 與 -PI 間
Line.prototype.getT = function getT(){
    var x = this.p2.x - this.p1.x;
    var y = this.p2.y - this.p1.y;
    if (Math.abs(x) < 1E-100) {
        return y < 0.0 ? -Math.PI/2 : Math.PI/2;
    }else{
        return Math.atan2(y, x);
    }
}
// setTail 方法 for Line
Line.prototype.setTail = function setTail(pt){
    this.pt = pt;
    this.Tail.Eq(pt);
    this.Head.setPoint(this.pt.x + this.x, this.pt.y + this.y);
}
// getHead 方法 for Line
Line.prototype.getHead = function getHead(){
    return this.Head;
}
Line.prototype.getTail = function getTail(){
    return this.Tail;
}
Line.prototype.drawMe = function drawMe(g){
    this.g = g;
    this.g.beginPath();
    this.g.moveTo(this.p1.x,this.p1.y);
    this.g.lineTo(this.p2.x,this.p2.y);
    this.g.stroke();
}
// 轉換函式
// we only call this function in Javascript
function degToRad(x) {
    return x / 180 * Math.PI;
}
// we only call this function in Javascript
function radToDeg(x) {
    return x / Math.PI * 180;
}
//
// 建立一個物件繼承函式
// We need a utility function to do the inheritance
function inherit(superClass, subClass) {
    for(var i in superClass.prototype) {
        subClass.prototype[i] = superClass.prototype[i]
    }
}
// 建立 Link function 物件
// Link function object, use JSConstructor to convert into Brython object
// under Brython, link = JSConstructor(Link) to convert Javascript's Link into Brython's link object
var Link = function Link(p1,p2){
    this.p1 = p1;
    this.p2 = p2;
    this.length = Math.sqrt(Math.pow(this.p2.x-this.p1.x, 2)+Math.pow(this.p2.y-this.p1.y,2));
}
// 讓 Link 繼承 Line 的方法與屬性
inherit(Line,Link);
//
// 建立 Link 特有的 drawMe 方法
Link.prototype.drawMe = function drawMe(g){
    this.g = g;
    var hole = 5;
    var radius = 10;
    var length = this.getR();
    // 儲存先前的繪圖狀態
    this.g.save();
    this.g.translate(this.p1.x,this.p1.y);
    // 這裡的轉角必須配合最初的 Link 是畫在 x 軸上或是 y 軸上來進行座標轉換, 目前是以畫在 y 軸上進行座標軸旋轉, 並且確定 Math.atan2(y,x)
    // 以下 alert 用來 debug
    //alert("角度為"+ radToDeg(this.getT()));
    //alert("座標軸轉角為"+radToDeg(-(Math.PI/2-this.getT())));
    this.g.rotate(-(Math.PI/2-this.getT()));
    // 必須配合畫在 y 軸上的 Link, 進行座標轉換, 也可以改為畫在 x 軸上...
    this.g.moveTo(0,0);
    this.g.beginPath();
    this.g.arc(0, 0, hole, 0, 2*Math.PI, true);
    this.g.stroke();
    //
    this.g.moveTo(0,length);
    this.g.beginPath();
    this.g.arc(0,length, hole, 0, 2*Math.PI, true);
    this.g.stroke();
    //
    this.g.moveTo(0,0);
    this.g.beginPath();
    this.g.arc(0,0, radius, 0, Math.PI, true);
    this.g.moveTo(0+radius,0);
    this.g.lineTo(0+radius,0+length);
    this.g.stroke();
    this.g.moveTo(0,0+length);
    //
    this.g.beginPath();
    this.g.arc(0, 0+length, radius, Math.PI, 0, true);
    this.g.moveTo(0-radius,0+length);
    this.g.lineTo(0-radius,0);
    this.g.stroke();
    //
    this.g.restore();
}
//
// ap1 角為 p1 點所在的角度, lenp1 長度則為 ap1 角度對應的邊長
// ap2 角為 p2 點所在的角度, lenp2 長度則為 ap2 角度對應的邊長
// ap3 角為 p3 點所在的角度, lenp3 長度則為 ap3 角度對應的邊長
// Triangle function object, use JSConstructor to convert into Brython object
// under Brython, triangle = JSConstructor(Triangle) to convert Javascript's Triangle into Brython's triangle object
var Triangle = function Triangle(p1,p2,p3){
    // 先將輸入變數轉為函式物件性質
    this.p1 = p1;
    this.p2 = p2;
    this.p3 = p3;
}
//
Triangle.prototype.getLenp3 = function getLenp3(){
    var p1 = this.p1;
    var ret = p1.distance(this.p2);
    return ret;
}
//
Triangle.prototype.getLenp1 = function getLenp1(){
    var p2 = this.p2;
    var ret = p2.distance(this.p3);
    return ret;
}
//
Triangle.prototype.getLenp2 = function getLenp2(){
    var p1 = this.p1;
    var ret = p1.distance(this.p3);
    return ret;
}
    
// 角度
Triangle.prototype.getAp1 = function getAp1(){
    var ret = Math.acos(((this.getLenp2() * this.getLenp2() + this.getLenp3() * this.getLenp3()) - this.getLenp1() * this.getLenp1()) / (2* this.getLenp2() * this.getLenp3()));
    return ret;
}
//
Triangle.prototype.getAp2 = function getAp2(){
    var ret =Math.acos(((this.getLenp1() * this.getLenp1() + this.getLenp3() * this.getLenp3()) - this.getLenp2() * this.getLenp2()) / (2* this.getLenp1() * this.getLenp3()));
    return ret;
}
//
Triangle.prototype.getAp3 = function getAp3(){
    var ret = Math.acos(((this.getLenp1() * this.getLenp1() + this.getLenp2() * this.getLenp2()) - this.getLenp3() * this.getLenp3()) / (2* this.getLenp1() * this.getLenp2()));
    return ret;
}
//
Triangle.prototype.drawMe = function drawMe(g){
    this.g = g;
    var r = 5;
    // 繪出三個頂點
    this.p1.drawMe(this.g,r);
    this.p2.drawMe(this.g,r);
    this.p3.drawMe(this.g,r);
    var line1 = new Line(this.p1,this.p2);
    var line2 = new Line(this.p1,this.p3);
    var line3 = new Line(this.p2,this.p3);
    // 繪出三邊線
    line1.drawMe(this.g);
    line2.drawMe(this.g);
    line3.drawMe(this.g);
}
// ends Triangle function
// 透過三個邊長定義三角形
Triangle.prototype.setSSS = function setSSS(lenp3,lenp1,lenp2){
    this.lenp3 = lenp3;
    this.lenp1 = lenp1;
    this.lenp2 = lenp2;
    this.ap1 = Math.acos(((this.lenp2 * this.lenp2 + this.lenp3 * this.lenp3) - this.lenp1 * this.lenp1) / (2* this.lenp2 * this.lenp3));
    this.ap2 = Math.acos(((this.lenp1 * this.lenp1 + this.lenp3 * this.lenp3) - this.lenp2 * this.lenp2) / (2* this.lenp1 * this.lenp3));
    this.ap3 = Math.acos(((this.lenp1 * this.lenp1 + this.lenp2 * this.lenp2) - this.lenp3 * this.lenp3) / (2* this.lenp1 * this.lenp2));
}
// ends setSSS
// 透過兩個邊長與夾角定義三角形
Triangle.prototype.setSAS = function setSAS(lenp3,ap2,lenp1){
    this.lenp3 = lenp3;
    this.ap2 = ap2;
    this.lenp1 = lenp1;
    this.lenp2 = Math.sqrt((this.lenp3 * this.lenp3 + this.lenp1 * this.lenp1) - 2* this.lenp3 * this.lenp1 * Math.cos(this.ap2));
    //等於 SSS(AB, BC, CA);
}
// ends setSAS
//
Triangle.prototype.setSaSS = function setSaSS(lenp2,lenp3,lenp1){
    this.lenp2 = lenp2;
    this.lenp3 = lenp3;
    this.lenp1 = lenp1;
    var ret;
    if(this.lenp1 > (this.lenp2 + this.lenp3)){
    // <CAB 夾角為 180 度, 三點共線且 A 介於 BC 之間
        ret = Math.PI;
    } else {
        // <CAB 夾角為 0, 三點共線且 A 不在 BC 之間
        if((this.lenp1 < (this.lenp2 - this.lenp3)) || (this.lenp1 < (this.lenp3 - this.lenp2))){
        ret = 0.0;
        } else {
        // 透過餘絃定理求出夾角 <CAB 
            ret = Math.acos(((this.lenp2 * this.lenp2 + this.lenp3 * this.lenp3) - this.lenp1 * this.lenp1) / (2 * this.lenp2 * this.lenp3));
        }
    }
    return ret;
}
// 取得三角形的三個邊長值
Triangle.prototype.getSSS = function getSSS(){
    var temp = new Array(2);
    temp[0] = this.getLenp1();
    temp[1] = this.getLenp2();
    temp[2] = this.getLenp3();
    return temp;
}
// 取得三角形的三個角度值
Triangle.prototype.getAAA = function getAAA(){
    var temp = new Array(2);
    temp[0] = this.getAp1();
    temp[1] = this.getAp2();
    temp[2] = this.getAp3();
    return temp;
}
// 取得三角形的三個角度與三個邊長
Triangle.prototype.getASASAS = function getASASAS(){
    var temp = new Array(5);
    temp[0] = this.getAp1();
    temp[1] = this.getLenp1();
    temp[2] = this.getAp2();
    temp[3] = this.getLenp2();
    temp[4] = this.getAp3();
    temp[5] = this.getLenp3();
    return temp;
}
Triangle.prototype.setPPSS = function setPPSS(p1,p3,lenp1,lenp3){
var temp = new Array(1);
this.p1 = p1;
this.p3 = p3;
this.lenp1 = lenp1;
this.lenp3 = lenp3;
this.lenp2 = this.p1.distance(this.p3);
// bp3 is the angle beside p3 point, cp3 is the angle for line23, p2 is the output
var ap3,bp3,cp3,p2;
var line31 = new Line(p3,p1);
ap3 = Math.acos(((this.lenp1 * this.lenp1 + this.lenp2 * this.lenp2) - this.lenp3 * this.lenp3) / (2 * this.lenp1 * this.lenp2));
bp3 = line31.getT();
cp3 = bp3 - ap3;
temp[0] = p3.x + this.lenp1*Math.cos(cp3); // p2.x
temp[1] = p3.y + this.lenp1*Math.sin(cp3); // p2.y
return temp;
}
