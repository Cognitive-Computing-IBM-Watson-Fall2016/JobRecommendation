@app.route('/signin')
def signin():
  return render_template("login.html")

@app.route('/query1')
def query1():
  try:
    cur = g.conn.execute("SELECT A.name FROM actors A, Movies M, Star_in S WHERE A.pid=S.pid AND M.mid=S.mid AND M.BoxOffice > (SELECT AVG(M1.BoxOffice) FROM Movies M1);")
    m = []
    for rst in cur:
        m.append(rst['name'])
    print m
    cur.close()
    context = dict(data1 = m, data2='actors')
    return render_template("result.html",**context)
  except:
    return render_template("index.html", [])

@app.route('/query2')
def query2():
  try:
    cur = g.conn.execute("SELECT tmp1.name, tmp1.address FROM (SELECT p1.name, p1.address, p1.start_time FROM playin p1 LEFT OUTER JOIN movies m1 ON p1.mid=m1.mid WHERE m1.title='Forrest Gump')AS tmp1, (SELECT p2.name, p2.address, p2.start_time FROM playin p2 LEFT OUTER JOIN movies m2 ON p2.mid=m2.mid WHERE m2.title='Lucy')AS tmp2 WHERE tmp1.name=tmp2.name AND tmp1.address=tmp2.address AND tmp1.start_time=tmp2.start_time;")
    t = ['theatres']
    #cur = g.conn.execute("SELECT * from theatres;")
    m = []
    for rst in cur:
        m.append(rst['name'])
    print m
    cur.close()
    context = dict(data1 = m,data2= t)
    return render_template("result.html",**context)
  except:
    return render_template("index.html", [])



@app.route('/query3')
def query3():
  try:
    cur = g.conn.execute("SELECT W1.name, W1.nationality FROM Writers W1, Write W2, ( SELECT tmp1.mid FROM (SELECT c1.mid, COUNT(*) AS num_of_awards FROM confer c1 GROUP BY c1.mid)AS tmp1 WHERE tmp1.num_of_awards > ( SELECT AVG(num_of_awards) FROM ( SELECT c1.mid, COUNT(*) AS num_of_awards FROM confer c1 GROUP BY c1.mid)AS tmp))AS tmp2 WHERE W1.pid=W2.pid AND W2.mid=tmp2.mid;")
    m = []
    for rst in cur:
        m.append(rst['name'])
    print m
    cur.close()
    context = dict(data1 = m, data2='writers')
    return render_template("result.html",**context)
  except:
    return render_template("index.html", [])
