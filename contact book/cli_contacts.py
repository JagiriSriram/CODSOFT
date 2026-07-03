from db_contacts import ContactDatabase
import sys

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                 ⚡ CONTACT BOOK ⚡                   ║
    ║             Interactive Command Line Mode            ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def get_non_empty_input(prompt_text, error_msg="Field cannot be empty!"):
    while True:
        val = input(prompt_text).strip()
        if val.lower() in ['q', 'exit', 'quit']:
            print("\nExiting Contact Book. Goodbye!")
            sys.exit(0)
        if val:
            return val
        print(f"❌ {error_msg}")

def get_optional_input(prompt_text):
    val = input(prompt_text).strip()
    if val.lower() in ['q', 'exit', 'quit']:
        print("\nExiting Contact Book. Goodbye!")
        sys.exit(0)
    return val

def display_contact_details(contact):
    print("─"*40)
    print(f"  🧑 Name:    {contact['name']}")
    print(f"  📞 Phone:   {contact['phone']}")
    print(f"  📧 Email:   {contact['email'] if contact['email'] else 'Not set'}")
    print(f"  🏠 Address: {contact['address'] if contact['address'] else 'Not set'}")
    print(f"  📅 Created: {contact['created_at']}")
    print("─"*40)

def run_cli_contacts():
    db = ContactDatabase()
    print_banner()
    print("Type 'q' or 'exit' at any prompt to quit.\n")

    while True:
        print("Menu Operations:")
        print("  [1] View All Contacts")
        print("  [2] Add New Contact")
        print("  [3] Search Contact")
        print("  [4] Update Contact Details")
        print("  [5] Delete Contact")
        print("  [Q] Quit")
        
        choice = input("\nEnter choice (1-5 or Q): ").strip().lower()
        if choice in ['q', 'quit', 'exit']:
            print("\nExiting Contact Book. Goodbye!")
            break

        if choice == '1':
            contacts = db.get_contacts()
            print("\n" + "═"*54)
            print("  📂 SAVED CONTACTS LIST:")
            if not contacts:
                print("  (No contacts saved yet)")
            else:
                print(f"  {'ID':<5} {'NAME':<24} {'PHONE':<15}")
                print("  " + "─"*48)
                for c in contacts:
                    print(f"  {f'[{c['id']}]':<5} {c['name']:<24} {c['phone']:<15}")
            print("═"*54 + "\n")

        elif choice == '2':
            print("\n--- Add New Contact ---")
            name = get_non_empty_input("Enter Name*: ", "Name is required!")
            phone = get_non_empty_input("Enter Phone Number*: ", "Phone number is required!")
            email = get_optional_input("Enter Email: ")
            address = get_optional_input("Enter Address: ")
            
            db.add_contact(name, phone, email, address)
            print(f"\n✓ Contact '{name}' added successfully!\n")

        elif choice == '3':
            query = get_non_empty_input("\nEnter name or phone to search: ")
            matches = db.get_contacts(search_query=query)
            print("\n" + "═"*54)
            print(f"  🔍 SEARCH MATCHES FOR '{query}':")
            if not matches:
                print("  No matching contacts found.")
            else:
                for c in matches:
                    display_contact_details(c)
            print("═"*54 + "\n")

        elif choice == '4':
            # List all first to check ID
            contacts = db.get_contacts()
            if not contacts:
                print("\n❌ No contacts available to update.\n")
                continue

            print("\nSelect ID of the contact to update:")
            for c in contacts:
                print(f"  [{c['id']}] {c['name']} ({c['phone']})")
                
            id_input = get_non_empty_input("\nEnter Contact ID: ")
            try:
                contact_id = int(id_input)
            except ValueError:
                print("❌ Invalid ID format!\n")
                continue
                
            contact = db.get_contact(contact_id)
            if not contact:
                print("❌ Contact with that ID does not exist!\n")
                continue

            print(f"\nEditing Details for '{contact['name']}' (leave empty to keep current):")
            name = input(f"Name ({contact['name']}): ").strip() or contact['name']
            phone = input(f"Phone ({contact['phone']}): ").strip() or contact['phone']
            email = input(f"Email ({contact['email']}): ").strip() or contact['email']
            address = input(f"Address ({contact['address']}): ").strip() or contact['address']
            
            db.update_contact(contact_id, name, phone, email, address)
            print(f"\n✓ Contact updated successfully!\n")

        elif choice == '5':
            # List all first
            contacts = db.get_contacts()
            if not contacts:
                print("\n❌ No contacts available to delete.\n")
                continue

            print("\nSelect ID of the contact to delete:")
            for c in contacts:
                print(f"  [{c['id']}] {c['name']} ({c['phone']})")

            id_input = get_non_empty_input("\nEnter Contact ID: ")
            try:
                contact_id = int(id_input)
            except ValueError:
                print("❌ Invalid ID format!\n")
                continue

            contact = db.get_contact(contact_id)
            if not contact:
                print("❌ Contact with that ID does not exist!\n")
                continue

            confirm = input(f"Are you sure you want to delete '{contact['name']}'? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                db.delete_contact(contact_id)
                print(f"\n✓ Contact '{contact['name']}' deleted.\n")
            else:
                print("\nDeletion cancelled.\n")
        else:
            print("❌ Invalid menu choice! Please enter a number 1 to 5, or Q.\n")

if __name__ == "__main__":
    try:
        run_cli_contacts()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
