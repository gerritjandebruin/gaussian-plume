import importlib

import pandas
import numpy
import PythonTools.ClassTools as CT
import GPFunctions as GPF
import GPImport as GPI
import GPSource as GPSO
import GPChannel as GPCH

importlib.reload(GPF)
importlib.reload(GPI)
importlib.reload(GPSO)
importlib.reload(GPCH)

class GaussianPlume(CT.ClassTools):
    """
    Attributes
    ---------
    source : list
        List with sources.
        
        
    
    
    """

    def __init__(self, verbose = 0, **kwargs):
        """
        
        Attributes
        ---------
        
        
        """
        self.verbose = verbose
        
        verbose = GPF.print_vars(function_name = "GaussianPlume.GaussianPlume.__init__()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        self.sources = kwargs.get("sources", None)
        self.channels = kwargs.get("channels", None)
        self.molecules = kwargs.get("molecules", None)
        self.plumes = kwargs.get("plumes", None)

        self.log = kwargs.get("log", {"comment": ""})

        if "comment" in kwargs:
            self.log["comment"] = "{:s}\n__init__: {:s}".format(self.log["comment"], kwargs["comment"])
        
        # self.wind_speed = None
        # self.tc = None
        # self.dispersion_mode = None
        # self.plume_number = None

        # self._stability_index = None
        # self._stability_class = None

        # if "df" in kwargs:
            # self.df = kwargs["df"]
        # else:
            # self._df = None
        
        self.df = kwargs.get("df", None)
        self.df_sources = kwargs.get("df_sources", None)
        self.df_channels = kwargs.get("df_channels", None)
        self.df_static = kwargs.get("df_static", None)
        
        # self.wind_speed = kwargs.get("wind_speed", self.wind_speed)
        # self.tc = kwargs.get("tc", self.tc)
        # self.dispersion_mode = kwargs.get("dispersion_mode", self.dispersion_mode)
        # self.plume_number = kwargs.get("plume_number", self.plume_number)

        # if "stability_index" in kwargs:
            # self.stability_index = kwargs["stability_index"]
        # elif "stability_class" in kwargs:
            # self.stability_class = kwargs["stability_class"]

    # @property
    # def stability_index(self):
        # """
        # Index of the stability class. 0 equals class A, 5 equals class F.
        # """
        # return self._stability_index

    # @stability_index.setter
    # def stability_index(self, value):
        # self._stability_index = value
        # self._stability_class = GPF.stability_index2class(value)

    # @property
    # def stability_class(self):
        # """
        # Stability class. Class A equals index 0, class F equals index 5. 
        # """    
        # return self._stability_class

    # @stability_class.setter
    # def stability_class(self, value):
        # self._stability_class = value
        # self._stability_index = GPF.stability_class2index(value)   

    # @property
    # def df(self):
        # """
        
        # """
        # return self._df

    # @df.setter
    # def df(self, value):
        # self._df = value
        # cn = value.columns
        # if "wind_speed" in cn:
            # self.wind_speed = value.loc[:,"wind_speed"].to_numpy() 
        # if "tc" in cn:
            # self.tc = value.loc[:,"tc"].to_numpy() 
        # if "dispersion_mode" in cn:
            # self.dispersion_mode = value.loc[:,"dispersion_mode"].to_numpy() 
        # if "plume_number" in cn:
            # self.plume_number = value.loc[:,"plume_number"].to_numpy()             

        # if "stability_index" in cn:
            # self.stability_index = value.loc[:,"stability_index"].to_numpy() 
        # if "stability_class" in cn:
            # self.stability_class = value.loc[:,"stability_class"].to_numpy()             
    
    
    def import_static_parameters(self, sheetname = None, filename = None, path = None, verbose = 0, **kwargs):
        """
        
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_static_parameters()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)

        if sheetname is None:
            sheetname = "static parameters"

        df_static = GPI.import_df_from_Excel(paf[0], sheetname, index_col = 0, header = None)   

        df_static = df_static.transpose()
        df_static = df_static.reset_index(drop = True)

        self.df_static = df_static

        # self.df_static = df_static
        
        # cn = df_static.index
        # if "latR" in cn:
            # self.latR = df_static.loc["latR",1]
        # if "lonR" in cn:
            # self.lonR = df_static.loc["lonR",1]            

        # if "latM" in cn:
            # self.latM = df_static.loc["latM",1]
        # if "lonM" in cn:
            # self.lonM = df_static.loc["lonM",1]   
            
        # if "latS" in cn:
            # self.latS = df_static.loc["latS",1]
        # if "lonS" in cn:
            # self.lonS = df_static.loc["lonS",1]               

        # if "wind_speed" in cn:
            # self.wind_speed = df_static.loc["wind_speed",1]
        # if "tc" in cn:
            # self.tc = df_static.loc["tc",1]
        # if "dispersion_mode" in cn:
            # self.dispersion_mode = df_static.loc["dispersion_mode",1]

        # if "stability_index" in cn:
            # self.stability_index = df_static.loc["stability_index",1]
        # if "stability_class" in cn:
            # self.stability_class = df_static.loc["stability_class",1]
        
    
    def import_measurement_data_from_Excel(self, sheetname = None, filename = None, path = None, drop_non_plume = False, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_measurement_data_from_Excel()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  
        
        # if filename is None and path is None:
            
        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)
        
        if sheetname is None:
            sheetname = "data"
        
        df = GPI.import_df_from_Excel(paf[0], sheetname)
    
        # if drop_non_plume:
            # df.drop(df.index[df['plume_number'] == 0], inplace=True)
            # df.drop(df.index[numpy.isnan(df['plume_number'])], inplace=True)
            
        
        self.df = df



    def import_measurement_data_from_csv(self, filename = None, path = None, drop_non_plume = False, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_measurement_data_from_csv()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  
        
        # if filename is None and path is None:
            
        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)

        df = GPI.import_df_from_csv(paf[0])
    
        # if drop_non_plume:
            # df.drop(df.index[df['plume_number'] == 0], inplace=True)
            # df.drop(df.index[numpy.isnan(df['plume_number'])], inplace=True)
            
        
        self.df = df

    def import_sources_from_Excel(self, sheetname = None, filename = None, path = None, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_sources_from_Excel()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)

        if sheetname is None:
            sheetname = "sources"

        self.df_sources = GPI.import_df_from_Excel(paf[0], sheetname)
        
        n_sources = self.df_sources.shape[0]
        
        self.sources = []
        for i in range(n_sources):
            
            source = GPSO.Source(source_id = self.df_sources.loc[i,"source_id"], molecule = self.df_sources.loc[i,"molecule"])

            # cn = source_df.columns
            # if "latS" in cn:
                # source.latS = source_df.loc[i,"latS"]  
            # if "lonS" in cn:
                # source.lonS = source_df.loc[i,"lonS"]     

            # if "dlatS" in cn:
                # source.dlatS = source_df.loc[i,"dlatS"]  
            # if "dlonS" in cn:
                # source.dlonS = source_df.loc[i,"dlonS"]                     

            # if "qs" in cn:
                # source.qs = source_df.loc[i,"qs"]  
            # if "hs" in cn:
                # source.hs = source_df.loc[i,"hs"]   
                
            # if "z0" in cn:
                # source.z0 = source_df.loc[i,"z0"]  
            # if "offset_sigma_z" in cn:
                # source.offset_sigma_z = source_df.loc[i,"offset_sigma_z"]   
            
            self.sources.append(source)

        # self.df_sources = df_sources


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



    def import_channels_from_Excel(self, sheetname = None, filename = None, path = None, verbose = 0, **kwargs):
        """
        
        """
        verbose = GPF.print_vars(function_name = "GaussianPlume.import_channels_from_Excel()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        paf = GPF.handle_filename_path(filename = filename, path = path, verbose = verbose)

        if sheetname is None:
            sheetname = "channels"

        df_channels = GPI.import_df_from_Excel(paf[0], sheetname)        
        
        n_channels = df_channels.shape[0]
        
        self.channels = []
        for i in range(n_channels):
            channel = GPCH.Channel(channel_id = df_channels.loc[i,"channel_id"], device_name = df_channels.loc[i,"device_name"], molecule = df_channels.loc[i,"molecule"])
            
            self.channels.append(channel)
        
        self.df_channels = df_channels
            
        

    # def update_sources_from_df(self, verbose = 0, **kwargs):
        # """
        # """
        # verbose = GPF.print_vars(function_name = "GaussianPlume.update_sources_from_df()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

        # cn = self.df.columns
        # for source_index, source in enumerate(self.sources):
            # if "latM" in cn:
                # source.latM = self.df.loc[:,"latM"].to_numpy()    
            # if "lonM" in cn:
                # source.lonM = self.df.loc[:,"lonM"].to_numpy()   
            # if "wind_direction" in cn:
                # source.wind_direction = self.df.loc[:,"wind_direction"].to_numpy()    
            # if "wind_speed" in cn:
                # source.wind_speed = self.df.loc[:,"wind_speed"].to_numpy()    
            # if "stability_index" in cn:
                # source.stability_index = self.df.loc[:,"stability_index"].to_numpy()  
            
            # label = "latS{:d}".format(source.source_id)
            # if label in cn:
                # source.latS = self.df.loc[:,label].to_numpy()   
                
            # label = "lonS{:d}".format(source.source_id)
            # if label in cn:
                # source.lonS = self.df.loc[:,label].to_numpy()            

    


    def calculate_concentration(self, verbose = 0, **kwargs):
        """
        
        """        
        verbose = GPF.print_vars(function_name = "GaussianPlume.calculate_concentration()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)    

        # dispersion_constants = GPF.get_dispersion_constants(dispersion_mode = self.dispersion_mode, verbose = verbose)
        
        for source_index, source in enumerate(self.sources):

            log_label = "S{:d} dispersion_constants".format(source.source_id)
            if source.dispersion_constants is None:
                if source.dispersion_mode is None:
                    raise ValueError("Please set source.dispersion_mode")
                source.dispersion_constants = GPF.get_dispersion_constants(source.dispersion_mode, verbose = verbose)
                self.log[log_label] = "calculated during calculate_concentration"
            else:
                self.log[log_label] = "set earlier"
            
            log_label = "S{:d} tc".format(source.source_id)
            if source.tc is None:
                source.tc = GPF.calculate_tc(source.dx, source.wind_speed, verbose = verbose)
                self.log[log_label] = "calculated during calculate_concentration"
            else:
                self.log[log_label] = "set earlier"       

            log_label = "S{:d} sigma y and z".format(source.source_id)
            if source.sigma_y is None or source.sigma_z is None:
                source.calculate_sigma_y_z(verbose = verbose)
                self.log[log_label] = "calculated during calculate_concentration"
            else:
                self.log[log_label] = "set earlier"                
            
            # source.dispersion_mode = self.dispersion_mode
            
            # source.calculate_dxdy(verbose = verbose)
            
            
        for channel_index, channel in enumerate(self.channels):
        
            channel.concentration_model = numpy.zeros((len(source.dx), len(self.sources)))
            channel.plume_number = self.df.loc[:,"plume_number"].to_numpy()
            if verbose > 2:
                print("channel, index {:d}: {:4s} {:s}".format(channel_index, channel.molecule.name, channel.device_name))
            
            molecule = channel.molecule
            # if verbose > 2:
                # print("  molecule, index {:d}: {:s}".format(molecule_index, molecule.name))
            
            total_concentration = 0 
            
            for source_index, source in enumerate(self.sources):
                if verbose > 2:
                    print("    source, index {:d}: {:}".format(source_index, source.label))
                    
                channel.concentration_model[:,source_index] = source.calculate_concentration(verbose = verbose)
                    
                    
                # print(molecule.molecular_mass)
                # channel.concentration_model[:,source_index] = GPF.calculate_concentration(qs = source.qs, wind_speed = self.df.loc[:,"wind_speed"].to_numpy(), sigma_y = source.sigma_y, sigma_z = source.sigma_z, dy = source.dy, zr = self.df.loc[:,"zr"].to_numpy(), hs = source.hs, hm = self.df.loc[:,"hm"].to_numpy(), molecular_mass = molecule.molecular_mass, verbose = verbose)
                
                # for plume_index, plume in enumerate(self.plumes):
                    # conc = channel.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = True, verbose = verbose)
                    # print("source: {:s}, plume: {:d}:{:6.2f}".format(source.label, plume, conc))

                    # conc = channel.get_concentration_for_plume(plume, model = True, source_index = source_index, cumulative = False, verbose = verbose)
                    # print(conc)
                        
    def export_to_excel(self, verbose = 0, **kwargs):
        """
        
        
        """
        n_plumes = len(self.plumes)
        
        concentration_measured = numpy.zeros((n_plumes, len(self.channels)))
        concentration_model = numpy.zeros((n_plumes, len(self.channels)))
        dist = numpy.zeros(n_plumes)
        sigma_y = numpy.zeros(n_plumes)
        sigma_z = numpy.zeros(n_plumes)
        tc = numpy.zeros(n_plumes)
        wind_speed = numpy.zeros(n_plumes)
        wind_direction = numpy.zeros(n_plumes)
        offset_sigma_z = numpy.zeros(n_plumes)
        
        s_idx = -2
        
        # print(self.sources[s_idx])
        
        for plume_index, plume in enumerate(self.plumes):
            idx = numpy.where(self.plume_number == plume)[0]
            last_idx = idx[-1]
            # print(self.sources[0].dlonM[idx])
            # dx = numpy.mean(self.sources[-1].dx[idx])
            # dy = numpy.mean(self.sources[-1].dy[idx])
            # for source_index, source in enumerate(self.sources):
                # if source.source_id == 3:
                    # print(source.source_id)
                    # print("dx", self.sources[source_index].dx[last_idx])
                    # print("dy", self.sources[source_index].dy[last_idx])
                    # print("dlatS", self.sources[source_index].dlatS)
                    # print("dlonS", self.sources[source_index].dlonS)
                    # # print("dlatM", self.sources[source_index].dlatM[idx])
                    # # print("dlonM", self.sources[source_index].dlonM[idx])
                    # print("wind_direction", self.sources[source_index].wind_direction[idx])                
                    # print()
            # dx = self.sources[-1].dx[idx]
            # dy = self.sources[-1].dy[idx]
                # print("source", source.source_id)
                # print(source.dlatS)
                # print(source.dlonS)
            dlatM = self.sources[s_idx].dlatM[idx]
            dlonM = self.sources[s_idx].dlonM[idx]   
            # print("dx", dx)
            # print(dx, dy)
            d = numpy.sqrt(dlatM**2 + dlonM**2)
            # print(d[-1])
            dist[plume_index] = d[-1]
            # print(d)
            
            # print(self.sources[s_idx].sigma_y[idx])
            sigma_y[plume_index] = self.sources[s_idx].sigma_y[last_idx]
            sigma_z[plume_index] = self.sources[s_idx].sigma_z[last_idx]
            offset_sigma_z[plume_index] = self.sources[s_idx].offset_sigma_z
            
            tc[plume_index] = self.sources[s_idx].tc[last_idx]
            wind_speed[plume_index] = self.sources[s_idx].wind_speed[last_idx]
            wind_direction[plume_index] = self.sources[s_idx].wind_direction[last_idx]
            
            for channel_index, channel in enumerate(self.channels):
                label = "channel{:d} ppb".format(channel.channel_id)
                concentration_measured[plume_index, channel_index] = numpy.sum(self.df.loc[idx, label].to_numpy())
                
                concentration_model[plume_index, channel_index] = channel.get_concentration_for_plume(plume, model = True, source_index = None, cumulative = True, verbose = verbose)

        df = {
            "dist": dist,
            "sigma_y": sigma_y,
            "sigma_z": sigma_z,
            "offset_sigma_z": offset_sigma_z,
            "tc": tc,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
        }
        
        for channel_index, channel in enumerate(self.channels):
            label = "ppbC{:d} model".format(channel.channel_id)
            df[label] = concentration_model[:, channel_index]
            label = "ppbC{:d} measured".format(channel.channel_id)
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
                    raise ValueError("GaussianPlume.parse_wind: No valid source for wind_direction, can't calculate distances.")
                source.dx, source.dy = GPF.dlatdlon2dxdy(dlatS = source.dlatS, dlonS = source.dlonS, dlatM = source.dlatM, dlonM = source.dlonM, wind_direction = source.wind_direction, verbose = verbose, **kwargs)
            
            self.parse_other_source_parameters(source_index, source, verbose = verbose, **kwargs)

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
                source.stability_index = self.df_static.loc[source_index,"stability_index"]
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
                source.stability_class = self.df_static.loc[source_index,"stability_class"]
                self.log[log_label] = "from df_static"                  
            else:
                self.log[log_label] = "not set"
                if verbose > 1:
                    print("GaussianPlume.parse_other_source_parameters: No valid source for stability_class")
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
    
        verbose = GPF.print_vars(function_name = "GaussianPlume.parse_data_dx_dy()", function_vars = vars(), verbose = verbose, self_verbose = self.verbose)  

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

            source.dlatS, source.dlonS = GPF.latlon2dlatdlon(lat = source.latS, lon = source.lonS, latR = source.latR, lonR = source.lonR, verbose = verbose, **kwargs)


        # flag_latS_lonS = False
        # if source.latS is not None and source.lonS is not None:
            # flag_latS_lonS = True

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

            source.dlatM, source.dlonM = GPF.latlon2dlatdlon(lat = source.latM, lon = source.lonM, latR = source.latR, lonR = source.lonR, verbose = verbose, **kwargs)










        