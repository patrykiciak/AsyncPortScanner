import socket
import time
import asyncio
import sys

open_ports = []
counter = []
CONNECTION_TIME_OUT = 5
BUFFER_SIZE = 15000
port_tasks = asyncio.Queue(BUFFER_SIZE)


async def main(ip, ports):
    for port in ports:
        await port_tasks.put(asyncio.create_task(test_port(ip, port)))
        if port_tasks.full():
            await do_port_tasks()
    await do_port_tasks()


async def do_port_tasks():
    while port_tasks.qsize():
        task = await port_tasks.get()
        await task
        port_tasks.task_done()


async def test_port(ip, port):
    try:
        conn = asyncio.open_connection(ip, port)
        await asyncio.wait_for(conn, CONNECTION_TIME_OUT)
        conn.close()
        open_ports.append(port)
        print(port)
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, PermissionError):
        pass
    return False


async def start():
    if len(sys.argv) < 2:
        target = input('Enter the host to be scanned: ')
    else:
        target = sys.argv[1]

    start_time = time.time()
    host = socket.gethostbyname(target)
    print('Starting scan on host: ', host)

    scope = range(1, 10000)
    await main(host, scope)
    print('Time taken:', time.time() - start_time)
    print('Number of open ports:', len(open_ports))


asyncio.get_event_loop().run_until_complete(start())