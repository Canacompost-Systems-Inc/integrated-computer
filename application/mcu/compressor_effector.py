class CompressorEffector:

    def setCompressor(self, state: bool):
        # TODO: Compressor should wait 2 seconds before starting so that we don't blow up the valves
        print("Setting air compressor state to " + str(state))