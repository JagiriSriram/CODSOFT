import sys
import argparse
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="Contact Book - Multi-Mode CLI/GUI")
    parser.add_argument("--cli", action="store_true", help="Launch in command-line CLI mode")
    args = parser.parse_args()

    if args.cli:
        from cli_contacts import run_cli_contacts
        try:
            run_cli_contacts()
        except KeyboardInterrupt:
            print("\nContact Book closed. Goodbye!")
            sys.exit(0)
    else:
        # Default Tkinter GUI launching
        from gui_contacts import GUIContacts
        try:
            root = tk.Tk()
            app = GUIContacts(root)
            app.pack(fill="both", expand=True)
            root.mainloop()
        except Exception as e:
            print(f"❌ Error launching GUI Mode: {e}")
            print("Falling back to CLI Mode...\n")
            from cli_contacts import run_cli_contacts
            run_cli_contacts()

if __name__ == "__main__":
    main()
