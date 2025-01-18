import sys
from ui.gui import gui
from ui.cli import cli


def main():
    if len(sys.argv) > 1:
        cli.run()
    else:
        gui.run()


if __name__ == "__main__":
    main()
