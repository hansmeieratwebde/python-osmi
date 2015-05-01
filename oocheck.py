__author__ = 'S Hinse'


class HelloWorld:
    x= "Hallo Welt"
    def __init__(self):

       print "Hallo Konstruktor"

    def sayHello(self):
        print self.x
        print "Hello"





def objectCall():
    """

    :rtype : object
    """
    x = HelloWorld()
    x.sayHello()
    print("objectCall")

objectCall()