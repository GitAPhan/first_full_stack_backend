import mariadb as db
import dbcreds as c

# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=c.user,
                          password=c.password,
                          host=c.host,
                          port=c.port,
                          database=c.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except Exception:
        print("DB Connection Error: General error message")
    return conn, cursor  

# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception as e:
        print(e)
        print("DB Cursor Close Error: General error message")

    try:
        conn.close()
    except Exception as e:
        print(e)
        print("DB Connection Close Error: General error message")

# grabbing candy posts from database
def get_candy_db():
    conn, cursor = connect_db()
    candys = None
    ordered_candys = []

    try:
        cursor.execute("select id, name, description, user_id from candy")
        candys = cursor.fetchall()
    except:
        print('generic db error: get')

    disconnect_db(conn, cursor)

    for candy in candys:
        candies = {
            "id": candy[0],
            "name": candy[1],
            "description": candy[2],
            "user_id": candy[3]
        }
        ordered_candys.append(candies)
    
    return ordered_candys

# adding candy posts to database
def post_candy_db(name, description):
    conn, cursor = connect_db()

    try:
        cursor.execute("insert into candy (name, description) values (?,?)", [name, description])
        conn.commit()
    except:
        print("generic db error: post")
        return "error message"

    disconnect_db(conn, cursor)

    return "success message"

# edit existing candy posts in database
def patch_candy_db(id, name, description):
    conn, cursor = connect_db()

    try:
        cursor.execute("update candy set name=?, description=? where id=?", [name, description, id])
        conn.commit()
    except:
        print("generic db error: patch")
        return "error message"

    disconnect_db(conn, cursor)

    return "success message"

# delete existing candy from database
def delete_candy_db(id):
    conn, cursor = connect_db()

    try:
        cursor.execute("delete from candy where id=?", [id])
        conn.commit()
    except:
        print("generic db error: delete")
        return "error message"

    disconnect_db(conn, cursor)

    return "success message"