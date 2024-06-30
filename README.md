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
請在anaconda/VScode的終端機上執行指令
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
