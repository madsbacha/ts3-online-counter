from telnetlib import Telnet
from redis import Redis
import sched, time
from utils import env, periodic

def get_client_list(host, port, username, password):
    ts3_welcome_line = "Welcome to the TeamSpeak 3 ServerQuery interface, type \"help\" for a list of commands and \"help <command>\" for information on a specific command."
    ok_line = "error id=0 msg=ok"
    
    login_command = f"login {username} {password}"
    use_command = "use 1"
    clientlist_command = "clientlist"
    exit_command = "quit"
  
    byte_res = b""
    with Telnet(host, port) as tn:
        tn.read_until(ts3_welcome_line.encode("ascii"))
        tn.write(login_command.encode("ascii") + b"\n")
        tn.write(use_command.encode("ascii") + b"\n")
        tn.write(clientlist_command.encode("ascii") + b"\n")
        tn.write(exit_command.encode("ascii") + b"\n")
        byte_res = tn.read_all().decode("ascii")
    res_lines = byte_res.splitlines()
    clientlist = ""
    for line in res_lines:
        if f"client_nickname={username}" in line:
            clientlist = line
            break
    return clientlist


def count_clients(clientlist, include_queryuser=False):
    return len(clientlist.split("|")) - (0 if include_queryuser else 1)


def get_redis():
    return Redis(env("REDIS_HOST", "localhost"), env("REDIS_PORT", 6379, int), db=0, socket_timeout=10000)


def update_counter(ts_host, ts_port, ts_username, ts_password):
    line = get_client_list(ts_host, ts_port, ts_username, ts_password)
    counter = count_clients(line)
    r = get_redis()
    r.set('counter', counter)
    print(f"Updated counter: {counter}")


if __name__ == "__main__":
    ts_host = env("TS_HOST")
    ts_port = env("TS_PORT", 10011, int)
    ts_username = env("TS_USERNAME", "serveradmin")
    ts_password = env("TS_PASSWORD")
    r = get_redis()
    r.set('counter', 0)
    s = sched.scheduler(time.time, time.sleep)
    periodic(s, 5, update_counter, (ts_host, ts_port, ts_username, ts_password))
    s.run()
    