# encoding: utf-8

from ckan.plugins import implements, SingletonPlugin, IValidators

class WeirdValidators(SingletonPlugin):
    """
    Plugin that implements a number of dummy validators for testing purposes.
    """
    implements(IValidators)

    def foolidator(self, value):
        return "FOOOO ---> {} <--- BAAAAR".format(value)

    def three_is_neither_two_nor_four(self, value, balue, dalue):
        return "don't use me"

    def vier_ist_trumpf(self, value, balue, dalue, nalue):
        return "Hurra!"

    def get_validators(self):
        return {
            "foolidator": self.foolidator ,
            "three_is_neither_two_nor_four": self.three_is_neither_two_nor_four ,
            "vier_ist_trumpf": self.vier_ist_trumpf
        }