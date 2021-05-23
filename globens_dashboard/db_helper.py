from psycopg2 import extras as psycopg2_extras
import psycopg2

db_conn = None


def get_db_connection():
    global db_conn
    if db_conn is None:
        db_conn = psycopg2.connect(
            host='globens-db.cssqpqimlbjy.ap-northeast-2.rds.amazonaws.com',
            database='globens_db',
            user='postgres',
            password='postgres'
        )
        print('database initialized', db_conn)
    return db_conn


def end():
    get_db_connection().close()


def get_user(email=None, user_id=None, session_key=None):
    cur = get_db_connection().cursor(cursor_factory=psycopg2_extras.DictCursor)
    if email is not None:
        cur.execute('select * from "gb_user" where "email" = %s;', (
            email,
        ))
    elif user_id is not None:
        cur.execute('select * from "gb_user" where "id" = %s;', (
            user_id,
        ))
    elif session_key is not None:
        cur.execute('select * from "gb_user" where "sessionKey" = %s;', (
            session_key,
        ))
    gb_user = cur.fetchone()
    cur.close()
    return gb_user


def get_business_page(business_page_id):
    cur = get_db_connection().cursor(cursor_factory=psycopg2_extras.DictCursor)

    cur.execute('select * from "gb_business_page" where "id" = %s;', (
        business_page_id,
    ))
    gb_business_page = cur.fetchone()

    cur.close()
    return gb_business_page


def get_product(product_id):
    cur = get_db_connection().cursor(cursor_factory=psycopg2_extras.DictCursor)
    cur.execute('select * from "gb_product" where "id" = %s;', (
        product_id,
    ))
    gb_product = cur.fetchone()

    cur.close()
    return gb_product


def get_product_publish_requests(country_code):
    cur = get_db_connection().cursor(cursor_factory=psycopg2_extras.DictCursor)
    cur.execute('select * from "gb_product_publish_request" where "countryCode"=%s;', (country_code,))
    rows = cur.fetchall()
    cur.close()
    return rows


def publish_product(gb_product):
    cur = get_db_connection().cursor(cursor_factory=psycopg2_extras.DictCursor)
    cur.execute('update "gb_product" set "published" = %s where "id"=%s;', (
        True,
        gb_product['id']
    ))
    cur.close()
    get_db_connection().commit()


def remove_product_publish_request(gb_product):
    cur = get_db_connection().cursor(cursor_factory=psycopg2_extras.DictCursor)
    cur.execute('delete from "gb_product_publish_request" where "product_id"=%s;', (gb_product['id'],))
    cur.close()
    get_db_connection().commit()
