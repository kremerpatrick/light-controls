def input_handler(command: str):
    print(f"Command entered: {command}")

while True:
    cmd = input('Enter command, q to quit: ')
    if cmd == "q": break
    input_handler(cmd)