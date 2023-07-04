import asyncio
from game import Game
from ble import Ble

state = b'\x01\x00\x00\x00'

async def main():

    node_state_queue = asyncio.Queue()
    node = Ble()

    polling = True
    while polling:
        print("Polling for devices...")
        polltask = asyncio.create_task(node.poll_devices())
        await polltask

        if(polltask.result() == None):
            print("Failed to connect, retrying in 5 seconds")
            await asyncio.sleep(5)
        else:
            polling = False

    devices = polltask.result()
    for i in range(0, len(devices)):
        if(devices[i].name != None):
            print(str(i) + ": " + devices[i].name + " (" + devices[i].address + ")")
    print("--------------------")

    print("Please select device to connect to (0-" + str(len(devices) - 1) + "):")
    device_idx = int(input())

    connecting = True
    while connecting:
        print("Connecting to "+ devices[device_idx].name + " (" + devices[device_idx].address + ")")
        connecttask = asyncio.create_task(node.connect(devices[device_idx].address))
        await connecttask
        if(connecttask.result() == True):
            print("Connected to device")
            connecting = False
        else:
            print("Retrying in 5 seconds")
            await asyncio.sleep(5)

    if(connecttask.result() == False):
        print("Failed to connect")

    polltask = asyncio.create_task(poll(node, node_state_queue))
    gametask = asyncio.create_task(game(node_state_queue))

    await gametask
    polltask.cancel()

async def game(node_state_queue):
    global state

    game = Game()
    while True:
        await asyncio.sleep(0.01)
        try:
            data = node_state_queue.get_nowait()
            state = data
        except asyncio.QueueEmpty:
            data = state
        await game.tick(state)

async def poll(node, node_state_queue):
    while True:
        await asyncio.sleep(0.1)
        await node_state_queue.put(await node.request_status()) # Put the status into the queue

if __name__ == "__main__":
    asyncio.run(main())
