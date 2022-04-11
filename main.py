import yaml

from dynoGUI import DynoGUI


if __name__ == '__main__':
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Error reading config file")
            exit()

    dyno = DynoGUI(config)
    dyno.create_page()
    dyno.run()
