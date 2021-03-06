#! /usr/bin/env python
import re

STATE_FILE_EXT = '.state'
OUTPUT_FILE = 'hw_handlers.txt'

def create_hw_settings(output_path, hw_data):
    """ Create the hw settings file and the state files.

    output_path -- path to the output folder
    hw_data     -- HW_Settings data
    """

    file_path = output_path + OUTPUT_FILE;

    hw_file = open(file_path, 'wb')
    hw_file.write('; This file was auto generated by the script extract_hw_db.py\n\n');
    hw_file.write('; When changing the main structure of this file also update the script.\n\n');
    hw_file.write('; If editing this file keep sections ordered:\n')
    hw_file.write(';  - Sections containing index, sort by index.\n')
    hw_file.write(';  - The rest, sort alphabetically.\n\n\n')

    _write_device(hw_file, hw_data)
    _write_combo(hw_file, hw_data)
    _write_data(hw_file, hw_data)
    _write_FIR(hw_file, hw_data)
    _write_ANC(hw_file, hw_data)
    hw_file.close()

    _create_state_files(output_path, hw_data)


def _write_header(file, text, start):
    """ Write a section header
    """
    header = ';' + ' ' * start + text
    file.write(header)
    file.write(';' + '-' * (len(header) - 2) + '\n')

def _parse_device_line(line):
    """ Parse a HW_Settings_Device line
        Returns (Device, Index)
    """
    sp = re.compile(r"""INSERT INTO "HW_Settings_Device" VALUES\('(.*)',(\d*)\);""")
    return sp.search(line).groups()

def _parse_combo_line(line):
    """ Parse a HW_Settings_Combo line
        Returns (Codec/Chip, Dev1, Dev2, Dev3, Dev4, Dev5, Dev6, Index)
    """
    sp = re.compile(r"""INSERT INTO "HW_Settings_Combo" VALUES\('(.*)','(.*)','(.*)','(.*)','(.*)','(.*)','(.*)',(\d*)\);""")
    return sp.search(line).groups()

def _parse_data_line(line):
    """ Parse a HW_Settings_Data line
        Returns (index, data)
    """
    sp = re.compile(r"""INSERT INTO "HW_Settings_Data" VALUES\((\d*),\'(.*)\'\);""")
    return sp.search(line).groups()

def _get_device_index_and_file_name(line):
    """ Generate file name from a HW_Settings_Device line
        Returns (Index, File name)
    """
    device, index = _parse_device_line(line)
    file_name = 'dev_' + device.lower() + STATE_FILE_EXT
    return index, file_name

def _get_combo_index_and_file_name(line):
    """ Generate file name from a HW_Settings_Combo line
        Returns (Index, File name)
    """
    p = _parse_combo_line(line)
    codec = p[0]
    devices = p[1:7]
    index = p[7]

    file_name = codec.lower()
    for dev in devices:
        if dev:
            file_name += '_' + dev.lower()

    if file_name == codec.lower():
        file_name += '_default'

    file_name += STATE_FILE_EXT
    return index, file_name

def _get_index_to_name_mapping(data):
    """ Create a dictionary that maps indexes to state file names
    """
    dict = {}
    for line in data:
        if 'HW_Settings_Device' in line:
            index, name = _get_device_index_and_file_name(line)
            dict[index] = name
        elif 'HW_Settings_Combo' in line:
            index, name = _get_combo_index_and_file_name(line)
            dict[index] = name
    return dict

def _write_device(file, data):
    _write_header(file, 'Device (Custom)    Index (Data)\n', 38)
    list = []
    for line in data:
        if 'HW_Settings_Device' in line:
            device, index = _parse_device_line(line)
            list.append((index, device))

    # Sort on index
    list.sort(lambda a,b: cmp(int(a[0]),int(b[0])))

    for line in list:
        index = line[0]
        device = "'%s'," % line[1]
        wline = "INSERT INTO HW_Settings_Device VALUES (%-19s%s);\n" % (device, index)
        file.write(wline)
    file.write('\n')

