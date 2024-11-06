
#!/bin/bash

# Set up the GPIO pin for the LED (assume GPIO pin 17 for this example)
LED_PIN=17
# Setup the GPIO pin to output mode
gpio -g mode $LED_PIN out

# Function to handle ping packets
handle_ping() {
    local data=$1

    if [[ "$data" == *"aaaa"* ]]; then
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
sudo tcpdump -i wlan0 -n -vvv -X icmp and 'icmp[0] == 8' 2>/dev/null | while read -r line; do
    # Extract the byte data in hex form (search for the payload after 0x)
    if [[ "$line" =~ (0x[0-9a-fA-F]{2}.*) ]]; then
        data="${BASH_REMATCH[1]}"

        # Remove the initial "0x" prefix for easier comparison
        data="${data//0x/}"

        # Call the handle_ping function with the extracted data
        handle_ping "$data"
    fi
done
