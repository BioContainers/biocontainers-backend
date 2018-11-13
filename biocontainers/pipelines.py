import argparse
import configparser


from biocontainers.quayio.models import QuayIOReader


def get_config():
    """
    This method read the default configuration file configuration.ini in the same path of the pipeline execution
    :return:
    """
    config = configparser.ConfigParser()
    config.read("configuration.ini")
    return config


def get_parameters():
    """
    This method provide a possibility to read arguments for the pipeline and combine then with the default
    configuration
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--import_quayio", help="Import Quay.io Recipes", action='store_true')
    parser.add_argument("-d", "--import_docker", help="Import Docker Recipes", action='store_true')

    return parser


def import_quayio(config):
    """
    Import quayio containers into the registry database
    :param config: Parameters for quayio
    :return:
    """
    print("Starting importing Conda packages")

    reader = QuayIOReader()
    reader.quayio_list_url(config['DEFAULT']['QUAYIO_CONTAINER_LIST'])
    reader.quayio_details_url(config['DEFAULT']['QUAYIO_CONTAINER_DETAILS'])
    reader.namespace(config['DEFAULT']['NAMESPACE'])

    reader.get_list_containers()
    containers = reader.get_containers()




def main(parameters):
    config = get_config()

    if config['DEFAULT']['VERBOSE'] == "True":
        for key in config['DEFAULT']:
            print(key + "=" + config['DEFAULT'][key])
        print(parameters)
    if parameters.import_quayio is not False:
        import_quayio(config)

if __name__ == "__main__":
    parameters = get_parameters().parse_args()
    main(parameters)
