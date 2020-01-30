from apps import db2
#from apps.appReminder.models import Reminder


reminder_collection = db2.db.reminder
reminder_collection.insert({ 'title' : 'ReminderTagliando', 'text' : 'Devi Fare il Tagliando!' })

"""
reminder = Reminder(category='ReminderTagliando', text='Quest\' auto ha bisogno di un TAGLIANDO. Affrettati!')

reminder.save()


reminder = Reminder.query.filter(Reminder.category == 'ReminderTagliando').first()
print(reminder)
"""
