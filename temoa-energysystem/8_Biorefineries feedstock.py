import pandas as pd
import numpy as np
import sqlite3

database_name = "Temoa_Europe_solved.sqlite"
sector_name = "_8_Biorefineries feedstock"
years = np.array([2010,	2015, 2020, 2025, 2030,	2035, 2040,	2045, 2050])

# Following 4 lines should be used to set the export results.
# Set the flags to 1 to split by technologies/commodities, to 0 to not split.
# Set to_excel_flag to 1 to export data into a Excel file
# The arrays are used to select the technologies/commodities that should be considered.

technologies_in_flag = 1
technologies_out_flag = 1
commodities_in_flag = 1
commodities_out_flag = 1
to_excel_flag = 1

technologies=[
'UPS_BIO_BLD_LGC',
'IMP_BIO_OIL',
'UPS_BIO_REF_GEN1_CRUSHING_EXS',
'UPS_BIO_BLD_STC',
]
commodities_in = [
'RNW_POT_BIO_CRP_GRS',
'ethos',
'UPS_BIO_FS_OIL',
'UPS_ELC',
'UPS_HET',
'RNW_POT_BIO_CRP_STC',
]
commodities_out = [
'UPS_BIO_REF_FS_LGC',
'UPS_BIO_REF_FS_OIL',
]

# Input

comm = list()
tech = list()
vflow_in_2010 = list()
vflow_in_2015 = list()
vflow_in_2020 = list()
vflow_in_2025 = list()
vflow_in_2030 = list()
vflow_in_2035 = list()
vflow_in_2040 = list()
vflow_in_2045 = list()
vflow_in_2050 = list()

# To classify by technologies, commodities or both
if technologies_in_flag == 1 and commodities_in_flag == 1:
    for i_tech in range(0, len(technologies)):
        for i_comm in range(0, len(commodities_in)):
            conn = sqlite3.connect(database_name)
            Output_VFlow_In = pd.read_sql("select * from Output_VFlow_In where input_comm = '" + commodities_in[i_comm] + "' and tech = '" + technologies[i_tech] + "'", conn)
            conn.close()
            vflow_in = np.zeros_like(years, dtype=float)
            for i_year in range(0, len(years)):
                for i in range(0, len(Output_VFlow_In.t_periods)):
                    if years[i_year] == Output_VFlow_In.t_periods[i]:
                        vflow_in[i_year] = vflow_in[i_year] + Output_VFlow_In.vflow_in[i]
            comm.append(commodities_in[i_comm])
            tech.append(technologies[i_tech])
            vflow_in_2010.append(vflow_in[0])
            vflow_in_2015.append(vflow_in[1])
            vflow_in_2020.append(vflow_in[2])
            vflow_in_2025.append(vflow_in[3])
            vflow_in_2030.append(vflow_in[4])
            vflow_in_2035.append(vflow_in[5])
            vflow_in_2040.append(vflow_in[6])
            vflow_in_2045.append(vflow_in[7])
            vflow_in_2050.append(vflow_in[8])

elif technologies_in_flag == 0 and commodities_in_flag == 1:
    for i_comm in range(0, len(commodities_in)):
        vflow_in = np.zeros_like(years, dtype=float)
        for i_tech in range(0, len(technologies)):
            conn = sqlite3.connect(database_name)
            Output_VFlow_In = pd.read_sql("select * from Output_VFlow_In where input_comm = '" + commodities_in[i_comm] + "' and tech = '" + technologies[i_tech] + "'", conn)
            conn.close()
            for i_year in range(0, len(years)):
                for i in range(0, len(Output_VFlow_In.t_periods)):
                    if years[i_year] == Output_VFlow_In.t_periods[i]:
                        vflow_in[i_year] = vflow_in[i_year] + Output_VFlow_In.vflow_in[i]
        comm.append(commodities_in[i_comm])
        tech.append('')
        vflow_in_2010.append(vflow_in[0])
        vflow_in_2015.append(vflow_in[1])
        vflow_in_2020.append(vflow_in[2])
        vflow_in_2025.append(vflow_in[3])
        vflow_in_2030.append(vflow_in[4])
        vflow_in_2035.append(vflow_in[5])
        vflow_in_2040.append(vflow_in[6])
        vflow_in_2045.append(vflow_in[7])
        vflow_in_2050.append(vflow_in[8])

elif technologies_in_flag == 1 and commodities_in_flag == 0:
    for i_tech in range(0, len(technologies)):
        vflow_in = np.zeros_like(years, dtype=float)
        for i_comm in range(0, len(commodities_in)):
            conn = sqlite3.connect(database_name)
            Output_VFlow_In = pd.read_sql("select * from Output_VFlow_In where input_comm = '" + commodities_in[i_comm] + "' and tech = '" + technologies[i_tech] + "'", conn)
            conn.close()
            for i_year in range(0, len(years)):
                for i in range(0, len(Output_VFlow_In.t_periods)):
                    if years[i_year] == Output_VFlow_In.t_periods[i]:
                        vflow_in[i_year] = vflow_in[i_year] + Output_VFlow_In.vflow_in[i]
        comm.append('')
        tech.append(technologies[i_tech])
        vflow_in_2010.append(vflow_in[0])
        vflow_in_2015.append(vflow_in[1])
        vflow_in_2020.append(vflow_in[2])
        vflow_in_2025.append(vflow_in[3])
        vflow_in_2030.append(vflow_in[4])
        vflow_in_2035.append(vflow_in[5])
        vflow_in_2040.append(vflow_in[6])
        vflow_in_2045.append(vflow_in[7])
        vflow_in_2050.append(vflow_in[8])

