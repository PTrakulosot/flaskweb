from flask import Flask, jsonify, render_template, request
import sqlite3 as sql
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
import seaborn as sns
import math

app = Flask(__name__)
page = 1
pro_page = 1
sto_page = 1

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/order/revious', methods=['GET', 'POST'])
def orderPageRevious():
    tablename = "Orders"
    if 'current_page' in request.values:

        page = request.values['current_page']

        page = int(page) - 1
        if page == 0 or page == '':
            page = 1
        per_page = 20
        offset = page * per_page - 20
        if offset == 20:
            offtset = 0
        with sql.connect("database.db") as con:
            c = con.cursor() 
            c.execute("SELECT PROD_CODE, CUST_CODE, STORE_CODE, SHOP_DATE FROM orders ORDER BY SHOP_DATE DESC LIMIT " + str(per_page) + " OFFSET " + str(offset)) 
            rows = c.fetchall()
            return render_template('order.html', rows=rows, tbname=tablename, page=page)


@app.route('/order/next', methods=['GET', 'POST'])
def orderPageNext():
    tablename = "Orders"
    if 'current_page' in request.values:
        page = request.values['current_page']
        page = int(page) + 1

        per_page = 20
        offset = page * per_page - 20
        with sql.connect("database.db") as con:
            c = con.cursor()
            c.execute("SELECT PROD_CODE, CUST_CODE, STORE_CODE, SHOP_DATE FROM orders ORDER BY SHOP_DATE DESC LIMIT " + str(per_page) + " OFFSET " + str(offset)) 
            rows = c.fetchall()
            return render_template('order.html', rows=rows, tbname=tablename, page=page)

@app.route('/order', methods=['GET', 'POST'])
def searchorder():
    tablename = "Orders"
    if 'CUST_CODE' in request.values:
        custcode = request.values['CUST_CODE']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT PROD_CODE, CUST_CODE, STORE_CODE, SHOP_DATE FROM orders WHERE CUST_CODE = 'CUST" + custcode + "' ORDER BY SHOP_DATE DESC LIMIT 0,30")
            rows = c.fetchall()
            return render_template('order.html', rows=rows, tbname=tablename, page=page)
    else:
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT PROD_CODE, CUST_CODE, STORE_CODE, SHOP_DATE FROM orders ORDER BY SHOP_DATE DESC LIMIT 0,20")
            rows = c.fetchall()
            return render_template('order.html', rows=rows, tbname=tablename, page=page)


@app.route('/product/revious', methods=['GET', 'POST'])
def productPageRevious():
    tablename = "Products"
    if 'current_page' in request.values:

        pro_page = request.values['current_page']

        pro_page = int(pro_page) - 1
        if pro_page == 0 or pro_page == '':
            pro_page = 1
        per_page = 20
        offset = pro_page * per_page - 20
        if offset == 20:
            offtset = 0
        with sql.connect("database.db") as con:
            c = con.cursor() 
            s = "SELECT * FROM products LIMIT " + str(per_page) + " OFFSET " + str(offset)
            c.execute(s) 
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)

@app.route('/product/next', methods=['GET', 'POST'])
def productPageNext():
    tablename = "Products"
    if 'current_page' in request.values:
        pro_page = request.values['current_page']
        pro_page = int(pro_page) + 1

        per_page = 20
        offset = pro_page * per_page - 20
        if offset == 20:
            offtset = 0
        with sql.connect("database.db") as con:
            c = con.cursor() 
            s = "SELECT * FROM products LIMIT " + str(per_page) + " OFFSET " + str(offset)
            c.execute(s)
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)

@app.route('/product/form', methods=['GET', 'POST'])
def productform():
    tablename = "Products"

    if 'PROD_ID' in request.values:
        prdid = request.values['PROD_ID']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM products WHERE product_id='" + prdid + "'")
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)
    else:
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM products LIMIT 0,20")
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)

