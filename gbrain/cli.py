"""Command-line interface for Gbrain."""

import argparse
import sys
from gbrain import BrainManager


def main():
    parser = argparse.ArgumentParser(
        prog="gbrain",
        description="Gbrain - Go-based brain/chat bot framework.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gbrain list
  gbrain new "My Conversation"
  gbrain chat <conversation-id>
  gbrain send <conversation-id> "Hello, Gbrain!"
  gbrain history <conversation-id> --limit 20
  gbrain switch <conversation-id>
  gbrain current
  gbrain delete <conversation-id>
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    list_parser = subparsers.add_parser("list", help="List all conversations")

    # new command
    new_parser = subparsers.add_parser("new", help="Create a new conversation")
    new_parser.add_argument("title", nargs="?", default="", help="Conversation title")

    # chat command
    chat_parser = subparsers.add_parser("chat", help="Start interactive chat")
    chat_parser.add_argument("conversation_id", nargs="?", default="", help="Conversation ID")

    # send command
    send_parser = subparsers.add_parser("send", help="Send a message")
    send_parser.add_argument("conversation_id", help="Conversation ID")
    send_parser.add_argument("message", help="Message content")

    # reply command
    reply_parser = subparsers.add_parser("reply", help="Add an assistant reply")
    reply_parser.add_argument("conversation_id", help="Conversation ID")
    reply_parser.add_argument("message", help="Reply content")

    # history command
    history_parser = subparsers.add_parser("history", help="Show conversation history")
    history_parser.add_argument("conversation_id", help="Conversation ID")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of messages")

    # switch command
    switch_parser = subparsers.add_parser("switch", help="Switch to a conversation")
    switch_parser.add_argument("conversation_id", help="Conversation ID")

    # current command
    current_parser = subparsers.add_parser("current", help="Show current conversation")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a conversation")
    delete_parser.add_argument("conversation_id", help="Conversation ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    manager = BrainManager()

    if args.command == "list":
        conversations = manager.list_conversations()
        if not conversations:
            print("No conversations found.")
            return
        current = manager.current_conversation
        for c in conversations:
            marker = " (current)" if c.id == current else ""
            print(f"{c.id} - {c.title}{marker}")
            print(f"  Messages: {len(c.messages)}")
            print(f"  Updated: {c.updated_at}")
            print()

    elif args.command == "new":
        conv = manager.create_conversation(args.title)
        print(f"Created conversation: {conv.id} - {conv.title}")

    elif args.command == "chat":
        if args.conversation_id:
            conv = manager.switch_conversation(args.conversation_id)
            if not conv:
                print(f"Conversation '{args.conversation_id}' not found.")
                sys.exit(1)
        else:
            conv = manager.get_current_conversation()
            if not conv:
                print("No conversation. Create one with 'gbrain new'.")
                sys.exit(1)

        print(f"Chatting in: {conv.title} [{conv.id}]")
        print("Type 'exit' or 'quit' to leave.\n")
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("Goodbye!")
                    break
                if not user_input:
                    continue
                manager.send_message(conv.id, user_input)
                print("(Message sent. Use 'gbrain reply' to add assistant response.)")
            except EOFError:
                break

    elif args.command == "send":
        msg = manager.send_message(args.conversation_id, args.message)
        if msg:
            print(f"Sent: {msg.content}")
        else:
            print(f"Conversation '{args.conversation_id}' not found.")
            sys.exit(1)

    elif args.command == "reply":
        msg = manager.reply(args.conversation_id, args.message)
        if msg:
            print(f"Replied: {msg.content}")
        else:
            print(f"Conversation '{args.conversation_id}' not found.")
            sys.exit(1)

    elif args.command == "history":
        conv = manager.get_conversation(args.conversation_id)
        if not conv:
            print(f"Conversation '{args.conversation_id}' not found.")
            sys.exit(1)
        history = conv.get_history(args.limit)
        for msg in history:
            role = "You" if msg.role == "user" else "Gbrain"
            print(f"{role}: {msg.content}")
            print()

    elif args.command == "switch":
        success = manager.switch_conversation(args.conversation_id)
        if success:
            print(f"Switched to conversation '{args.conversation_id}'.")
        else:
            print(f"Conversation '{args.conversation_id}' not found.")
            sys.exit(1)

    elif args.command == "current":
        conv = manager.get_current_conversation()
        if conv:
            print(f"Current: {conv.title} [{conv.id}]")
            print(f"Messages: {len(conv.messages)}")
        else:
            print("No current conversation.")

    elif args.command == "delete":
        success = manager.delete_conversation(args.conversation_id)
        if success:
            print(f"Deleted conversation '{args.conversation_id}'.")
        else:
            print(f"Conversation '{args.conversation_id}' not found.")
            sys.exit(1)


if __name__ == "__main__":
    main()
