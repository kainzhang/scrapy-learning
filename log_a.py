import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s [%(asctime)s] '
                           '[%(filename)s:%(lineno)d] '
                           '%(message)s',
                    datefmt='%d/%b/%Y %H:%M:%S'
                    )

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('info log')
    logger.warning('warning log')