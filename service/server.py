import frm
log = frm.start_log_prod()

import zmq
import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import servicemanager
import socket
import sys
import json

class FlaskSvc (win32serviceutil.ServiceFramework):
	_svc_name_ = "CentralCache"
	_svc_display_name_ = "Central Cache"

	def __init__(self, *args):
		win32serviceutil.ServiceFramework.__init__(self, *args)
		self.hWaitStop = win32event.CreateEvent(None,0,0,None)
		socket.setdefaulttimeout(5)
		self.stop_requested = False

	def kill_0mq(self):
		if self.socket.closed == False:
			self.socket.close()
		self.socket.unbind('ipc://cache/mm')
		self.context.destroy()

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)
		self.ReportServiceStatus(win32service.SERVICE_STOPPED)
		self.stop_requested = True
		log.info("Stopping the service")
		self.kill_0mq()

	def SvcDoRun(self):
		servicemanager.LogMsg(
			servicemanager.EVENTLOG_INFORMATION_TYPE,
			servicemanager.PYS_SERVICE_STARTED,
			(self._svc_name_,'')
		)
		self.main()

	def main(self):
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind('ipc://cache/mm')
		log.info("Checkpoint 1")
		while True:
			try:
				message = self.socket.recv_json()
				log.info(message)
				self.socket.send_json(json.dumps({"test" : "1"}))
			except Exception as e:
				log.exception(e)
				self.kill_0mq()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		servicemanager.Initialize()
		servicemanager.PrepareToHostSingle(FlaskSvc)
		servicemanager.StartServiceCtrlDispatcher()
	else:
		win32serviceutil.HandleCommandLine(FlaskSvc)