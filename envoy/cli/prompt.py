from ..exceptions import CommandError


def confirm(prompt) -> bool:
    for _ in range(3):
        response = input(f"{prompt} [y/N]: ").strip().lower()
        if response in {'yes', 'y'}:
            return True
        elif response in {'no', 'n'}:
            return False
        else:
            print("Invalid response. Please enter 'y'/'yes' or 'n'/'no'.")

    raise CommandError("could not confirm operation")