@app.route('/product/insert', methods=['GET', 'POST'])
def insertproduct():
    tablename = "Products"
    if 'pid' in request.values and 'pid' != "":
        pid = request.values['pid']
        pname = request.values['pname']
        price = request.values['price']
        if not pid or not pname or price:
            with sql.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM products LIMIT 0,20")
                rows = c.fetchall()
                return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            s = "INSERT INTO products VALUES ('" + \
                pid + "','" + pname + "','" + price + "')"
            c.execute(s)
            c = conn.cursor()
            s = "SELECT * FROM products WHERE product_id = '" + pid + "'"
            c.execute(s)
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)


@app.route('/product/delete', methods=['GET', 'POST'])
def deleteproduct():
    tablename = "Products"
    if 'pid' in request.values:
        pid = request.values['pid']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            s = "DELETE FROM products WHERE product_id = '" + pid + "'"
            c.execute(s)
            c = conn.cursor()
            s = "SELECT * FROM products LIMIT 0,20"
            c.execute(s)
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)

@app.route('/product/edit', methods=['GET', 'POST'])
def editproduct():
    tablename = "Products"
    if 'pid' in request.values:
        pid = request.values['pid']
        pname = request.values['pname']
        price = request.values['price']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            s = "UPDATE products SET product_name = '" + pname + \
                "', price = '" + price + "' WHERE product_id = '" + pid + "'"
            c.execute(s)
            c = conn.cursor()
            s = "SELECT * FROM products WHERE product_id = '" + pid + "'"
            c.execute(s)
            rows = c.fetchall()
            return render_template('product.html', rows=rows, tbname=tablename, pro_page=pro_page)


@app.route('/search/bestsell/form', methods=['GET', 'POST'])
def searchbestsellform():
    tablename = "Products"
    return render_template('bestsell.html', tbname=tablename)


@app.route('/search/bestsell', methods=['GET', 'POST'])
def searchbestsell():
    tablename = "Products"
    if request.values:
        shop_d = request.values['SHOP_DATE']
        shop_h = request.values['SHOP_HOUR']
        store_id = request.values['STORE_CODE']
        if shop_d == '' or shop_h == '':
            with sql.connect("database.db") as conn:
                tablename = "BEST SELL"
                return render_template('bestsell.html', tbname=tablename)
        elif store_id == '':
            with sql.connect("database.db") as conn:
                c = conn.cursor()
                s = "SELECT SHOP_DATE, SHOP_HOUR, PROD_CODE, product_name, sum(QUANTITY) FROM orders INNER JOIN products ON orders.PROD_CODE = products.product_id WHERE SHOP_DATE = '" + \
                    shop_d + "' AND SHOP_HOUR = '" + shop_h + \
                    "' GROUP BY PROD_CODE ORDER BY sum(QUANTITY) DESC LIMIT 0,50"
                c.execute(s)
                rows = c.fetchall()
                head0 = "No"
                head1 = "SHOP_DATE"
                head2 = "SHOP_HOUR"
                head3 = "PROD_CODE"
                head4 = "PROD_NAME"
                head5 = "QUANTITY"
                return render_template('bestsell.html', rows=rows, tbname=tablename, head0=head0, head1=head1, head2=head2, head3=head3, head4=head4, head5=head5)
        else:
            with sql.connect("database.db") as conn:
                c = conn.cursor()
                s = "SELECT STORE_CODE, SHOP_DATE, SHOP_HOUR, PROD_CODE, product_name, sum(QUANTITY) FROM orders INNER JOIN products ON orders.PROD_CODE = products.product_id WHERE SHOP_DATE = '" + \
                    shop_d + "' AND SHOP_HOUR = '" + shop_h + "' AND STORE_CODE = 'STORE" + \
                    store_id + \
                    "' GROUP BY PROD_CODE ORDER BY sum(QUANTITY) DESC"
                c.execute(s)
                rows = c.fetchall()
                head0 = "No"
                head1 = "STORE_CODE"
                head2 = "SHOP_DATE"
                head3 = "SHOP_HOUR"
                head4 = "PROD_CODE"
                head5 = "PROD_NAME"
                head6 = "QUANTITY"
                return render_template('bestsell.html', rows=rows, tbname=tablename, head0=head0, head1=head1, head2=head2, head3=head3, head4=head4, head5=head5, head6=head6)
    else:
        with sql.connect("database.db") as conn:
            tablename = "BEST SELL"
            return render_template('bestsell.html', tbname=tablename)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    store_code = 'STORE00001'
    amount = 0
    with sql.connect("database.db") as conn:
        c = conn.cursor()
        s = "SELECT sum(spend) FROM orders WHERE STORE_CODE = '" + \
            store_code + "'"
        c.execute(s)
        amount = c.fetchall()[0]
        s = "SELECT SHOP_DATE, sum(spend) as amount FROM orders WHERE STORE_CODE = '" + \
                                   store_code + "' GROUP BY SHOP_DATE "
        result = c.execute(s)
        sqldf = pd.DataFrame()
        img = io.BytesIO()
        for row in result:
            date = row[0] % 100
            amount = row[1]
            row_sql = {"SHOP_DATE":  date, "amount": amount}
            # sqldf.append(row)
            sqldf = sqldf.append(row_sql, ignore_index=True)

        sns_plot = sns.lineplot(x='SHOP_DATE', y='amount', data=sqldf, label="amount")
        plt.figure()
        fig = sns_plot.get_figure()
        fig.savefig(img, format='png')
        plot1 = base64.b64encode(img.getvalue()).decode()

        s = "SELECT STORE_CODE, SHOP_DATE, SUM(SPEND) as amount"\
            " FROM orders "\
            " WHERE STORE_CODE = '" +  store_code  + "'"\
            " GROUP BY STORE_CODE, SHOP_DATE "\
            " ORDER BY STORE_CODE "
        result = c.execute(s)
        sqldf = pd.DataFrame()
        img2 = io.BytesIO()
        for row in result:
            c1 = row[0]
            c2 = row[1] % 100
            c3 = row[2]
            row_sql = {'STORE_CODE' : c1, 'SHOP_DATE' : c2 ,  'AMOUNT' :  c3 }
            # sqldf.append(row)
            sqldf = sqldf.append(row_sql, ignore_index=True)

        sns_plot2 = sns.barplot(x="SHOP_DATE", y="AMOUNT", data=sqldf)
        plt.figure()
        fig = sns_plot2.get_figure()
        fig.savefig(img2, format='png')
        plot2 = base64.b64encode(img2.getvalue()).decode()
        
        
    return render_template('dashboard.html', amount=math.floor(amount), plot1=plot1, plot2=plot2 ,store_code=store_code)


