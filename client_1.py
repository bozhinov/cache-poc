import zmq, json

context = zmq.Context()
try:
	socket = context.socket(zmq.REQ)
	socket.connect('ipc://cache/mm')
	socket.send_json(json.dumps(["BOO BOO - 1", 123]))
	message = socket.recv_json()
	print(message)
except:
	if socket.closed == False:
		socket.close()
