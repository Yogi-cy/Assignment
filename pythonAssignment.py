import pandas as pd
from collections import Counter
import csv

logFile = 'sample.log'

def countRequestsByIp(logLines):
    """
    Counts the number of requests per IP address from the log lines.

    Args:
        logLines (list): List of log entries.

    Returns:
        pd.DataFrame: A sorted DataFrame with IP addresses and their request counts.
    """
    
    # initialize counter to count the request per IP
    requestCounter = Counter()
    for entry in logLines:
        try:
            ipAddress = entry.split(' ')[0]
            requestCounter[ipAddress] += 1
        except IndexError:
            # handling indexErrors in logLines gracefully
            continue

    # create a df from the counter
    ipRequestTable = pd.DataFrame(requestCounter.items(), columns=["IP Address", "Request Count"])
    ipRequestTable = ipRequestTable.sort_values(by="Request Count", ascending=False)

    # display the result for requests per ip address.
    print("Requests per IP: ")
    print(ipRequestTable.to_string(index=False))
    return ipRequestTable

def countRequestsByEndpoint(logLines):
    """
    Counts the number of requests per endpoint from the log lines.

    Args:
        logLines (list): List of log entries.

    Returns:
        pd.DataFrame: A sorted DataFrame with endpoints and their access counts.
    """

    # initialize counter to count the request per endpoint
    requestCounter = Counter()
    for logEntry in logLines:
        try:
            requestPart = logEntry.split('"')[1]
            endpoint = requestPart.split(' ')[1]
            requestCounter[endpoint] += 1
        except IndexError:
            # handling indexErrors in logLines gracefully
            continue

    # create a df from counter
    endpointAccessTable = pd.DataFrame(requestCounter.items(), columns=["Endpoint", "Access Count"])
    endpointAccessTable = endpointAccessTable.sort_values(by="Access Count", ascending=False)

    # display the result for the most frequently accessed endpoints.
    print("Most Accessed Endpoint: ")
    print(endpointAccessTable.to_string(index=False))
    return endpointAccessTable

def detectSuspiciousActivity(logLines, failureThreshold=10):
    """
    Detects potential brute force login attempts by flagging IP addresses 
    with failed login attempts exceeding a configurable threshold.

    Args:
        logLines (list): List of log entries from the log file.
        failureThreshold (int): The maximum allowed failed login attempts before flagging an IP address.

    Returns:
        pd.DataFrame: A DataFrame of flagged IP addresses and their failed login counts.
    """
    failedLoginCounter = Counter()

    # iterating logLines
    for logEntry in logLines:
        try:
            # extract Ip Address, statusCode and failureMessage.
            ipAddress = logEntry.split(' ')[0]
            statusCode = logEntry.split(' ')[-4]
            failureMessage = logEntry.split('"')[-2].strip()

            if statusCode == "401" or "Invalid credentials" in failureMessage:
                failedLoginCounter[ipAddress] += 1
        except IndexError:
            # handling indexErrors in logLines gracefully
            continue

    # filter Ip that exceeds the threshold
    flaggedIPs = {ip: count for ip, count in failedLoginCounter.items() if count > failureThreshold}

    # create df for filtered Ip
    flaggedIpTable = pd.DataFrame(flaggedIPs.items(), columns=["Ip Address", "Failed Login Count"])

    # display the result for the Suspecious Ips.
    if not flaggedIpTable.empty:
        print("Suspicious Activity: ")
        print(flaggedIpTable.to_string(index=False))
    else:
        print("No suspicious activity detected.")

    return flaggedIpTable


def main():
    """
    Main function to process the log file and display counts for IPs and endpoints.
    """
    try:
        # read the log file in main fucntion and pass the log lines, so that we do not read files in each function.
        with open(logFile, 'r') as file:
            logLines = file.readlines()

        if not logLines:
            print(f"The log file {logFile} is empty.")
            return

        # Calling the functions and passing the log lines.
        ipRequestTable = countRequestsByIp(logLines)
        endpointAccessTable = countRequestsByEndpoint(logLines)
        # default failureThreshold is 10.
        flaggedIpTable = detectSuspiciousActivity(logLines, failureThreshold=4)

        with open('log_analysis_results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # writing request per ip table 
            csvwriter.writerow(['Requests per IP: '])
            csvwriter.writerow(['IP Address', 'Request Count'])
            for row in ipRequestTable.itertuples(index=False):
                csvwriter.writerow(row)
            csvwriter.writerow([])  # blank space to separate the tables
            
            # writing most accessed endpoint table
            csvwriter.writerow(['Most Accessed Endpoint: '])
            csvwriter.writerow(['Endpoint', 'Access Count'])
            for row in endpointAccessTable.itertuples(index=False):
                csvwriter.writerow(row)
            csvwriter.writerow([])  # blank space to separate the tables
            
            # writing the suspecious activity table
            csvwriter.writerow(['Suspicious Activity: '])
            csvwriter.writerow(['IP Address', 'Failed Login Count'])
            for row in flaggedIpTable.itertuples(index=False):
                csvwriter.writerow(row)

    except FileNotFoundError:
        print(f"The file {logFile} does not exist.")
    except csv.Error as csvError:
        print(f"An error occurred while writing to the CSV file: {csvError}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