def _write_combo(file, data):
    _write_header(file, 'Codec/Chip    Dev1          Dev2          Dev3          Dev4          Dev5          Dev6          Index (Data)\n', 37)
    list = []
    for line in data:
        if 'HW_Settings_Combo' in line:
            p = _parse_combo_line(line)
            codec = p[0]
            devices = p[1:7]
            index = p[7]
            list.append((index, codec, devices))

    # Sort on index
    list.sort(lambda a,b: cmp(int(a[0]),int(b[0])))

    for line in list:
        index = line[0]
        codec = "'" + line[1] + "',"
        dev1 = "'" + line[2][0] + "',"
        dev2 = "'" + line[2][1] + "',"
        dev3 = "'" + line[2][2] + "',"
        dev4 = "'" + line[2][3] + "',"
        dev5 = "'" + line[2][4] + "',"
        dev6 = "'" + line[2][5] + "',"
        str = "INSERT INTO HW_Settings_Combo VALUES (%-14s%-14s%-14s%-14s%-14s%-14s%-14s%s);\n" % (codec, dev1, dev2, dev3, dev4, dev5, dev6, index)
        file.write(str)
    file.write('\n')

def _write_data(file, data):
    _write_header(file, 'Index    Data file\n', 36)
    indexes = []
    for line in data:
        if 'HW_Settings_Data' in line:
            index, state_data = _parse_data_line(line)
            indexes.append(int(index))

    indexes.sort()

    i2n = _get_index_to_name_mapping(data)

    for i in indexes:
        state_file_name = '<' + i2n[str(i)] + '>'
        index = str(i) + ','
        wline = 'INSERT INTO HW_Settings_Data VALUES (%-9s%s);\n' % (index, state_file_name)
        file.write(wline)

    file.write('\n')

def _write_FIR(file, data):
    _write_header(file, 'Sidetone FIR-coeffecient presets\n', 1)
    for line in data:
        if 'HW_Settings_FIR' in line:
            file.write(line + '\n')

    file.write('\n')

def _write_ANC(file, data):
    _write_header(file, 'ANC presets\n', 1)
    for line in data:
        if 'HW_Settings_ANC' in line:
            file.write(line + '\n')

    file.write('\n')


def _format_data(data):
    """Replace spaces with line feed and tabs to conform with the state file structure.
    """
    out = 'null'
    if len(data) > 4:
        # divide stuff into rows
        out = data.replace("''","'").replace('{   ','{\n').replace('{  ','{\n').replace('  }  ','\n}\n').replace('   ','\n')
        # remove empty lines
        out = out.replace('\n\n\n\n','\n')
        out = out.replace('\n\n\n','\n')
        out = out.replace('\n\n','\n')
        out = out.replace('\n \n','\n')
        # strip some odd leading spaces
        out = out.replace(' control','control')
        out = out.replace('  comment','comment')
        out = out.replace('  iface','iface')
        out = out.replace('  name','name')
        out = out.replace('  value','value')
        #indentation
        out = out.replace('}\ncontrol','\t}\ncontrol')
        out = out.replace('control','\tcontrol')
        out = out.replace('comment','\t\tcomment')
        out = out.replace('iface','\t\tiface')
        out = out.replace('name','\t\tname')
        out = out.replace('value','\t\tvalue')
        # identation of closing curly brackets
        out = out.replace('  } }','\n\t}\n}\n')
        out = out.replace('} }','\t}\n}\n')

    return out

def _create_state_files(path, data):
    i2n = _get_index_to_name_mapping(data)
    for line in data:
        if 'HW_Settings_Data' in line:
            index, state_data = _parse_data_line(line)
            file_name = i2n[index]
            file = open(path + file_name, 'wb')
            file.write(_format_data(state_data))
            file.close()
