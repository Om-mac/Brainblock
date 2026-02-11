"""
BrainBlock CLI - Beautiful Terminal Interface
Interactive command-line for student IP protection
"""

import os
import sys
import time
from main import BrainBlock, Contributor


# ANSI Color Codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_CYAN = '\033[46m'


LOGO = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   ██████╗ ██████╗  █████╗ ██╗███╗   ██╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗  ║
    ║   ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝  ║
    ║   ██████╔╝██████╔╝███████║██║██╔██╗ ██║██████╔╝██║     ██║   ██║██║     █████╔╝   ║
    ║   ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗   ║
    ║   ██████╔╝██║  ██║██║  ██║██║██║ ╚████║██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗  ║
    ║   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝  ║
    ║                                                                  ║
    ║   {Colors.YELLOW}🧠 Protect Your Innovation with AI + Blockchain 🔗{Colors.CYAN}             ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
{Colors.END}
"""

MINI_LOGO = f"""
{Colors.CYAN}╭──────────────────────────────────────────╮
│  {Colors.BOLD}🧠 BRAINBLOCK{Colors.END}{Colors.CYAN} - Student IP Protection  │
╰──────────────────────────────────────────╯{Colors.END}
"""

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text, style="box"):
    """Print styled header"""
    if style == "box":
        width = len(text) + 4
        print(f"\n{Colors.CYAN}╭{'─' * width}╮")
        print(f"│  {Colors.BOLD}{text}{Colors.END}{Colors.CYAN}  │")
        print(f"╰{'─' * width}╯{Colors.END}\n")
    elif style == "line":
        print(f"\n{Colors.CYAN}{'─' * 50}{Colors.END}")
        print(f"{Colors.BOLD}{text}{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")


def animated_loading(text, duration=2):
    """Show animated loading"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.CYAN}{frames[i % len(frames)]} {text}...{Colors.END}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{Colors.GREEN}✓ {text} Complete!{Colors.END}     ")


def progress_bar(current, total, prefix="Progress", length=40):
    """Display progress bar"""
    filled = int(length * current / total)
    bar = f"{Colors.GREEN}{'█' * filled}{Colors.END}{'░' * (length - filled)}"
    percent = f"{100 * current / total:.1f}%"
    print(f"\r{prefix} |{bar}| {percent}", end="", flush=True)
    if current >= total:
        print()


def print_table(headers, rows, title=None):
    """Print formatted table"""
    if title:
        print(f"\n{Colors.BOLD}{title}{Colors.END}")
    
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Print header
    header_line = f"{Colors.CYAN}┌" + "┬".join("─" * (w + 2) for w in widths) + f"┐{Colors.END}"
    print(header_line)
    
    header_row = f"{Colors.CYAN}│{Colors.END}" + f"{Colors.CYAN}│{Colors.END}".join(
        f" {Colors.BOLD}{h.ljust(widths[i])}{Colors.END} " for i, h in enumerate(headers)
    ) + f"{Colors.CYAN}│{Colors.END}"
    print(header_row)
    
    separator = f"{Colors.CYAN}├" + "┼".join("─" * (w + 2) for w in widths) + f"┤{Colors.END}"
    print(separator)
    
    # Print rows
    for row in rows:
        row_str = f"{Colors.CYAN}│{Colors.END}" + f"{Colors.CYAN}│{Colors.END}".join(
            f" {str(cell).ljust(widths[i])} " for i, cell in enumerate(row)
        ) + f"{Colors.CYAN}│{Colors.END}"
        print(row_str)
    
    footer = f"{Colors.CYAN}└" + "┴".join("─" * (w + 2) for w in widths) + f"┘{Colors.END}"
    print(footer)


def print_card(title, content_dict, color=Colors.BLUE):
    """Print information card"""
    max_key_len = max(len(k) for k in content_dict.keys())
    max_val_len = max(len(str(v)) for v in content_dict.values())
    width = max(max_key_len + max_val_len + 5, len(title) + 4)
    
    print(f"\n{color}╭{'─' * width}╮{Colors.END}")
    print(f"{color}│{Colors.END} {Colors.BOLD}{title}{Colors.END}{' ' * (width - len(title) - 1)}{color}│{Colors.END}")
    print(f"{color}├{'─' * width}┤{Colors.END}")
    
    for key, value in content_dict.items():
        line = f"{key}: {Colors.WHITE}{value}{Colors.END}"
        padding = width - len(key) - len(str(value)) - 3
        print(f"{color}│{Colors.END} {line}{' ' * padding}{color}│{Colors.END}")
    
    print(f"{color}╰{'─' * width}╯{Colors.END}")


