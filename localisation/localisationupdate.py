# coding: utf-8
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

mod_name = 'autobuild'
tablet_id = '1CzLnUlMqkkBVBkR75U_lFpeeLK4uut7fBmMOcgCGbaA'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('localisationupdate.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key(tablet_id).get_worksheet(0)

loc_keys = sh.col_values(1)
loc_rows = sh.row_values(1)
loc_indexes = [loc_rows.index(i) for i in loc_rows if i.startswith('l_')]
eng_fallback = sh.col_values(1+loc_rows.index('l_english:'))
for loc_index in loc_indexes:
    loc = sh.col_values(1+loc_index)
    out_file = mod_name + '_' + loc_rows[loc_index].replace(':', '') + '.yml'
    print(out_file)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(u'\uFEFF')
        f.write(loc_rows[loc_index] + '\n')
        for i, j in enumerate(loc):
            print(loc[i])
            if loc_keys[i] != '':
                if loc_keys[i].startswith('#'):
                    f.write(' ' + loc_keys[i] + '\n')
                elif loc[i] != '':
                    f.write(' {0}:0 "{1}"\n'.format(loc_keys[i], loc[i]))
                elif eng_fallback[i] == '':
                    f.write(' {0}:0 "{1}"\n'.format(loc_keys[i], ' '))
                else:
                    f.write(' {0}:0 "{1}"\n'.format(loc_keys[i], eng_fallback[i]))