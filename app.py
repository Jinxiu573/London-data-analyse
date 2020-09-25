from flask import Flask,render_template,request,session,redirect,jsonify
from dao.UserDao import UserDao,User
from dao.DataDao import DataDao,Data
import csv, io, time

app = Flask(__name__)
# The secret key must be set to operate on session
# Flask session requires the key string to be used
app.config["SECRET_KEY"] = "admin"

# ===================== Init End ============================


# ===================== Search Start ========================

@app.route('/search', methods=['GET'])
def do_search():
    search = request.values.get("search")
    result = DataDao().query("SELECT id, site, species, DATE_FORMAT(reading_date_time,'%Y-%m-%d %H:%i:%s') as 'reading_date_time', `value`, units, pr FROM t_data WHERE site LIKE '%" + search + "%' OR species LIKE '%" + search +"%'")
    return render_template('user-search.html',result=result)

# ===================== Search End ==========================


# ===================== Data Handler Start ===========================

@app.route('/analyse', methods=['GET'])
def do_analyse():
    return render_template('user-analyse.html', msg=None)

@app.route('/analyse/calculateAvg', methods=['GET'])
def do_calculate_avg():
    """
    Statistical average value of two months (统计两个月平均数值)
    :return:
    """
    try:
        m1 = request.values.get('m1')
        m2 = request.values.get('m2')
        result = DataDao().query("SELECT species, AVG(`value`) as 'avgs' FROM t_data WHERE DATE_FORMAT(reading_date_time,'%Y-%m') BETWEEN '" + m1 + "' AND '" + m2 + "' AND `value` != '' GROUP BY species")
        if len(result) > 0:
            return render_template('user-analyse.html', result=result, msg="Calculate success")
        else:
            return render_template('user-analyse.html', msg="Fill in the format error, please check again")
    except Exception as e:
        print(e)
        return render_template('user-analyse.html', msg="Fill in the format error, please check again")

