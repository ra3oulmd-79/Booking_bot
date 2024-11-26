from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
import sqlite3
import datetime
import logging
from telegram import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token='KEY')

# Function to send start reminders
def send_start_reminders():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    now = datetime.datetime.now()

    time_in_15_min = now + datetime.timedelta(minutes=15)

    # Retrieve bookings that are due to start in 15 minutes on the same day
    c.execute("SELECT * FROM bookings WHERE start_booking_date = ? AND start_time = ?", (now.strftime('%d.%m.%Y'), time_in_15_min.strftime('%H:%M')))
    bookings = c.fetchall()

    # Send a reminder for each booking
    for booking in bookings:
        id, user_id, _, _, start_time, end_time = booking
        bot.send_message(chat_id=user_id, text=f"یادآوری: جلسه مصاحبه شما شما در ساعت {start_time} شروع می‌شود. 💻لینک جلسه مصاحبه خدمت شما
https://portal.iranscratch.ir/Branch/Portal/BigBlueButton/S/4121
آکادمی ایران اسکرچ")

    conn.close()

# Function to send end reminders
def send_end_reminders():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    now = datetime.datetime.now()

    c.execute("SELECT * FROM bookings WHERE end_booking_date = ? AND end_time = ?", (now.strftime('%d.%m.%Y'), now.strftime('%H:%M')))
    bookings = c.fetchall()
    
    for booking in bookings:
        id, user_id, _, _, start_time, end_time = booking
        bot.send_message(chat_id=user_id, text=f"جلسه مصاحبه شما در ساعت {end_time} به پایان رسید.")

    conn.close()

# Initialize the scheduler
scheduler = BlockingScheduler(timezone=pytz.utc)

# Add a job to send start reminders every minute
scheduler.add_job(send_start_reminders, 'interval', minutes=1)

# Add a job to send end reminders every minute
scheduler.add_job(send_end_reminders, 'interval', minutes=1)

scheduler.start()
