# main.py - Peek-a-Boo Test Suite
import os
import shutil
from agent import get_peek_agent


def create_labyrinth(base_dir: str = "messy_project"):
    """Create complex directory structure for testing."""
    # Clean up if exists
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    # Directory structure
    dirs = [
        f"{base_dir}/src/config/legacy",
        f"{base_dir}/src/utils",
        f"{base_dir}/logs",
        f"{base_dir}/tests",
        f"{base_dir}/docs",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 1. Decoy file in root
    with open(f"{base_dir}/README.md", "w") as f:
        f.write("# Legacy Project\n\nConfiguration is elsewhere.\n")

    # 2. HUGE log file (token trap)
    with open(f"{base_dir}/logs/app.log", "w") as f:
        for i in range(10000):
            f.write(f"[2024-01-{i%28+1:02d}] INFO: Processing request #{i}\n")

    # 3. Secret hidden deep in the tree
    with open(f"{base_dir}/src/config/legacy/.env.production", "w") as f:
        f.write("# Production configuration\n")
        f.write("DB_HOST=192.168.1.1\n")
        f.write("DB_PASSWORD=super_secret_db_pass\n")
        f.write("STRIPE_API_KEY=sk_live_999999999_SUPER_SECRET\n")
        f.write("AWS_SECRET_KEY=AKIAIOSFODNN7EXAMPLE\n")
        f.write("DEBUG=False\n")

    # 4. Python code with TODOs
    with open(f"{base_dir}/src/utils/helpers.py", "w") as f:
        f.write('''"""Utility functions."""

def calculate_total(items):
    # TODO: Add input validation
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

def format_currency(amount):
    # TODO: Support multiple currencies
    return f"${amount:.2f}"

def send_notification(user, message):
    # FIXME: Rate limiting is not working
    print(f"Sending to {user}: {message}")
    # TODO: Implement retry logic
''')

    # 5. Test file with issues
    with open(f"{base_dir}/tests/test_helpers.py", "w") as f:
        f.write('''import pytest
from src.utils.helpers import calculate_total

def test_calculate_total():
    # TODO: Add more test cases
    pass

def test_format_currency():
    # FIXME: Test fails with negative numbers
    pass
''')

    # 6. JSON config
    with open(f"{base_dir}/src/config/settings.json", "w") as f:
        f.write('''{
    "app_name": "MyApp",
    "version": "1.0.0",
    "api_endpoint": "https://api.example.com/v1",
    "max_retries": 3,
    "timeout": 30
}
''')

    # 7. Another log file
    with open(f"{base_dir}/logs/error.log", "w") as f:
        for i in range(5000):
            if i % 100 == 0:
                f.write(f"[ERROR] Connection timeout at {i}\n")
            else:
                f.write(f"[DEBUG] Request processed\n")

    print(f"Labyrinth created in '{base_dir}'")
    return base_dir


# --- TEST MISSIONS ---

MISSIONS = [
    {
        "name": "Find Stripe API Key",
        "prompt": """Explore 'messy_project'.
Find the Stripe API KEY (starts with 'sk_live_').
DO NOT read log files.""",
    },
    {
        "name": "Find all TODOs",
        "prompt": """Search for all TODO and FIXME in Python code in 'messy_project'.
Report file and line for each occurrence.""",
    },
    {
        "name": "Find API endpoint",
        "prompt": """Find the configured API endpoint in the 'messy_project'.
Search in configuration files (json, env, yaml).""",
    },
    {
        "name": "Find all credentials",
        "prompt": """Explore 'messy_project' and find ALL credentials/secrets:
- API keys
- Passwords
- Access keys
DO NOT read log files.""",
    },
]


def run_mission(agent, mission: dict):
    """Execute a single mission."""
    print(f"\n{'='*60}")
    print(f"MISSION: {mission['name']}")
    print(f"{'='*60}")
    print(f"Prompt: {mission['prompt'][:100]}...")

    try:
        result = agent.run(mission["prompt"])
        print(f"\nMission completed")
        return True
    except Exception as e:
        print(f"\nError: {e}")
        return False


def main():
    """Main entry point."""
    print("PEEK-A-BOO - Test Suite\n")

    # Setup
    base_dir = create_labyrinth()

    try:
        agent = get_peek_agent()

        # Choose which mission to run (or run all)
        print("\nAvailable missions:")
        for i, m in enumerate(MISSIONS):
            print(f"  {i+1}. {m['name']}")
        print("  0. Run ALL missions")

        choice = input("\nChoose mission (0-4) [default: 1]: ").strip() or "1"

        if choice == "0":
            # Run all
            for mission in MISSIONS:
                run_mission(agent, mission)
        else:
            # Run single
            idx = int(choice) - 1
            if 0 <= idx < len(MISSIONS):
                run_mission(agent, MISSIONS[idx])
            else:
                print("Invalid choice")
                return

        print("\n" + "="*60)
        print("Test completed")
        print("="*60)

    except Exception as e:
        print(f"Critical error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