@app.route('/analyse/calculateAQI', methods=['GET'])
def do_calculate_aqi():
    """
    Calculate the VALUE of AQI for a given day(计算某一天的AQI值)
    :return:
    """
    try:
        t = request.values.get("time")
        result = DataDao().query("SELECT DATE_FORMAT(reading_date_time,'%Y-%m-%d') AS dates, species, AVG(`value`) AS 'avgs' FROM t_data WHERE DATE_FORMAT(reading_date_time,'%Y-%m-%d') = '" + t + "' AND `value` != '' GROUP BY DATE_FORMAT(reading_date_time,'%Y-%m-%d'), species")
        aqi = -1
        for i in result:
            if i['species'] == 'CO':
                avgs = i['avgs']
                value = 0
                if avgs >= 0 and avgs < 2:
                    value = 50 / 2 * avgs
                if avgs >= 2 and avgs < 4:
                    value = 50 / 2 * (avgs - 2) + 50
                if avgs >= 4 and avgs < 14:
                    value = 50 / 10 * (avgs - 4) + 100
                if avgs >= 14 and avgs < 24:
                    value = 50 / 10 * (avgs - 14) + 150
                if avgs >= 24 and avgs < 36:
                    value = 100 / 12 * (avgs - 24) + 200
                if avgs >= 36 and avgs < 48:
                    value = 100 / 12 * (avgs - 36) + 300
                if avgs >= 48 and avgs < 60:
                    value = 100 / 12 * (avgs - 48) + 400
                if value > aqi:
                    aqi = value
            if i['species'] == 'NO2':
                avgs = i['avgs']
                value = 0
                if avgs >= 0 and avgs < 40:
                    value = 50 / 40 * avgs
                if avgs >= 40 and avgs < 80:
                    value = 50 / 40 * (avgs - 40) + 50
                if avgs >= 80 and avgs < 180:
                    value = 50 / 100 * (avgs - 80) + 100
                if avgs >= 180 and avgs < 280:
                    value = 50 / 100 * (avgs - 180) + 150
                if avgs >= 280 and avgs < 565:
                    value = 100 / 285 * (avgs - 280) + 200
                if avgs >= 565 and avgs < 750:
                    value = 100 / 185 * (avgs - 565) + 300
                if avgs >= 750 and avgs < 940:
                    value = 100 / 190 * (avgs - 750) + 400
                if value > aqi:
                    aqi = value
            if i['species'] == 'O3':
                avgs = i['avgs']
                value = 0
                if avgs >= 0 and avgs < 160:
                    value = 50 / 160 * avgs
                if avgs >= 160 and avgs < 200:
                    value = 50 / 40 * (avgs - 160) + 50
                if avgs >= 200 and avgs < 300:
                    value = 50 / 100 * (avgs - 200) + 100
                if avgs >= 300 and avgs < 400:
                    value = 50 / 100 * (avgs - 300) + 150
                if avgs >= 400 and avgs < 800:
                    value = 100 / 400 * (avgs - 400) + 200
                if avgs >= 800 and avgs < 1000:
                    value = 100 / 200 * (avgs - 800) + 300
                if avgs >= 1000 and avgs < 1200:
                    value = 100 / 200 * (avgs - 1000) + 400
                if value > aqi:
                    aqi = value
            if i['species'] == 'PM10':
                avgs = i['avgs']
                value = 0
                if avgs >= 0 and avgs < 50:
                    value = 50 / 50 * avgs
                if avgs >= 50 and avgs < 150:
                    value = 50 / 100 * (avgs - 50) + 50
                if avgs >= 150 and avgs < 250:
                    value = 50 / 100 * (avgs - 150) + 100
                if avgs >= 250 and avgs < 350:
                    value = 50 / 100 * (avgs - 250) + 150
                if avgs >= 350 and avgs < 420:
                    value = 100 / 70 * (avgs - 350) + 200
                if avgs >= 420 and avgs < 500:
                    value = 100 / 80 * (avgs - 420) + 300
                if avgs >= 500 and avgs < 600:
                    value = 100 / 100 * (avgs - 500) + 400
                if value > aqi:
                    aqi = value
        if aqi > -1:
            return render_template('user-analyse.html', resultAQI=aqi, msgAqi="Calculate success")
        else:
            return render_template('user-analyse.html', msgAqi="Fill in the format error, please check again")
    except Exception as e:
        print(e)
        return render_template('user-analyse.html', msgAqi="Fill in the format error, please check again")

# ===================== Data Handler End ===========================


# ===================== Data Analyse Show Start ==================

@app.route('/show', methods=['GET'])
def do_show():
    return render_template('user-show.html')

@app.route('/data/show1', methods=['GET'])
def do_get_show1_data():
    """
    Calculate the average proportion of each pollutant(计算各污染物平均值占比)
    :return:
    """
    results = DataDao().query("SELECT species AS 'name', AVG(`value`) AS 'value' FROM t_data WHERE `value` != '' GROUP BY species")
    print(results)
    return jsonify(results)

@app.route('/data/show2', methods=['GET'])
def do_get_show2_data():
    """
    Calculate the contaminant line chart(计算污染物折线图)
    :return:
    """
    result = DataDao().query("SELECT DATE_FORMAT(reading_date_time,'%Y-%m') AS dates, species, AVG(`value`) AS 'avgs' FROM t_data WHERE `value` != '' GROUP BY DATE_FORMAT(reading_date_time,'%Y-%m'), species")
    type_list = []
    data_dic = {}
    time_list = []
    for i in result:
        if not i['species'] in type_list:
            type_list.append(i['species'])
        if not i['dates'] in time_list:
            time_list.append(i['dates'])
        if i['species'] in data_dic:
            data_dic[i['species']].append(i['avgs'])
        else:
            data_dic[i['species']] = [i['avgs']]

    data_list = []
    for i in data_dic:
        map = {}
        map["name"] = i
        map["type"] = 'line'
        map["stack"] = '均值'
        map["data"] = data_dic[i]
        data_list.append(map)
    return jsonify({"data_list": data_list, "type_list": type_list, "time_list": time_list})

