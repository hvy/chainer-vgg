from chainer import serializers
from chainer import Variable
from VGG import VGG
from vggrpn import VGGRPN


def load_model(filename, model):
    print('Loading model {:s}'.format(filename))
    serializers.load_hdf5(filename, model)
    print('Successfully loaded model')
    return model


def save_model(filename, model):
    print('Saving model {:s}'.format(filename))
    serializers.save_hdf5(filename, model)
    print('Successfully saved model')


if __name__ == '__main__':
    """Makes a copy of a (trained) VGG model to a VGG RPN model
    and saved it to a file named 'VGGRPN.model'
    """
    # Create an empty VGG model (w random weights)
    vgg = VGG()

    # Load the parameter data (weights and biases) from file
    vgg = load_model('VGG.model', vgg)

    # Create an empty VGG RPN model (w random weights)
    vgg_rpn = VGGRPN()

    # Copy the shared parameters from the VGG model to the VGG RPN model
    for attr in vgg.namedlinks(skipself=True):
        print('Copying layer {:s}'.format(attr[0][1:]))
        layer = getattr(vgg_rpn, attr[0][1:])
        layer.W = Variable(attr[1].W.data)
        layer.b = Variable(attr[1].b.data)
        setattr(vgg_rpn, attr[0], layer)

    # Save the new VGG RPN model to file
    save_model('vggrpn.model', vgg_rpn)

    print('Done')
