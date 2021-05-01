import sys
import subprocess


def install_packages():
    print("Upgrading Pip...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    print("Installing pyfiglet...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyfiglet'])
    print("Installing pymsteams...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymsteams'])
    print("Installing prompt_toolkit...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'prompt_toolkit'])
    print("Installing pypager...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pypager'])
    print("Installing bs4...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])
    print("All packages installed :D To finish installation follow next step...")
    print("\n\nInstall google client:")
    print(
        "copy this command and run:\npip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    print("\nAfter installing google client run program with: python main.py")

    return True


def main():
    print("Installation of required packages")
    print("\nWill upgrade pip, install pyfliglet, pymsteams, promp_toolkit, pypager, and bs4, "
          "you will need to manually install google client, command will be provided at the end\n")
    print("If already satisfied it will just continue")
    while True:
        user_choice = input("Would you like to continue (y/n): ")
        if user_choice.lower() == 'y':
            install_packages()
            break
        elif user_choice.lower() == 'n':
            print("See yah! ")
            break
        else:
            print("invalid command")


if __name__ == "__main__":
    main()