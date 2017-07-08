import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {'Owner': 'liuxinxin'}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
