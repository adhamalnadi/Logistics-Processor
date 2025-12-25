"""
 Name: Adham Alnadi
 ID: 201811041
 
 Course: Python Programming
 Assignment: Logistics Data Processor

 Date: 2025-12-25
 Description: A program to process logistics shipment data from a text file.
 GitHub Repository: https://github.com/adhamalnadi/Logistics-Processor.git

"""

from typing import List, Dict
import os


class ShipmentProcessor:

    #A class to process shipment data from text files.


    def __init__(self, filename: str):
        self.filename = filename
        self.shipments: List[Dict] = []


    # File Reading

    def read_shipments(self) -> None:

       # Reads shipment data from the file and stores it as a list of dictionaries.

        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"File '{self.filename}' not found.")

        self.shipments.clear()

        with open(self.filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                try:
                    shipment_id, origin, destination, weight, status = line.split(",")
                    self.shipments.append({
                        "id": shipment_id,
                        "origin": origin,
                        "destination": destination,
                        "weight": float(weight),
                        "status": status
                    })
                except ValueError:
                    print(f"Skipping invalid line: {line}")


    # Filtering

    def filter_by_weight(self, min_weight: float) -> List[Dict]:

        #Returns shipments with weight above the given threshold.

        return [s for s in self.shipments if s["weight"] > min_weight]

    def filter_by_status(self, status: str) -> List[Dict]:

        #Returns shipments matching the given status.

        return [s for s in self.shipments if s["status"].lower() == status.lower()]


    # Update Records
    # ->   its a type hint that I learn it this week this give the
    # compiler the type of dataType the function should return

    def update_status(self, shipment_id: str, new_status: str) -> bool:
        """
        Updates the status of a shipment by ID.
        Returns True if updated, False if not found.
        """
        for shipment in self.shipments:
            if shipment["id"] == shipment_id:
                shipment["status"] = new_status
                return True
        return False

    # Report Generation

    def generate_report(self, output_file: str) -> None:

        #Generates a summary report and saves it to a file.

        total_shipments = len(self.shipments)
        if total_shipments == 0:
            raise ValueError("No shipment data available.")

        status_count = {}
        total_weight = 0

        for shipment in self.shipments:
            status = shipment["status"]
            status_count[status] = status_count.get(status, 0) + 1
            total_weight += shipment["weight"]

        avg_weight = total_weight / total_shipments

        with open(output_file, "w") as file:
            file.write("Shipment Report\n")
            file.write("-----------------\n")
            file.write(f"Total Shipments: {total_shipments}\n\n")

            file.write("Shipments by Status:\n")
            for status, count in status_count.items():
                file.write(f"- {status}: {count}\n")

            file.write(f"\nAverage Shipment Weight: {avg_weight:.2f}\n")

    # Save Updated Data

    def save_shipments(self) -> None:

        #Saves current shipment data back to the file.

        with open(self.filename, "w") as file:
            for s in self.shipments:
                file.write(
                    f"{s['id']},{s['origin']},{s['destination']},{s['weight']},{s['status']}\n"
                )



# Helper Functions

def display_shipments(shipments: List[Dict]) -> None:

   # Prints shipment records to the console.

    if not shipments:
        print("No records found.")
        return

    for s in shipments:
        print(f"{s['id']},{s['origin']},{s['destination']},{s['weight']},{s['status']}")



# Main Menu

def main():
    processor = ShipmentProcessor("./shipments.txt")

    try:
        processor.read_shipments()
    except Exception as e:
        print(e)
        return

    while True:
        print("\nWelcome to the Logistics Data Processor!")
        print("1. View shipments with weight above a certain value")
        print("2. View shipments by status")
        print("3. Update shipment status")
        print("4. Generate report")
        print("5. Exit")

        choice = input("> ")

        if choice == "1":
            weight = float(input("Enter the weight threshold: "))
            result = processor.filter_by_weight(weight)
            display_shipments(result)

        elif choice == "2":
            status = input("Enter shipment status: ")
            result = processor.filter_by_status(status)
            display_shipments(result)

        elif choice == "3":
            shipment_id = input("Enter shipment ID: ")
            new_status = input("Enter new status: ")
            if processor.update_status(shipment_id, new_status):
                processor.save_shipments()
                print("Shipment status updated successfully.")
            else:
                print("Shipment ID not found.")

        elif choice == "4":
            try:
                processor.generate_report("shipment_report.txt")
                print("Report generated: shipment_report.txt")
            except Exception as e:
                print(e)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")



# Entry Point

if __name__ == "__main__":
    main()
