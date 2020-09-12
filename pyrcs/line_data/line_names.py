""" Collecting British railway line names.

Data source: http://www.railwaycodes.org.uk/misc/line_names.shtm
"""

import copy
import os
import re
import urllib.parse

import pandas as pd
import requests
from pyhelpers.dir import validate_input_data_dir
from pyhelpers.ops import confirmed, fake_requests_headers
from pyhelpers.store import load_pickle, save_pickle

from pyrcs.utils import cd_dat, get_catalogue, get_last_updated_date, homepage_url, parse_table


class LineNames:
    """
    A class for collecting British railway line names.

    :param data_dir: name of data directory, defaults to ``None``
    :type data_dir: str, None
    :param update: whether to check on update and proceed to update the package data, defaults to ``False``
    :type update: bool

    **Example**::

        from pyrcs.line_data import LineNames

        ln = LineNames()

        print(ln.Name)
        # Railway line names

        print(ln.SourceURL)
        # http://www.railwaycodes.org.uk/misc/line_names.shtm
    """

    def __init__(self, data_dir=None, update=False):
        """
        Constructor method.
        """
        self.Name = 'Railway line names'
        self.HomeURL = homepage_url()
        self.SourceURL = urllib.parse.urljoin(self.HomeURL, '/misc/line_names.shtm')
        self.Catalogue = get_catalogue(self.SourceURL, update=update, confirmation_required=False)
        self.Date = get_last_updated_date(self.SourceURL, parsed=True, as_date_type=False)
        self.Key = 'Line names'
        self.LUDKey = 'Last updated date'
        if data_dir:
            self.DataDir = validate_input_data_dir(data_dir)
        else:
            self.DataDir = cd_dat("line-data", self.Key.lower().replace(" ", "-"))
        self.CurrentDataDir = copy.copy(self.DataDir)

    def cdd_ln(self, *sub_dir):
        """
        Change directory to "dat\\line-data\\line-names" and sub-directories (and/or a file)

        :param sub_dir: sub-directory or sub-directories (and/or a file)
        :type sub_dir: str
        :return: path to the backup data directory for ``LineNames``
        :rtype: str

        :meta private:
        """

        path = self.DataDir
        for x in sub_dir:
            path = os.path.join(path, x)
        return path

    def collect_line_names(self, confirmation_required=True, verbose=False):
        """
        Collect data of railway line names from source web page.

        :param confirmation_required: whether to require users to confirm and proceed, defaults to ``True``
        :type confirmation_required: bool
        :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
        :type verbose: bool
        :return: railway line names and routes data and date of when the data was last updated
        :rtype: dict, None

        **Example**::

            from pyrcs.line_data import LineNames

            ln = LineNames()

            confirmation_required = True

            line_names_data = ln.collect_line_names(confirmation_required)
            # To collect British railway line names? [No]|Yes:
            # >? yes

            print(line_names_data)
            # {'Line names': <code>,
            #  'Last updated date': <date>}
        """

        if confirmed("To collect British railway {}?".format(self.Key.lower()),
                     confirmation_required=confirmation_required):

            if verbose == 2:
                print("Collecting the railway {}".format(self.Key.lower()), end=" ... ")

            try:
                source = requests.get(self.SourceURL, headers=fake_requests_headers())
                row_lst, header = parse_table(source, parser='lxml')
                line_names = pd.DataFrame([[r.replace('\xa0', '').strip() for r in row] for row in row_lst],
                                          columns=header)

                # Parse route column
                def parse_route_column(x):
                    if 'Watford - Euston suburban route' in x:
                        route, route_note = 'Watford - Euston suburban route', x
                    elif ', including Moorgate - Farringdon' in x:
                        route_note = 'including Moorgate - Farringdon'
                        route = x.replace(', including Moorgate - Farringdon', '')
                    elif re.match(r'.+(?= \[\')', x):
                        route, route_note = re.split(r' \[\'\(?', x)
                        route_note = route_note.strip(")']")
                    elif re.match(r'.+\)$', x):
                        if re.match(r'.+(?= - \()', x):
                            route, route_note = x, None
                        else:
                            route, route_note = re.split(r' \(\[?\'?', x)
                            route_note = route_note.rstrip('\'])')
                    else:
                        route, route_note = x, None
                    return route, route_note

                line_names[['Route', 'Route_note']] = line_names.Route.map(parse_route_column).apply(pd.Series)

                last_updated_date = get_last_updated_date(self.SourceURL)

                line_names_data = {self.Key: line_names, self.LUDKey: last_updated_date}

                print("Done. ") if verbose == 2 else ""

                pickle_filename = self.Key.lower().replace(" ", "-") + ".pickle"
                path_to_pickle = self.cdd_ln(pickle_filename)
                save_pickle(line_names_data, path_to_pickle, verbose=verbose)

            except Exception as e:
                print("Failed. {}".format(e))
                line_names_data = None

            return line_names_data

    def fetch_line_names(self, update=False, pickle_it=False, data_dir=None, verbose=False):
        """
        Fetch data of railway line names from local backup.

        :param update: whether to check on update and proceed to update the package data, defaults to ``False``
        :type update: bool
        :param pickle_it: whether to replace the current package data with newly collected data, defaults to ``False``
        :type pickle_it: bool
        :param data_dir: name of package data folder, defaults to ``None``
        :type data_dir: str, None
        :param verbose: whether to print relevant information in console as the function runs, defaults to ``False``
        :type verbose: bool
        :return: railway line names and routes data and date of when the data was last updated
        :rtype: dict

        **Example**::

            from pyrcs.line_data import LineNames

            ln = LineNames()

            update = False
            pickle_it = False
            data_dir = None

            line_names_data = ln.fetch_line_names(update, pickle_it, data_dir)

            print(line_names_data)
            # {'Line names': <code>,
            #  'Last updated date': <date>}
        """

        pickle_filename = self.Key.lower().replace(" ", "-") + ".pickle"
        path_to_pickle = self.cdd_ln(pickle_filename)

        if os.path.isfile(path_to_pickle) and not update:
            line_names_data = load_pickle(path_to_pickle)

        else:
            line_names_data = self.collect_line_names(confirmation_required=False,
                                                      verbose=False if data_dir or not verbose else True)
            if line_names_data:  # line-names is not None
                if pickle_it and data_dir:
                    self.CurrentDataDir = validate_input_data_dir(data_dir)
                    path_to_pickle = os.path.join(self.CurrentDataDir, pickle_filename)
                    save_pickle(line_names_data, path_to_pickle, verbose=verbose)
            else:
                print("No data of the railway {} has been collected.".format(self.Key.lower()))

        return line_names_data
