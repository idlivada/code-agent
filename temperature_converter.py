#!/usr/bin/env python3
"""
Temperature Converter

A simple command-line utility to convert temperatures between Celsius and Fahrenheit.
This module provides functions for converting temperatures and a command-line interface
for user interaction.

Functions:
    celsius_to_fahrenheit(celsius): Convert Celsius to Fahrenheit
    fahrenheit_to_celsius(fahrenheit): Convert Fahrenheit to Celsius
    main(): Run the interactive command-line interface
"""

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def main():
    """
    Run the interactive temperature conversion command-line interface.
    
    This function presents a menu to the user with options to:
    1. Convert from Celsius to Fahrenheit
    2. Convert from Fahrenheit to Celsius
    3. Exit the program
    
    The function handles user input validation and provides formatted output
    with temperatures rounded to 2 decimal places.
    """
    print("Temperature Converter")
    print("====================")
    
    while True:
        print("\nSelect an option:")
        print("1. Convert Celsius to Fahrenheit")
        print("2. Convert Fahrenheit to Celsius")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            try:
                celsius = float(input("Enter temperature in Celsius: "))
                fahrenheit = celsius_to_fahrenheit(celsius)
                print(f"{celsius}°C is equal to {fahrenheit:.2f}°F")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == '2':
            try:
                fahrenheit = float(input("Enter temperature in Fahrenheit: "))
                celsius = fahrenheit_to_celsius(fahrenheit)
                print(f"{fahrenheit}°F is equal to {celsius:.2f}°C")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == '3':
            print("Thank you for using the Temperature Converter. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()