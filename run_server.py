import sys
import eventlet
from coincast import create_app
application, socketio = create_app()


from coincast.bot.server_push import listen, update_last_tick
eventlet.spawn(listen, update_last_tick, 10)
eventlet.monkey_patch()


if __name__ == '__main__':
    print("starting test server...")
    #application.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(application)