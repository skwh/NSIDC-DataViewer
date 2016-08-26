from datetime import datetime, timedelta
import numpy as np
import struct
import matplotlib.image as mpimg

COLORMAPS = ["Blues", "jet", "terrain_r", "winter", "gist_ncar", "rainbow", "magma", "prism", "spectral", "cool", "gist_earth_r"]

#blatantly copied from http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def single_daterange(timeframe):
    for n in range(int ((timeframe[1] - timeframe[0]).days)):
        yield timeframe[0] + timedelta(n)        

def week_daterange(timeframe):    
    for n in range(int ((timeframe[1] - timeframe[0]).days / 7)):
        yield timeframe[0] + timedelta(n*7)
        
def form_smashed_date(date):
    return str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)

def form_uri(current_source, start_date, **kwargs):
    if 'end_date' in kwargs:
        return current_source.format(yyyy=start_date.year, 
                                     yymmdd=form_smashed_date(start_date), 
                                     syymmdd=form_smashed_date(start_date), 
                                     eyymmdd=form_smashed_date(kwargs['end_date']))
    else:
        return current_source.format(yyyy=start_date.year, 
                                     yymmdd=form_smashed_date(start_date), 
                                     syymmdd=form_smashed_date(start_date))
def generate_dates_array(timeframe, **kwargs):
    dates_array = []
    if 'week' in kwargs:
        for date in week_daterange(timeframe):
            dates_array.append(date)
    else:
        for date in single_daterange(timeframe):
            dates_array.append(date)
    return dates_array

def get_current_datetime(dates_array, index):
    return dates_array[index]

def separate_data(data, byte):
    return np.minimum(data, byte)

def set_last_dataset(new_dataset):
    global LAST_DATASET 
    LAST_DATASET = new_dataset
    
def get_last_dataset():
    return LAST_DATASET

def create_plot(plot, date, data, colormap, separate_byte, **kwargs):
    if 'title' in kwargs:
        plot.title(kwargs['title'] + " " + str(date))
    else:
        plot.title(str(date))
        
    if separate_byte != 0:
        image = plot.imshow(separate_data(data, separate_byte), cmap=colormap, animated=True)
    else:
        image = plot.imshow(data, cmap=colormap, animated=True)
     
    return image

def get_colormaps():
    return COLORMAPS

def pretty_print_colormaps():
    for s in COLORMAPS:
        print(s)
        

def pretty_print_sources(dataset):
    if dataset == "0051":
        for key in nsidc0051.get_formats_dict():
            print(key + " = " + nsidc0051.get_formats_dict()[key] + "\n")
    else:
        for key in nsidc0046.get_formats_dict():
            print(key + " = " + nsidc0046.get_formats_dict()[key] + "\n")
            
def get_sources(dataset):
    if dataset == "0051":
        return nsidc0051.get_formats_tup()
    else:
        return nsidc0046.get_formats_tup()
    
def get_current_dataset_shape(data_file_uri, col_st, row_st):
    with open(data_file_uri, 'rb') as fp:
        data = fp.read()
        cols = int(data[row_st:row_st+4].decode("utf-8"))
        rows = int(data[col_st:col_st+4].decode("utf-8"))
    return (rows, cols)
    

class nsidc0051:
    NSIDC_0051_NORTH_URL_FORMAT = "/projects/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/north/daily/{yyyy}/nt_{yymmdd}_f17_v1.1_n.bin"

    NSIDC_0051_SOUTH_URL_FORMAT = "/projects/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/{yyyy}/nt_{yymmdd}_f17_v1.1_s.bin"

    NSIDC_0051_NORTH_STAGING_URL_FORMAT = "/disks/sidads_staging/DATASETS/nsidc0051_ gsfc_nasateam_seaice/final-gsfc/north/daily/{yyyy}/nt_{yymmdd}_f17_v1.1_n.bin"

    NSIDC_0051_SOUTH_STAGING_URL_FORMAT = "/disks/sidads_staging/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/{yyyy}/nt_{yymmdd}_f17_v1.1_s.bin"
    
    @staticmethod
    def get_formats_tup():
        return (nsidc0051.NSIDC_0051_NORTH_URL_FORMAT, 
                nsidc0051.NSIDC_0051_SOUTH_URL_FORMAT, 
                nsidc0051.NSIDC_0051_NORTH_STAGING_URL_FORMAT, 
                nsidc0051.NSIDC_0051_SOUTH_STAGING_URL_FORMAT)
    
    @staticmethod
    def get_formats_dict():
        return {"NSIDC_0051_NORTH_URL_FORMAT":nsidc0051.NSIDC_0051_NORTH_URL_FORMAT, 
                "NSIDC_0051_SOUTH_URL_FORMAT":nsidc0051.NSIDC_0051_SOUTH_URL_FORMAT, 
                "NSIDC_0051_NORTH_STAGING_URL_FORMAT":nsidc0051.NSIDC_0051_NORTH_STAGING_URL_FORMAT, 
                "NSIDC_0051_SOUTH_STAGING_URL_FORMAT":nsidc0051.NSIDC_0051_SOUTH_STAGING_URL_FORMAT}

