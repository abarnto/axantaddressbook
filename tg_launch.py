if __name__ == '__main__':
    from gearbox.main import GearBox
    gearbox = GearBox()
    gearbox.run(["serve", "--config=development.ini"])