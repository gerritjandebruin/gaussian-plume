"""
Data processing is done in three steps:

1. Import data
2. Parse data
3. Calculate results





Import data
===========
















"""



import importlib
import pathlib
import pandas
import numpy


import ClassTools as CT
import GPFunctions as GPF
import GPImport as GPI
import GPSource as GPSO
import GPChannel as GPCH
import GPMolecule as GPMO

importlib.reload(GPF)
importlib.reload(GPI)
importlib.reload(GPSO)
importlib.reload(GPCH)
importlib.reload(GPMO)

class GaussianPlume(CT.ClassTools):
    """
    
    Attributes
    ----------
    sources : list (optional, None)
        List with sources.
    channels : list (optional, None)
        List with channels.
    molecules : list (optional, None)
        List with molecules.
    plumes : list (optional, None)
        List with plumes.
    df : pandas.DataFrame (optional, None)
        DataFrame with the measurement data
    df_sources : pandas.DataFrame (optional, None)
        DataFrame with the sources
    df_channels : pandas.DataFrame (optional, None)
        DataFrame with the channels
    df_static : pandas.DataFrame (optional, None)
        DataFrame with static measurement parameters    
    log : dict (optional)
        A log of where values were set. If it is not given, a new one will be made.
    comment : str (optional)
        A comment that can be added to the log.
    filename : Path or str (optional, None)
        The filename where static parameters, sources, and channels are listed. 
    path : Path or str (optional, None)
        The path where static parameters, sources, and channels are listed. 
        
        
    
    
    """

    def __init__(self, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        sources : list (optional, None)
            List with sources.
        channels : list (optional, None)
            List with channels.
        molecules : list (optional, None)
            List with molecules.
        plumes : list (optional, None)
            List with plumes.
        df : pandas.DataFrame (optional, None)
            DataFrame with the measurement data
        df_sources : pandas.DataFrame (optional, None)
            DataFrame with the sources
        df_channels : pandas.DataFrame (optional, None)
            DataFrame with the channels
        df_static : pandas.DataFrame (optional, None)
            DataFrame with static measurement parameters    
        log : dict (optional)
            A log of where values were set. If it is not given, a new one will be made.
        comment : str (optional)
            A comment that can be added to the log.
        filename : Path or str (optional, None)
            The filename where static parameters, sources, and channels are listed. 
        path : Path or str (optional, None)
            The path where static parameters, sources, and channels are listed. 

        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GaussianPlume.GaussianPlume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        self.sources = kwargs.get("sources", None)
        self.channels = kwargs.get("channels", None)
        self.molecules = kwargs.get("molecules", [])
        self.plumes = kwargs.get("plumes", None)

        self.plume_number = None

        self.log = kwargs.get("log", {"comment": ""})

        if "comment" in kwargs:
            self.log["comment"] = "{:s}\n__init__: {:s}".format(self.log["comment"], kwargs["comment"])
 
        self.df = kwargs.get("df", None)
        self.df_sources = kwargs.get("df_sources", None)
        self.df_channels = kwargs.get("df_channels", None)
        self.df_static = kwargs.get("df_static", None)
        
        self.filename = kwargs.get("filename", None)
        self.path = kwargs.get("path", None)
        self.paf = GPF.handle_filename_path(filename = self.filename, path = self.path, verbose = verbose)
        
        self.paf_data = kwargs.get("paf_data", None)
        
        self.concentration_model = None


    def import_data(self, filename = None, path = None, verbose = 0, **kwargs):
        """
        Import all data. 
        
        Arguments
        ---------
        sheetname : str (optional, "static parameters")
            The name of the sheet with the static parameters
        filename : Path or str (optional, None)
            Filename. For more information, see GPFunctions.handle_filename_path.
        path : Path or str (optional, None)
            Path. For more information, see GPFunctions.handle_filename_path.
            
        Notes
        -----
        If both `filename` and `path` are None (default), it will use the path-and-filename set during initialization. 

        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_data()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        if filename is None and path is None:
            paf = self.paf
        else:
            paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)

        self.import_static_parameters(verbose = verbose, **kwargs)
        self.import_sources_from_Excel(verbose = verbose, **kwargs)
        self.import_channels_from_Excel(verbose = verbose, **kwargs)
        
        if str(self.paf_data.suffix) == ".csv":
            self.import_measurement_data_from_csv(filename = self.paf_data, verbose = verbose)
        elif str(self.paf_data.suffix) == "xlsx":
            self.import_measurement_data_from_Excel(filename = self.paf_data, verbose = verbose)

            
    def import_static_parameters(self, sheetname = "static parameters", filename = None, path = None, verbose = 0, **kwargs):
        """
        Import static parameters. 
        
        Arguments
        ---------
        sheetname : str (optional, "static parameters")
            The name of the sheet with the static parameters
        filename : Path or str (optional, None)
            Filename. For more information, see GPFunctions.handle_filename_path.
        path : Path or str (optional, None)
            Path. For more information, see GPFunctions.handle_filename_path.
            
        Notes
        -----
        If both `filename` and `path` are None (default), it will use the path-and-filename set during initialization. 

        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_static_parameters()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        if filename is None and path is None:
            paf = self.paf
        else:
            paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)
        
        df_static = GPI.import_df_from_Excel(paf[0], sheetname, index_col = 0, header = None)   

        df_static = df_static.transpose()
        df_static = df_static.reset_index(drop = True)

        self.df_static = df_static
        
        if "filename_measurement_data" in self.df_static:
            self.paf_data = pathlib.Path(self.df_static.loc[0,"filename_measurement_data"])
    
    def import_measurement_data_from_Excel(self, sheetname = "data", filename = None, path = None, drop_non_plume = False, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_measurement_data_from_Excel()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)

        df = GPI.import_df_from_Excel(paf[0], sheetname)
    
        # if drop_non_plume:
            # df.drop(df.index[df['plume_number'] == 0], inplace=True)
            # df.drop(df.index[numpy.isnan(df['plume_number'])], inplace=True)
            
        
        self.df = df



    def import_measurement_data_from_csv(self, filename = None, path = None, drop_non_plume = False, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_measurement_data_from_csv()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  
 
        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)
        
        df = GPI.import_df_from_csv(paf[0])
    
        # if drop_non_plume:
            # df.drop(df.index[df['plume_number'] == 0], inplace=True)
            # df.drop(df.index[numpy.isnan(df['plume_number'])], inplace=True)
            
        
        self.df = df

    def import_sources_from_Excel(self, sheetname = "sources", filename = None, path = None, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        sheetname : str (optional, "sources")
            The name of the sheet with the static parameters
        filename : Path or str (optional, None)
            Filename. For more information, see GPFunctions.handle_filename_path.
        path : Path or str (optional, None)
            Path. For more information, see GPFunctions.handle_filename_path.
            
        Notes
        -----
        If both `filename` and `path` are None (default), it will use the path-and-filename set during initialization. 
            
            
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_sources_from_Excel()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        if filename is None and path is None:
            paf = self.paf
        else:
            paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)
            
        if sheetname is None:
            sheetname = "sources"

        self.df_sources = GPI.import_df_from_Excel(paf[0], sheetname)
        
        n_sources = self.df_sources.shape[0]
        
        self.sources = []
        for i in range(n_sources):
            
            source = GPSO.Source(source_id = self.df_sources.loc[i,"source_id"], molecule = self.df_sources.loc[i,"molecule"])
            
            molecule_list = []
            for molecule in self.molecules:
                molecule_list.append(molecule.molecule_id)
            
            if source.molecule.molecule_id not in molecule_list:
                self.molecules.append(GPMO.Molecule(molecule = source.molecule.molecule))
                molecule_list.append(source.molecule.molecule_id)
                
            self.sources.append(source)                




    def generate_sources(self, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.generate_sources()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  
        
        if self.sources is None:
            if self.df_sources is not None:
                n_sources = self.df_sources.shape[0]
                self.sources = []
                for i in range(n_sources):
                    self.sources.append(GPSO.Source(source_id = self.df_sources.loc[i,"source_id"], molecule = self.df_sources.loc[i,"molecule"]))



    def import_channels_from_Excel(self, sheetname = "channels", filename = None, path = None, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        sheetname : str (optional, "channels")
            The name of the sheet with the static parameters
        filename : Path or str (optional, None)
            Filename. For more information, see GPFunctions.handle_filename_path.
        path : Path or str (optional, None)
            Path. For more information, see GPFunctions.handle_filename_path.
            
        Notes
        -----
        If both `filename` and `path` are None (default), it will use the path-and-filename set during initialization. 
            
            
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_channels_from_Excel()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        if filename is None and path is None:
            paf = self.paf
        else:
            paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)
            
        if sheetname is None:
            sheetname = "channels"

        df_channels = GPI.import_df_from_Excel(paf[0], sheetname)        
        
        n_channels = df_channels.shape[0]
        
        self.channels = []
        for i in range(n_channels):
            channel = GPCH.Channel(channel_id = df_channels.loc[i,"channel_id"], device_name = df_channels.loc[i,"device_name"], molecule = df_channels.loc[i,"molecule"])

            molecule_list = []
            for molecule in self.molecules:
                molecule_list.append(molecule.molecule_id)
                
            if channel.molecule.molecule_id not in molecule_list:
                self.molecules.append(GPMO.Molecule(molecule = channel.molecule.molecule))
                molecule_list.append(channel.molecule.molecule_id)
                
            self.channels.append(channel)
        
        self.df_channels = df_channels
            
        

    


    def calculate_concentration(self, verbose = 0, **kwargs):
        """
        
        """        
        verbose = GPF.print_vars(function_name = "GaussianPlume.calculate_concentration()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        self.concentration_model = numpy.zeros((self.n_datapoints, self.n_molecules, self.n_sources))
        self.concentration_model[:,:,:] = numpy.nan

        for molecule_index, molecule in enumerate(self.molecules):
            for source_index, source in enumerate(self.sources):
                if molecule.name == source.molecule.name:
                    conc = source.calculate_concentration(verbose = verbose)
                    self.concentration_model[:, molecule_index, source_index] = conc
            
 
                        
    def export_to_excel(self, verbose = 0, **kwargs):
        """
        
        
        """
        
        
        n_plumes = numpy.amax(self.plume_number) - 1 # len(self.plumes)
        self.plumes = numpy.arange(1,n_plumes+1)
        
        concentration_measured = numpy.zeros((n_plumes, self.n_channels))
        concentration_model = numpy.zeros((n_plumes, self.n_molecules))
        dist = numpy.zeros(n_plumes)
        sigma_y = numpy.zeros(n_plumes)
        sigma_z = numpy.zeros(n_plumes)
        tc = numpy.zeros(n_plumes)
        wind_speed = numpy.zeros(n_plumes)
        wind_direction = numpy.zeros(n_plumes)
        offset_sigma_z = numpy.zeros(n_plumes)
        
        s_idx = -2


        for plume_index, plume in enumerate(self.plumes):
            idx = numpy.where(self.plume_number == plume)[0]
            last_idx = idx[-1]

            dlatM = self.sources[s_idx].dlatM[idx]
            dlonM = self.sources[s_idx].dlonM[idx]   

            d = numpy.sqrt(dlatM**2 + dlonM**2)

            dist[plume_index] = d[-1]

            

            sigma_y[plume_index] = self.sources[s_idx].sigma_y[last_idx]
            sigma_z[plume_index] = self.sources[s_idx].sigma_z[last_idx]
            offset_sigma_z[plume_index] = self.sources[s_idx].offset_sigma_z
            
            if type(self.sources[s_idx].tc) == numpy.ndarray:
                tc[plume_index] = self.sources[s_idx].tc[last_idx]
            else:
                tc[plume_index] = self.sources[s_idx].tc
                
            wind_speed[plume_index] = self.sources[s_idx].wind_speed[last_idx]
            wind_direction[plume_index] = self.sources[s_idx].wind_direction[last_idx]
            
            for molecule_index, molecule in enumerate(self.molecules):
                # label = "ppb {:s}".format(molecule.molecule_id)
            
                concentration_model[plume_index, molecule_index] = self.get_concentration(plume = plume, model = True, source = None, channel = None, molecule = molecule_index, cumulative = True, verbose = verbose, **kwargs)
                

            for channel_index, channel in enumerate(self.channels):
                # label = "channel{:d} ppb".format(channel.channel_id)
                # concentration_measured[plume_index, channel_index] = numpy.sum(self.df.loc[idx, label].to_numpy())
                
                concentration_measured[plume_index, channel_index] = self.get_concentration(plume = plume, model = False, source = None, channel = channel_index, molecule = None, cumulative = True, verbose = verbose, **kwargs)

        df = {
            "dist": dist,
            "sigma_y": sigma_y,
            "sigma_z": sigma_z,
            "offset_sigma_z": offset_sigma_z,
            "tc": tc,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
        }
        
        for molecule_index, molecule in enumerate(self.molecules):
            label = "ppb {:s}".format(molecule.molecule_id)
            df[label] = concentration_model[:, molecule_index]
            
        for channel_index, channel in enumerate(self.channels):
        
            label = "ppb C{:d} measured".format(channel.channel_id)
            df[label] = concentration_measured[:, channel_index]
        
        
        res = pandas.DataFrame(df)
        
        print(res)

            
            
        
        # print(dist)
        # print(concentration_measured)
        # print(concentration_model)
        # print(sigma_y)
        # print(sigma_z)
        # print(tc)
        
    



    def parse_data(self, verbose = 0, **kwargs):
        """
        
        
        Notes
        -----
        
        
      
        
        """

        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_data()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose) 

        self.generate_sources(verbose = verbose, **kwargs)

        self.n_datapoints = self.df.shape[0]
        self.n_sources = len(self.sources)
        self.n_channels = len(self.channels)
        self.n_molecules = len(self.molecules)

        self.concentration_measured = numpy.zeros((self.n_datapoints, self.n_channels))
        
        
        for source_index, source in enumerate(self.sources):
            
            self.parse_wind(source_index, source, verbose = verbose, **kwargs)
            
            # check if dx and dy exist
            flag_dxdy = self.parse_dx_dy(source_index, source, verbose = verbose, **kwargs)
            if flag_dxdy == False:
                # check if dlat/dlon M/S exist
                flag_dlatS_dlonS, flag_dlatM_dlonM = self.parse_dlat_dlon(source_index, source, verbose = verbose, **kwargs)
                # if they don't exist, look for lat/lon for M/S/R and calculate dlat/dlon M/S
                # if this can't be calculated, it will raise an error
                self.parse_lat_lon(source_index, source, flag_dlatS_dlonS, flag_dlatM_dlonM, verbose = verbose, **kwargs)
                # calculate dx dy
                if source.wind_direction is None:
                    raise ValueError("GaussianPlume.parse_data: No valid source for wind_direction, can't calculate distances.")
                source.dx, source.dy = GPF.dlatdlon2dxdy(dlatS = source.dlatS, dlonS = source.dlonS, dlatM = source.dlatM, dlonM = source.dlonM, wind_direction = source.wind_direction, warn_distance_above_meter = source.warn_distance_above_meter, verbose = verbose, **kwargs)
            
            self.parse_other_source_parameters(source_index, source, verbose = verbose, **kwargs)

            log_label = "S{:d} dispersion_constants".format(source.source_id)
            if source.dispersion_constants is None:
                if source.dispersion_mode is None:
                    raise ValueError("Please set source.dispersion_mode")
                source.dispersion_constants = GPF.get_dispersion_constants(source.dispersion_mode, verbose = verbose)
                self.log[log_label] = "calculated during parse_data"
            else:
                self.log[log_label] = "set earlier"
            
            log_label = "S{:d} tc".format(source.source_id)
            if source.tc is None:
                if self.df_sources is not None and "tc" in self.df_sources:
                    source.tc = self.df_sources.loc[source_index,"tc"]
                    self.log[log_label] = "from df_sources"
                elif self.df_static is not None and "tc" in self.df_static:
                    source.tc = self.df_static.loc[source_index,"tc"]
                    self.log[log_label] = "from df_static"              
                else:
                    source.tc = GPF.calculate_tc(source.dx, source.wind_speed, verbose = verbose)
                    self.log[log_label] = "calculated during parse_data"
            else:
                self.log[log_label] = "set earlier"       

            log_label = "S{:d} sigma y and z".format(source.source_id)
            if source.sigma_y is None or source.sigma_z is None:
                source.calculate_sigma_y_z(verbose = verbose)
                self.log[log_label] = "calculated during parse_data"
            else:
                self.log[log_label] = "set earlier"     


        for channel_index, channel in enumerate(self.channels):
            self.parse_channel_parameters(channel_index, channel, verbose = 0, **kwargs)

        self.plume_number = self.channels[0].plume_number
        
            
    def parse_channel_parameters(self, channel_index, channel, verbose = 0, **kwargs):
    
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_channel_parameters()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose) 
        
        label = "ppb C{:d}".format(channel.channel_id)
        self.concentration_measured[:,channel_index] = self.df.loc[:,label].to_numpy()
                    
        log_label = "C{:d} plume_number".format(channel.channel_id)
        if channel.plume_number is None:
            if self.df is not None and "plume_number" in self.df:
                channel.plume_number = self.df.loc[:,"plume_number"].to_numpy()
                idx = numpy.isnan(channel.plume_number)
                channel.plume_number[idx] = 0
                channel.plume_number = numpy.asarray(channel.plume_number, dtype = int)
                self.log[log_label] = "from df"
            else:
                channel.plume_number = numpy.ones(self.n_datapoints)
                self.log[log_label] = "set to 1 (default)"
        else:
            self.log[log_label] = "set earlier"         


    def parse_other_source_parameters(self, source_index, source, verbose = 0, **kwargs):
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_other_source_parameters()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose) 
        
        log_label = "S{:d} qs".format(source.source_id)
        if source.qs is None:
            if self.df_sources is not None and "qs" in self.df_sources:
                source.qs = self.df_sources.loc[source_index,"qs"]
                self.log[log_label] = "from df_sources"
            elif self.df_static is not None and "qs" in self.df_static:
                source.qs = self.df_static.loc[source_index,"qs"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                raise ValueError("GaussianPlume.parse_other_source_parameters: No valid source for qs")
        else:
            self.log[log_label] = "set earlier"     

        log_label = "S{:d} hs".format(source.source_id)
        if source.hs is None:
            if self.df_sources is not None and "hs" in self.df_sources:
                source.hs = self.df_sources.loc[source_index,"hs"]
                self.log[log_label] = "from df_sources"
            elif self.df_static is not None and "hs" in self.df_static:
                source.hs = self.df_static.loc[source_index,"hs"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                raise ValueError("GaussianPlume.parse_other_source_parameters: No valid source for hs")
        else:
            self.log[log_label] = "set earlier"                 

        log_label = "S{:d} hm".format(source.source_id)
        if source.hm is None:
            if self.df_sources is not None and "hm" in self.df_sources:
                source.hm = self.df_sources.loc[source_index,"hm"]
                self.log[log_label] = "from df_sources"
            elif self.df is not None and "hm" in self.df:
                source.hm = self.df.loc[:,"hm"].to_numpy()
                self.log[log_label] = "from df"                
            elif self.df_static is not None and "hm" in self.df_static:
                source.hm = self.df_static.loc[source_index,"hm"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                raise ValueError("GaussianPlume.parse_other_source_parameters: No valid source for hm")
        else:
            self.log[log_label] = "set earlier"   

        log_label = "S{:d} z0".format(source.source_id)
        if source.z0 is None:
            if self.df_sources is not None and "z0" in self.df_sources:
                source.z0 = self.df_sources.loc[source_index,"z0"]
                self.log[log_label] = "from df_sources"
            elif self.df_static is not None and "z0" in self.df_static:
                source.z0 = self.df_static.loc[source_index,"z0"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                raise ValueError("GaussianPlume.parse_other_source_parameters: No valid source for z0")
        else:
            self.log[log_label] = "set earlier"   

        log_label = "S{:d} zr".format(source.source_id)
        if source.zr is None:
            if self.df_sources is not None and "zr" in self.df_sources:
                source.zr = self.df_sources.loc[source_index,"zr"]
                self.log[log_label] = "from df_sources"
            elif self.df is not None and "zr" in self.df:
                source.zr = self.df.loc[:,"zr"].to_numpy()
                self.log[log_label] = "from df"                
            elif self.df_static is not None and "zr" in self.df_static:
                source.zr = self.df_static.loc[source_index,"zr"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                raise ValueError("GaussianPlume.parse_other_source_parameters: No valid source for zr")
        else:
            self.log[log_label] = "set earlier"   

        log_label = "S{:d} offset_sigma_z".format(source.source_id)
        if source.offset_sigma_z is None:
            if self.df_sources is not None and "offset_sigma_z" in self.df_sources:
                source.offset_sigma_z = self.df_sources.loc[source_index,"offset_sigma_z"]
                self.log[log_label] = "from df_sources"
            else:
                source.offset_sigma_z = 0
                self.log[log_label] = "set to 0 (default)"
        else:
            self.log[log_label] = "set earlier"   

        log_label = "S{:d} dispersion_mode".format(source.source_id)
        if source.dispersion_mode is None:
            if self.df_static is not None and "dispersion_mode" in self.df_static:
                source.dispersion_mode = self.df_static.loc[0,"dispersion_mode"]
                self.log[log_label] = "from df_static"
            else:
                source.dispersion_mode = "farm"
                self.log[log_label] = "set to farm (default)"
        else:
            self.log[log_label] = "set earlier"   

        # first check for stability index. When this is set, stability_class is also set. I.e. it won't look for stability_class anymore. 
        log_label = "S{:d} stability_index".format(source.source_id)
        if source.stability_index is None:
            if self.df is not None and "stability_index" in self.df:
                source.stability_index = self.df.loc[:,"stability_index"].to_numpy()
                self.log[log_label] = "from df"
            elif self.df_static is not None and "stability_index" in self.df_static:
                source.stability_index = self.df_static.loc[0,"stability_index"]
                self.log[log_label] = "from df_static"                  
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_other_source_parameters: No valid source for stability_index")
        else:
            self.log[log_label] = "set earlier"

        log_label = "S{:d} stability_class".format(source.source_id)
        if source.stability_class is None:
            if self.df is not None and "stability_class" in self.df:
                source.stability_class = self.df.loc[:,"stability_class"].to_numpy()
                self.log[log_label] = "from df"
            elif self.df_static is not None and "stability_class" in self.df_static:
                source.stability_class = self.df_static.loc[0,"stability_class"]
                self.log[log_label] = "from df_static"                  
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_other_source_parameters: No valid source for stability_class")
        else:
            self.log[log_label] = "set earlier"

        log_label = "S{:d} tc_minimum".format(source.source_id)
        if source.tc_minimum is None:
            if self.df_sources is not None and "tc_minimum" in self.df_sources:
                source.tc_minimum = self.df_sources.loc[source_index,"tc_minimum"]
                self.log[log_label] = "from df_sources"
            elif self.df_static is not None and "tc_minimum" in self.df_static:
                source.tc_minimum = self.df_static.loc[0,"tc_minimum"]
                self.log[log_label] = "from df_static"              
            else:
                source.tc_minimum = 0
                self.log[log_label] = "set to 0 (default)"
        else:
            self.log[log_label] = "set earlier"   


     

    def parse_wind(self, source_index, source, verbose = 0, **kwargs):
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_data_dx_dy()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        log_label = "S{:d} wind_direction".format(source.source_id)
        if source.wind_direction is None:
            if self.df is not None and "wind_direction" in self.df:
                source.wind_direction = self.df.loc[:,"wind_direction"].to_numpy()
                self.log[log_label] = "from df"
            elif self.df_static is not None and "wind_direction" in self.df_static:
                source.wind_direction = self.df_static.loc[source_index,"wind_direction"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_wind: No valid source for wind_direction")                
        else:
            self.log[log_label] = "set earlier"

        log_label = "S{:d} wind_speed".format(source.source_id)
        if source.wind_speed is None:
            if self.df is not None and "wind_speed" in self.df:
                source.wind_speed = self.df.loc[:,"wind_speed"].to_numpy()
                self.log[log_label] = "from df"
            elif self.df_static is not None and "wind_speed" in self.df_static:
                source.wind_speed = self.df_static.loc[source_index,"wind_speed"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                raise ValueError("GaussianPlume.parse_wind: No valid source for wind_speed")
        else:
            self.log[log_label] = "set earlier"

                

    def parse_dx_dy(self, source_index, source, verbose = 0, **kwargs):
    
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_dx_dy()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        log_label = "S{:d} dx".format(source.source_id)
        if source.dx is None:
            label = "dxS{:d}".format(source.source_id)
            if self.df is not None and label in self.df:
                source.dx = self.df.loc[:,label].to_numpy()
                self.log[log_label] = "from df SX"
            elif self.df_sources is not None and "dx" in self.df_sources:
                source.dx = self.df_sources.loc[source_index,"dx"]
                self.log[log_label] = "from df_sources"
            elif self.df is not None and "dxS" in self.df:
                source.dx = self.df.loc[:,"dxS"].to_numpy()   
                self.log[log_label] = "from df S"    
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_dx_dy: No valid source for dx for Source with source_id {:d}".format(source.source_id))
        else:
            self.log[log_label] = "set earlier"
    
        log_label = "S{:d} dy".format(source.source_id)
        if source.dy is None:
            label = "dyS{:d}".format(source.source_id)
            if self.df is not None and label in self.df:
                source.dy = self.df.loc[:,label].to_numpy()
                self.log[log_label] = "from df SX"
            elif self.df_sources is not None and "dy" in self.df_sources:
                source.dy = self.df_sources.loc[source_index,"dy"]
                self.log[log_label] = "from df_sources"
            elif self.df is not None and "dyS" in self.df:
                source.dy = self.df.loc[:,"dyS"].to_numpy()   
                self.log[log_label] = "from df S"                      
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_dx_dy: No valid source for dy for Source with source_id {:d}".format(source.source_id))
        else:
            self.log[log_label] = "set earlier"

        
        if source.dx is not None and source.dy is not None:
            return True
        else:
            return False

    def parse_dlat_dlon(self, source_index, source, verbose = 0, **kwargs):
        """
        
        """        
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_dlat_dlon()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        log_label = "S{:d} warn_distance_above_meter".format(source.source_id)
        if source.warn_distance_above_meter is None:
            if self.df_sources is not None and "warn_distance_above_meter" in self.df_static:
                source.warn_distance_above_meter = self.df_static.loc[0,"warn_distance_above_meter"]
                self.log[log_label] = "from df_static"
            else:
                source.warn_distance_above_meter = 100000
                self.log[log_label] = "set to 100000 (default)"

        log_label = "S{:d} dlatS".format(source.source_id)
        if source.dlatS is None:
            label = "dlatS{:d}".format(source.source_id)
            if self.df is not None and label in self.df:
                source.dlatS = self.df.loc[:,label].to_numpy()
                self.log[log_label] = "from df SX"
            elif self.df_sources is not None and "dlatS" in self.df_sources:
                source.dlatS = self.df_sources.loc[source_index,"dlatS"]
                self.log[log_label] = "from df_sources"
            elif self.df is not None and "dlatS" in self.df:
                source.dlatS = self.df.loc[:,"dlatS"].to_numpy()   
                self.log[log_label] = "from df S"    
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_dlat_dlon: No valid source for dlatS for Source with source_id {:d}".format(source.source_id))
        else:
            self.log[log_label] = "set earlier"
    
        log_label = "S{:d} dlonS".format(source.source_id)
        if source.dlonS is None:
            label = "dlonS{:d}".format(source.source_id)
            if self.df is not None and label in self.df:
                source.dlonS = self.df.loc[:,label].to_numpy()
                self.log[log_label] = "from df SX"
            elif self.df_sources is not None and "dlonS" in self.df_sources:
                source.dlonS = self.df_sources.loc[source_index,"dlonS"]
                self.log[log_label] = "from df_sources"
            elif self.df is not None and "dlonS" in self.df:
                source.dlonS = self.df.loc[:,"dlonS"].to_numpy()   
                self.log[log_label] = "from df S"    
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_dlat_dlon: No valid source for dlonS for Source with source_id {:d}".format(source.source_id))
        else:
            self.log[log_label] = "set earlier"

        flag_dlatS_dlonS = False
        if source.dlatS is not None and source.dlonS is not None:
            flag_dlatS_dlonS = True

        log_label = "S{:d} dlatM".format(source.source_id)
        if source.dlatM is None:
            label = "dlatM{:d}".format(source.source_id)
            if self.df is not None and label in self.df:
                source.dlatM = self.df.loc[:,label].to_numpy()
                self.log[log_label] = "from df"
            elif self.df_static is not None and "dlatM" in self.df_static:
                source.dlatM = self.df_static.loc[source_index,"dlatM"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_dlat_dlon: No valid source for dlatM for Source with source_id {:d}".format(source.source_id))
        else:
            self.log[log_label] = "set earlier"
    
        log_label = "S{:d} dlonM".format(source.source_id)
        if source.dlonM is None:
            label = "dlonM{:d}".format(source.source_id)
            if self.df is not None and label in self.df:
                source.dlonM = self.df.loc[:,label].to_numpy()
                self.log[log_label] = "from df"
            elif self.df_static is not None and "dlonM" in self.df_static:
                source.dlonM = self.df_static.loc[source_index,"dlonM"]
                self.log[log_label] = "from df_static"  
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_dlat_dlon: No valid source for dlonM for Source with source_id {:d}".format(source.source_id))
        else:
            self.log[log_label] = "set earlier"

        flag_dlatM_dlonM = False
        if source.dlatM is not None and source.dlonM is not None:
            flag_dlatM_dlonM = True
        
        return flag_dlatS_dlonS, flag_dlatM_dlonM

    def parse_lat_lon(self, source_index, source, flag_dlatS_dlonS = False, flag_dlatM_dlonM = False, verbose = 0, **kwargs):
        """
        
        """        
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_lat_lon()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        # the distances to the reference is missing for the source, the measurement. First check if the reference position is known. 
        if flag_dlatS_dlonS == False or flag_dlatM_dlonM == False:
            log_label = "S{:d} latR".format(source.source_id)
            if source.latR is None:
                if self.df_static is not None and "latR" in self.df_static:
                    source.latR = self.df_static.loc[0,"latR"]
                    self.log[log_label] = "from df_static" 
                else:
                    self.log[log_label] = "not set"
                    raise ValueError("GaussianPlume.parse_lat_lon(): The position of the reference (latR) is unknown, can't calculate the distances.")
            else:
                self.log[log_label] = "set earlier"

            log_label = "S{:d} lonR".format(source.source_id)
            if source.lonR is None:
                if self.df_static is not None and "lonR" in self.df_static:
                    source.lonR = self.df_static.loc[0,"lonR"]
                    self.log[log_label] = "from df_static" 
                else:
                    self.log[log_label] = "not set"
                    raise ValueError("GaussianPlume.parse_lat_lon(): The position of the reference (lonR) is unknown, can't calculate the distances.")
            else:
                self.log[log_label] = "set earlier"

        if source.latR is None or source.lonR is None:
            raise ValueError("GaussianPlume.parse_lat_lon(): The position of the reference is unknown, can't calculate the distances.")
    
        if flag_dlatS_dlonS == False:
            log_label = "S{:d} latS".format(source.source_id)
            if source.latS is None:
                label = "latS{:d}".format(source.source_id)
                if self.df is not None and label in self.df:
                    source.latS = self.df.loc[:,label].to_numpy()
                    self.log[log_label] = "from df SX"
                elif self.df_sources is not None and "latS" in self.df_sources:
                    source.latS = self.df_sources.loc[source_index,"latS"]
                    self.log[log_label] = "from df_sources"
                elif self.df is not None and "latS" in self.df:
                    source.latS = self.df.loc[:,"latS"].to_numpy()   
                    self.log[log_label] = "from df S"    
                else:
                    self.log[log_label] = "not set"
                    raise ValueError("GaussianPlume.parse_lat_lon(): The position of Source {:d} (latS) is unknown, can't calculate the distances.".format(source.source_id))
            else:
                self.log[log_label] = "set earlier"

            log_label = "S{:d} lonS".format(source.source_id)
            if source.lonS is None:
                label = "lonS{:d}".format(source.source_id)
                if self.df is not None and label in self.df:
                    source.lonS = self.df.loc[:,label].to_numpy()
                    self.log[log_label] = "from df SX"
                elif self.df_sources is not None and "lonS" in self.df_sources:
                    source.lonS = self.df_sources.loc[source_index,"lonS"]
                    self.log[log_label] = "from df_sources"
                elif self.df is not None and "lonS" in self.df:
                    source.lonS = self.df.loc[:,"lonS"].to_numpy()   
                    self.log[log_label] = "from df S"    
                else:
                    self.log[log_label] = "not set"
                    raise ValueError("GaussianPlume.parse_lat_lon(): The position of Source {:d} (lonS) is unknown, can't calculate the distances.".format(source.source_id))
            else:
                self.log[log_label] = "set earlier"

            if source.latS is None or source.lonS is None:
                raise ValueError("GaussianPlume.parse_lat_lon(): The position of the source is unknown, can't calculate the distances.")

            source.dlatS, source.dlonS = GPF.latlon2dlatdlon(lat = source.latS, lon = source.lonS, latR = source.latR, lonR = source.lonR, warn_distance_above_meter = source.warn_distance_above_meter, verbose = verbose, **kwargs)

        if flag_dlatM_dlonM == False:
            log_label = "S{:d} latM".format(source.source_id)
            if source.latM is None:
                if self.df is not None and "latM" in self.df:
                    source.latM = self.df.loc[:,"latM"].to_numpy()
                    self.log[log_label] = "from df"
                elif self.df_static is not None and "latM" in self.df_static:
                    source.latM = self.df_static.loc[source_index,"latM"]
                    self.log[log_label] = "from df_static" 
                else:
                    self.log[log_label] = "not set"
                    raise ValueError("GaussianPlume.parse_lat_lon(): The position of the measurement (latM) is unknown, can't calculate the distances.")
            else:
                self.log[log_label] = "set earlier"

            log_label = "S{:d} lonM".format(source.source_id)
            if source.lonM is None:
                if self.df is not None and "lonM" in self.df:
                    source.lonM = self.df.loc[:,"lonM"].to_numpy()
                    self.log[log_label] = "from df"
                elif self.df_static is not None and "lonM" in self.df_static:
                    source.lonM = self.df_static.loc[source_index,"lonM"]
                    self.log[log_label] = "from df_static" 
                else:
                    self.log[log_label] = "not set"
                    raise ValueError("GaussianPlume.parse_lat_lon(): The position of the measurement (lonM) is unknown, can't calculate the distances.")
            else:
                self.log[log_label] = "set earlier"

            if source.latM is None or source.lonM is None:
                raise ValueError("GaussianPlume.parse_lat_lon(): The position of the measurement is unknown, can't calculate the distances.")

            source.dlatM, source.dlonM = GPF.latlon2dlatdlon(lat = source.latM, lon = source.lonM, latR = source.latR, lonR = source.lonR, warn_distance_above_meter = source.warn_distance_above_meter, verbose = verbose, **kwargs)



    def get_concentration(self, plume = None, model = True, source = None, channel = None, molecule = None, cumulative = False, verbose = 0, **kwargs):
        """
        
        Arguments
        ---------
        plume : number or list (default None)
            The plume number(s). If None, it will return all data points.
        model : Bool (True)
            If True, return the data from the model. If False, return the measured data.
        source : number (default None)
            The number of the source. If None, return all sources. Only used for model data.
        channel : number (default None)
            The number of the channel. If None, return all channels. Only used for measured data.
        molecule : number (default None)
            The number of the molecule. If None, return all molecule. Only used for model data.  
        cumulative : Bool (False)
            If True, sum all data. If False, return as an array. 
            
        """        
        verbose = GPF.print_vars(function_name = "GaussianPlume.get_concentration()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        if type(plume) in (list, numpy.ndarray):
            idx = numpy.array([], dtype = int)
            for p in plume:
                _idx = numpy.where(p == self.plume_number)[0]
                idx = numpy.concatenate((idx, _idx))
        elif plume is None:
            idx = numpy.arange(self.n_datapoints)
        else:
            idx = numpy.where(plume == self.plume_number)[0]
        
        if model:
            source_idx = None 
            if source is not None:
                source_idx = source

            molecule_idx = None 
            if molecule is not None:
                molecule_idx = molecule     
      
            if source_idx is None and molecule_idx is None:
                conc = self.concentration_model[idx,:,:]
            elif source_idx is None and molecule_idx is not None:
                conc = self.concentration_model[idx,molecule_idx,:] 
            elif source_idx is not None and molecule_idx is None:
                conc = self.concentration_model[idx,:,source_idx]
            else:
                conc = self.concentration_model[idx,molecule_idx,:][:,source_idx]

        else:
            channel_idx = None
            if channel is not None:
                channel_idx = channel        
            
            if channel_idx is None:
                conc = self.concentration_measured[idx,:]
            else:
                conc = self.concentration_measured[idx,channel_idx]

        if cumulative:
            return numpy.nansum(conc)
        else:
            return conc




























        