#!/bin/bash

# Setup the GPIO pin for the LED
LED_PIN=17
# Setup the GPIO pin to output mode
gpio -g mode $LED_PIN out # -g GPIO numbering set to output

# Function to handle ping packets
check_Ping() {
    local data=$1 # assign the first argument to this local variable

    if [[ "$data" == *"aaaa"* ]]; then # * * wildcard characters that check pattern in data
        # Turn the LED on
        gpio -g write $LED_PIN 1
        echo "LED turned ON."
    elif [[ "$data" == *"bbbb"* ]]; then
        # Turn the LED off
        gpio -g write $LED_PIN 0
        echo "LED turned OFF."
    else
        # Print message if the pattern does not match
        echo "PING message received: $data"
    fi
}

# Use tcpdump to capture incoming ICMP packets and filter out the byte data
# Listen to incoming packets, and look for the data payload in hex format
# -i: interface -n: does not resolve hostnames or service names -vvv: shows all packet info
# -X: display contents in both hex and ASCII; icmp[0] == 8 filters only echo request header is 8
# /dev/null: discard unwanted errors
sudo tcpdump -i wlan0 -n -vvv -X icmp and 'icmp[0] == 8' 2>/dev/null | while read -r line; do
    # Extract the byte data in hex form (search for the payload after 0x)
    if [[ "$line" =~ (0x[0-9a-fA-F]{2}.*) ]]; then
        data="${BASH_REMATCH[1]}" #store the string

        # Remove the initial 0x prefix for easier comparison
        data="${data//0x/}"

        # Call the handle_ping function with the extracted data
        check_Ping "$data"
    fi
done
