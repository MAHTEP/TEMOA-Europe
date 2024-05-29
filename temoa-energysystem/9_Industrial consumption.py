import pandas as pd
import numpy as np
import sqlite3

database_name = "Temoa_Europe_solved.sqlite"
sector_name = "_9_Industrial consumption"
years = np.array([2010,	2015, 2020, 2025, 2030,	2035, 2040,	2045, 2050])

# The following 5 lines should be used to set the export results.
# Set the flags to 1 to split by technologies/commodities, to 0 not to split.
# Set to_excel_flag to 1 to export data into a Excel file
# The arrays are used to select the technologies/commodities that should be considered.

technologies_in_flag = 1
technologies_out_flag = 1
commodities_in_flag = 1
commodities_out_flag = 1
to_excel_flag = 1

technologies=[
'IND_CH_OLF_EXS',
'IND_CH_BTX_EXS',
'IND_CH_AMM_EXS',
'IND_CH_MTH_EXS',
'IND_CH_CHL_EXS',
'IND_CH_OCH_EXS',
#'IND_CH_TECH_EXS',
'IND_CH_EC_EXS',
'IND_CH_OTH_HFO_EXS',
'IND_CH_OTH_DST_EXS',
'IND_CH_OTH_NGA_EXS',
'IND_CH_OTH_COA_EXS',
'IND_CH_OTH_COK_EXS',
'IND_CH_OTH_ETH_EXS',
'IND_CH_OTH_NAP_EXS',
'IND_CH_OTH_ELC_EXS',
'IND_CH_OTH_LPG_EXS',
'IND_CH_MD_ELC_EXS',
'IND_CH_MD_OIL_EXS',
'IND_CH_HVC_NAPSC_NEW',
'IND_CH_HVC_ETHSC_NEW',
'IND_CH_HVC_GSOSC_NEW',
'IND_CH_HVC_LPGSC_NEW',
'IND_CH_HVC_NCC_NEW',
'IND_CH_HVC_BDH_NEW',
'IND_CH_OLF_PDH_NEW',
'IND_CH_OLF_MTO_NEW',
'IND_CH_AMM_NGASR_NEW',
'IND_CH_AMM_NAPPOX_NEW',
'IND_CH_AMM_COAGSF_NEW',
'IND_CH_AMM_BIOGSF_NEW',
'IND_CH_AMM_ELCSYS_NEW',
'IND_CH_AMM_NGASR_CCS_NEW',
'IND_CH_MTH_NGASR_NEW',
'IND_CH_MTH_COGSR_NEW',
'IND_CH_MTH_LPGPOX_NEW',
'IND_CH_MTH_COAGSF_NEW',
'IND_CH_MTH_BIOGSF_NEW',
'IND_CH_MTH_ELCSYS_NEW',
'IND_CH_MTH_NGASR_CCS_NEW',
'IND_CH_CHL_MERC_NEW',
'IND_CH_CHL_DIAP_NEW',
'IND_CH_CHL_MEMB_NEW',
'IND_CH_EC_NEW',
'IND_CH_OTH_HFO_NEW',
'IND_CH_OTH_DST_NEW',
'IND_CH_OTH_NGA_NEW',
'IND_CH_OTH_COA_NEW',
'IND_CH_OTH_COK_NEW',
'IND_CH_OTH_ELC_NEW',
'IND_CH_OTH_LPG_NEW',
'IND_CH_OTH_ETH_NEW',
'IND_CH_OTH_BIO_NEW',
'IND_CH_MD_OIL_NEW',
'IND_CH_MD_ELC_NEW',
'IND_CH_HET_REC',
'IND_IS_BOF_EXS',
'IND_IS_DRI_EXS',
'IND_IS_SCR_EXS',
'IND_FEA_EXS',
#'IND_IS_TECH_EXS',
'IND_IS_EC_EXS',
'IND_IS_EC_NEW',
'IND_IS_MD_ELC_EXS',
'IND_IS_MD_OIL_EXS',
'IND_IS_BOF_BFBOF_NEW',
'IND_IS_DRI_DRIEAF_NEW',
'IND_IS_SCR_NEW',
'IND_IS_BOF_SRD_NEW',
'IND_IS_BOF_BFBOF_CCS_NEW',
'IND_IS_BOF_TGR_CCS_NEW',
'IND_IS_BOF_HISBOF_NEW',
'IND_IS_BOF_HISBOF_CCS_NEW',
'IND_IS_DRI_DRIEAF_CCS_NEW',
'IND_IS_DRI_ULCORED_CCS_NEW',
'IND_IS_DRI_HDREAF_NEW',
'IND_IS_BOF_ULCOWIN_NEW',
'IND_IS_BOF_ULCOLYSIS_NEW',
'IND_IS_MD_OIL_NEW',
'IND_IS_MD_ELC_NEW',
'IND_IS_HET_REC',
'IND_FEA_NEW',
'IND_NF_ALU_EXS',
'IND_NF_COP_EXS',
'IND_NF_ZNC_EXS',
'IND_NF_AMN_EXS',
'IND_NF_EC_EXS',
#'IND_NF_TECH_EXS',
'IND_NF_MD_ELC_EXS',
'IND_NF_MD_OIL_EXS',
'IND_NF_AMN_BAY_NEW',
'IND_NF_ALU_HLH_NEW',
'IND_NF_ALU_SEC_NEW',
'IND_NF_ALU_HLHIA_NEW',
'IND_NF_ALU_CBT_NEW',
'IND_NF_ALU_KAO_NEW',
'IND_NF_COP_NEW',
'IND_NF_ZNC_NEW',
'IND_NF_EC_NEW',
'IND_NF_MD_OIL_NEW',
'IND_NF_MD_ELC_NEW',
'IND_NM_CLK_DRY_EXS',
'IND_NM_CLK_WET_EXS',
'IND_NM_LIM_EXS',
'IND_NM_GLS_EXS',
'IND_NM_CRM_EXS',
#'IND_NM_TECH_EXS',
'IND_NM_EC_EXS',
'IND_NM_MD_ELC_EXS',
'IND_NM_MD_OIL_EXS',
'IND_NM_CLK_DRY_NEW',
'IND_NM_CLK_WET_NEW',
'IND_NM_CLK_DRY_PCCS_NEW',
'IND_NM_CLK_DRY_OCCS_NEW',
'IND_NM_CEM_BLN_NEW',
'IND_NM_LIM_LRK_NEW',
'IND_NM_GLS_FOSS_NEW',
'IND_NM_GLS_ELEC_NEW',
'IND_NM_CRM_NEW',
'IND_NM_EC_NEW',
'IND_NM_MD_OIL_NEW',
'IND_NM_MD_ELC_NEW',
'IND_PP_PUL_CHEM_EXS',
'IND_PP_PUL_MEC_EXS',
'IND_PP_PUL_RCP_EXS',
'IND_PP_PAP_EXS',
'IND_PP_OTH_EXS',
#'IND_PP_TECH_EXS',
'IND_PP_SB_BIO_EXS',
'IND_PP_PH_HFO_EXS',
'IND_PP_PH_NGA_EXS',
'IND_PP_PH_COA_EXS',
'IND_PP_PH_BIO_EXS',
'IND_PP_DH_OIL_EXS',
'IND_PP_DH_NGA_EXS',
'IND_PP_DH_LPG_EXS',
'IND_PP_PUL_KRF_NEW',
'IND_PP_PUL_SUL_NEW',
'IND_PP_PUL_MEC_NEW',
'IND_PP_PUL_SCH_NEW',
'IND_PP_PUL_RCP_NEW',
'IND_PP_PAP_NEW',
'IND_PP_PH_HFO_NEW',
'IND_PP_PH_NGA_NEW',
'IND_PP_PH_BIO_NEW',
'IND_PP_PH_REC_NEW',
'IND_PP_DH_NGA_NEW',
'IND_PP_DH_OIL_NEW',
'IND_PP_DH_LPG_NEW',
'IND_PP_DH_REC_NEW',
'IND_PP_MD_ELC_NEW',
'IND_PP_HET_REC',
#'IND_STM_HET',
'IND_PP_MD_ELC_EXS',
'IND_OTH_SB_HFO_EXS',
'IND_OTH_SB_OIL_EXS',
'IND_OTH_SB_NGA_EXS',
'IND_OTH_SB_COA_EXS',
'IND_OTH_SB_COG_EXS',
'IND_OTH_SB_LPG_EXS',
'IND_OTH_SB_BIO_EXS',
'IND_OTH_SB_HET_EXS',
#'IND_OTH_TECH_EXS',
'IND_OTH_PH_HFO_EXS',
'IND_OTH_PH_OIL_EXS',
'IND_OTH_PH_NGA_EXS',
'IND_OTH_PH_COA_EXS',
'IND_OTH_PH_COK_EXS',
'IND_OTH_PH_ELC_EXS',
'IND_OTH_PH_LPG_EXS',
'IND_OTH_MD_ELC_EXS',
'IND_OTH_EC_ELC_EXS',
'IND_OTH_OTH_HFO_EXS',
'IND_OTH_OTH_OIL_EXS',
'IND_OTH_OTH_NGA_EXS',
'IND_OTH_OTH_COK_EXS',
'IND_OTH_OTH_PTC_EXS',
'IND_OTH_OTH_ELC_EXS',
'IND_OTH_OTH_GEO_EXS',
'IND_OTH_OTH_BIO_EXS',
'IND_OTH_OTH_LTH_EXS',
#'IND_NEU_TECH_EXS',
'IND_OTH_SB_HFO_NEW',
'IND_OTH_SB_OIL_NEW',
'IND_OTH_SB_NGA_NEW',
'IND_OTH_SB_COA_NEW',
'IND_OTH_SB_ELC_NEW',
'IND_OTH_SB_BIO_NEW',
'IND_OTH_PH_HFO_NEW',
'IND_OTH_PH_OIL_NEW',
'IND_OTH_PH_NGA_NEW',
'IND_OTH_PH_COA_NEW',
'IND_OTH_PH_COK_NEW',
'IND_OTH_PH_ELC_NEW',
'IND_OTH_PH_LPG_NEW',
'IND_OTH_MD_ELC_NEW',
'IND_OTH_OTH_HFO_NEW',
'IND_OTH_OTH_OIL_NEW',
'IND_OTH_OTH_NGA_NEW',
'IND_OTH_OTH_COA_NEW',
'IND_OTH_OTH_COK_NEW',
'IND_OTH_OTH_LTH_NEW',
'IND_OTH_OTH_ELC_NEW',
'IND_OTH_OTH_GEO_NEW',
'IND_OTH_OTH_LPG_NEW',
'IND_OTH_OTH_BIO_NEW',
'IND_OTH_EC_ELC_NEW',
]
commodities_in = [
#'IND_CH_EC',
'IND_NGA',
'IND_LPG',
'IND_HFO',
'IND_OIL',
'IND_BIO',
'IND_ETH',
'IND_NAP',
#'IND_CH_FS',
#'IND_CH_MD',
'IND_COA',
#'IND_CH_SB',
#'IND_CH_OTH',
#'IND_CH_OLF',
#'IND_CH_BTX',
#'IND_CH_AMM',
#'IND_CH_MTH',
#'IND_CH_CHL',
#'IND_CH_OCH',
'IND_CH_ELC',
'RNW_POT_BIO_WOD',
'RNW_POT_BIO_LIQ',
'RNW_POT_BIO_GAS',
'RNW_BIO_ETH',
'PRI_COA_HCO',
'PRI_COA_BCO',
'PRI_OIL_DST',
'PRI_GAS_ETH',
'SYN_MTH',
'PRI_GAS_NGA',
'SYN_NGA',
'HH2_BL',
'SYN_CCUS_NGA',
'PRI_GAS_LNG',
'PRI_OIL_LPG',
'PRI_OIL_NAP',
'RNW_BIO_NAP',
'PRI_OIL_HFO',
#'IND_FS_NGA',
#'IND_FS_LPG',
#'IND_FS_LNG',
#'IND_FS_COA',
#'IND_FS_HFO',
#'IND_FS_DST',
#'IND_FS_ETH',
#'IND_FS_NAP',
#'IND_FS_BIO',
#'IND_FS_BIO_ETH',
#'IND_FS_MTH',
'IND_COK',
'IND_COG',
'IND_BFG',
'IND_PTC',
#'IND_IS_MD',
#'IND_IS_EC',
'IND_IS_BOF',
'IND_IS_EAF',
'IND_IS_SCR',
'IND_IS_ELC',
#'IND_NF_EC',
#'IND_NF_MD',
#'IND_NF_SB',
'IND_NF_ELC',
#'IND_NF_ALU',
#'IND_NF_ZNC',
#'IND_NF_COP',
#'IND_NF_AMN',
#'IND_NM_MD',
#'IND_NM_EC',
#'IND_NM_CMT',
#'IND_NM_LIM',
#'IND_NM_GLS',
#'IND_NM_CRM',
#'IND_NM_ELC',
#'IND_PP_MD',
#'IND_PP_SB',
#'IND_PP_PH',
#'MAT_WOD',
#'IND_PP_DH',
#'MAT_RCP',
#'IND_PP_PUL',
#'IND_PP_PAP',
#'IND_PP_PRN',
'IND_HET',
'IND_IS_SB_REC',
'IND_CH_SB_REC',
'IND_PP_SB_REC',
'IND_PP_ELC',
#'IND_OTH_SB',
#'IND_OTH_PH',
#'IND_OTH_MD',
#'IND_OTH_EC',
'IND_OTH_OTH',
'IND_OTH_ELC',
'IND_GEO',
#'IND_LTH',
'PRI_COA_OVC',
'PRI_OIL_NSP',
'PRI_OIL_PTC',
'PRI_OIL_WSP',
'PRI_OIL_LUB',
'PRI_OIL_ASP',
'PRI_OIL_WAX',
#'IND_CH_FS_NAP',
#'IND_CH_FS_ETH',
#'IND_CH_FS_DST',
#'IND_CH_FS_LPG',
'IND_BIO_ETH',
#'IND_CH_FS_BIO_ETH',
#'IND_CH_FS_MTH',
#'IND_CH_FS_NGA',
#'IND_CH_FS_COA',
#'IND_CH_FS_BIO',
'IND_HH2_WE',
'IND_HH2',
'IND_BGS',
#'IND_NM_SB',
#'IND_NM_CLK',
#'MAT_BFS',
]
commodities_out = [
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