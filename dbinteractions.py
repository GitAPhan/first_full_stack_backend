import secrets
from uuid import uuid4
import mariadb as db
import dbcreds as c


# Exceptions:
# id of that item is non existent
class IdNonExistent(Exception):
    pass


# input value string too long
class InputStringTooLong(Exception):
    pass


# wrong login info
class IncorrectLoginCredentials(Exception):
    pass


# user does not have permission
class PermissionDenied(Exception):
    pass


# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(
            user=c.user,
            password=c.password,
            host=c.host,
            port=c.port,
            database=c.database,
        )
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
        print("generic db error: get")

    disconnect_db(conn, cursor)

    for candy in candys:
        candies = {
            "id": candy[0],
            "name": candy[1],
            "description": candy[2],
            "user_id": candy[3],
        }
        ordered_candys.append(candies)

    return ordered_candys


# adding candy posts to database
def post_candy_db(name, description, login_token):
    conn, cursor = connect_db()

    # status message and code
    status_message = "generic post db error"
    status_code = 400

    # database request
    try:
        # login token check
        cursor.execute("select user_id from login where login_token=?", [login_token])
        user_id = int(cursor.fetchone()[0])
    except TypeError:
        return "Token Error: invalid user token", status_code
    except:
        return "Token Error: Generic DB error", status_code

    # conditional to catch if string entered is too long
    try:
        if len(name) > 100:
            raise InputStringTooLong
        if len(description) > 255:
            raise InputStringTooLong
    except InputStringTooLong:
        return (
            "Input Error:'name' value too long. Please limit to 100 characters",
            status_code,
        )

    # database request
    try:
        cursor.execute(
            "insert into candy (name, description, user_id) values (?,?,?)", [name, description, user_id]
        )
        conn.commit()

        # success message
        status_message = "success message"
        status_code = 200
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code


# edit existing candy posts in database
def patch_candy_db(id, name, description, login_token):
    conn, cursor = connect_db()

    # status message and code
    status_message = "generic patch db error"
    status_code = 400

    # conditional to catch if string entered is too long
    try:
        if len(name) > 100:
            raise InputStringTooLong
        if len(description) > 255:
            raise InputStringTooLong
    except InputStringTooLong:
        return (
            "Input Error:'name' value too long. Please limit to 100 characters",
            status_code,
        )

    # database request
    try:
        # login token check
        cursor.execute("select user_id from login where login_token=?", [login_token])
        user_id = int(cursor.fetchone()[0])
    except TypeError:
        return "Token Error: invalid user token", status_code
    except:
        return "Token Error: Generic DB error"

    try:
        # compare user_id from login with user_id from candy to have a more specific exception
        cursor.execute("select user_id from candy where id=?", [id])
        candy_user_id = cursor.fetchone()[0]
        if user_id != candy_user_id:
            raise PermissionDenied
    except PermissionDenied:
        return "Permission Error: user does not have permission", status_code
    except TypeError:
        return "Update Error: 'id' does not exist", status_code
    # except:
    #     return status_message, status_code

    try:
        cursor.execute(
            "update candy set name=?, description=? where id=? and user_id=?",
            [name, description, id, user_id],
        )
        conn.commit()
        # conditional to raise custom exception if row count is 0
        if cursor.rowcount == 0:
            raise IdNonExistent

        # update status
        status_message = "success message"
        status_code = 200
    except IdNonExistent:
        return "Update Error: no entries were updated", status_code
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code


# delete existing candy from database
def delete_candy_db(id, login_token):
    conn, cursor = connect_db()

    # status message and code
    status_message = "generic delete db error"
    status_code = 400

    try:
        cursor.execute(
            "delete c from candy c inner join login l on l.user_id = c.user_id where c.id=? and l.login_token=?",
            [id, login_token],
        )
        conn.commit()
        # conditional to raise custom exception if row count is 0
        if cursor.rowcount == 0:
            raise IdNonExistent

        # update status
        status_message = "success message"
        status_code = 200
    except IdNonExistent:
        return "Input Error: No entry found", status_code
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code


# login attempt request from database
def login_attempt_db(username, password):
    conn, cursor = connect_db()

    # status message and code
    status_message = "generic login attempt db error"
    status_code = 400

    try:
        # verify username and password and return the id
        cursor.execute(
            "select id from user where username=? and password=?", [username, password]
        )
        user_id = int(cursor.fetchone()[0])

        # generate unique login token
        loginToken = {"loginToken": secrets.token_urlsafe()}

        # add login session to login table
        cursor.execute(
            "insert into login (login_token, user_id) values (?,?)",
            [loginToken["loginToken"], user_id],
        )
        conn.commit()

        status_message = loginToken
        status_code = 200
    except TypeError:
        return "Input Error: incorrect login credentials", status_code
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code


# logout attempt request from database
def logout_attempt_db(login_token):
    conn, cursor = connect_db()
    print(login_token)
    # status message and code
    status_message = "generic logout attempt db error"
    status_code = 400

    try:
        # remove login session from database
        cursor.execute("delete from login where login_token=?", [login_token])
        conn.commit()

        # check to see if any entry has been deleted
        if cursor.rowcount == 0:
            raise IdNonExistent

        # update status
        status_message = "success message"
        status_code = 200
    except IdNonExistent:
        return "Input Error: 'loginToken' does not exist", status_code
    except:
        return status_message, status_code

    disconnect_db(conn, cursor)

    return status_message, status_code
