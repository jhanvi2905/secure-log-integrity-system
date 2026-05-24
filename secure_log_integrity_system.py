import hashlib
from datetime import datetime


# -------- LOG CLASS --------
class Log:
    def __init__(self, index, event_type, desc, prev_hash):
        self.index = index
        self.event_type = event_type
        self.desc = desc
        self.prev_hash = prev_hash

        # FIXED TIMESTAMP (with milliseconds)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        self.hash = self.generate_hash()

    def generate_hash(self):
        data = (
            str(self.index)
            + self.timestamp
            + self.event_type
            + self.desc
            + self.prev_hash
        )
        return hashlib.sha256(data.encode()).hexdigest()


# -------- LOG SYSTEM --------
class LogSystem:
    def __init__(self):
        self.logs = []

    # ADD LOG
    def add_log(self):
        event = input("Enter event type: ")
        desc = input("Enter description: ")

        prev_hash = self.logs[-1].hash if self.logs else "0"

        new_log = Log(len(self.logs), event, desc, prev_hash)
        self.logs.append(new_log)

        print("Log added.\n")

    # SHOW LOGS
    def show_logs(self):
        if not self.logs:
            print("No logs available.\n")
            return

        print("\n====== LOGS ======")
        for log in self.logs:
            print("\n------------------")
            print("Index:", log.index)
            print("Time:", log.timestamp)
            print("Event:", log.event_type)
            print("Description:", log.desc)
            print("Hash:", log.hash[:15], "...")
            print("Prev Hash:", log.prev_hash[:15], "...")

    # VERIFY INTEGRITY
    def verify_logs(self):
        print("\nChecking integrity...\n")

        for i in range(len(self.logs)):
            curr = self.logs[i]

            # detect modification
            if curr.hash != curr.generate_hash():
                return f"❌ Log {i} modified (data tampered)"

            # detect reordering
            if curr.index != i:
                return f"❌ Log order changed at position {i}"

            # detect deletion / chain break
            if i > 0:
                prev = self.logs[i - 1]
                if curr.prev_hash != prev.hash:
                    return f"❌ Chain broken at log {i} (possible deletion)"

        return "✅ All logs are secure"

    # FULLY DYNAMIC TAMPER
    def tamper_log(self):
        if not self.logs:
            print("No logs available.\n")
            return

        self.show_logs()

        try:
            idx = int(input("\nEnter log index to tamper: "))

            if idx < 0 or idx >= len(self.logs):
                print("Invalid index\n")
                return

            log = self.logs[idx]

            print("\nWhat do you want to change?")
            print("1. Event Type")
            print("2. Description")
            print("3. Timestamp")
            print("4. Index (reordering test)")

            choice = input("Choice: ")

            if choice == "1":
                print("Before:", log.event_type)
                log.event_type = input("New event type: ")
                print("After:", log.event_type)

            elif choice == "2":
                print("Before:", log.desc)
                log.desc = input("New description: ")
                print("After:", log.desc)

            elif choice == "3":
                print("Before:", log.timestamp)
                log.timestamp = input("New timestamp: ")
                print("After:", log.timestamp)

            elif choice == "4":
                print("Before:", log.index)
                log.index = int(input("New index: "))
                print("After:", log.index)

            else:
                print("Invalid choice\n")
                return

            print("\nTampering completed.\n")

        except:
            print("Invalid input\n")


# -------- MAIN MENU --------
def main():
    system = LogSystem()

    while True:
        print("\n====== MENU ======")
        print("1. Add Log")
        print("2. View Logs")
        print("3. Verify Integrity")
        print("4. Tamper Log")
        print("5. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            system.add_log()

        elif ch == "2":
            system.show_logs()

        elif ch == "3":
            print(system.verify_logs())

        elif ch == "4":
            system.tamper_log()

        elif ch == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice\n")


if __name__ == "__main__":
    main() 