import argparse
# workflow:
# Still use CV2 video capture to access webcam - the fun part comes in generating output webstream

if __name__ == '__main__':
    print('hi')
    camstream = None
    while (True):
        if camstream is None:
            print('No Camstream currently detected')
            camstream = 'hi' # some api call to set camstream

        if camstream is not None:
            newCamstream = wesleyCode(camstream)

