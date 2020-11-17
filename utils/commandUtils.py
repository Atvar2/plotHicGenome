import argparse
def str2bool(boolValue):
    if boolValue.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif boolValue.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')
