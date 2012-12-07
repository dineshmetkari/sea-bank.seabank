import requests

from models import Property

class Sms(object):
	SMS_API_COMMAND = "http://api.clickatell.com/http/sendmsg?api_id={api_id}&user={user}&password={password}&to={to}&text={text}"
	SMS_API_ID = "SMS_API_ID"
	SMS_PASSWORD = "SMS_PASSWORD"
	SMS_LOGIN = "SMS_LOGIN"

	def __init__(self, receiver="", text=""):
		self.receiver = receiver
		self.text = text

	def send(self):
		api_id = Property.objects.get(name=self.SMS_API_ID)
		user = Property.objects.get(name=self.SMS_LOGIN)
		password = Property.objects.get(name=self.SMS_PASSWORD)

		requests.get(self.SMS_API_COMMAND.format(api_id=api_id.value, user=user.value, password=password.value, to=self.receiver, text=self.text))
