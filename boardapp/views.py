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
	
def logout(request):  #登出
	auth.logout(request)
	return redirect('/index/')

def adminmain(request, pageindex=None):  #管理頁面
	global page
	pagesize = 3
	boardall = models.BoardUnit.objects.all().order_by('-id')
	datasize = len(boardall)
	totpage = math.ceil(datasize / pagesize)
	if pageindex==None:
		page =0
		boardunits = models.BoardUnit.objects.order_by('-id')[:pagesize]
	elif pageindex=='prev':
		start = (page-1)*pagesize
		if start >= 0:
			boardunits = models.BoardUnit.objects.order_by('-id')[start:(start+pagesize)]
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

def delete(request, boardid=None, deletetype=None):  #刪除資料
	unit = models.BoardUnit.objects.get(id=boardid)  #讀取指定資料
	if deletetype == 'del':  #按確定刪除鈕
		unit.delete()
		return redirect('/adminmain/')
	return render(request, "delete.html", locals())