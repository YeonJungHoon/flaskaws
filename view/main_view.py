from flask import Blueprint, render_template, url_for, request
from myproject import db
from myproject.selenium import crawl
from myproject.models import Data
import os
from myproject.ai import Preprocessing, Javis
import shutil




main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def base_view():
    return render_template('base.html')

@main.route('/home')
def main_view():
    files = []
    for file in os.listdir('static/refine_images'):
        files.append(file)
    
    return render_template('main_view.html', files = files)
    
@main.route('/database')
def database_view():
    querys = Data.query.order_by(Data.id).all()
    return render_template('data.html', querys = querys) #Reparing

@main.route('data_delete', methods = ['GET', 'POST'])
def data_delete():
    if request.method == 'POST':
        datas = Data.query.order_by(Data.id).all()
        for data in datas:
            db.session.delete(data)
            db.session.commit()
        shutil.rmtree('static/img')
        
    return render_template('data_delete.html')

@main.route('/zerochan', methods=['POST', 'GET'])
def execute():
    crawler = crawl('url_for(chromedriver.exe)')
    if request.method =='POST':
        data = request.form['search']
        num = request.form['num']
        num = int(num)
        for i in range(num):
            y_train=Data(data = data)
            db.session.add(y_train)
            db.session.commit()
        img_urls = crawler.zerochan(data,num)
        crawler.url_to_img(img_urls)
        return render_template('zerochan.html')
        
    return render_template('zerochan.html')

@main.route('/pinterest', methods=['POST', 'GET'])
def execute2():
    crawler = crawl('url_for(chromedriver.exe)')
    if request.method == 'POST':
        data = request.form['search_pin']
        num = request.form['num_pin']
        num = int(num)
        for i in range(num):
            y_train=Data(data = data)
            db.session.add(y_train)
            db.session.commit()
        
        img_urls = crawler.pinterest(data,num)
        crawler.url_to_img(img_urls)
        return render_template('pinterest.html')
    return render_template('pinterest.html')

@main.route('/ai_train', methods=['POST','GET'])
def execute3():
    if request.method == "POST":
        length = request.form['image_length']
        length = int(length)
        preprocessing = Preprocessing(length)

        preprocessing.image_resize()
        var = preprocessing.img_to_array()
        y_train = preprocessing.make_y_train()
        y_train = preprocessing.one_hot_encoding(y_train)
        x_train = preprocessing.make_x_train(var)
        javis = Javis( 30,3, x_train, y_train ,length)
    
        model, summary = javis.LeNet()
        javis.LeNet_train(model)
        


        

        return render_template('ai_summary.html', summary = summary)

    return render_template('ai_train.html')


    