import sys
import argparse
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="TaskFlow Password Generator - Multi-Mode CLI/GUI")
    parser.add_argument("--cli", action="store_true", help="Launch in command-line CLI mode")
    args = parser.parse_args()

    if args.cli:
        from cli_generator import run_cli_generator
        try:
            run_cli_generator()
        except KeyboardInterrupt:
            print("\nGenerator closed. Goodbye!")
            sys.exit(0)
    else:
        # Default Tkinter GUI launching
        from gui_generator import GUIPasswordGenerator
        try:
            root = tk.Tk()
            app = GUIPasswordGenerator(root)
            app.pack(fill="both", expand=True)
            root.mainloop()
        except Exception as e:
            print(f"❌ Error launching GUI Mode: {e}")
            print("Falling back to CLI Mode...\n")
            from cli_generator import run_cli_generator
            run_cli_generator()

if __name__ == "__main__":
    main()