def get_input(prompt, default=None):
    """Get user input with styling"""
    if default:
        prompt = f"{prompt} [{Colors.CYAN}{default}{Colors.END}]"
    user_input = input(f"{Colors.YELLOW}➤ {Colors.END}{prompt}: ").strip()
    return user_input if user_input else default


def get_multiline_input(prompt):
    """Get multiline input"""
    print(f"{Colors.YELLOW}➤ {Colors.END}{prompt}")
    print(f"  {Colors.CYAN}(Enter content, then press Enter twice to finish){Colors.END}")
    lines = []
    empty_count = 0
    while empty_count < 1:
        line = input()
        if line == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line)
    return "\n".join(lines)


def menu(options, title="Select an option"):
    """Display interactive menu"""
    print(f"\n{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
    for i, option in enumerate(options, 1):
        icon = option.get('icon', '▸')
        print(f"  {Colors.CYAN}{i}{Colors.END}. {icon} {option['label']}")
    
    print(f"{Colors.CYAN}{'─' * 40}{Colors.END}")
    
    while True:
        try:
            choice = int(get_input("Enter choice"))
            if 1 <= choice <= len(options):
                return options[choice - 1]['value']
            print_error("Invalid choice. Try again.")
        except ValueError:
            print_error("Please enter a number.")


class BrainBlockCLI:
    """Interactive CLI for BrainBlock"""
    
    def __init__(self):
        self.brainblock = BrainBlock()
        self.current_user = None
        self.wallet = None
        
    def run(self):
        """Run the CLI application"""
        clear_screen()
        print(LOGO)
        self.main_menu()
        
    def main_menu(self):
        """Display main menu"""
        while True:
            options = [
                {"label": "Submit Individual Project", "value": "submit", "icon": "📝"},
                {"label": "Submit Group Project", "value": "group", "icon": "👥"},
                {"label": "Verify Ownership", "value": "verify", "icon": "🔍"},
                {"label": "View Dashboard", "value": "dashboard", "icon": "📊"},
                {"label": "Connect Wallet", "value": "wallet", "icon": "💰"},
                {"label": "Import from GitHub", "value": "github", "icon": "🐙"},
                {"label": "Run Demo", "value": "demo", "icon": "🎮"},
                {"label": "Help", "value": "help", "icon": "❓"},
                {"label": "Exit", "value": "exit", "icon": "🚪"},
            ]
            
            choice = menu(options, "🧠 BRAINBLOCK MAIN MENU")
            
            if choice == "submit":
                self.submit_project()
            elif choice == "group":
                self.submit_group_project()
            elif choice == "verify":
                self.verify_ownership()
            elif choice == "dashboard":
                self.show_dashboard()
            elif choice == "wallet":
                self.connect_wallet()
            elif choice == "github":
                self.import_github()
            elif choice == "demo":
                self.run_demo()
            elif choice == "help":
                self.show_help()
            elif choice == "exit":
                print(f"\n{Colors.CYAN}Thanks for using BrainBlock! 👋{Colors.END}\n")
                sys.exit(0)
                
    def submit_project(self):
        """Submit individual project"""
        print_header("📝 Submit Individual Project")
        
        title = get_input("Project Title")
        author = get_input("Your Name")
        wallet = get_input("Wallet Address", "ALGO_DEMO_WALLET_ADDRESS")
        email = get_input("Email (optional)", "")
        
        print(f"\n{Colors.CYAN}Enter your project description/code:{Colors.END}")
        content = get_multiline_input("Project Content")
        
        if not title or not content:
            print_error("Title and content are required!")
            return
        
        print()
        animated_loading("Analyzing with AI", 1)
        animated_loading("Checking originality", 1)
        animated_loading("Registering on blockchain", 1.5)
        
        result = self.brainblock.submit_project(
            title=title,
            content=content,
            author=author,
            wallet=wallet,
            email=email if email else None
        )
        
        if result['success']:
            print_card("🎉 Submission Successful!", {
                "Title": title,
                "Transaction": result['blockchain']['tx_id'][:20] + "...",
                "Block": result['blockchain']['block'],
                "Proof URL": result['proof_url'][:50] + "..."
            }, Colors.GREEN)
            
            print(f"\n{Colors.GREEN}Share this proof URL to verify your ownership!{Colors.END}")
        else:
            print_error(f"Submission failed: {result.get('reason', 'Unknown error')}")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def submit_group_project(self):
        """Submit group project"""
        print_header("👥 Submit Group Project")
        
        title = get_input("Project Title")
        num_contributors = int(get_input("Number of contributors", "2"))
        
        contributors = []
        for i in range(num_contributors):
            print(f"\n{Colors.BOLD}Contributor {i + 1}:{Colors.END}")
            name = get_input("  Name")
            wallet = get_input("  Wallet", f"ALGO_WALLET_{i+1}")
            
            contrib_types = [
                {"label": "Algorithm/Core Logic", "value": "algorithm", "icon": "🧮"},
                {"label": "Implementation", "value": "implementation", "icon": "💻"},
                {"label": "Design/UI", "value": "design", "icon": "🎨"},
                {"label": "Documentation", "value": "docs", "icon": "📄"},
                {"label": "Research", "value": "research", "icon": "🔬"},
            ]
            contrib_type = menu(contrib_types, "  Contribution Type")
            
            contribution = get_multiline_input("  Contribution Description")
            
            contributors.append(Contributor(
                name=name,
                wallet_address=wallet,
                contribution=contribution,
                contribution_type=contrib_type
            ))
        
        print()
        animated_loading("Analyzing contributions", 1.5)
        animated_loading("Calculating fair ownership", 1)
        animated_loading("Deploying smart contract", 2)
        
        result = self.brainblock.submit_group_project(
            title=title,
            contributors=contributors
        )
        
        if result['success']:
            print_header("🎉 Group Project Protected!", "line")
            
            headers = ["Contributor", "Type", "Ownership"]
            rows = [
                [c['name'], c['contribution_type'], f"{c['ownership_percentage']}%"]
                for c in result['contributors']
            ]
            print_table(headers, rows, "Ownership Distribution")
            
            print_card("Smart Contract Details", {
                "Contract ID": result['contract_id'],
                "Transaction": result['blockchain']['tx_id'][:20] + "...",
                "Block": result['blockchain']['block']
            }, Colors.GREEN)
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def verify_ownership(self):
        """Verify ownership"""
        print_header("🔍 Verify Ownership")
        
        tx_id = get_input("Enter Transaction ID or Contract ID")
        
        if not tx_id:
            print_error("Transaction ID is required!")
            return
        
        animated_loading("Querying blockchain", 1)
        
        result = self.brainblock.verify_ownership(tx_id)
        
        if result['verified']:
            print_success(result['message'])
            print_card("Verification Result", {
                "Status": "✅ Verified",
                "Block": result['transaction']['block'],
                "Timestamp": result['transaction']['timestamp'][:19]
            }, Colors.GREEN)
        else:
            print_error(result['message'])
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def show_dashboard(self):
        """Show platform dashboard"""
        print_header("📊 Platform Dashboard")
        
        stats = self.brainblock.get_dashboard_stats()
        
        # Stats cards
        print(f"""
{Colors.CYAN}╭─────────────────╮ ╭─────────────────╮ ╭─────────────────╮{Colors.END}
{Colors.CYAN}│{Colors.END}  {Colors.BOLD}Submissions{Colors.END}    {Colors.CYAN}│{Colors.END} {Colors.CYAN}│{Colors.END}  {Colors.BOLD}Users{Colors.END}          {Colors.CYAN}│{Colors.END} {Colors.CYAN}│{Colors.END}  {Colors.BOLD}Groups{Colors.END}         {Colors.CYAN}│{Colors.END}
{Colors.CYAN}│{Colors.END} {Colors.GREEN}{stats['total_submissions']:>13,}{Colors.END}   {Colors.CYAN}│{Colors.END} {Colors.CYAN}│{Colors.END} {Colors.GREEN}{stats['total_users']:>13,}{Colors.END}   {Colors.CYAN}│{Colors.END} {Colors.CYAN}│{Colors.END} {Colors.GREEN}{stats['total_groups']:>13,}{Colors.END}   {Colors.CYAN}│{Colors.END}
{Colors.CYAN}│{Colors.END}  {Colors.YELLOW}+{stats['submissions_today']} today{Colors.END}       {Colors.CYAN}│{Colors.END} {Colors.CYAN}│{Colors.END}  {Colors.YELLOW}+{stats['active_users_today']} active{Colors.END}    {Colors.CYAN}│{Colors.END} {Colors.CYAN}│{Colors.END}  {Colors.YELLOW}{stats['uptime']} uptime{Colors.END}   {Colors.CYAN}│{Colors.END}
{Colors.CYAN}╰─────────────────╯ ╰─────────────────╯ ╰─────────────────╯{Colors.END}
        """)
        
        print_card("Platform Metrics", {
            "Blockchain Transactions": f"{stats['blockchain_transactions']:,}",
            "Total Protected Value": stats['total_protected_value'],
            "Platform Uptime": stats['uptime']
        }, Colors.BLUE)
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def connect_wallet(self):
        """Connect wallet"""
        print_header("💰 Connect Wallet")
        
        wallets = [
            {"label": "Pera Wallet (Mobile)", "value": "pera", "icon": "📱"},
            {"label": "MyAlgo Wallet (Web)", "value": "myalgo", "icon": "🌐"},
            {"label": "AlgoSigner (Extension)", "value": "algosigner", "icon": "🔌"},
            {"label": "Defly Wallet", "value": "defly", "icon": "✈️"},
            {"label": "Generate New Wallet", "value": "new", "icon": "🆕"},
        ]
        
        choice = menu(wallets, "Select Wallet Type")
        
        animated_loading(f"Connecting to {choice}", 1.5)
        
        result = self.brainblock.connect_wallet(choice)
        
        print_success(f"Connected to {result['provider']}")
        print_card("Wallet Info", {
            "Address": result['address'][:20] + "...",
            "Balance": result['balance'],
            "Network": result['network']
        }, Colors.GREEN)
        
        self.wallet = result['address']
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def import_github(self):
        """Import from GitHub"""
        print_header("🐙 Import from GitHub")
        
        repo_url = get_input("GitHub Repository URL", "https://github.com/user/repo")
        
        animated_loading("Fetching repository", 1)
        animated_loading("Analyzing codebase", 1.5)
        
        result = self.brainblock.import_from_github(repo_url)
        
        print_card("Repository Imported", {
            "Name": result['name'],
            "Stars": result['stars'],
            "Language": result['language'],
            "Files Analyzed": result['files_analyzed']
        }, Colors.GREEN)
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def run_demo(self):
        """Run demo"""
        print_header("🎮 Running Full Demo")
        
        from demo import run_demo
        run_demo()
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        
    def show_help(self):
        """Show help"""
        print_header("❓ Help & Documentation")
        
        help_text = f"""
{Colors.BOLD}What is BrainBlock?{Colors.END}
BrainBlock is an innovative "Idea Vault" that combines AI and blockchain
to protect student innovations with immutable timestamps.

{Colors.BOLD}How it works:{Colors.END}
1. {Colors.CYAN}Upload{Colors.END} - Submit your project description or code
2. {Colors.CYAN}Analyze{Colors.END} - AI extracts unique fingerprint
3. {Colors.CYAN}Verify{Colors.END} - Plagiarism check confirms originality
4. {Colors.CYAN}Register{Colors.END} - Hash stored on Algorand blockchain
5. {Colors.CYAN}Prove{Colors.END} - Share explorer link as proof

{Colors.BOLD}Features:{Colors.END}
• 🧠 AI-powered innovation fingerprinting
• ⛓️  Algorand blockchain timestamps
• 👥 Group project smart contracts
• 🔍 Ownership verification
• 📊 Real-time analytics
• 🔔 Multi-channel notifications

{Colors.BOLD}Commands:{Colors.END}
• Submit Project - Register individual innovation
• Group Project - Co-creator vault with smart contracts
• Verify - Check ownership using transaction ID
• Dashboard - View platform statistics
• Connect Wallet - Link your Algorand wallet
        """
        print(help_text)
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def main():
    """Entry point"""
    cli = BrainBlockCLI()
    cli.run()


if __name__ == "__main__":
    main()
