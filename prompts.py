import json

def prompt_unsw(row):
    return f'Record total duration = {row["dur"]}\n' + \
             f'Transaction protocol = {row["proto"]}\n' + \
             f'http, ftp, smtp, ssh, dns, ftp-data ,irc  and (-) if not much used = {row["service"]}\n' + \
             f'Indicates to the state and its dependent protocol, e.g. ACC, CLO, CON, ECO, ECR, FIN, INT, MAS, PAR, REQ, RST, TST, TXD, URH, URN, and - if not used = {row["state"]}\n' + \
             f'Source to destination packet count  = {row["spkts"]}\n' + \
             f'Destination to source packet count = {row["dpkts"]}\n' + \
             f'Source to destination transaction bytes  = {row["sbytes"]}\n' + \
             f'Destination to source transaction bytes = {row["dbytes"]}\n' + \
             f'rate = {row["rate"]}\n' + \
             f'Source to destination time to live value  = {row["sttl"]}\n' + \
             f'Destination to source time to live value = {row["dttl"]}\n' + \
             f'Source bits per second = {row["sload"]}\n' + \
             f'Destination bits per second = {row["dload"]}\n' + \
             f'Source packets retransmitted or dropped  = {row["sloss"]}\n' + \
             f'Destination packets retransmitted or dropped = {row["dloss"]}\n' + \
             f'Source interpacket arrival time (mSec) = {row["sinpkt"]}\n' + \
             f'Destination interpacket arrival time (mSec) = {row["dinpkt"]}\n' + \
             f'Source jitter (mSec) = {row["sjit"]}\n' + \
             f'Destination jitter (mSec) = {row["djit"]}\n' + \
             f'Source TCP window advertisement value = {row["swin"]}\n' + \
             f'Source TCP base sequence number = {row["stcpb"]}\n' + \
             f'Destination TCP base sequence number = {row["dtcpb"]}\n' + \
             f'Destination TCP window advertisement value = {row["dwin"]}\n' + \
             f'TCP connection setup round-trip time, the sum of synack and ackdat = {row["tcprtt"]}\n' + \
             f'TCP connection setup time, the time between the SYN and the SYN_ACK packets = {row["synack"]}\n' + \
             f'TCP connection setup time, the time between the SYN_ACK and the ACK packets = {row["ackdat"]}\n' + \
             f'Mean of the packet size transmitted by the src = {row["smean"]}\n' + \
             f'Mean of the packet size transmitted by the dst = {row["dmean"]}\n' + \
             f'Represents the pipelined depth into the connection of http ' + \
             f'request/response transaction = {row["trans_depth"]}\n' + \
             f'Actual uncompressed content size of the data transferred from the server http service = {row["response_body_len"]}\n' + \
             f'No. of connections that contain the same service (14) and source address ' + \
             f'(1) in 100 connections according to the last time (26). = {row["ct_srv_src"]}\n' + \
             f'No. for each state (6) according to specific range of values for ' + \
             f'source/destination time to live (10) (11). = {row["ct_state_ttl"]}\n' + \
             f'No. of connections of the same destination address (3) in 100 ' + \
             f'connections according to the last time (26). = {row["ct_dst_ltm"]}\n' + \
             f'No of connections of the same source address (1) and the destination ' + \
             f'port (4) in 100 connections according to the last time (26). = ' + \
             f'{row["ct_src_dport_ltm"]}\n' + \
             f'No of connections of the same destination address (3) and the source ' + \
             f'port (2) in 100 connections according to the last time (26). = ' + \
             f'{row["ct_dst_sport_ltm"]}\n' + \
             f'No of connections of the same source (1) and the destination (3) address ' + \
             f'in in 100 connections according to the last time (26). = {row["ct_dst_src_ltm"]}\n' + \
             f'If the ftp session is accessed by user and password then 1 else 0.  = ' + \
             f'{row["is_ftp_login"]}\n' + \
             f'No of flows that has a command in ftp session. = {row["ct_ftp_cmd"]}\n' + \
             f'No. of flows that has methods such as Get and Post in http service. = ' + \
             f'{row["ct_flw_http_mthd"]}\n' + \
             f'No. of connections of the same source address in 100 connections according to the last time = {row["ct_src_ltm"]}\n' + \
             f'No. of connections that contain the same service (14) and destination ' + \
             f'address (3) in 100 connections according to the last time (26). = ' + \
             f'{row["ct_srv_dst"]}\n' + \
             f'If source and destination IP addresses equal and port numbers equal then, this variable takes value 1 else 0 = {row["is_sm_ips_ports"]}\n'

def prompt_beth(row):
    return f"""
seconds since system boot = {row['timestamp']}
integer label for the process spawning this log = {row['processId']}
integer label for the thread spawning this log = {row['threadId']}
parent's integer label for the process spawning this log = {row['parentProcessId']}
Login integer ID of user spawning this log = {row['userId']}
Set mounting restrictions this process log works within = {row['mountNamespace']}
String command executed = {row['processName']}
Name of host server = {row['hostName']}
ID for the event generating this log = {row['eventId']}
Name of the event generating this log = {row['eventName']}
stack memory addresses relevant to the process = {row['stackAddresses']}
number of args = {row['argsNum']}
Value returned from this event log (usually 0) = {row['returnValue']}
List of arguments passed to this process = {row['args']}
"""


def extract_json(text):
    jsonstr = ''
    brackets = 0
    for c in text:
        if c == '{':
            brackets += 1
            jsonstr += c
        elif c == '}':
            brackets -= 1
            jsonstr += c
            if brackets == 0:
                break
        elif brackets > 0:
            jsonstr += c

    return json.loads(jsonstr)