import pymysql
pymysql.install_as_MySQLdb()

from django.db.backends.mysql.base import DatabaseFeatures

# Bypass the MariaDB 10.5 check for XAMPP
DatabaseFeatures.is_mariadb = False