@app.route('/data/show3', methods=['GET'])
def do_get_show3_data():
    """
    Calculate AQI data visualization(计算AQI 数据可视化)
    :return:
    """
    data_list = []
    result = DataDao().query("SELECT DATE_FORMAT(reading_date_time,'%Y-%m-%d') AS dates, species, AVG(`value`) AS 'avgs' FROM t_data WHERE `value` != '' GROUP BY DATE_FORMAT(reading_date_time,'%Y-%m-%d'), species")
    data_dict = {}
    for i in result:
        if i['dates'] in data_dict:
            data_dict[i['dates']].append(i)
        else:
            data_dict[i['dates']] = [i]
    for i in data_dict:
        aqi = 0
        for j in data_dict[i]:
            if j['species'] == 'CO':
                avgs = j['avgs']
                value = 0
                if avgs >= 0 and avgs < 2:
                    value = 50 / 2 * avgs
                if avgs >= 2 and avgs < 4:
                    value = 50 / 2 * (avgs - 2) + 50
                if avgs >= 4 and avgs < 14:
                    value = 50 / 10 * (avgs - 4) + 100
                if avgs >= 14 and avgs < 24:
                    value = 50 / 10 * (avgs - 14) + 150
                if avgs >= 24 and avgs < 36:
                    value = 100 / 12 * (avgs - 24) + 200
                if avgs >= 36 and avgs < 48:
                    value = 100 / 12 * (avgs - 36) + 300
                if avgs >= 48 and avgs < 60:
                    value = 100 / 12 * (avgs - 48) + 400
                if value > aqi:
                    aqi = value
            if j['species'] == 'NO2':
                avgs = j['avgs']
                value = 0
                if avgs >= 0 and avgs < 40:
                    value = 50 / 40 * avgs
                if avgs >= 40 and avgs < 80:
                    value = 50 / 40 * (avgs - 40) + 50
                if avgs >= 80 and avgs < 180:
                    value = 50 / 100 * (avgs - 80) + 100
                if avgs >= 180 and avgs < 280:
                    value = 50 / 100 * (avgs - 180) + 150
                if avgs >= 280 and avgs < 565:
                    value = 100 / 285 * (avgs - 280) + 200
                if avgs >= 565 and avgs < 750:
                    value = 100 / 185 * (avgs - 565) + 300
                if avgs >= 750 and avgs < 940:
                    value = 100 / 190 * (avgs - 750) + 400
                if value > aqi:
                    aqi = value
            if j['species'] == 'O3':
                avgs = j['avgs']
                value = 0
                if avgs >= 0 and avgs < 160:
                    value = 50 / 160 * avgs
                if avgs >= 160 and avgs < 200:
                    value = 50 / 40 * (avgs - 160) + 50
                if avgs >= 200 and avgs < 300:
                    value = 50 / 100 * (avgs - 200) + 100
                if avgs >= 300 and avgs < 400:
                    value = 50 / 100 * (avgs - 300) + 150
                if avgs >= 400 and avgs < 800:
                    value = 100 / 400 * (avgs - 400) + 200
                if avgs >= 800 and avgs < 1000:
                    value = 100 / 200 * (avgs - 800) + 300
                if avgs >= 1000 and avgs < 1200:
                    value = 100 / 200 * (avgs - 1000) + 400
                if value > aqi:
                    aqi = value
            if j['species'] == 'PM10':
                avgs = j['avgs']
                value = 0
                if avgs >= 0 and avgs < 50:
                    value = 50 / 50 * avgs
                if avgs >= 50 and avgs < 150:
                    value = 50 / 100 * (avgs - 50) + 50
                if avgs >= 150 and avgs < 250:
                    value = 50 / 100 * (avgs - 150) + 100
                if avgs >= 250 and avgs < 350:
                    value = 50 / 100 * (avgs - 250) + 150
                if avgs >= 350 and avgs < 420:
                    value = 100 / 70 * (avgs - 350) + 200
                if avgs >= 420 and avgs < 500:
                    value = 100 / 80 * (avgs - 420) + 300
                if avgs >= 500 and avgs < 600:
                    value = 100 / 100 * (avgs - 500) + 400
                if value > aqi:
                    aqi = value
        data_list.append([i, aqi])
    return jsonify(data_list)