@app.route('/dashboard/search', methods=['GET', 'POST'])
def dashboardsearch():
    if 'STORE_CODE' in request.values:
        store_code = request.values['STORE_CODE']
        amount = 0
        if not store_code:
            return render_template('dashboard.html')
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            s = "SELECT sum(spend) FROM orders WHERE STORE_CODE = '" + \
                store_code + "'"
            c.execute(s)
            amount = c.fetchall()[0]
            s = "SELECT SHOP_DATE, sum(spend) as amount FROM orders WHERE STORE_CODE = 'STORE" + \
                                    store_code + "' GROUP BY SHOP_DATE "
            result = c.execute(s)
            sqldf = pd.DataFrame()
            img = io.BytesIO()
            for row in result:
                date = row[0] % 100
                amount = row[1]
                row_sql = {"SHOP_DATE":  date, "amount": amount}
                # sqldf.append(row)
                sqldf = sqldf.append(row_sql, ignore_index=True)

            sns_plot = sns.lineplot(x='SHOP_DATE', y='amount', data=sqldf, label="amount")
            plt.figure()
            fig = sns_plot.get_figure()
            fig.savefig(img, format='png')
            plot1 = base64.b64encode(img.getvalue()).decode()

            s = "SELECT STORE_CODE, SHOP_DATE, SUM(SPEND) as amount"\
                " FROM orders "\
                " WHERE STORE_CODE = 'STORE" +  store_code  + "'"\
                " GROUP BY STORE_CODE, SHOP_DATE "\
                " ORDER BY STORE_CODE "
            result = c.execute(s)
            sqldf = pd.DataFrame()
            img2 = io.BytesIO()
            for row in result:
                c1 = row[0]
                c2 = row[1] % 100
                c3 = row[2]
                row_sql = {'STORE_CODE' : c1, 'SHOP_DATE' : c2 ,  'AMOUNT' :  c3 }
                # sqldf.append(row)
                sqldf = sqldf.append(row_sql, ignore_index=True)

            sns_plot2 = sns.barplot(x="SHOP_DATE", y="AMOUNT", data=sqldf)
            plt.figure()
            fig = sns_plot2.get_figure()
            fig.savefig(img2, format='png')
            plot2 = base64.b64encode(img2.getvalue()).decode()
            
            
        return render_template('dashboard.html', store_code=store_code, amount=math.floor(amount), plot1=plot1, plot2=plot2)

