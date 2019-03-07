from binstar_client.utils import get_server_api
import logging

logger = logging.getLogger('biocontainers.conda.conda_metrics')
logger.setLevel(logging.INFO)
conda_channels = ['bioconda']


class CondaMetrics:

    @staticmethod
    def get_number_downloas(package):
        package_total_dls = 0
        for conda_channel in conda_channels:
            aserver_api = get_server_api("5b55044589a6f388059dada9", "anaconda.org", 1)
            try:
                package_obj = aserver_api.package(conda_channel, package)
            except:
                continue
            channel_total_dls = 0
            for version_str in package_obj['versions']:
                version = aserver_api.release(conda_channel, package, version_str)
                for d in version['distributions']:
                    distribution_os = d['attrs']['machine']
                    distribution_arch = d['attrs']['platform']
                    distribution_build = d['attrs']['build']
                    distribution_downloads = d['ndownloads']
                    distribution_upload_time = d['upload_time']

                    np_version = None
                    py_version = None
                    for item in d['dependencies']['depends']:
                        try:
                            if item['name'] == 'numpy':
                                np_version = item['specs'][0][1]
                            if item['name'] == 'python':
                                py_version = item['specs'][0][1]
                        except:
                            pass

                    if np_version is None:
                        np_version = "None"
                    if py_version is None:
                        py_version = "None"
                    if distribution_arch is None:
                        distribution_arch = "None"
                    if distribution_os is None:
                        distribution_os = "None"

                    logger.info(
                        "Conda Package -- " + package + " version -- " + version_str + " Distributed build -- " + distribution_build + " Distributed OS -- " + distribution_os + " Distributed Arch -- " + distribution_arch + " Distributed Downloads -- " + str(
                            distribution_downloads) + " Py Version -- " + py_version + " NP Version -- " + np_version + "Distribution time -- " + str(
                            distribution_upload_time))
                    channel_total_dls += distribution_downloads
            package_total_dls += channel_total_dls
            logger.info("Total downloads of package -- " + package + ": " + str(channel_total_dls))
        logger.info("Total downloads of -- " + package + ": " + str(package_total_dls))
        return package_total_dls


    @staticmethod
    def get_number_downloas_by_version(package, version):
        package_total_dls = 0
        for conda_channel in conda_channels:
            aserver_api = get_server_api("5b55044589a6f388059dada9", "anaconda.org", 1)
            try:
                package_obj = aserver_api.package(conda_channel, package)
            except:
                continue
            channel_total_dls = 0

            size = 0
            last_update = ''
            for version_str in package_obj['versions']:
                if version_str == version:
                   version = aserver_api.release(conda_channel, package, version_str)
                   for d in version['distributions']:
                       distribution_os = d['attrs']['machine']
                       distribution_arch = d['attrs']['platform']
                       distribution_build = d['attrs']['build']
                       distribution_downloads = d['ndownloads']
                       distribution_upload_time = d['upload_time']

                       np_version = None
                       py_version = None
                       for item in d['dependencies']['depends']:
                          try:
                              if item['name'] == 'numpy':
                                 np_version = item['specs'][0][1]
                              if item['name'] == 'python':
                                 py_version = item['specs'][0][1]
                          except:
                             pass

                       if np_version is None:
                          np_version = "None"
                       if py_version is None:
                          py_version = "None"
                       if distribution_arch is None:
                          distribution_arch = "None"
                       if distribution_os is None:
                          distribution_os = "None"

                       if 'size' in d:
                           size = d['size']

                       if 'upload_time' in d:
                           last_update = d['upload_time']

                       logger.info(
                          "Conda Package -- " + package + " version -- " + version_str + " Distributed build -- " + distribution_build + " Distributed OS -- " + distribution_os + " Distributed Arch -- " + distribution_arch + " Distributed Downloads -- " + str(
                            distribution_downloads) + " Py Version -- " + py_version + " NP Version -- " + np_version + "Distribution time -- " + str(
                            distribution_upload_time))
                       channel_total_dls += distribution_downloads
                package_total_dls += channel_total_dls
                logger.info("Total downloads of package -- " + package + ": " + str(channel_total_dls))
        logger.info("Total downloads of -- " + package + ": " + str(package_total_dls))
        return {'version': version_str, 'size': size, 'last_update': last_update, 'downloads':package_total_dls}

if __name__ == "__main__":
    metrics = CondaMetrics()
    metrics.get_number_downloas("BIOCONDUCTOR-MSGFPLUS")
    print(str(metrics.get_number_downloas_by_version("BIOCONDUCTOR-MSGFPLUS", "1.16.1")))
