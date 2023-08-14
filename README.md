<h1 align="center">Shops Scraper  </h1>

<div align="center">
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://github.com/milaan9/90_Python_Examples/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-g.svg" alt="MIT License"/></a>
    
</div>

Shops scraper aims to collect data of a single product in different shops

<h3>Technologies</h3>
<p align="center">
  <a href="https://www.selenium.dev" target="_blank" rel="noreferrer"> <img src="https://selenium.dev/images/selenium_logo_square_green.png" alt="selenium" width="40" height="40"/> </a>
  <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
  <a href="https://www.mysql.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/mysql/mysql-original.svg" alt="mysql" width="40" height="40"/> </a>
</p>

## About Instalation

Run the current project in a virtual environment and install the proper dependencies of this project.
```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Usage

To use the Scraper and Quoter, first emulate a local server and then run:

```bash
$ python .\src\run.py
Database 'shops_scraper' successfully created!
Connected to shops_scraper database.    
Table created successfully!
Type the product you want to be quoted: _______
```

This will create and connect to the proper database where products will be stored.
Once you type the product, the scraper will open the browser to scrape the prices per store. Once scraped it will show the name, price and url of the products correctly succcessfully found. You will to enter the index of the product you want to continuosly quote (let's say the product to scrape was Iphone 11).

```bash
...
Product N° 16:
        Name: Apple iPhone 11 Pro
        Price: 490.0
        Url: https://www.amazon.com//-/es/iPhone-11-Pro-Apple/dp/B07ZQT1L6B/ref=sr_1_16?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=Iphone+13&qid=1692032389&sr=8-16

Enter the index of one of the products displayed above: 16

<Display of eBay products>
...
Product N° 40:
        Name: iPhone 13 128g negro usado probablemente solo para piezas
        Price: 249.0
        Url: https://www.ebay.com/itm/145238830305?hash=item21d0e8ace1:g:gVQAAOSwBTJk1urP&amdata=enc%3AAQAIAAAAwCpt2TXRiFpJbbbZi0%2B3SmC2IC%2BteQEF6aD622t5cqaBk6ZLjD7CtuFXwptN2Aw%2Bkm%2FHgAfunDKsqpI2wE38Lbj2T8lyibZwfwFl3ow2s0ctWMF2Lfwse96lEhrDOh5vob%2FRSV6%2FcNzP1qbb2DFjxyvRCsvrsbdh%2FmCU6c8w0tMccRPlh9HJqY4asYPtTTnBU4iB6ZDzDM%2BML%2F7VyZcnjoXD%2BYpF7xULvWzLobp3QxKP4j%2F8AV4pZ5MXrILTyoQw6g%3D%3D%7Ctkp%3ABk9SR-CE7M--Yg
Enter the index of one of the products displayed above: 25

Type the product you want to be quoted: _______
```
Once typed the indexes, the scraper will prompt you again the name of a different product if you want to quote another one.

In other console run the quoter (it is recommended to type a product to scrape before running the quoter).
```bash
$ python .\src\quoter.py
Starting quoting...
```

It will quote every hour if prices changed in the different products (price is displayed in USD for all the scraped products) and eventually will display notifications in desktop if there were a discount in the product.