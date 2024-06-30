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
