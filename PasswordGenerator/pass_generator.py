import random
import datetime
from pathlib import Path
class PasswordGenerator:

    def __init__(self):
        # Dane hasła
        self.password = ""
        self.password_length = 0
        self.password_strength = ""

        # Pula znaków
        self.basic_password_chars = "abcdefghijklmnoprstuwxyz"
        self.capital_letters_chars = "ABCDEFGHIJKLMNOPRSTUWXYZ"
        self.numbers_in_password_chars = "0123456789"
        self.special_characters_chars = "!@#$%^&*()_-+={[]};:'<,>.?/|"

        
        self.special_characters = ""
        self.capital_letters = ""
        self.numbers_in_password = ""

    def Welcome(self):
        self.score = 0
        try:
            print("What do you want to do today?")
            print("\n1.Check the security of your password")
            print("2.Generate your own password and check its security\n")
            choice = int(input("Your choice: (1/2): "))

            if choice == 1:
                password_input = input("Enter your password: ")
                password_length = input("Is your password at least 12 characters long? (yes/no/y/n)").lower()
                password_special_chars = input("Have your password special chars? (yes/no/y/n)").lower()
                password_capital_letters = input("Have your password capital letter? (yes/no/y/n)").lower()
                password_numbers = input("Have your password any number? (yes/no/y/n)").lower()
                if password_length == "yes" or password_length == "y":
                    self.score += 1

                if password_special_chars == "yes" or password_special_chars == "y":
                    self.score += 1

                if password_capital_letters == "yes" or password_capital_letters == "y":
                    self.score += 1

                if password_numbers == "yes" or password_numbers == "y":
                    self.score += 1
                
                if self.score == 4:
                    self.password_strength = "Strong"
                elif self.score == 3:
                    self.password_strength = "Medium"
                else:
                    self.password_strength = "Weak"

                print(f"Your password is: {self.password_strength}")

                if self.password_strength == "Medium" or self.password_strength == "Weak":
                    print("Do you want to generate a strong password?")
                    choice = input("Your choice: (yes/no): ").lower()

                    if choice == "yes":
                        self.main()

                    else:
                        print("Okay! \nThank you for using the password generator \nGoodbye, Have a nice day.")

            if choice == 2:
                self.main()

        except Exception as e:
            print(f"Unexpected error: {e}")

        


    def user_preferences(self):
        self.password_length = int(input("Enter password length: "))

        self.special_characters = input(
            "Generate password with special characters? (yes/no/y/n): "
        ).lower()

        self.capital_letters = input(
            "Should the password contain capital letters? (yes/no/y/n): "
        ).lower()

        self.numbers_in_password = input(
            "Should the password contain numbers? (yes/no/y/n): "
        ).lower()

        try:
            self.special_characters = (self.special_characters == "yes" or self.special_characters == "y")
            self.capital_letters = (self.capital_letters == "yes" or self.capital_letters == "y")
            self.numbers_in_password = (self.numbers_in_password == "yes" or self.numbers_in_password == "y")
            
        except Exception as e:
            print(f"Unexpected error: {e}")

    def evaluate_password_strength(self):
        score = 0

        if self.password_length >= 12:
            score += 1
        if self.special_characters:
            score += 1
        if self.capital_letters:
            score += 1
        if self.numbers_in_password:
            score += 1

        if score == 4:
            self.password_strength = "Strong"
        elif score == 3:
            self.password_strength = "Medium"
        else:
            self.password_strength = "Weak"

    def generate_password(self):
        chars = self.basic_password_chars

        if self.special_characters:
            chars += self.special_characters_chars
        if self.capital_letters:
            chars += self.capital_letters_chars
        if self.numbers_in_password:
            chars += self.numbers_in_password_chars

        self.password = ""

        for _ in range(self.password_length):
            self.password += random.choice(chars)

        # Set current date
        self.current_date = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

        # Set default path
        self.home = Path(__file__).resolve().parent

        print(f"\nGenerated password: {self.password} at {self.current_date}")
        print("Password strength:", self.password_strength)
        choice = input("Do you want to save your password in file? (yes/no/y/n): ").lower()

        if choice in ("yes", "y"):
            # Get file name
            file_name = input("Enter name of saving file (without extention): ")

            # Does user want to say path?
            choose_path = input(f"Do you want to choose path in which generated password will be save? (yes/no/y/n) or save it on default path {self.home}: ").lower()
            if choose_path in ("yes", "y"):
                enter_path = input("Enter your path (relative to script or absolute, e.g. MyPasswords/ or C:/Users/...): ")
                save_dir = Path(enter_path)
                if not save_dir.is_absolute():
                    save_dir = self.home / save_dir
                save_dir.mkdir(parents=True, exist_ok=True)
                file_path = save_dir / f"{file_name}.txt"
            else:
                file_path = self.home / f"{file_name}.txt"

            # Zapis w trybie dopisywania
            with file_path.open("a", encoding="utf-8") as file:
                file.write(f"{self.password} - {self.current_date}\n")
            print(f"Password saved to {file_path}")

    def main(self):
        self.user_preferences()
        self.evaluate_password_strength()
        self.generate_password()


# Running program
password_generator = PasswordGenerator()
password_generator.Welcome()
