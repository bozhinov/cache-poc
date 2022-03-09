import atexit
import logging
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from queue import Queue

logging.captureWarnings(True)
format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

class QueueListenerHandler(QueueHandler):

	def __init__(self, handlers, respect_handler_level=False, auto_run=True, queue=Queue(-1)):
		super().__init__(queue)
		self._listener = QueueListener(queue, *handlers, respect_handler_level=respect_handler_level)
		if auto_run:
			self.start()
			atexit.register(self.stop)

	def start(self):
		self._listener.start()

	def stop(self):
		self._listener.stop()

	def emit(self, record):
		return super().emit(record)

def start_log_prod():
	log = logging.getLogger('cccache')
	log.setLevel(logging.INFO)
	fh = RotatingFileHandler(f'logs/CentralCache.log', maxBytes=(1048576*5), backupCount=5)
	fh.setFormatter(format)
	queueHandle = QueueListenerHandler(handlers=[fh])
	log.addHandler(queueHandle)
	log.info("Central Cache started")
	return log

def get_log_instance():
	l = logging.getLogger('cccache')
	if not l.hasHandlers():
		raise Exception("Logging facility not initiated")
	return l