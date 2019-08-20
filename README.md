# PyRCS

**Author**: Qian Fu [![Twitter URL](https://img.shields.io/twitter/url/https/Qian_Fu?label=Follow&style=social)](https://twitter.com/Qian_Fu)

[![PyPI](https://img.shields.io/pypi/v/pyrcs)](https://pypi.org/project/pyrcs/)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyrcs)]()
[![PyPI - License](https://img.shields.io/pypi/l/pyrcs)](https://github.com/mikeqfu/pyrcs/blob/master/LICENSE)
[![GitHub repo size](https://img.shields.io/github/repo-size/mikeqfu/pyrcs?color=yellowgreen)]()
[![Website](https://img.shields.io/website/http/www.railwaycodes.org.uk?down_color=lightgrey&down_message=offline&label=railwaycodes.org.uk&up_color=9cf&up_message=online)](http://www.railwaycodes.org.uk/)

A web-scrapper for collecting GB's railway codes. (*Work still in progress*)



## Contents

* [Installation](##Installation)
* [Examples - A quick start](##Examples - A quick start)
  - [1. CRS, NLC, TIPLOC and STANOX Codes](###1. CRS, NLC, TIPLOC and STANOX Codes)
    - [1.1 Location codes for a given initial letter](####1.1 Locations beginning with a given letter)
    - [1.2 All available location codes](####1.2 All available location codes in this category)
  - [2. Engineer's Line References (ELRs)](###2. Engineer's Line References (ELRs))
    - [2.1 ELR codes](####2.1 ELR codes)
    - [2.2 Mileage files](####2.2 Mileage files)
  - [3. Railway stations data](###3. Railway stations data)
* [Acknowledgement](http://www.railwaycodes.org.uk/misc/acknowledgements.shtm)
* [Note](http://www.railwaycodes.org.uk/misc/contributing.shtm)





## Installation

```bash
$ pip install --upgrade pyrcs
```

**Note**: 

* Make sure you have the most up-to-date version of `pip` installed.

  ```bash
  $ python -m pip install --upgrade pip
  ```

* `Python-Levenshtein`, one of the dependencies of this package, may fail to be installed on a Windows OS without VC2015 (or above). A workaround is to download and install its [Windows binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-levenshtein) from the [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/). In this case, you should go for `python_Levenshtein‑0.12.0‑cp37‑cp37m‑win_amd64.whl` if you're using Python 3.7 on 64-bit OS: 

  ```bash
  $ pip install full\path\to\python_Levenshtein‑0.12.0‑cp37‑cp37m‑win_amd64.whl
  ```





## Examples - A quick start

The following examples provide a quick guide to how the package works.



### 1. CRS, NLC, TIPLOC and STANOX Codes

If your preferred import style is `from <module> import <name>`:

```python
from pyrcs.line_data_cls import crs_nlc_tiploc_stanox as ldlc
```

If your preferred import style is `import <module>.<name>`:

```python
import pyrcs.line_data_cls.crs_nlc_tiploc_stanox as ldlc
```

After importing the module, you can create a 'class' for the location codes (including all CRS, NLC, TIPLOC, STANME and STANOX) :

```python
location_codes = ldlc.LocationIdentifiers()
```



***Given different preferences, there are several alternative ways of importing the module.* **

***Alternative 1***: 

```python
from pyrcs.line_data import crs_nlc_tiploc_stanox as ldlc
location_codes = ldlc.LocationIdentifiers()
```

***Alternative 2*** (*Preferred and used for the following examples*):

```python
from pyrcs.line_data import LineData
line_data_cls = LineData()  # contains all classes under the category of 'Line data'
location_codes = line_data_cls.LocationIdentifiers
```



#### 1.1 Locations beginning with a given letter

You can get the location codes starting with a specific letter, say 'A' or 'a', by using the method`collect_location_codes_by_initial`, which returns a `dict`. 

```python
# The input is case-insensitive
location_codes_a = location_codes.collect_location_codes_by_initial('A')
```

The keys of `location_codes_a` include: 

* `'A'`
* `'Last_updated_date'`
* `'Additional_note'`

The corresponding values are:

* `location_codes_a['A']`  is a `pandas.DataFrame` that contains the table data. You may compare it with the table on the web page: http://www.railwaycodes.org.uk/crs/CRSa.shtm
* `location_codes_a['Last_updated_date']` is the date (in `str`) when the web page was last updated
* `location_codes_a['Additional_note']` is some important additional information on the web page (if available)



#### 1.2 All available location codes in this category

You can also get all available location codes in this category as a whole , using the method `fetch_location_codes`, which also returns a `dict`:

```python
location_codes_data = location_codes.fetch_location_codes()
```

The keys of `location_codes_a` include: 

- `'Location_codes'`
- `'Latest_updated_date'` 
- `'Additional_note'`
- `'Other_systems'`

The corresponding values are:

- `location_codes_data['Location_codes']`  is a `pandas.DataFrame` that contains all table data (from 'A' to 'Z')
- `location_codes_data['Latest_updated_date']` is the latest 'Last_updated_date' (in `str`) among all initial-specific table data
- `location_codes_data['Additional_note']` is some important additional information on the web page (if available)
- `location_codes_data['Other_systems']` is a `dict` for [Other systems](http://www.railwaycodes.org.uk/crs/CRS1.shtm)



### 2. Engineer's Line References (ELRs)

```python
em = line_data_cls.ELRMileages
```



#### 2.1 ELR codes

To get ELR codes starting with a specific letter, say `'A'`, by using the method `collect_elr_by_initial`, which returns a `dict`. 

```python
elr_a = em.collect_elr_by_initial('A')  # em.collect_elr_by_initial('a')
```

The keys of `elr_a` include: 

- `'A'`
- `'Last_updated_date'`

The corresponding values are:

- `elr_a['A']`  is a `pandas.DataFrame` that contains the table data. You may compare it with the table on the web page: http://www.railwaycodes.org.uk/elrs/elra.shtm
- `elr_a['Last_updated_date']` is the date (in `str`) when the web page was last updated

To get all available ELR codes, by using the method `fetch_elr`, which returns a `dict`:

```python
elr_codes = em.fetch_elr()
```

The keys of `elr_codes` include: 

- `'ELRs_mileages'`
- `'Latest_updated_date'`

The corresponding values are:

- `elr_codes['ELRs_mileages']`  is a `pandas.DataFrame` that contains all table data (from 'A' to 'Z')
- `elr_codes['Latest_updated_date']` is the latest 'Last_updated_date' (in `str`) among all initial-specific table data



#### 2.2 Mileage files

To collect more detailed mileage data for a given ELR, say `'AAM'`, by using the method `fetch_mileage_file`, which returns a `dict`:

```python
em_amm = em.fetch_mileage_file('AAM')
```

The keys of `em_amm` include: 

- `'ELR'`
- `'Line'`
- `'Sub-Line'`
- `'AAM'`

The corresponding values are:

- `em_amm['ELR']`  is the name (in `str`) of the given ELR
- `em_amm['Line']` is associated line name (in `str`) 
- `em_amm['Sub-Line']` is associated sub line name (in `str`), if available
- `em_amm['AAM']` is a `pandas.DataFrame` of the mileage file data



### 3. Railway stations data

The data of railway stations belongs to another category, '[Other assets](http://www.railwaycodes.org.uk/otherassetsmenu.shtm)'

```python
from pyrcs.other_assets import OtherAssets
other_assets_cls = OtherAssets()
```

Similar to getting 'CRS, NLC, TIPLOC and STANOX Codes' above, to get stations data by a given initial letter (say 'A'):

```python
stations_a = other_assets_cls.Stations.collect_station_locations('A')
```

To get all available stations data:

```python
stations = other_assets_cls.Stations.fetch_station_locations()
```

The data type of both `stations_a` and `stations` are `dict` .

