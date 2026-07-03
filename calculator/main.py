import sys
import argparse
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="TaskFlow Calculator - Multi-Mode CLI/GUI")
    parser.add_argument("--cli", action="store_true", help="Launch the calculator in CLI mode")
    args = parser.parse_args()

    if args.cli:
        from cli_calc import run_cli_calculator
        try:
            run_cli_calculator()
        except KeyboardInterrupt:
            print("\nCalculator closed. Goodbye!")
            sys.exit(0)
    else:
        # Defaults to launching Tkinter visual mode
        from gui_calc import GUICalculator
        try:
            root = tk.Tk()
            app = GUICalculator(root)
            root.mainloop()
        except Exception as e:
            print(f"❌ Error launching GUI Mode: {e}")
            print("Falling back to CLI Mode...\n")
            from cli_calc import run_cli_calculator
            run_cli_calculator()

if __name__ == "__main__":
    main()
