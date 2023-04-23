import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

host = "udaproj3-sv.postgres.database.azure.com"
dbname = "techconfdb"
user = "azureadmin@udaproj3-sv"
password = "Udathangnh36"
sslmode = "require"

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)

    try:
        cur = conn.cursor()

        # TODO: Get notification message and subject from database using the notification_id
        cur.execute(f'SELECT message, subject FROM notification WHERE id={notification_id}')
        message_user, subject = cur.fetchone()

        # TODO: Get attendees email and name
        cur.execute('SELECT email, first_name FROM attendee')
        attendees = cur.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            message = Mail(
                from_email='from_email@example.com',
                to_emails=attendee[0],
                subject=f'{attendee[1]}: {subject}',
                html_content=message_user)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                # print(response.body)
                # print(response.headers)
            except Exception as e:
                print("Nothing")

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        total_attendees = f'Notified {len(attendees)} attendees'
        cur.execute(f"UPDATE notification SET status = '{total_attendees}' WHERE id={notification_id}")
        cur.execute(f"UPDATE notification SET completed_date = '{datetime.utcnow()}' WHERE id={notification_id}")
        cur.execute(f"UPDATE notification SET submitted_date = NULL WHERE id={notification_id}")
        print(datetime.utcnow())

        conn.commit()


    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        conn.close()