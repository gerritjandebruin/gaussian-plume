import numpy
import pandas


class GPData():

    def __init__(self, df, sources, channels, molecules):
        
        self.df = pandas.DataFrame(df)
        self.sources = sources
        self.channels = channels
        self.molecules = molecules
        
    def calculate(self, plumes):
    
        df_column_names = self.df.columns
        for plume_nr in plumes:
            print("plume: {:d}".format(plume_nr))
            idx = numpy.where(self.df["plume_number"] == plume_nr)[0]
        
            for molecule_index, molecule in enumerate(self.molecules):
                print("  {:s}".format(molecule.molecule))
                for channel_index, channel in enumerate(self.channels):
                    
                    if channel.molecule == molecule.molecule:
                        print("    channel {:d}: {:s}, {:s}".format(channel.index, channel.molecule, channel.device))
                
                        for source_index, source in enumerate(self.sources):
                            if channel.molecule in source.molecule:
                                print("      source {:d}: {:s}".format(source.index, source.label))

                                col_name = "{:s} latS".format(source.col_name_prefix)
                                if col_name in df_column_names:
                                    latS = self.df.loc[idx,col_name]
                                else:
                                    latS = self.df.loc[idx,"latS"]
                                    # print(latS)

                

class GPSource():
    
    def __init__(self, index, molecule, label):
        self.index = index
        self.molecule = molecule
        self.label = label
        
        self.col_name_prefix = "source{:d}".format(self.index)

class GPChannel():
    
    def __init__(self, index, molecule, device):
        self.index = index
        self.molecule = molecule
        self.device = device

        self.col_name_prefix = "channel{:d}".format(self.index)

class GPMolecule():
    
    def __init__(self, molecule):
        self.molecule = molecule
        if molecule == "no":
            self.molecular_weight = 30
        elif  molecule == "ch4":
            self.molecular_weight = 16
        else:
            self.molecular_weight = None

        
if __name__ == "__main__":
    plume_number = numpy.zeros(110)
    plume_number[30:50] = 1
    plume_number[80:100] = 2
    df = {
        "datetime": numpy.arange(110),
        "source0 latS": numpy.arange(10,120),
        "source0 lonS": numpy.arange(110,220),
        "source1 latS": numpy.arange(20,130),
        "source1 lonS": numpy.arange(120,230),
        "source2 latS": numpy.arange(30,140),
        "source2 lonS": numpy.arange(130,240),
        "source3 latS": numpy.arange(40,150),
        "source3 lonS": numpy.arange(140,250),     
        "source4 latS": numpy.arange(50,160),
        "source4 lonS": numpy.arange(150,260),
        "source5 latS": numpy.arange(60,170),
        "source5 lonS": numpy.arange(160,270),    
        "latS": numpy.arange(70,180), # for source 6 and 7
        "lonS": numpy.arange(170,280), # for source 6 and 7       
        "lonM": numpy.arange(30,140),
        "latM": numpy.arange(30,140),
        "channel0 concentration": numpy.arange(110)/10,
        "channel1 concentration": numpy.arange(110)/20,
        "channel2 concentration": numpy.arange(110)/20,
        "wind_speed": numpy.arange(100,210),
        "wind_direction": numpy.arange(200,310),
        "plume_number": plume_number,
    }
    
    sources = [     
        GPSource(index = 0, molecule = "no", label = "stal 0"),
        GPSource(index = 1, molecule = "ch4", label = "stal 1"),
        GPSource(index = 2, molecule = ["no", "ch4"], label = "stal 2"),
        GPSource(index = 3, molecule = "no", label = "wc 3"),
        GPSource(index = 4, molecule = "no", label = "schuur 4"),
        GPSource(index = 5, molecule = "no", label = "schuur 5"),
        GPSource(index = 6, molecule = "no", label = "schuur X"),
        GPSource(index = 7, molecule = "no", label = "schuur Y"),
        
    ]
    
    channels = [
        GPChannel(0, "ch4", "QCL"),
        GPChannel(1, "no", "MIRA"),
        GPChannel(2, "no", "QCL"),
    ]
    
    molecules = [
        GPMolecule("ch4"),
        GPMolecule("no"),
        # {
        # "molecule": "ch4",
        # "molecular weight": 16,
        # },
        # {
        # "molecule": "no",
        # "molecular weight": 30,
        # }
    ]
    
    
    
    G = GPData(df, sources, channels, molecules)
    
    print(G.df) #.df.columns)
    # print(G.sources)
    # print(G.channels)
    
    # G.calculate(plumes = [1,2])
    