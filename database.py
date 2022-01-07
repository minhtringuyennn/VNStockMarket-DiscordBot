import json, csv
import pandas as pd

from pathlib import Path

pharmacy    = ['AMV', 'CDP', 'DBD', 'DBT', 'DCL', 'DDN', 'DHG', 'DHT', 'DMC', 'DNM', 'DP1', 'DVN', 'HDP', 'IMP', 'JVC', 'LDP', 'MTP', 'OPC', 'PBC', 'PPP', 'TRA', 'VDP', 'VMD', 'YTC']
harbour     = ['CCR', 'CDN', 'CLL', 'CNG', 'DVP', 'DXP', 'GIC', 'GMD', 'GSP', 'HAH', 'ILB', 'MVN', 'PHP', 'PVT', 'SGP', 'TCD', 'TCL', 'VNA', 'VOS', 'VSC']
garment     = ['AAT', 'ADS', 'EVE', 'GIL', 'GMC', 'KMR', 'M10', 'MSH', 'PPH', 'SDG', 'STK', 'TCM', 'TNG', 'TVT', 'VGG', 'VGT']
power       = ['BCG', 'BTP', 'DNH', 'DTK', 'GE2', 'GEG', 'HNA', 'HND', 'NBP', 'NT2', 'PGV', 'POW', 'PPC', 'QTP', 'SJD', 'TTA', 'VSH']
construct   = ['BCC', 'BCE', 'BTS', 'C32', 'C4G', 'CII', 'CTD', 'CTI', 'DHA', 'DPG', 'FCN', 'G36', 'HBC', 'HHV', 'HOM', 'HT1', 'HTN', 'HUT', 'KSB', 'LCG', 'NNC', 'PC1', 'PHC', 'QNC', 'ROS', 'S99', 'SCI', 'SCJ', 'TTA', 'TV2', 'VCG', 'VCS', 'VGC', 'VTV']
home_estate = ['AGG', 'CEO', 'CKG', 'CRE', 'DIG', 'DXG', 'DXS', 'FLC', 'HDC', 'HDG', 'HPX', 'HQC', 'KDH', 'KHG', 'L14', 'LDG', 'NLG', 'NTL', 'NVL', 'PDR', 'REE', 'SCR', 'SSH', 'VCR', 'VHM', 'VIC', 'VRE']
insd_estate = ['BCM', 'D2D', 'GVR', 'IDC', 'IJC', 'ITA', 'KBC', 'LHG', 'NTC', 'PHR', 'SNZ', 'SZB', 'SZC', 'SZL', 'TIP', 'VGC']
aquaculture = ['ACL', 'ANV', 'ASM', 'CMX', 'FMC', 'IDI', 'MPC', 'SEA', 'SSN', 'VHC']
chemistry   = ['BFC', 'DCM', 'DDV', 'DGC', 'DHB', 'DPM', 'HSI', 'LAS', 'NFC', 'PCE', 'PMB', 'PSW', 'SFG', 'VAF']
retail      = ['DGW', 'FRT', 'MSN', 'MWG', 'PET', 'PSD']
bank        = ['ABB', 'ACB', 'BAB', 'BID', 'BVB', 'CTG', 'EIB', 'HDB', 'KLB', 'LPB', 'MBB', 'MSB', 'NAB', 'NVB', 'OCB', 'PGB', 'SGB', 'SHB', 'SSB', 'STB', 'TCB', 'TPB', 'VAB', 'VCB', 'VIB', 'VPB']
oilgas      = ['ASP', 'BSR', 'CNG', 'GAS', 'GSP', 'OIL', 'PGC', 'PGD', 'PGS', 'PLC', 'PLX', 'POW', 'PSH', 'PVB', 'PVC', 'PVD', 'PVG', 'PVM', 'PVO', 'PVP', 'PVS', 'PVT', 'PVX', 'PXS']
steel_inds  = ['HPG', 'HSG', 'NKG', 'POM', 'SMC', 'TIS', 'TLH', 'TVN', 'VCA', 'VGS', 'VIS']
stocks      = ['AAS', 'AGR', 'APG', 'APS', 'ART', 'BMS', 'BSI', 'BVS', 'CTS', 'DSC', 'EVS', 'FTS', 'HBS', 'HCM', 'IVS', 'MBS', 'ORS', 'PSI', 'SBS', 'SHS', 'SSI', 'TCI', 'TVB', 'TVS', 'VCI', 'VDS', 'VFS', 'VIG', 'VIX', 'VND', 'WSS']
airline     = ['ACV', 'ASG', 'AST', 'CIA', 'HVN', 'MAS', 'NCS', 'NCT', 'SAS', 'SCS', 'VJC']

## Fetch information for each stock categories --> to temp_data.json

# loader = dl.FetchCategories()
# data = loader.batch_download(steel_inds)

# result = data.to_json(orient="table")
# parsed = json.loads(result)

# idx = 0
# for value in parsed['data']:
#     value['index'] = idx
#     idx += 1

# with open('temp_data.json', 'w', encoding='utf-8') as f:
#     json.dump(parsed, f, ensure_ascii=False, indent=4)

## ---------------------------------------------------------

## Conver stock_list.json to smaller .csv files

# p = Path(r'stock_list.json')

# with p.open('r', encoding='utf-8') as f:
#     data = json.loads(f.read())

# file_name = ['HOSE_List', 'HNX_List', 'UPCOM_List', 'VN30_List', 'DuocPham_List', 'Cang_List', 'DetMay_List', 'NangLuong_List', 'XayDung_List', 'BDSNHAO_List', 'BDSCN_List', 'ThuySan_List', 'PhanBonHoaChat_List', 'BanLe_List', 'NganHang_List', 'DauKhi_List', 'Thep_List', 'ChungKhoan_List', 'HangKhong_List']

# idx = 0
# for name in file_name:
#     df = pd.json_normalize(data[idx]['stocks'])
#     df.drop('listedDate', axis =1, inplace = True)
#     df.drop('delistedDate', axis =1, inplace = True)
#     df.to_csv(f'./database/{name}.csv', index=False, encoding='utf-8')
#     idx += 1