# ===================== Data Analyse Show End ====================


# ===================== File Start ==========================

@app.route('/upload', methods=['POST'])
def upload():
    """
    Upload CSV file(上传csv文件)
    :return:
    """
    try:
        f = request.files['file']
        dd = DataDao()
        dd.delete()
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        datas = []
        for row in csv_input:
            if 'ReadingDateTime' == row[2]:
                continue
            timeStruct = time.strptime(row[2], "%d/%m/%Y %H:%M")
            row[2] = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
            print(row)
            datas.append(row)
        dd.save(datas)
        return render_template('user-upload.html', state="upload successful")
    except Exception as e:
        print(e)
        return render_template('user-upload.html', state="upload failed")


@app.route('/upload.html', methods=['GET'])
def do_upload_page():
    """
    Jump upload interface(跳转上传界面)
    :return:
    """
    return render_template("user-upload.html")


# ===================== File End ============================

# ===================== User start ===========================

@app.route('/')
@app.route('/index')
def do_index_page():
    """
    Jump page(跳转首页)
    :return:
    """
    return render_template("home.html")

@app.route('/login.html')
def do_login_page():
    """
    Jump login interface(跳转登录界面)
    :return:
    """
    return render_template("login.html")

@app.route('/register.html')
def do_register_page():
    """
    Jump registration interface(跳转注册界面)
    :return:
    """
    return render_template("register.html")

@app.route('/login', methods=['post'])
def do_login():
    """
    login(登录)
    :return:
    """
    username = request.values.get("username")
    password = request.values.get("password")
    auth = request.values.get("auth")
    try:
        u = User(username, None, auth)
        user = UserDao().get(user= u)
        user = user[0] if len(user) == 1 else None
        if(user != None and user['password'] == password):
            session["user"] = user['username']
            session["user_auth"] = auth
            return render_template("user-center.html")
        else:
            return render_template("login.html", errorMsg = "Login failed, please check whether the account password is wrong")
    except Exception as e:
        print(e)
        return render_template("login.html", errorMsg = "Login failed, please check whether the account password is wrong")

@app.route('/register', methods=['post'])
def do_register():
    """
    registered(注册)
    :return:
    """
    username = request.values.get("username")
    password = request.values.get("password")
    auth = request.values.get("auth")
    try:
        u = User(username, password, auth)
        UserDao().save(u)
        session["user"] = u.username
        session["user_auth"] = u.auth
        return render_template("user-center.html")
    except Exception as e:
        print(e)
        return render_template("register.html", errorMsg="Register failed, please check whether the account password is wrong")

@app.route('/logout', methods=['get'])
def do_logout():
    """
    Logout(退出)
    :return:
    """
    session["user"] = None
    session["user_auth"] = None
    return redirect("/login.html")

# ========================== User End ==========================

@app.before_request
def do_before_request():
    """
    Interface interceptor(界面拦截器)
    :return:
    """
    request_url = request.url
    white_path = ['login', 'index', 'register', 'logout', 'static']
    is_pass = False
    for i in white_path:
        if i in request_url:
            is_pass = True
    if is_pass == False:
        if 'http://127.0.0.1:5000/' == request_url:
            is_pass = True
        if is_pass == False:
            print(request_url, is_pass)
            if session.get("user") == None and is_pass == False:
                print("skip", 'login.html', session.get("user"))
                return render_template('login.html')

if __name__ == '__main__':
    app.run()


