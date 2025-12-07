import os
from dotenv import load_dotenv
from datapizza.agents import Agent  # type: ignore
from datapizza.clients import ClientFactory  # type: ignore
from tools import peek_tools

# Load environment variables
load_dotenv()


def get_peek_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in .env file")

    # 1. "Frugal" System Prompt
    system_instruction = """
    You are the Peek-a-Boo Agent. Your creed is token saving.
    NEVER read an entire file unless strictly necessary.

    Standard operating procedure:
    1. ListFiles -> Orient yourself in the current directory.
    2. FindFiles -> Search for files by pattern (*.env, *secret*, *.py) across the tree.
    3. ReadPreview -> Understand the structure of interesting files (head+tail).
    4. GrepSearch -> Search keyword in ONE specific file.
    5. GrepRecursive -> Search keyword in ALL files of a directory.

    Surgical strategy:
    - Looking for a file type (e.g. config): use FindFiles with pattern.
    - Looking for a keyword in a known file: use GrepSearch.
    - Looking for a keyword but don't know where: use GrepRecursive.
    - REGEX support: pass use_regex=True for complex patterns (e.g. "sk_live_[0-9]+").

    Example: "find the Stripe API key"
    -> GrepRecursive(directory=".", keyword="sk_live_", pattern="*.env")
    DO NOT read entire files!
    """

    # 2. Client Configuration for Google Gemini
    client = ClientFactory.create(
        provider="google",
        api_key=api_key,
        model="gemini-2.0-flash-exp",  # Fast and economical, perfect for tools
        system_prompt=system_instruction,
        temperature=0.0  # We want precision, not creativity
    )

    # 3. Agent Creation
    agent = Agent(
        name="Minimalist Auditor",
        client=client,
        tools=peek_tools,
        system_prompt=system_instruction
    )

    return agent
