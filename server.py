import zmq
import signal
import json

signal.signal(signal.SIGINT, signal.SIG_DFL);

if __name__ == '__main__':

	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind('ipc://cache/mm')

	while True:
		try:
			message = socket.recv_json()
			print(message)
			socket.send_json(json.dumps({"data" : "BLA BLA"}))
		except Exception as e:
			print(e)
			if socket.closed == False:
				socket.close()
			socket.unbind('ipc://cache/mm')
			context.destroy()