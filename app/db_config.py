from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
app.config['MYSQL_DATABASE_DB'] = 'teste_cam'
app.config['MYSQL_DATABASE_HOST'] = '192.168.20.11'
#app.config['MYSQL_DATABASE_PORT'] = '3306'
mysql.init_app(app)