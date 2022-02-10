import mariadb as db
import dbcreds as c


# Exceptions:
# id of that item is non existent
class IdNonExistent(Exception):
    pass


# input value string too long
class InputStringTooLong(Exception):
    pass

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

    # status message and code
    status_message = "generic post db error"
    status_code = 400 

    # conditional to catch if string entered is too long
    try:
        if len(name) > 100:
            raise InputStringTooLong
        if len(description) >255:
            raise InputStringTooLong
    except InputStringTooLong:
        return "Input Error:'name' value too long. Please limit to 100 characters", status_code

    # database request
    try:
        cursor.execute("insert into candy (name, description) values (?,?)", [name, description])
        conn.commit()

        # success message
        status_message = "success message"
        status_code = 200
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code

# edit existing candy posts in database
def patch_candy_db(id, name, description):
    conn, cursor = connect_db()

    # status message and code
    status_message = "generic patch db error"
    status_code = 400 

    # conditional to catch if string entered is too long
    try:
        if len(name) > 100:
            raise InputStringTooLong
        if len(description) >255:
            raise InputStringTooLong
    except InputStringTooLong:
        return "Input Error:'name' value too long. Please limit to 100 characters", status_code

    # database request
    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from candy where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent

        cursor.execute("update candy set name=?, description=? where id=?", [name, description, id])
        conn.commit()

        # update status
        status_message = "success message"
        status_code = 200
    except IdNonExistent:
        return "Input Error: 'id' does not exist", status_code
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code

# delete existing candy from database
def delete_candy_db(id):
    conn, cursor = connect_db()

    # status message and code
    status_message = "generic delete db error"
    status_code = 400 

    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from candy where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent

        cursor.execute("delete from candy where id=?", [id])
        conn.commit()

        # update status
        status_message = "success message"
        status_code = 200
    except IdNonExistent:
        return "Input Error: 'id' does not exist", status_code
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code