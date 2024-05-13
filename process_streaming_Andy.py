"""

Streaming Process: Uses port 9999

Create a fake stream of data. 

Important! 

We'll stream forever - or until we read the end of the file. 
Use use Ctrl-C to stop. (Hit Control key and c key at the same time.)

Explore more at 
https://wiki.python.org/moin/UdpCommunication

"""
import csv
import socket
import time
import logging

# Set up basic configuration for logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "Overdose.csv"
OUTPUT_FILE_NAME = "out9.txt"

def prepare_message_from_row(row):
    State, Year, Month, Period, Indicator, DataValue, PercentComplete, PercentPendingInvestigation, StateName, Footnote, FootnoteSymbol, PredictedValue = row
    """Prepare a binary message from a given row."""
    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
    fstring_message = f"[{State}, {Year}, {Month}, {Period}, {Indicator}, {DataValue}, {PercentComplete}, {PercentPendingInvestigation}, {StateName}, {Footnote}, {FootnoteSymbol}, {PredictedValue}]"

    # prepare a binary (1s and 0s) message to stream
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE


def stream_row(input_file_name, output_file_name, address_tuple):
    """Read from input file and stream data."""
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")

    # Create a file object for input (r = read access)
    with open(input_file_name, "r") as input_file, open(output_file_name, "w", newline="") as output_file:
        logging.info(f"Opened for reading: {input_file_name}.")
        logging.info(f"Opened for writing: {output_file_name}.")
        # Create a CSV reader object
        reader = csv.reader(input_file, delimiter=",")
        # Create a CSV writer object
        writer = csv.writer(output_file, delimiter=",")
        # Write the header row to the output file
        writer.writerow(["State", "Year", 'Month', 'Period', 'Indicator', 'DataValue', 'PercentComplete', 'PercentPendingInvestigation', 'StateName', 'Footnote', 'FootnoteSymbol', 'PredictedValue'])

        header = next(reader)  # Skip header row
        logging.info(f"Skipped header row: {header}")

        # use socket enumerated types to configure our socket object
        # Set our address family to (IPV4) for 'internet'
        # Set our socket type to UDP (datagram)
        ADDRESS_FAMILY = socket.AF_INET 
        SOCKET_TYPE = socket.SOCK_DGRAM 

        # Call the socket constructor, socket.socket()
        # A constructor is a special method with the same name as the class
        # Use the constructor to make a socket object
        # and assign it to a variable named `sock_object`
        sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)
        
        for row in reader:
            State, Year, Month, Period, Indicator, DataValue, PercentComplete, PercentPendingInvestigation, StateName, Footnote, FootnoteSymbol, PredictedValue = row
            MESSAGE = prepare_message_from_row(row)
            sock_object.sendto(MESSAGE, address_tuple)
            logging.info(f"Sent: {MESSAGE} on port {PORT}. Hit CTRL-c to stop.")
            writer.writerow([State, Year, Month, Period, Indicator, DataValue, PercentComplete, PercentPendingInvestigation, StateName, Footnote, FootnoteSymbol, PredictedValue])  
            logging.info(f"Line written to output. Hit CTRL-c to stop.")
            time.sleep(3) # wait 3 seconds between messages

if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, OUTPUT_FILE_NAME, ADDRESS_TUPLE)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

