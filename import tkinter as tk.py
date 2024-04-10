import tkinter as tk
import sys

class CRC:
    def __init__(self, polynomial):
        self.polynomial = polynomial

    def encode(self, data):
        # Data Padding
        padded_data = data + [0] * (len(self.polynomial) - 1)
        # Perform CRC Calculation
        remainder = self.polynomial_division(padded_data, self.polynomial)[1]
        # Append CRC to Data
        return data + remainder

    def decode(self, received_data):
        # Perform CRC Decoding
        _, remainder = self.polynomial_division(received_data, self.polynomial)
        # Check for Errors
        return any(remainder)

    def polynomial_division(self, dividend, divisor):
        # Perform polynomial division
        remainder = list(dividend)
        while len(remainder) >= len(divisor):
            # Calculate the next remainder
            for i in range(len(divisor)):
                remainder[i] ^= divisor[i]
            # Remove leading zeros
            while remainder and remainder[0] == 0:
                remainder.pop(0)
        return dividend[:-len(remainder)], remainder

def simulate_errors(data, error_rate):
    import random
    num_errors = int(error_rate * len(data))
    error_indices = random.sample(range(len(data)), num_errors)
    for i in error_indices:
        data[i] ^= 1  # Flip the bit

# Function to print text in a box format
def print_box(text):
    width = len(text) + 4
    print("*" * width)
    print("* " + text + " *")
    print("*" * width)

# Create GUI window
window = tk.Tk()
window.title("Error Detection and Correction")

# Input field for binary data
data_entry = tk.Entry(window, width=50)
data_entry.grid(row=0, column=0, padx=10, pady=10)

# Label for polynomial
polynomial_label = tk.Label(window, text="Polynomial:")
polynomial_label.grid(row=1, column=0, padx=10, pady=5)

# Input field for polynomial
polynomial_entry = tk.Entry(window, width=10)
polynomial_entry.grid(row=1, column=1, padx=10, pady=5)

# Button to encode data with CRC
encode_button = tk.Button(window, text="Encode Data")
encode_button.grid(row=2, column=0, padx=10, pady=10)

# Output field for encoded data
encoded_data_entry = tk.Entry(window, width=50)
encoded_data_entry.grid(row=3, column=0, padx=10, pady=10)

# Button to simulate errors
error_button = tk.Button(window, text="Simulate Errors")
error_button.grid(row=4, column=0, padx=10, pady=10)

# Output field for error detection
error_entry = tk.Entry(window, width=50)
error_entry.grid(row=5, column=0, padx=10, pady=10)

# Function to encode data with CRC
def encode_data():
    polynomial = [int(x) for x in polynomial_entry.get().split()]
    crc = CRC(polynomial)
    data = [int(x) for x in data_entry.get()]
    encoded_data = crc.encode(data)
    encoded_data_entry.delete(0, tk.END)
    encoded_data_entry.insert(0, encoded_data)

# Function to simulateerrors and detect them
def simulate_and_detect_errors():
    polynomial = [int(x) for x in polynomial_entry.get().split()]
    crc = CRC(polynomial)
    data = [int(x) for x in data_entry.get()]
    encoded_data = crc.encode(data)
    simulate_errors(encoded_data, error_rate=0.1)  # Simulate 10% error rate
    error_detected = crc.decode(encoded_data)
    error_entry.delete(0, tk.END)
    error_entry.insert(0, "Errors detected." if error_detected else "No errors detected.")

# Bind button commands
encode_button.config(command=encode_data)
error_button.config(command=simulate_and_detect_errors)

# Run the GUI
window.mainloop()