import logging.config

from conf_logger import dict_config

logging.config.dictConfig(dict_config)

sub_sub_1 = logging.getLogger("sub_2.sub_sub_1")
sub_sub_1.setLevel("DEBUG")


def main():
    sub_sub_1.debug("message for sub_sub_1",
                    extra = {
                        "very": "Ну ты понял? Новый атрибут 'very'! А если не передать, то ValueError"
                    })


if __name__ == '__main__':
    main()