@app.route('/store/revious', methods=['GET', 'POST'])
def storePageRevious():
    tablename = "Stores"
    if 'current_page' in request.values:

        sto_page = request.values['current_page']

        sto_page = int(sto_page) - 1
        if sto_page == 0 or sto_page == '':
            sto_page = 1
        per_page = 20
        offset = sto_page * per_page - 20
        if offset == 20:
            offtset = 0
        with sql.connect("database.db") as con:
            c = con.cursor() 
            c.execute("SELECT * FROM stores LIMIT " + str(per_page) + " OFFSET " + str(offset)) 
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)

@app.route('/store/next', methods=['GET', 'POST'])
def storePageNext():
    tablename = "Stores"
    if 'current_page' in request.values:
        sto_page = request.values['current_page']
        sto_page = int(sto_page) + 1

        per_page = 20
        offset = sto_page * per_page - 20
        if offset == 20:
            offtset = 0
        with sql.connect("database.db") as con:
            c = con.cursor() 
            s = "SELECT * FROM stores LIMIT " + str(per_page) + " OFFSET " + str(offset)
            c.execute(s) 
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)

@app.route('/store/form', methods=['GET', 'POST'])
def storeform():
    tablename = "Stores"

    if 'STORE_CODE' in request.values:
        storeid = request.values['STORE_CODE']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM stores WHERE store_id='STORE" + storeid + "'")
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)
    else:
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM stores LIMIT 0,20")
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)

@app.route('/store/insert', methods=['GET', 'POST'])
def insertstore():
    tablename = "Store"
    if 'sid' in request.values:
        sid = request.values['sid']
        sname = request.values['sname']
        locate = request.values['locate']
        contact = request.values['contact']
        if not sid or not sname:
            with sql.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM stores LIMIT 0,20")
                rows = c.fetchall()
                return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)
        with sql.connect("database.db") as conn:
            sid = "STORE" + sid
            c = conn.cursor()
            s = "INSERT INTO stores VALUES ('" + \
                sid + "','" + sname + "','" + locate + "','" + contact + "')"
            c.execute(s)
            c = conn.cursor()
            s = "SELECT * FROM stores WHERE store_id = '" + sid + "'"
            c.execute(s)
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)

@app.route('/store/delete', methods=['GET', 'POST'])
def deletestore():
    tablename = "Stores"
    if 'sid' in request.values:
        sid = request.values['sid']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            s = "DELETE FROM stores WHERE store_id = '" + sid + "'"
            c.execute(s)
            c = conn.cursor()
            s = "SELECT * FROM stores LIMIT 0,20"
            c.execute(s)
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)

@app.route('/store/edit', methods=['GET', 'POST'])
def editstore():
    tablename = "Stores"
    if 'sid' in request.values:
        sid = request.values['sid']
        sname = request.values['sname']
        locate = request.values['locate']
        contact = request.values['contact']
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            s = "UPDATE stores SET store_name = '" + sname + \
                "', locate = '" + locate + "', contact = '" + contact + "' WHERE store_id = '" + sid + "'"
            c.execute(s)
            c = conn.cursor()
            s = "SELECT * FROM stores WHERE store_id = '" + sid + "'"
            c.execute(s)
            rows = c.fetchall()
            return render_template('store.html', rows=rows, tbname=tablename, sto_page=sto_page)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
