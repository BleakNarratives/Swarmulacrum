"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: interactive_guide.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import os
import sys
import json

def clear_screen():
    os.system('clear')

# Load UI config
with open("ui_config.json", "r") as f:
    config = json.load(f)["wizard"]

def get_binary_choice(question):
    while True:
        choice = input(f"\n{question} (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("[-] Please enter 'y' for Yes or 'n' for No.")

def run_wizard():
    clear_screen()
    print("=" * 60)
    print(f"        {config['title']}")
    print("=" * 60)
    print(config['description'])
    print("-" * 60)

    # Questions
    print("\n[Step 1: The Actor]")
    color_of_law = get_binary_choice(config['steps']['STEP_1'])

    print("\n[Step 2: The Action]")
    deprivation = get_binary_choice(config['steps']['STEP_2'])

    print("\n[Step 3: Public Trust]")
    duty = get_binary_choice(config['steps']['STEP_3'])

    print("\n[Step 4: The Violation]")
    misconduct = get_binary_choice(config['steps']['STEP_4'])

    # Process and display results
    clear_screen()
    print("=" * 60)
    print(f"                    {config['results']['TITLE']}")
    print("=" * 60)

    # 42 USC 1983 Evaluation
    print(f"\n--> {config['results']['CLAIM_1983']}:")
    if color_of_law and deprivation:
        print(f"    [CAN HAPPEN]: {config['results']['CAN_1983']}")
    else:
        print(f"    [CANNOT HAPPEN]: {config['results']['CANNOT_1983']}")

    # Oath Evaluation
    print(f"\n--> {config['results']['CLAIM_OATH']}:")
    if duty and misconduct:
        print(f"    [CAN HAPPEN]: {config['results']['CAN_OATH']}")
    else:
        print(f"    [CANNOT HAPPEN]: {config['results']['CANNOT_OATH']}")

    print("\n" + "=" * 60)
    input("\nPress Enter to exit the guide...")

if __name__ == "__main__":
    run_wizard()