# To find rows with only zero elements
delete_index = list()
for i_comm in range(0, len(comm)):
    flag_zero = 0
    if vflow_in_2010[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2015[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2020[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2025[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2030[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2035[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2040[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2045[i_comm] != 0:
        flag_zero = 1
    elif vflow_in_2050[i_comm] != 0:
        flag_zero = 1

    if flag_zero == 0:
        delete_index.append(i_comm)

# To remove rows with only zeros elements
for i_delete in range(0, len(delete_index)):
    tech.pop(delete_index[i_delete])
    comm.pop(delete_index[i_delete])
    vflow_in_2010.pop(delete_index[i_delete])
    vflow_in_2015.pop(delete_index[i_delete])
    vflow_in_2020.pop(delete_index[i_delete])
    vflow_in_2025.pop(delete_index[i_delete])
    vflow_in_2030.pop(delete_index[i_delete])
    vflow_in_2035.pop(delete_index[i_delete])
    vflow_in_2040.pop(delete_index[i_delete])
    vflow_in_2045.pop(delete_index[i_delete])
    vflow_in_2050.pop(delete_index[i_delete])

    for j_delete in range(0, len(delete_index)):
        delete_index[j_delete] = delete_index[j_delete] - 1

# Building and printing the table
vflow_in_DF = pd.DataFrame(
    {
        "tech": pd.Series(tech, dtype='str'),
        "input_comm": pd.Series(comm, dtype='str'),
        "2010": pd.Series(vflow_in_2010, dtype='float'),
        "2015": pd.Series(vflow_in_2015, dtype='float'),
        "2020": pd.Series(vflow_in_2020, dtype='float'),
        "2025": pd.Series(vflow_in_2025, dtype='float'),
        "2030": pd.Series(vflow_in_2030, dtype='float'),
        "2035": pd.Series(vflow_in_2035, dtype='float'),
        "2040": pd.Series(vflow_in_2040, dtype='float'),
        "2045": pd.Series(vflow_in_2045, dtype='float'),
        "2050": pd.Series(vflow_in_2050, dtype='float'),
    }
)

pd.set_option('display.max_rows', len(vflow_in_DF))
pd.set_option('display.max_columns', 16)
pd.set_option('display.precision', 2)
pd.set_option('display.float_format', '{:5,.2f}'.format)
print(vflow_in_DF)
print("\n")
pd.reset_option('display.max_rows')



# Output

comm = list()
tech = list()
vflow_out_2010 = list()
vflow_out_2015 = list()
vflow_out_2020 = list()
vflow_out_2025 = list()
vflow_out_2030 = list()
vflow_out_2035 = list()
vflow_out_2040 = list()
vflow_out_2045 = list()
vflow_out_2050 = list()

# To classify by technologies, commodities or both
if technologies_out_flag == 1 and commodities_out_flag == 1:
    for i_tech in range(0, len(technologies)):
        for i_comm in range(0, len(commodities_out)):
            conn = sqlite3.connect(database_name)
            Output_VFlow_Out = pd.read_sql("select * from Output_VFlow_Out where output_comm = '" + commodities_out[i_comm] + "' and tech = '" + technologies[i_tech] + "'", conn)
            conn.close()
            vflow_out = np.zeros_like(years, dtype=float)
            for i_year in range(0, len(years)):
                for i in range(0, len(Output_VFlow_Out.t_periods)):
                    if years[i_year] == Output_VFlow_Out.t_periods[i]:
                        vflow_out[i_year] = vflow_out[i_year] + Output_VFlow_Out.vflow_out[i]
            comm.append(commodities_out[i_comm])
            tech.append(technologies[i_tech])
            vflow_out_2010.append(vflow_out[0])
            vflow_out_2015.append(vflow_out[1])
            vflow_out_2020.append(vflow_out[2])
            vflow_out_2025.append(vflow_out[3])
            vflow_out_2030.append(vflow_out[4])
            vflow_out_2035.append(vflow_out[5])
            vflow_out_2040.append(vflow_out[6])
            vflow_out_2045.append(vflow_out[7])
            vflow_out_2050.append(vflow_out[8])

elif technologies_out_flag == 0 and commodities_out_flag == 1:
    for i_comm in range(0, len(commodities_out)):
        vflow_out = np.zeros_like(years, dtype=float)
        for i_tech in range(0, len(technologies)):
            conn = sqlite3.connect(database_name)
            Output_VFlow_Out = pd.read_sql("select * from Output_VFlow_Out where output_comm = '" + commodities_out[i_comm] + "' and tech = '" + technologies[i_tech] + "'", conn)
            conn.close()
            for i_year in range(0, len(years)):
                for i in range(0, len(Output_VFlow_Out.t_periods)):
                    if years[i_year] == Output_VFlow_Out.t_periods[i]:
                        vflow_out[i_year] = vflow_out[i_year] + Output_VFlow_Out.vflow_out[i]
        comm.append(commodities_out[i_comm])
        tech.append('')
        vflow_out_2010.append(vflow_out[0])
        vflow_out_2015.append(vflow_out[1])
        vflow_out_2020.append(vflow_out[2])
        vflow_out_2025.append(vflow_out[3])
        vflow_out_2030.append(vflow_out[4])
        vflow_out_2035.append(vflow_out[5])
        vflow_out_2040.append(vflow_out[6])
        vflow_out_2045.append(vflow_out[7])
        vflow_out_2050.append(vflow_out[8])

elif technologies_out_flag == 1 and commodities_out_flag == 0:
    for i_tech in range(0, len(technologies)):
        vflow_out = np.zeros_like(years, dtype=float)
        for i_comm in range(0, len(commodities_out)):
            conn = sqlite3.connect(database_name)
            Output_VFlow_Out = pd.read_sql("select * from Output_VFlow_Out where output_comm = '" + commodities_out[i_comm] + "' and tech = '" + technologies[i_tech] + "'", conn)
            conn.close()
            for i_year in range(0, len(years)):
                for i in range(0, len(Output_VFlow_Out.t_periods)):
                    if years[i_year] == Output_VFlow_Out.t_periods[i]:
                        vflow_out[i_year] = vflow_out[i_year] + Output_VFlow_Out.vflow_out[i]
        comm.append('')
        tech.append(technologies[i_tech])
        vflow_out_2010.append(vflow_out[0])
        vflow_out_2015.append(vflow_out[1])
        vflow_out_2020.append(vflow_out[2])
        vflow_out_2025.append(vflow_out[3])
        vflow_out_2030.append(vflow_out[4])
        vflow_out_2035.append(vflow_out[5])
        vflow_out_2040.append(vflow_out[6])
        vflow_out_2045.append(vflow_out[7])
        vflow_out_2050.append(vflow_out[8])

# To find rows with only zero elements
delete_index = list()
for i_comm in range(0, len(comm)):
    flag_zero = 0
    if vflow_out_2010[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2015[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2020[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2025[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2030[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2035[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2040[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2045[i_comm] != 0:
        flag_zero = 1
    elif vflow_out_2050[i_comm] != 0:
        flag_zero = 1

    if flag_zero == 0:
        delete_index.append(i_comm)

# To remove rows with only zeros elements
for i_delete in range(0, len(delete_index)):
    tech.pop(delete_index[i_delete])
    comm.pop(delete_index[i_delete])
    vflow_out_2010.pop(delete_index[i_delete])
    vflow_out_2015.pop(delete_index[i_delete])
    vflow_out_2020.pop(delete_index[i_delete])
    vflow_out_2025.pop(delete_index[i_delete])
    vflow_out_2030.pop(delete_index[i_delete])
    vflow_out_2035.pop(delete_index[i_delete])
    vflow_out_2040.pop(delete_index[i_delete])
    vflow_out_2050.pop(delete_index[i_delete])
    vflow_out_2045.pop(delete_index[i_delete])

    for j_delete in range(0, len(delete_index)):
        delete_index[j_delete] = delete_index[j_delete] - 1

# Building and printing the table
vflow_out_DF = pd.DataFrame(
    {
        "tech": pd.Series(tech, dtype='str'),
        "output_comm": pd.Series(comm, dtype='str'),
        "2010": pd.Series(vflow_out_2010, dtype='float'),
        "2015": pd.Series(vflow_out_2015, dtype='float'),
        "2020": pd.Series(vflow_out_2020, dtype='float'),
        "2025": pd.Series(vflow_out_2025, dtype='float'),
        "2030": pd.Series(vflow_out_2030, dtype='float'),
        "2035": pd.Series(vflow_out_2035, dtype='float'),
        "2040": pd.Series(vflow_out_2040, dtype='float'),
        "2045": pd.Series(vflow_out_2045, dtype='float'),
        "2050": pd.Series(vflow_out_2050, dtype='float'),
    }
)

pd.set_option('display.max_rows', len(vflow_out_DF))
pd.set_option('display.max_columns', 16)
pd.set_option('display.precision', 2)
pd.set_option('display.float_format', '{:0,.2f}'.format)
print(vflow_out_DF)
print("\n")
pd.reset_option('display.max_rows')



# Save to Excel



if to_excel_flag == 1:
    writer = pd.ExcelWriter(sector_name + '.xlsx', engine='xlsxwriter')
    vflow_in_DF.to_excel(writer, sheet_name='Input')
    vflow_out_DF.to_excel(writer, sheet_name='Output')
    writer.save()