import pymysql
from app import app
from tables import Results
from db_config import mysql
from flask import session, flash, render_template, request, redirect

@app.route('/', methods=['GET','POST'])
def landing():
    if request.method == 'GET':
        if 'username' in session:
            return redirect('/phonebook')
        return render_template('index.html')
    if request.method == 'POST':
        conn = None
        cursor = None
        try: 
            _username = request.form['Username']
            _password = request.form['Password']
            # validate the received values
            if _username and _password:
                #do not save password as a plain text
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (_username, _password))
                logged = cursor.fetchone()
                if logged:
                    session['loggedin'] = True
                    session['id'] = logged['id']
                    session['username'] = logged['username']
                else:
                    # Account doesnt exist or username/password incorrect
                    flash('Autenticação falhou, usuário ou senha incorretos')  
                    return redirect('/')

                return redirect('/phonebook')
            else:
                return 'Erro na autenticação'
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'GET':
        return render_template('singup.html')
    if request.method == 'POST':
        conn = None
        cursor = None
        try: 
            _name = request.form['Name']
            _email = request.form['Username']
            _password = request.form['Password']
            # validate the received values
            if _name and _email and _password:
                #do not save password as a plain text
                # save edits
                sql = "INSERT INTO users(name, username, password) VALUES(%s, %s, %s)"
                data = (_name, _email, _password,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                flash('Registrado com sucesso!')
                return redirect('/')
            else:
                return 'Erro ao adicionar o usuário'
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET':
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            id = session['id']
            cursor.execute("SELECT * FROM users WHERE id=%s", id)
            row = cursor.fetchone()
            if row:
                return render_template('edit_user.html', row=row)
            else:
                return 'Erro ao carregar os dados #{id}'.format(id=id)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    if request.method == 'POST':
        conn = None
        cursor = None
        try: 
            _name = request.form['Name']
            _username = request.form['Username']
            _password = request.form['Password']
            _id = session['id']
            if _name and _username and _password and _id:
                #do not save password as a plain text
                # save edits
                sql = "UPDATE users SET name=%s, username=%s, password=%s WHERE id=%s"
                data = (_name, _username, _password, _id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                flash('Atualizado com sucesso!')
                return redirect('/logout')
            else:
                return 'Erro ao atualizar o cadastro'
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

@app.route('/delete_user/')
def delete_user():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        id = session['id']
        cursor.execute("DELETE FROM users WHERE id=%s", id)
        conn.commit()
        flash('Dados deletados com sucesso!')
        return redirect('/logout')
    except Exception as e:
        print(e)
        return 'Erro ao deletar o usuário'
    finally:
        cursor.close() 
        conn.close()

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/phonebook')
def phonebook():
    if 'username' in session:
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM phonebook WHERE user_id=%s", session['id'])
            rows = cursor.fetchall()
            table = Results(rows)
            table.border = True
            return render_template('phonebook.html', table=table)
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()
    else:
        return redirect('/')

@app.route('/add_phone', methods=['GET', 'POST'])
def add_phone():
    if request.method == 'GET':
        return render_template('add_phone.html')
    if request.method == 'POST':
        conn = None
        cursor = None
        try: 
            _name = request.form['Name']
            _phone = request.form['Phone']
            _email = request.form['Email']
            # validate the received values
            if _name and _email and _phone:
                #do not save password as a plain text
                # save edits
                sql = "INSERT INTO phonebook(user_id, name, phone, mail) VALUES(%s, %s, %s, %s)"
                data = (session['id'], _name, _phone, _email)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect('/phonebook')
            else:
                return 'Error while adding phone entry'
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

@app.route('/edit_phone/<int:id>')
def edit_phone(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM phonebook WHERE id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('edit_phone.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        
@app.route('/update_phone', methods=['POST'])
def update_phone():
    conn = None
    cursor = None
    try: 
        _name = request.form['Name']
        phone = request.form['Phone']
        _email = request.form['Email']
        _id = request.form['id']
        user_id = session['id']
        # validate the received values
        if _name and _email and phone and _id and request.method == 'POST':
            # save edits
            sql = "UPDATE phonebook SET name=%s, phone=%s, mail=%s WHERE id=%s AND user_id=%s "
            data = (_name, phone, _email, _id, user_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/phonebook')
        else:
            return 'Error while updating phonebook entry'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/delete_phone/<int:id>')
def delete_phone(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        user_id = session['id']
        cursor.execute("DELETE FROM phonebook WHERE id=%s AND user_id=%s", (id, user_id))
        conn.commit()
        return redirect('/phonebook')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run()