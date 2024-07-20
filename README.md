# website-Bulletin-board
# 一、說明
本專題在 Python 中使用 Django 建立出 web 專案製作出網站留言板，可以訪客留言及觀看，管理者登入後可修改留言內容及刪除留言，也可以對訪客留言的人做回應，對開發者是最方便的簡單的互動留言網站。
# 二、相關文章
網站留言板：又稱為電腦網站公佈欄，是一個允許用戶在網站上發表評論、提問或分享意見的區域。它常用於社交互動、客戶服務、產品反饋以及建立社區等目的。以下是一些相關文章的主題和簡要介紹。
1.	留言板的功能：讓用戶發表評論、提問或分享意見，通常包括留言發佈、回覆、編輯、刪除等功能。
2.	技術實現：使用Django架設網站，後端使用MySQL或SQLServer資料庫。
3.	其他：適用於企業內部留言或公告，也可作為私人筆記板，並具有良好的安全性。
網站留言板流程圖：
![螢幕擷取畫面 (73)](https://github.com/LonelyCaesar/website-Bulletin-board/assets/101235367/5f5d777f-6df3-4106-8014-4a5b7d4056c0)

# 三、實作
請在anaconda/VScode的終端機上執行django-simple-captcha模組後，建立下圖上的資料夾，然後切換到cd board0專案後實作，專案以「python manage.py runserver」啟動伺服器。

### 執行套件
```
pip install django
django-admin startproject board0
python manage.py startapp accounts #自己的帳號、密碼權限
python manage.py makemigrations
python manage.py migrate
```
### 1.	網站留言板資料庫結構：
資料庫結構定義在boardapp\models.py中，內含BoardUnit資料表。
### boardapp\models.py程式碼：
```python
from django.db import models

class BoardUnit(models.Model):
    bname = models.CharField(max_length=20, null=False)
    bgender = models.CharField(max_length=2, default='m', null=False)
    bsubject = models.CharField(max_length=100, null=False)
    btime = models.DateTimeField(auto_now=True)
    bmail = models.EmailField(max_length=100, blank=True, default='')
    bweb = models.CharField(max_length=200, blank=True, default='')
    bcontent = models.TextField(null=False)
    bresponse = models.TextField(blank=True, default='')

    def __str__(self):
        return self.bsubject
```
### 2.	settings.py加入captcha：
使用圖形驗證碼，在board0\settings.py檔的INSTALLED_APPS項目加入captcha。
### board0\settings.py程式碼：
```
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'boardapp',
    'captcha',
]

CAPTCHA_NOISE_FUNCTIONS = (
     'captcha.helpers.noise_null', #没有樣式  
)
```
### 3.	URL配置檔：
### board\urls.py程式碼：
```python
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from boardapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('index/<str:pageindex>/', views.index),
    path('post/', views.post),
    path('login/', views.login),
    path('logout/', views.logout),
    path('adminmain/', views.adminmain),
    path('adminmain/<str:pageindex>/', views.adminmain),
    path('delete/<int:boardid>/', views.delete),
    path('delete/<int:boardid>/<str:deletetype>/', views.delete),
    path('captcha/', include('captcha.urls')),
]
```
### 4.	建立網頁模板：
先在templates\建立<index.html>、<post.html>和<login.html>，然後在templates\base.html建立網頁模板，含標題、右上方瀏覽留言功能鈕及下方的版權部分。
### templates\base.html程式碼：
```html
{% extends "base.html" %}
{% load static %}

{% block title %}<title>網站留言版</title>{% endblock %}

{% block twomenu %}
	<img src="{% static "images/comment.png" %}" width="16" height="16" align="absmiddle" /> <a href="/post/">我要留言</a> 
	<img src="{% static "images/key.png" %}" width="16" height="16" align="absmiddle" /> <a href="/login/">版主管理</a>
{% endblock %}

{% block content %}
	 </td>
  </tr>
  {% for unit in boardunits %}
	<tr>
	  <td background="{% static "images/g_r3_c3.png" %}">
		  <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" background="{% static "images/g_r5_c4.png" %}"
			<tr>
			  <td valign="top" style="background:url"({% static "images/g_r4_c4.png" %}); background-repeat:no-repeat">
				<div class="floorDiv">
					{% if unit.bgender == "m" %}
						<img src="{% static "images/boy.png" %}" width="52" height="80" />
					{% else %}
						<img src="{% static "images/girl.png" %}" width="52" height="80" />
					{% endif %}
				</div>
				<div class="contentDiv">
				  <p class="title">{{unit.bsubject}}</p>
				  <p></p>
				  <p>{{unit.bcontent}}</p>
				  {% if unit.bresponse != "" %}
					<div class="responseDiv">
					  <p><strong>版主回應</strong>：{{unit.bresponse}}</p>
					</div>
				  {% endif %}
				  <p class="editor"><img src="{% static "images/user.png" %}" width="16" height="16" align="absmiddle">{{unit.bname}}&nbsp; 
					<img src="{% static "images/date.png" %}" width="16" height="16" align="absmiddle">{{unit.btime}}&nbsp;
					{% if unit.bmail != "" %}
					  <a href="mailto:{{unit.bmail}}" target="_blank">
					  <img src="{% static "images/email.png" %}" width="16" height="16" border="0" align="absmiddle"></a>
					{% endif %}
					&nbsp;
					{% if unit.bweb != "" %}
					  <a href="{{unit.bweb}}" target="_blank">
					  <img src="{% static "images/world.png" %}" width="16" height="16" border="0" align="absmiddle"></a>
					{% endif %}
				  </p>
				</div>
			  </td>
			</tr>
			<tr>
			  <td><img name="g_r7_c4" src="{% static "images/g_r7_c4.png" %}" width="600" height="12" border="0" alt=""></td>
			</tr>
		  </table>
		  <span class="functionDiv">
			  <img src="{% static "images/g_r9_c3.png" %}" width="600" height="20" border="0" />
		  </span>
	</tr>
  {% empty %}
	<tr>
	  <td background="{% static "images/g_r3_c3.png" %}">
		  <div class="messageDiv"><img src="{% static "images/exclamation.png" %}" width="16" height="16" align="absmiddle"> 目前沒有新的資料，歡迎您留言。</div></td>
	</tr>
  {% endfor %}
	  <tr>
		<td background="{% static "images/g_r3_c3.png" %}">
		  <div class="pagebutton">
		  {% if currentpage > 1 %}
			   <a href="/index/prev/" title="上一頁">
			  <img src="{% static "images/prevpage.png" %}" alt="上一頁" width="64" height="24" /></a>
		  {% endif %}
		  {% if currentpage < totpage %}
			  <a href="/index/next/" title="下一頁">
			  <img src="{% static "images/nextpage.png" %}" alt="下一頁" width="64" height="24" /></a>
		  {% endif %}
		  </div>
		</td>
	  </tr>
	  <tr>
		<td background="{% static "images/g_r3_c3.png" %}">
{% endblock %}
```
### 執行結果：
![image](https://github.com/LonelyCaesar/website-Bulletin-board/assets/101235367/8f554306-ebef-4699-93b6-23725da5488c)

在templates\baseadmin.html建立網頁模板。
### 程式碼：
``` html
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	{% block title %}{% endblock %}
	{% load static %}
	<link href="{% static "css/style.css" %}" rel="stylesheet" type="text/css" />
</head>
<body bgcolor="#ffffff">
	<div id="warp">
	  <table width="600" border="0" align="center" cellpadding="0" cellspacing="0">
		<tr>
		  <td height="180" background="{% static "images/g_r1_c3.png" %}">&nbsp;</td>
		</tr>
		<tr>
		  <td background="{% static "images/g_r3_c3.png" %}">
			  <div class="functionDiv">
				<table width="92%" border="0" align="center" cellpadding="0" cellspacing="0">
				  <tr>
					<td align="right">
						 <img src="{% static "images/door_out.png" %}" width="16" height="16" align="absmiddle" /> <a href="/logout/">登出管理</a></td>
					</td>
				  </tr>
				</table>
				<img src="{% static "images/g_r9_c3.png" %}" width="600" height="20" border="0" />
			  </div>
			  {% block content %}{% endblock %}
				<div id="siteinfo"> 留言版&nbsp;個人所有 &copy; 2024&nbsp; GuestBook Personally owned. </div></td>
			</tr>
	  </table>
	</div>
</body>
</html>
```
### 執行結果：
![image](https://github.com/LonelyCaesar/website-Bulletin-board/assets/101235367/d3f44812-543c-46e0-89a9-0def90149cc3)

### 5.	表單類別檔：
在Django中圖形驗證通常是配合表單類別forms.py使用。
### boardapp\forms.py程式碼：
```python django
from django import forms
from captcha.fields import CaptchaField

class PostForm(forms.Form):
    boardsubject = forms.CharField(max_length=100,initial='')
    boardname = forms.CharField(max_length=20,initial='')
    boardgender = forms.BooleanField()
    boardmail = forms.EmailField(max_length=100,initial='',required=False)
    boardweb = forms.URLField(max_length=100,initial='',required=False)
    boardcontent = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()
```
### 6.	首頁處理函式及模板：
### boardapp\views.py程式碼：
``` python django
from django.shortcuts import render, redirect
from boardapp import models, forms
from django.contrib.auth import authenticate
from django.contrib import auth
import math

page = 0

def index(request, pageindex=None):  #首頁
	global page  #重複開啟本網頁時需保留 page1 的值
	pagesize = 3  #每頁顯示的資料筆數
	boardall = models.BoardUnit.objects.all().order_by('-id')  #讀取資料表,依時間遞減排序
	datasize = len(boardall)  #資料筆數
	totpage = math.ceil(datasize / pagesize)  #總頁數
	if pageindex==None:  #無參數
		page = 0
		boardunits = models.BoardUnit.objects.order_by('-id')[:pagesize]
	elif pageindex=='prev':  #上一頁
		start = (page-1)*pagesize  #該頁第1筆資料
		if start >= 0:  #有前頁資料就顯示
			boardunits = models.BoardUnit.objects.order_by('-id')[start:(start+pagesize)]
			page -= 1
	elif pageindex=='next':  #下一頁
		start = (page+1)*pagesize  #該頁第1筆資料
		if start < datasize:  #有下頁資料就顯示
			boardunits = models.BoardUnit.objects.order_by('-id')[start:(start+pagesize)]
			page += 1
	currentpage = page + 1  #將目頁前頁面以區域變數傳回html
	return render(request, "index.html", locals())
```
### templates\index.html程式碼：
``` html
{% extends "base.html" %}
{% load static %}

{% block title %}<title>網站留言版</title>{% endblock %}

{% block twomenu %}
	<img src="{% static "images/comment.png" %}" width="16" height="16" align="absmiddle" /> <a href="/post/">我要留言</a> 
	<img src="{% static "images/key.png" %}" width="16" height="16" align="absmiddle" /> <a href="/login/">版主管理</a>
{% endblock %}

{% block content %}
	 </td>
  </tr>
  {% for unit in boardunits %}
	<tr>
	  <td background="{% static "images/g_r3_c3.png" %}">
		  <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" background="{% static "images/g_r5_c4.png" %}"
			<tr>
			  <td valign="top" style="background:url"({% static "images/g_r4_c4.png" %}); background-repeat:no-repeat">
				<div class="floorDiv">
					{% if unit.bgender == "m" %}
						<img src="{% static "images/boy.png" %}" width="52" height="80" />
					{% else %}
						<img src="{% static "images/girl.png" %}" width="52" height="80" />
					{% endif %}
				</div>
				<div class="contentDiv">
				  <p class="title">{{unit.bsubject}}</p>
				  <p></p>
				  <p>{{unit.bcontent}}</p>
				  {% if unit.bresponse != "" %}
					<div class="responseDiv">
					  <p><strong>版主回應</strong>：{{unit.bresponse}}</p>
					</div>
				  {% endif %}
				  <p class="editor"><img src="{% static "images/user.png" %}" width="16" height="16" align="absmiddle">{{unit.bname}}&nbsp; 
					<img src="{% static "images/date.png" %}" width="16" height="16" align="absmiddle">{{unit.btime}}&nbsp;
					{% if unit.bmail != "" %}
					  <a href="mailto:{{unit.bmail}}" target="_blank">
					  <img src="{% static "images/email.png" %}" width="16" height="16" border="0" align="absmiddle"></a>
					{% endif %}
					&nbsp;
					{% if unit.bweb != "" %}
					  <a href="{{unit.bweb}}" target="_blank">
					  <img src="{% static "images/world.png" %}" width="16" height="16" border="0" align="absmiddle"></a>
					{% endif %}
				  </p>
				</div>
			  </td>
			</tr>
			<tr>
			  <td><img name="g_r7_c4" src="{% static "images/g_r7_c4.png" %}" width="600" height="12" border="0" alt=""></td>
			</tr>
		  </table>
		  <span class="functionDiv">
			  <img src="{% static "images/g_r9_c3.png" %}" width="600" height="20" border="0" />
		  </span>
	</tr>
  {% empty %}
	<tr>
	  <td background="{% static "images/g_r3_c3.png" %}">
		  <div class="messageDiv"><img src="{% static "images/exclamation.png" %}" width="16" height="16" align="absmiddle"> 目前沒有新的資料，歡迎您留言。</div></td>
	</tr>
  {% endfor %}
	  <tr>
		<td background="{% static "images/g_r3_c3.png" %}">
		  <div class="pagebutton">
		  {% if currentpage > 1 %}
			   <a href="/index/prev/" title="上一頁">
			  <img src="{% static "images/prevpage.png" %}" alt="上一頁" width="64" height="24" /></a>
		  {% endif %}
		  {% if currentpage < totpage %}
			  <a href="/index/next/" title="下一頁">
			  <img src="{% static "images/nextpage.png" %}" alt="下一頁" width="64" height="24" /></a>
		  {% endif %}
		  </div>
		</td>
	  </tr>
	  <tr>
		<td background="{% static "images/g_r3_c3.png" %}">
{% endblock %}
```
### 執行結果
![image](https://github.com/LonelyCaesar/website-Bulletin-board/assets/101235367/dfbabe3f-520e-4360-b7a0-e6048621427c)
### 7.	新增留言網頁面處理函式及模板：
### boardapp\views.py程式碼：
``` python django
def post(request):
	if request.method == "POST":
		postform = forms.PostForm(request.POST)
		if postform.is_valid():
			subject = postform.cleaned_data['boardsubject']
			name =  postform.cleaned_data['boardname']
			gender =  request.POST.get('boardgender', None)
			mail = postform.cleaned_data['boardmail']
			web = postform.cleaned_data['boardweb']
			content =  postform.cleaned_data['boardcontent']
			unit = models.BoardUnit.objects.create(bname=name, bgender=gender, bsubject=subject, bmail=mail, bweb=web, bcontent=content, bresponse='')
			unit.save()
			message = '已儲存...'
			postform = forms.PostForm()
			return redirect('/index/')
		else:
			message = '驗證碼錯誤！'
	else:
		message = '標題、姓名、內容及驗證碼必須輸入！'
		postform = forms.PostForm()
	return render(request, "post.html", locals())
```
### templates\post.html程式碼：
``` html
{% extends "base.html" %}
略……
{% block content %}
略……
          <form action="." method="POST" name="form1">
            {% csrf_token %}
            <table width="100%" border="0" cellspacing="1" cellpadding="4">
              <tr>
                <th width="80" align="right" valign="baseline">標題</th>
                <td valign="baseline">{{postform.boardsubject}}</td>
              </tr>
              <tr>
                <th align="right" valign="baseline">姓名</th>
                <td valign="baseline">{{postform.boardname}}</td>
              </tr>
              <tr>
                <th align="right" valign="baseline">性別</th>
                <td valign="baseline">
                  <input name="boardgender" type="radio" id="boardgender" value="m" checked="checked" />
                  <img src="{% static "images/boy.png" %}" width="52" height="80" alt="男生" />
                  <input name="boardgender" type="radio" id="boardgender2" value="f" />
                  <img src="{% static "images/girl.png" %}" width="52" height="80" alt="女生" /></td>
              </tr>
              <tr>
                <th align="right" valign="baseline">電子郵件</th>
                <td valign="baseline">{{postform.boardmail}}</td>
              </tr>
              <tr>
                <th align="right" valign="baseline">相關網站</th>
                <td valign="baseline">{{postform.boardweb}}</td>
              </tr>
              <tr>
                <th align="right" valign="baseline">內容</th>
                <td valign="baseline">{{postform.boardcontent}}</td>
              </tr>
              <tr>
                <th align="right" valign="baseline">驗證碼</th>
                <td valign="baseline">{{postform.captcha}}</td>
              </tr>
              <tr>
                <th colspan="2" align="center" valign="baseline">
                  <input type="submit" name="button" id="button" value="送出">
                  <input type="reset" name="button2" id="button2" value="重設"></th>
              </tr>
            </table>
            <span style="color:red">{{message}}</span>
          </form>
略……
{% endblock %}
```
### 8.	登入與登出頁面處理函式及模板：
使用者在首頁點選版主管理鈕就會執行<views.py>中的login函式債入<login.html>網頁。
### boardapp\views.py程式碼：
``` python django
def login(request):  #登入
	messages = ''  #初始時清除訊息
	if request.method == "POST":
		postform = forms.PostForm(request.POST)
		name = request.POST['username'].strip()
		password = request.POST['passwd']
		user1 = authenticate(username=name, password=password)
		if user1 is not None:
			if user1.is_active:  #帳號有效
				auth.login(request, user1)
				postform = forms.PostForm()
				return redirect('/adminmain/')
			else:
				message = '登入失敗！'
		else:
			message = '驗證碼錯誤！'
	else:
		postform = forms.PostForm()
	return render(request, "login.html", locals())
```
### templates\login.html程式碼：
``` html
略……
          <form action="." method="POST" name="form1">
            {% csrf_token %}
            <table border="0" align="center" cellpadding="4" cellspacing="1">
              <tr>
                <th align="right" valign="baseline">帳號</th>
                <td valign="baseline"><input name="username" type="text" id="username" style="width:200px"></td>
              </tr>
              <tr>
                <th align="right" valign="baseline">密碼</th>
                <td valign="baseline"><input name="passwd" type="password" id="passwd" style="width:200px"></td>
              </tr>
              <tr>
                <th align="right" valign="baseline">驗證碼</th>
                <td valign="baseline">{{postform.captcha}}</td>
              </tr>
              <tr>
                <th colspan="2" align="center" valign="baseline">
                  <input type="submit" name="button" id="button" value="送出">
                  <input type="reset" name="button2" id="button2" value="重設">
                </th>
                </tr>
            </table>
            <span style="color:red">{{message}}</span>
          </form>
略……
```
### 9.	管理頁面處理函式及模板：
使用者在登入頁面通過驗證就會執行<views.py>中的adminmain函式載入<adminmain.html>網頁(管理頁面)。
### boardapp\views.py程式碼：
``` python
略……
def logout(request):  #登出
	auth.logout(request)
	return redirect('/index/')
略……
def adminmain(request, pageindex=None):  #管理頁面
略……
			page -= 1
	elif pageindex=='next':
		start = (page+1)*pagesize
		if start < datasize:
			boardunits = models.BoardUnit.objects.order_by('-id')[start:(start+pagesize)]
			page += 1
	elif pageindex=='ret':  #按確定修改鈕後返回
		start = page*pagesize
		boardunits = models.BoardUnit.objects.order_by('-id')[start:(start+pagesize)]
	else:  #按確定修改鈕會以pageindex傳入資料id
		unit = models.BoardUnit.objects.get(id=pageindex)  #取得要修改的資料記錄
		unit.bsubject=request.POST.get('boardsubject', '')
		unit.bcontent=request.POST.get('boardcontent', '')
		unit.bresponse=request.POST.get('boardresponse', '')
		unit.save()  #寫入資料庫
		return redirect('/adminmain/ret/')  #返回管理頁面,參數為ret
	currentpage = page+1
	return render(request, "adminmain.html", locals())
略……
```
### templates\adminmain.html程式碼：
``` html
{% extends "baseadmin.html" %}
略……
				<form action="/adminmain/{{unit.id}}/" method="POST" name="form1">
				  {% csrf_token %}
				  <div class="floorDiv">
					  {% if unit.bgender == "m" %}
						  <img src="{% static "images/boy.png" %}" width="72" height="63" />
					  {% else %}
						  <img src="{% static "images/girl.png" %}" width="72" height="63" />
					  {% endif %}
					  <a href="/delete/{{unit.id}}/">
						<img src="{% static "images/cross.png" %}" width="16" height="16" border="0" align="absmiddle"> 刪除</a>
				  </div>
				  <div class="contentDiv">
					<p class="editor">
					  <img src="{% static "images/user.png" %}" width="16" height="16" align="absmiddle">{{unit.bname}}&nbsp; 
					  <img src="{% static "images/date.png" %}" width="16" height="16" align="absmiddle">{{unit.btime}}&nbsp; 
					  <a href="mailto:{{unit.bmail}}" target="_blank">
						<img src="{% static "images/email.png" %}" width="16" height="16" border="0" align="absmiddle"></a>&nbsp; 
					  <a href="{{unit.bweb}}" target="_blank">
						<img src="{% static "images/world.png" %}" width="16" height="16" border="0" align="absmiddle"></a>&nbsp; 
					</p>
					<p class="title">留言標題
					  <input name="boardsubject" type="text" id="boardsubject" style="margin-top:5px" value="{{unit.bsubject}}" size="40">
					</p>
					<p class="title"> 留言內容
					  <textarea name="boardcontent" cols="50" rows="5" id="boardcontent" style="margin-top:5px">{{unit.bcontent}}</textarea>
					</p>
					<p class="title">版主回應
					  <textarea name="boardresponse" cols="50" rows="5" id="boardresponse">{{unit.bresponse}}</textarea>
					</p>
					<p align="center">
					  <input type="submit" name="button" id="button" value="確定修改">
					</p>
				  </div>
				</form>
略……
```
### 10.	刪除頁面處理函式與模板：
使用者在管理頁面點選刪除鈕就會執行<views.py>中的delete函式載入<delete.html>網頁使用者刪除留言。
### boardapp\views.py
``` python
略……
def delete(request, boardid=None, deletetype=None):  #刪除資料
	unit = models.BoardUnit.objects.get(id=boardid)  #讀取指定資料
	if deletetype == 'del':  #按確定刪除鈕
		unit.delete()
		return redirect('/adminmain/')
	return render(request, "delete.html", locals())
```
### templates\delete.html程式碼：
``` html
{% extends "baseadmin.html" %}
略……
{% block content %}
  <form action="/delete/{{unit.id}}/del/" id="form1" name="form1" method="post">
    {% csrf_token %}
    <table width="600" border="0" align="center" cellpadding="0" cellspacing="0" background="{% static "images/g_r5_c4.png" %}">
      <tr>
        <td valign="top" style="background:url"({% static "images/g_r4_c4.png" %}); background-repeat:no-repeat">
          <div class="floorDiv"> 
            {% if unit.bgender == "m" %}
              <img src="{% static "images/boy.png" %}" width="72" height="63" />
            {% endif %}
            {% if unit.bgender == "f" %}
              <img src="{% static "images/girl.png" %}" width="72" height="63" />
            {% endif %}
          </div>
          <div class="contentDiv">
            <p class="title">{{unit.bsubject}}</p>
            <p></p>
            <p>{{unit.bcontent}}</p>
            <div class="responseDiv">
              <p><strong>版主回應</strong>：{{unit.bresponse}}</p>
            </div>
            <p class="editor"><img src="{% static "images/user.png" %}" width="16" height="16" align="absmiddle" />{{unit.bname}}&nbsp; 
              <img src="{% static "images/date.png" %}" width="16" height="16" align="absmiddle" />{{unit.btime}}&nbsp; 
              <a href="mailto:{{unit.bmail}}">
                <img src="{% static "images/email.png" %}" width="16" height="16" border="0" align="absmiddle" /></a>&nbsp; 
              <a href="{{unit.bweb}}">
                <img src="{% static "images/world.png" %}" width="16" height="16" border="0" align="absmiddle" /></a>&nbsp;
            </p>
            <div class="messageDiv">
              <img src="{% static "images/cancel.png" %}" width="16" height="16" align="absmiddle" /> 是否確定刪除這筆留言？
            </div>
            <p align="center">
              <input type="submit" name="button" id="button" value="確定刪除" />
              <input type="button" name="button2" id="button2" value="回上一頁" onclick="window.history.back();" />
            </p>
          </div>
……
{% endblock %}
```
# 四、結論
使用Django建立網站留言板是一個高效開發、安全性強、可擴展性佳的專案。Django提供內建功能和工具，使開發快速且高效。它內建多種安全措施，能有效防範常見攻擊。此外，Django具有良好的擴展性，易於維護和擴展，適合長期使用。

# 五、參考資料
Python架站特訓班(第二版) Django 3最強實戰學習資源。