class nsidc0046:
    NSIDC_0046_FORMAT = "/projects/DATASETS/nsidc0046_weekly_snow_seaice/data/EASE2_N25km.snowice.{syymmdd}-{eyymmdd}.v04.bin"

    NSIDC_0046_STAGING_FORMAT = "/disks/sidads_staging/DATASETS/nsidc0046_weekly_snow_seaice/data/EASE2_N25km.snowice.{syymmdd}-{eyymmdd}.v04.bin"

    NSIDC_0046_BROWSE_STAGING_FORMAT = "/disks/sidads_staging/DATASETS/nsidc0046_weekly_snow_seaice/browse/EASE2_N25km.snowice.{syymmdd}-{eyymmdd}.v04.png"
    
    @staticmethod
    def get_formats_tup():
        return (nsidc0046.NSIDC_0046_FORMAT,
                nsidc0046.NSIDC_0046_STAGING_FORMAT,
                nsidc0046.NSIDC_0046_BROWSE_STAGING_FORMAT)
    
    @staticmethod
    def get_formats_dict():
        return {"NSIDC_0046_FORMAT":nsidc0046.NSIDC_0046_FORMAT,
                "NSIDC_0046_STAGING_FORMAT":nsidc0046.NSIDC_0046_STAGING_FORMAT,
                "NSIDC_0046_BROWSE_STAGING_FORMAT":nsidc0046.NSIDC_0046_BROWSE_STAGING_FORMAT}
    
class const:
    CURRENT_SOURCE = ""
    DATES_ARRAY = []
    CURRENT_COLORMAP = ""
    DATASET_SHAPE = (0,0)
    PLOT = None
    SEPARATE_BYTE = 0
    VERBOSE = False
    PNG = False
    RANGE = False
    
    @staticmethod
    def set_constants(**kwargs):
        const.CURRENT_SOURCE = kwargs['cs']
        const.DATES_ARRAY = kwargs['da']
        const.CURRENT_COLORMAP = kwargs['cc']
        const.DATASET_SHAPE = kwargs['ds']
        const.PLOT = kwargs['p']
        const.SEPARATE_BYTE = kwargs['sb']
        const.VERBOSE = kwargs['v']
        const.PNG = kwargs['png']
        const.RANGE = kwargs['rng']
    
    
def render(*args):
    INDEX = args[0]
    if const.RANGE:
        start_date = get_current_datetime(const.DATES_ARRAY, INDEX)
        end_date = start_date + timedelta(days = 6)
        datetime = start_date
        file_uri = form_uri(const.CURRENT_SOURCE, start_date, end_date=end_date)
    else:
        datetime = get_current_datetime(const.DATES_ARRAY, INDEX)
        file_uri = form_uri(const.CURRENT_SOURCE, datetime)
    image = None
    try:
        if const.PNG:
            read_data = mpimg.imread(file_uri)
            image = create_plot(const.PLOT,
                                start_date, 
                                read_data,
                                const.CURRENT_COLORMAP,
                                const.SEPARATE_BYTE)
        else:
            with open(file_uri, 'rb') as fp:
                if "0051" in file_uri:
                    fp.seek(300)
                read_data = np.fromfile(fp, dtype=np.uint8).reshape(const.DATASET_SHAPE)
            image = create_plot(const.PLOT, 
                                datetime, 
                                read_data, 
                                const.CURRENT_COLORMAP,
                                const.SEPARATE_BYTE)
            set_last_dataset(read_data)
        if const.VERBOSE:
            print("Rendering data for " + str(datetime))
    except FileNotFoundError as e:
        print("----ERROR: No file for " + str(datetime) + "----")
        image = create_plot(const.PLOT, 
                            datetime, 
                            get_last_dataset(), 
                            const.CURRENT_COLORMAP,
                            const.SEPARATE_BYTE,
                            title="FILE MISSING FOR")
    except ValueError as e:
        print("----ERROR: Corrupt file for " + str(datetime) + "----")
        image = create_plot(const.PLOT, 
                            datetime, 
                            get_last_dataset(),
                            const.CURRENT_COLORMAP, 
                            const.SEPARATE_BYTE,
                            title="CORRUPTED FILE FOR")
    else:
        return [image]
    