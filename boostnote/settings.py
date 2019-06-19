# -*- coding: utf-8 -*-
import os

TOP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ConfigMeta(type):
    @property
    def logger(cls):
        return 'dd'

    @property
    def path(cls) -> list:
        return cls.get_boostnote()['path']

    @property
    def export_path(cls) -> str:
        return cls.get_boostnote()['export_path']


class ConfigSetting(object, metaclass=ConfigMeta):
    config_file = 'boostnote/boostnote.ini'
    _cfg = None
    _boostnote = {}

    @classmethod
    def get_config_name(cls):
        return os.path.join(TOP_DIR, cls.config_file)

    @classmethod
    def is_exists_config(cls):
        return os.access(ConfigSetting.get_config_name(), os.F_OK)

    @classmethod
    def init_config_name(cls):
        if cls.is_exists_config() == False:
            import shutil
            shutil.copy2(cls.get_config_name() + '_template', cls.get_config_name())

    @classmethod
    def get_config_parser(cls):
        if cls._cfg is None:
            from configparser import ConfigParser
            cls._cfg = ConfigParser()
            cls._cfg.read(cls.get_config_name(), encoding='utf-8')

        return cls._cfg

    @classmethod
    def get_boostnote(cls):
        rlt = cls._boostnote

        if rlt == {}:
            cfg = cls.get_config_parser()

            rlt['path'] = []
            for idx in range(1, 10):
                try:
                    path = cfg.get('boostnote', 'storage.%d' % idx)
                    if os.path.exists(path):
                        rlt['path'].append(path)
                except Exception as e:
                    break

            rlt['export_path'] = cfg.get('boostnote', 'export_path', fallback=os.path.join(os.path.dirname(__file__), os.path.pardir, 'output'))
            if not os.path.exists(rlt['export_path']):
                os.mkdir(rlt['export_path'])

            return rlt
        return rlt

ConfigSetting.init_config_name()
config = ConfigSetting
